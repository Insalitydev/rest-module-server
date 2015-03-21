# coding: utf-8

import json
import pymongo
from datetime import datetime

# RELATIVE IMPORT HACK
if __name__=="__main__":
	from _secret import USERNAME, PASSWORD
else:
	from ._secret import USERNAME, PASSWORD


def get_connection_records():
	client = pymongo.MongoClient("mongodb://%s:%s@ds029630.mongolab.com:29630/ludumdare32" % (USERNAME, PASSWORD))
	db = client.ludumdare32
	records = db['records']
	return records

records = get_connection_records()
keys = ["Username", "Score"]

def send_score(username, score):
	# Asserting value types
	if (not type(username) is str) or\
		(not type(score) is int):
		return "[Error]: Value type errors" 

	# Posting scores
	cur_date = datetime.now().strftime("%H:%M:%S %d.%m.%Y")

	record = records.find_one({"Username": username})
	if (record != None ):
		if (record["Score"] < score):
			records.remove(record)
			records.insert({"Username": username, "Score": score, "Date": cur_date})
			return "[OK]: Score updated on User %s" % record["Username"]
		else:
			return "[OK]: Score is not updated. Score is not highscore on User %s" % record["Username"]
	else:
		records.insert({"Username": username, "Score": score, "Date": cur_date})
		return "[OK]: Score created on User %s" % username

def get_score(username):
	rec = records.find_one({"Username": username})
	if rec == None:
		return "{}"

	new_rec = { key: rec[key] for key in keys}
	return json.dumps( new_rec )

def get_top():
	top = records.find().sort("Score", -1)
	top_list = []
	for rec in top.limit(10):
		new_rec = { key: rec[key] for key in keys}
		top_list.append(new_rec)

	return json.dumps( top_list )


if __name__=="__main__":
	# print(get_top())
	print(send_score("Imba", "10000"))