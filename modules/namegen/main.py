# coding: utf-8

import json
import logging
from . import Tags
from . import settings
from . import PhraseGen
from flask import request, render_template
from flask.views import MethodView

class UserAPI(MethodView):
	def get(self, tag=None):
		if tag is None:
			return render_template('index.html')
			# return PhraseGen.generate_phrase(tag)
		else:
			if (tag in Tags.Tags):
				return PhraseGen.generate_phrase(tag)
			elif (tag=="Boss"):
				return PhraseGen.generate_boss()
			else:
				return "[Error]: Tag should be: Item, Creature, Location or Boss"


def setup_routes(flask_app):
	logging.info("Start setup module %s" % settings.MODULE_NAME)

	user_view = UserAPI.as_view(settings.MODULE_ROUTE)
	flask_app.add_url_rule("/%s" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET",])
#	flask_app.add_url_rule("/%s/" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET",])
	flask_app.add_url_rule("/%s/<string:tag>" % settings.MODULE_ROUTE, view_func=user_view, methods=["GET", ])
