# coding: utf-8

import json
import logging
from . import settings
from flask import request
from flask.views import MethodView

class UserAPI(MethodView):
	def get(self, id=None):
		if id is None:
			return "Success GET Method ex2, list"
		else:
			return "Succes Get Method ex2, id %i" % id
	def post(self):
		keys = ["name"]
		try:
			data = json.loads(request.data.decode("utf-8"))
		except ValueError:
			return "Wrong JSON data ex2"

		for key in keys:
			if not key in data:
				return "Wrong JSON keys ex2"

		return "Success POST Method ex2. User: %s" % data["name"]


def setup_routes(flask_app):
	logging.info("Start setup module %s" % settings.MODULE_NAME)

	user_view = UserAPI.as_view(settings.MODULE_ROUTE)
	flask_app.add_url_rule("/%s" % settings.MODULE_ROUTE, view_func=user_view)
	flask_app.add_url_rule("/%s/" % settings.MODULE_ROUTE, view_func=user_view)
	flask_app.add_url_rule("/%s/<int:id>" % settings.MODULE_ROUTE, view_func=user_view)
