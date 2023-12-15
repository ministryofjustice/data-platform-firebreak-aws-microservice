import json

from jinja2 import Environment, PackageLoader


class JsonTemplates(Environment):
    def __init__(self, *args, **kwargs):
        kwargs["loader"] = PackageLoader("app", "templates")
        super().__init__(*args, **kwargs)
        self.filters["jsonify"] = json.dumps
