import json

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader("app"))
env.filters["jsonify"] = json.dumps
