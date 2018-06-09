import facebook
import re
import os
from facebook_post import init_facebook
from dateutil import parser


def new_post():
    return {'title': None,
            'summary': None,
            'image': None,
            'image_description': None,
            'games': [],
            'categories': [],
            'content': None,
            'event': {
                'date': None,
                'location': None,
                'facebook_link': None,
                'ticket_link': None,
                'lan_number': None
            }
            }


def read_event(graph, link):
    event_ids = list(map(int, re.findall(r'\d+', link)))
    if len(event_ids) == 1:
        event_id = event_ids[0]
    else:
        print("Let them choose.")
        event_id = 409928392815055
    event = graph.get_object(id=str(event_id),
                             fields='cover,description,name,place,start_time')
    return event


def process_event(event):
    post = new_post()
    post['title'] = event['name']
    post['content'] = event['description']
    post['image'] = event['cover']['source']
    post['event']['date'] = parser.parse(event['start_time'])
    post['event']['location'] = event['place']['name']
    post['event']['facebook_link'] = 'https://facebook.com/events/{}'.format(
        event['id'])
    return post
