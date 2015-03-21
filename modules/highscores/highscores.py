# coding: utf-8

import json
import pymongo
from datetime import datetime
from ._secret import USERNAME, PASSWORD


def get_connection_records():
	client = pymongo.MongoClient("mongodb://%s:%s@ds029630.mongolab.com:29630/ludumdare32" % (USERNAME, PASSWORD))
	db = client.ludumdare32
	records = db['records']
	return records

records = get_connection_records()
keys = ["Username", "Score"]

def send_scores(username, score):
	# records = get_connection_records()

	cur_date = datetime.now().strftime("%H:%M:%S %d.%m.%Y")

	record = records.find_one({"Username": username})
	if (record != None ):
		if (record["Score"] < score):
			records.remove(record)
	records.insert({"Username": username, "Score": score, "Date": cur_date})

def get_score(username):
	# records = get_connection_records()
	r = records.find_one({"Username": username})
	if r == None:
		return "{}"

	new_r = { key: r[key] for key in keys}
	return json.dumps( new_r )

def get_top():
	# records = get_connection_records()

	top = records.find().sort("Score", -1)
	tp = []
	for r in top.limit(3):
		new_r = { key: r[key] for key in keys}
		tp.append(new_r)

	return json.dumps( tp )

def test():
	return "Sdsd"

if __name__=="__main__":
	print(get_top())