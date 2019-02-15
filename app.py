from datetime import datetime
from time import sleep
import redis
import os
import json
import urllib.request

pollinterval = os.environ['POLL_INTERVAL']
passwd = os.environ['REDIS_PW']
dbhost = os.environ['REDIS_HOST']
dbport = os.environ['REDIS_DB_PORT']

stockAPI = "https://api.iextrading.com/1.0/tops/last?symbols=BAC,SNAP,FB,AIG,WTM,PRT,HBB,KFFB,SYBX,PIHPP,LFC,SMN,DOCU%2ba"

redisConnection = redis.Redis(host=dbhost,port=dbport,password=passwd)

def pollLatest():
	with urllib.request.urlopen(stockAPI) as response:
		json_content = json.loads(response.read())
		for stock in json_content:
			redisConnection.zadd(stock['symbol'],{json.dumps(stock):-int(stock['time'])})
		print(json_content)


if __name__ == "__main__":
	while True:
		pollLatest()
		sleep(int(pollinterval))
