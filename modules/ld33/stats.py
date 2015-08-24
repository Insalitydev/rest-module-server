# coding: utf-8

import json
import pymongo

from datetime import datetime

# RELATIVE IMPORT HACK
if __name__=="__main__":
	from _secret import USERNAME, PASSWORD
	from utils import hash_stats
else:
	from ._secret import USERNAME, PASSWORD
	from .utils import hash_stats


def get_connection_stats():
	client = pymongo.MongoClient("mongodb://%s:%s@ds059722.mongolab.com:59722/ludumdare33" % (USERNAME, PASSWORD))
	db = client.ludumdare33
	stats = db['stats']
	return stats

stats = get_connection_stats()
keys = ["Username", "Score", "Mode", "Gold", "Playtime", "IsWin"]

def send_stats(username, score, mode, gold, playtime, is_win, key):
	# Asserting value types
	# Mode: 0 - Softcore, 1 - Hardcore
	if (not type(username) is str) or\
		(not type(score) is int) or\
		(not type(key) is str) or\
		(not type(mode) is int) or\
		(not type(gold) is int) or\
		(not type(playtime) is int) or\
		(not type(is_win) is int):
		return "[Error]: Value type errors" 

	# Need to assert key
	if (key != hash_stats(username, score, mode, gold, playtime, is_win)):
		return "[Error]: Wrong secret key"


	if username == "": username = "Unnamed"
	username = username.strip()

	# Posting scores
	cur_date = datetime.now().strftime("%H:%M:%S %d.%m.%Y")

	stats.insert({"Username": username, "Score": score, "Mode": mode, "Date": cur_date, "Gold": gold, "Playtime": playtime, "IsWin": is_win})
	return "[OK]: Stats recorded on User %s" % username


def get_stats(username):
	user_stats = stats.find({"Username": username})
	if user_stats == None:
		return "{}"

	result = []
	for stat in user_stats:
		new_stat = { key: stat[key] for key in keys}
		result.append(new_stat)
	return json.dumps( result )

def get_overall_user_stats(username):
	all_stats = json.loads(get_stats(username))
	if (len(all_stats) == 0):
		return "Empty";

	time_total = 0
	coin_total = 0
	play_times = 0
	win_times = 0

	for stat in all_stats:
		time_total += stat["Playtime"]
		coin_total += stat["Gold"]
		play_times += 1
		if (stat["IsWin"]):
			win_times += 1

	ctx = {"time_total" : time_total, "coin_total": coin_total, "play_times": play_times, "win_times": win_times,
			"coin_average": (int)(coin_total/play_times), "time_average": (int)(time_total/play_times), "Username": username}
	return ctx

def get_overall_stats():
	time_total = 0
	coin_total = 0
	play_times = 0
	win_times = 0

	all_stats = stats.find();
	for stat in all_stats:
		time_total += stat["Playtime"]
		coin_total += stat["Gold"]
		play_times += 1
		if (stat["IsWin"]):
			win_times += 1


	ctx = {"time_total" : time_total, "coin_total": coin_total, "play_times": play_times, "win_times": win_times,
			"coin_average": (int)(coin_total/play_times), "time_average": (int)(time_total/play_times)}
	return ctx


if __name__=="__main__":
	print(get_stats("Hard"))

