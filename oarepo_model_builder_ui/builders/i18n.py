from collections import defaultdict
from pathlib import Path
from oarepo_model_builder.builders import OutputBuilder

from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder_ui.config import UI_ITEMS

from oarepo_model_builder.utils.python_name import module_to_path

class InvenioI18nBuilder(OutputBuilder):
    TYPE = "invenio_i18n"
    output_file_type = "po"

    def build_node(self, datatype: DataType):
        translation_config = datatype.section_translations.config

        path = module_to_path(translation_config['module'])
        self.output = self.builder.get_output("po", path)

        for node in datatype.deep_iter():
            if node != datatype:
                self.process_node(node)

    def process_node(self, node):
        ui_items = defaultdict(dict)

        for el, val in node.definition.items():
            for ui in UI_ITEMS:
                if el.startswith(f"{ui}."):
                    ui_items[ui][el[len(ui) + 1:]] = val

        key_proto = node.definition.get("i18n.key")
        for ui in UI_ITEMS:
            if "key" not in ui_items[ui]:
                if key_proto:
                    ui_items[ui]["key"] = f"{key_proto}.{ui}"
                else:
                    ui_items[ui]["key"] = (
                            node.path.replace('.', '/') + f".{ui}"
                    )

        # add translation for enums
        enum_keys = node.definition.get("enum", [])
        for en in enum_keys:
            if key_proto:
                ui_items[en]["key"] = f"{key_proto}.enum.{en}"
            else:
                ui_items[en]["key"] = (
                        node.path.replace('.', '/') + f".enum.{en}"
                )

        for ui, langs in ui_items.items():
            key = langs.pop("key")
            for lang, val in langs.items():
                self.output.add(key, val, language=lang)
            self.output.add(key)
