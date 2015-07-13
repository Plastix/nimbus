#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

mojang_status_link = 'http://status.mojang.com/check'

status = {
	'green': ':white_check_mark:',
	'yellow': ':warning:',
	'red': ':x:',
}


def get_mojang_status():
	r = requests.get(mojang_status_link)

	if r.status_code != 200:
		print "Can't get Mojang Status!"
		return
	else:
		status = r.json()

		return build_slack_attachment(status)


def build_slack_attachment(data):

	response = {}
	response['title'] = 'Mojang Status Summary'
	response['title_link'] = 'https://help.mojang.com/'
	response['text'] = ''
	response['mrkdwn_in'] = ['text']

	for service in data:
		service_name = next (iter (service.keys()))
		color = service[service_name]
		stat = status.get(color, ':question:')
		response['text'] += '%s *%s*\n' % (stat, service_name)

	return response


def mcstatus(text, content, sc):
	message = get_mojang_status()
 	content.update({'type': 'message', 'text': ' ', 'attachments': json.dumps([message])})
	sc.api_call('chat.postMessage', **content)
	print('Got mojang status')
	