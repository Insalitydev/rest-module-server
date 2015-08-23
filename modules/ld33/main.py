# coding: utf-8

import json
import logging
from flask import request, render_template
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

class InfoAPI(MethodView):
	def get(self, username=None):
		ctx = {}
		if username is None:
			ctx.update({"highscores": json.loads(highscores.get_top(0))})
			ctx.update(stats.get_overall_stats())
			return render_template('info.html', ctx=ctx)
		else:
			st = stats.get_overall_user_stats(username);
			if (st == "Empty"):
				return "[Error]: The username %s doesn't exist" % username
			ctx.update(st)
			return render_template('personal.html', ctx=ctx)

		



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

	info_view = InfoAPI.as_view(settings.MODULE_ROUTE+"/info")
	# flask_app.add_url_rule("/%s/info" % settings.MODULE_ROUTE, view_func=info_view, methods=["GET",])
	flask_app.add_url_rule("/%s/info/" % settings.MODULE_ROUTE, view_func=info_view, methods=["GET",])
	flask_app.add_url_rule("/%s/info/<string:username>" % settings.MODULE_ROUTE, view_func=info_view, methods=["GET",])
