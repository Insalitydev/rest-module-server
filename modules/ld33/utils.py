# coding: utf-8

import uuid
import hashlib

if __name__=="__main__":
	from _secret import KEY
else:
	from ._secret import KEY

def hash_highscore(username, score, mode):
	s = str(username) + str(score) + str(mode) + KEY
	s = s.encode("utf8")
	h = hashlib.sha1(s)
	return h.hexdigest().upper()

def hash_stats(username, score, mode, gold, playtime, is_win):
	s = str(username) + str(score) + str(mode) + str(gold) + str(playtime) + str(is_win) + str(KEY)
	s = s.encode("utf8")
	h = hashlib.sha1(s)
	return h.hexdigest().upper()


if __name__=="__main__":
	print(hash_highscore("St", "40000", 0))
