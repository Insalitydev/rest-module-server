# coding: utf-8

import json
import logging
from flask import request
from flask.views import MethodView
from . import settings, highscores, stats

class HighscoreAPI(MethodView):
	def get(self, username=None, mode=0):
		if username is None:
			return highscores.get_top(mode)
		else:
			return highscores.get_score(username, mode)
	def post(self):
		keys = ["Username", "Score", "Mode", "Key"]
		try:
			data = json.loads(request.data.decode("utf-8"))
		except ValueError:
			return "[Error]: Wrong JSON data"

		for key in keys:
			if not key in data:
				return "[Error]: Wrong JSON keys"

		send_result = highscores.send_score(data["Username"], data["Score"], data["Mode"], data["Key"])
		return send_result


class StatsAPI(MethodView):
	def get(self, username=None):
		if username is None:
			return "[Error]: No specified username"
		else:
			return stats.get_stats(username)
	def post(self):
		keys = ["Username", "Score", "Mode", "Gold", "Playtime", "IsWin", "Key"]
		try:
			data = json.loads(request.data.decode("utf-8"))
		except ValueError:
			return "[Error]: Wrong JSON data"

		for key in keys:
			if not key in data:
				return "[Error]: Wrong JSON keys"

		send_stats = stats.send_stats(data["Username"], data["Score"], data["Mode"], data["Gold"], data["Playtime"], data["IsWin"], data["Key"])
		return send_stats


def setup_routes(flask_app):
	logging.info("Start setup module %s" % settings.MODULE_NAME)

	user_view = HighscoreAPI.as_view(settings.MODULE_ROUTE+"/highscore")
	flask_app.add_url_rule("/%s/highscore" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", "POST",])
	flask_app.add_url_rule("/%s/highscore/" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", "POST",])
	flask_app.add_url_rule("/%s/highscore/<int:mode>" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET",])
	flask_app.add_url_rule("/%s/highscore/<string:username>:<int:mode>" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", ])

	stats_view = StatsAPI.as_view(settings.MODULE_ROUTE+"/stats")
	flask_app.add_url_rule("/%s/stats" % settings.MODULE_ROUTE, view_func=stats_view, methods=["GET", "POST",])
	flask_app.add_url_rule("/%s/stats/" % settings.MODULE_ROUTE, view_func=stats_view, methods=["GET", "POST",])
	flask_app.add_url_rule("/%s/stats/<string:username>" % settings.MODULE_ROUTE, view_func=stats_view, methods=["GET", ])
