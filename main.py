import datetime
import facebook_post
import twitter_post
import discord_post
import website_post


def new_post():
    return {'title': None,
            'summary': None,
            'image': None,
            'image_description': None,
            'games': [],
            'categories': None,
            'content': None,
            'event': {
                'date': None,
                'location': None
            }
            }


def write_attrs(post):
    for key in post:
        post = write_attr(post, key)
    return post


def write_attr(post, attr):
    if post[attr] == None:
        print('The post has no {} yet.'.format(attr))
    else:
        print('Current {}: {}'.format(attr, post[attr]))
    if isinstance(post[attr], list):
        print('Entering multiple items for {}.'.format(attr))
        list_input = ''
        while True:
            list_input = str(input('Add an item to the list: '))
            if list_input == 'exit':
                break
            post[attr].append(list_input)
    elif attr == 'date':
        date_input = str(
            input('Enter the {} of the post (YYYY-MM-DD HH:MM): '.format(attr)))
        post[attr] = datetime.datetime.strptime(date_input, '%Y-%m-%d %H:%M')
    elif isinstance(post[attr], dict):
        print('Writing attributes for {}.'.format(attr))
        for key in post[attr]:
            post[attr] = write_attr(post[attr], key)
    else:
        post[attr] = str(input('Enter the {} of the post: '.format(attr)))
    return post


def random_greeting():
    return 'Join us for a new event!'


def get_type(post):
    if 'unofficial' in post['categories']:
        return 'Unofficial Social'
    elif 'weekly-social' in post['categories']:
        return 'Weekly Social'
    elif 'lan' in post['categories']:
        return 'LAN Event'
    elif 'meeting' in post['categories']:
        return 'Society Meeting'
    else:
        return 'Other'


def format_post(post, post_type):
    if post_type == 'short':
        return '{}: {}\nOn {} at {} at {}'.format(
            get_type(post),
            post['title'],
            post['event']['date'].strftime("%Y-%m-%d"),
            post['event']['date'].strftime("%H:%M"),
            post['event']['location']
        )
    elif post_type == 'long':
        return '{}\n{}: {}\nOn {} at {} at {}\n{}'.format(
            post['summary'],
            get_type(post),
            post['title'],
            post['event']['date'].strftime("%Y-%m-%d"),
            post['event']['date'].strftime("%H:%M"),
            post['event']['location'],
            post['content']
        )
    elif post_type == 'markdown':
        return '\n__{}__\n**{}**: __**{}**__\nOn **{}** at **{}** at **{}**\n{}'.format(
            post['summary'],
            get_type(post),
            post['title'],
            post['event']['date'].strftime("%Y-%m-%d"),
            post['event']['date'].strftime("%H:%M"),
            post['event']['location'],
            post['content']
        )
    else:
        print('Please provide a correct parameter.')


def print_post(post):
    print(post)


def distribute_post(post, fb_post=False, dis_post=False, tw_post=False, site_post=True):
    # Share to Facebook
    if fb_post:
        graph = facebook_post.init_facebook()
        facebook_post.post_to_page(graph, format_post(post, 'long'))
        print('Posted to Facebook.')
    # Share to Twitter
    if tw_post:
        api = twitter_post.init_tweepy()
        twitter_post.update_status(api, format_post(post, 'short'))
        print('Posted to Twitter.')
    # Share to Discord
    if dis_post:
        discord_post.post_announcement(format_post(post, 'markdown'))
        print('Posted to Discord.')
    if site_post:
        website_post.create_announcement_file(post)


post = write_attrs(new_post())
distribute_post(post, True, True, True, True)
