import inflect

from oarepo_model_builder.builders.json_base import JSONBaseBuilder
from oarepo_model_builder.datatypes import Section

from oarepo_model_builder_ui.config import UI_ITEMS

"""
Will generate:
metadata: {
  // contents of ui child here
  label: <label.key>
  hint: <hint.key>
  help: <help.key>
  children: {
    k: child_def
  }, // or 
  child: {
    ...
  }

// invenio_stuff_here

it will be saved to package/model/ui.json
"""


class InvenioLayoutBuilder(JSONBaseBuilder):
    TYPE = "ui-layout"
    output_file_type = "json"
    output_file_name = ["ui", "file"]
    create_parent_packages = True

    def build_node(self, node):
        generated = self.generate_node(node)
        self.output.merge(generated)

    def generate(self, node):
        ui: Section = node.section_ui
        ret = {**ui.config}
        ret.pop('marshmallow', None)

        if ui.children:
            properties = ret.setdefault("children", {})
            for k, v in ui.children.items():
                v = self.generate(v)
                properties[k] = v
        if ui.item:
            ret["child"] = self.generate(ui.item)
        return ret

    def generate_node(self, node):
        ui = {}
        section = node.section_ui
        data = node.definition

        ui.update({k.replace("-", "_"): v for k, v in section.config.items()})
        ui.pop('marshmallow', None)
        if "type" in data:
            t = data["type"]
            if t in ("object", "nested"):
                t = inflect.engine().singular_noun(
                    node.path.split('.')[-1].lower()
                )
            ui.setdefault("detail", t)
            ui.setdefault("input", t)

        for fld in UI_ITEMS:
            ui[fld] = data.get(
                f"{fld}.key",
                node.path.replace('.', '/') + f".{fld}",
            )

        # facets = get_facet_details(
        #     self.stack, self.current_model, self.schema, set()
        # )
        #
        # if len(facets):
        #     ui["facet"] = facets[0]["path"]

        if node.children:
            children = ui.setdefault('children', {})
            for c in node.children.values():
                children[c.key] = self.generate_node(c)
        if hasattr(node, 'item'):
            ui['child'] = self.generate_node(node.item)

        return ui