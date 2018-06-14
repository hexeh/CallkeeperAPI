# -*- coding: utf-8 -*-

import pprint
import json
import datetime
from api import CallKeeper

if __name__ == '__main__':
	
	config = {
		'ck': {'key': 'my_own_api_key'}
	}
	pp = pprint.PrettyPrinter(indent = 4)
	fetch_date = datetime.date.today() - datetime.timedelta(1)
	ck = CallKeeperApi(config['ck']['key'])
	
	# Current User Info
	pp.pprint(ck.user)
	
	# Info for specific call
	pp.pprint(ck.getCallInfo(12345))
	
	# Calls for specific period by daterange
	pp.pprint(ck.captureStats('2018-01-01'))
	
	# Calls for specific period by daterange
	pp.pprint(ck.captureStats('2018-01-01'), statuses = [200,0])
