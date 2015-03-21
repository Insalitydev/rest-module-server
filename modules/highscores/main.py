# coding: utf-8

import json
import logging
from . import settings
from . import highscores
from flask import request
from flask.views import MethodView

class UserAPI(MethodView):
	def get(self, username=None):
		if username is None:
			return highscores.get_top()
		else:
			return highscores.get_score(username)
	def post(self):
		keys = ["Username", "Score"]
		try:
			data = json.loads(request.data.decode("utf-8"))
		except ValueError:
			return "Wrong JSON data"

		for key in keys:
			if not key in data:
				return "Wrong JSON keys"

		highscores.send_score(data["Username"], data["Score"])
		return "Success posting scores"


def setup_routes(flask_app):
	logging.info("Start setup module %s" % settings.MODULE_NAME)

	user_view = UserAPI.as_view(settings.MODULE_ROUTE)
	flask_app.add_url_rule("/%s" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", "POST",])
	flask_app.add_url_rule("/%s/" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", "POST",])
	flask_app.add_url_rule("/%s/<string:username>" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", ])
