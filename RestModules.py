# coding: utf-8

import os
import logging
from flask import Flask, request
from flask.views import MethodView


cur_dir = os.path.dirname(__file__)
if (cur_dir == ""):
	cur_dir = "."

modules_dir = "modules"

logging.basicConfig(filename=cur_dir+"/log/RestModules.log", level=logging.INFO,
					format = '[%(asctime)s] %(levelname)s: %(message)s',
					datefmt = '%Y-%m-%d %I:%M:%S')

app = Flask(__name__)

# ==============
# FLASK SETTINGS
# ==============
@app.errorhandler(404)
def page_not_found(e):
	return("[Error]: Wrong API request")

@app.before_request
def log():
	logging.info("%s: %s, Data: %s" % (request.method, request.url, request.data))


if __name__ == "__main__":
	full_modules_dir = cur_dir + "/" + modules_dir
	modules_list = [ name for name in os.listdir(full_modules_dir) if os.path.isdir(os.path.join(full_modules_dir, name)) ]

	for module in modules_list:
		try:
			module_link = __import__("%s.%s.main" % (modules_dir, module))
			module_attr = getattr(module_link, module)
			module_attr.main.setup_routes(app)
		except (AttributeError, ImportError) as e:
			logging.error("Error %s" % e)
			logging.error("Module %s is incorrect, removing from module list..." % module)
			modules_list.remove(module)

	logging.info("Loaded modules: %s " % ", ".join(modules_list))

	# Current routes list:
	routes = set()
	for rule in app.url_map.iter_rules():
		routes.add(rule.endpoint)

	routes.remove("static")
	logging.info("Loaded routes: %s" % ", ".join(routes))

	app.run(host='0.0.0.0', debug=False)