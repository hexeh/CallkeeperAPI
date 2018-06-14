# -*- coding: utf-8 -*-

try:
	try:
	    from urllib.parse import urlencode
	except ImportError:
	    from urllib import urlencode
	import json
	import datetime
	import requests
	import sys
except ImportError:
	sys.exit(
		'''Please install following packages using pip:
		urllib
		json
		requests
		'''
	)


class CallKeeper:

	def __init__(self, key, timezone = None):

		self.token = key
		self.url = 'https://api.callkeeper.ru/'
		if timezone is None:
			self.timezone = 'Europe/Moscow'
		else:
			self.timezone = timezone

		# Validating API-key
		touch_request = requests.get('{0!s}getUserInfo?api_key={1!s}'.format(self.url, self.token))
		if touch_request.status_code == 200:
			self.user = json.loads(touch_request.text)
		else:
			error_info = json.loads(touch_request.text)
			error_message = 'Failed to authentificate key \033[1;32;40m{0!r}\033[0m with error: \033[1;31;40m{1!s}\033[0m'.format(self.token, error_info[0]['reason'])
			sys.exit(error_message)

		# Checking paid period

		payment_date = datetime.datetime.strptime(self.user.get('paid_till')[:-6], '%Y-%m-%dT%H:%M:%S')
		if payment_date <= (datetime.datetime.now() + datetime.timedelta(days = 2)):
			print('\033[1;33;40mPaid period for this account is about to expire. Expiration date: {0!r}\033[0m'.format(payment_date.strftime('%d %B %Y')))

	def getCallInfo(self, call_id):

		cmd = 'getCallInfo'
		query = {
			'api_key': self.token,
			'id_call': str(call_id)
		}
		query = urlencode(query)
		req = requests.get('{0!s}{1!s}?{2!s}'.format(self.url, cmd, query))
		if(req.status_code == 200):
			response = json.loads(req.text)
			return(response['result'])
		else:
			error_info = json.loads(req.text)
			error_message = 'Failed to complete request with error: \033[1;31;40m{2!s}\033[0m'.format(error_info[0]['reason'])
			sys.exit(error_message)

	def captureStats(self, dateStart, dateEnd = None, statuses = []):

		if dateEnd is None:
			dateEnd = datetime.datetime.strptime(dateStart, '%Y-%m-%d') + datetime.timedelta(1)

		cmd = 'getCallsCompleted'		
		query = {
			'api_key': self.token,
			'date[from]': str(dateStart),
			'date[to]': str(dateEnd)
		}
		if len(statuses) > 0:
			query['statuses'] = ','.join(statuses)
			cmd = 'getCallsByStatus'
		query = urlencode(query)
		req = requests.get('{0!s}{1!s}?{2!s}'.format(self.url, cmd, query))
		if(req.status_code == 200):
			response = json.loads(req.text)
			return(response['result'])
		else:
			error_info = json.loads(req.text)
			error_message = 'Failed to complete request with error: \033[1;31;40m{2!s}\033[0m'.format(error_info[0]['reason'])
			sys.exit(error_message)
