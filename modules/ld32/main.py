# coding: utf-8

import json
import logging
from flask import request
from flask.views import MethodView
from . import settings, highscores

class HighscoreAPI(MethodView):
	def get(self, username=None):
		if username is None:
			return highscores.get_top()
		else:
			return highscores.get_score(username)
	def post(self):
		keys = ["Username", "Score", "Key"]
		try:
			data = json.loads(request.data.decode("utf-8"))
		except ValueError:
			return "[Error]: Wrong JSON data"

		for key in keys:
			if not key in data:
				return "[Error]: Wrong JSON keys"

		send_result = highscores.send_score(data["Username"], data["Score"], data["Key"])
		return send_result


def setup_routes(flask_app):
	logging.info("Start setup module %s" % settings.MODULE_NAME)

	user_view = HighscoreAPI.as_view(settings.MODULE_ROUTE)
	flask_app.add_url_rule("/%s/highscore" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", "POST",])
	flask_app.add_url_rule("/%s/highscore/" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", "POST",])
	flask_app.add_url_rule("/%s/highscore/<string:username>" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", ])
