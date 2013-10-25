#!/usr/bin/env python3

import argparse
import json
import requests
from datetime import datetime


class Meetup():
    '''Create, modify and display meetup details.
    '''
    EVENT_URI = '2/event'
    GROUPS_URI = '2/groups'
    RSVPS_URI = '2/rsvps'
    API_BASE_URL = 'https://api.meetup.com/'
    
    def __init__(self, apiKey):
        self.baseUrlParams = {'sign': 'true', 'key': apiKey}
    
    def _prepBaseUrl(self, uri, uriEventId=''):
        return self.API_BASE_URL + uri + '/' + uriEventId
    
    def _prepUrlParams(self, **params):
        params.update(self.baseUrlParams)
        return params
    
    def _handleResponse(self, response):
        if response.status_code not in (200, 201):
            raise Exception(response.json())
        return response.json()
    
    def _get(self, uri, uriEventId='', **params):
        url = self._prepBaseUrl(uri, uriEventId)
        params = self._prepUrlParams(**params)
        response = requests.get(url, params=params)
        return self._handleResponse(response)
    
    def _post(self, data, uri, uriEventId='', **params):
        url = self._prepBaseUrl(uri, uriEventId)
        params = self._prepUrlParams(**params)
        response = requests.post(url, params=params, data=data)
        return self._handleResponse(response)
    
    def groupId(self, groupUrlname):
        response = self._get(self.GROUPS_URI, group_urlname=groupUrlname)
        return response['results'][0]['id']
    
    def create(self, groupUrlname, name, description, time):
        newEvent = {'announce': 'true', 
                    'group_id': self.groupId(groupUrlname), 
                    'group_urlname': groupUrlname, 'name': name, 
                    'description': description, 'time': time}
        return self._post(newEvent, self.EVENT_URI)
    
    def update(self, uriEventId, **params):
        return self._post(params, self.EVENT_URI, uriEventId)
    
    def details(self, uriEventId):
        details = {}
        guests = {}
        
        event = self._get(self.EVENT_URI, uriEventId)
        rsvps = self._get(self.RSVPS_URI, event_id=uriEventId)
        
        details['title'] = event['name']
        # html description
        details['desc'] = event['description']
        for rsvp in rsvps['results']:
            guests[rsvp['member']['member_id']] = rsvp['member']['name']
        details['guests'] = guests
        
        return details


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('action', choices=('create', 'update', 'details'), 
                           help='''use "create" to create a new event, 
                           "update" to update an event and 
                           "details" to get the event info''')
    argParser.add_argument('--title', help='event title')
    argParser.add_argument('--desc', help='event description')
    argParser.add_argument('--filedesc', type=argparse.FileType('r'), 
                           help='''path to the text file containing event 
                           description''')
    argParser.add_argument('--date', help='''event date, for example 
                           2013-11-11 16:16''')
    argParser.add_argument('--id', help='event id or event url')
    argParser.add_argument('--group', default='Sydney-Linux-User-Group', 
                           help='group url or last part of it')
    args = argParser.parse_args()
    
    with open('config.json', 'r') as configFile:
        config = json.loads(configFile.read())
    
    meetup = Meetup(config['apiKey'])
    
    # fix input
    if args.date:
        secs = datetime.strptime(args.date, '%Y-%m-%d %H:%M').strftime('%s')
        args.date = int(secs)*1000
    if args.filedesc and not args.desc:
        args.desc = args.filedesc.read()
    if args.id:
        args.id = args.id.rstrip('/').rsplit('/', 1)[-1]
    if args.group:
        args.group = args.group.rstrip('/').rsplit('/', 1)[-1]
    
    if args.action == 'create':
        event = meetup.create(args.group, args.title, args.desc, args.date)
        print('Created: ' + event['event_url'])
    if args.action == 'update':
        event = {}
        if args.title:
            event['name'] = args.title
        if args.desc:
            event['description'] = args.desc
        if args.date:
            event['time'] = args.date
        meetup.update(args.id, **event)
        print('Event updated.')
    if args.action == 'details':
        print(meetup.details(args.id))

