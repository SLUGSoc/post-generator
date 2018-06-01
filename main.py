import datetime
import facebook_post
import twitter_post
import discord_post
import website_post
import facebook_event_retrieve
import os


def write_attrs(post):
    for key in post:
        post = write_attr(post, key)
    return post


def override_default(var, input_data):
    variable_empty = var == None
    override_variable = var != None and input_data != ''
    if variable_empty or override_variable:
        return input_data
    else:
        print('Not overriding existing value.')
        return var


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
            if list_input == 'exit':    # codeword to get out
                break
            if list_input.strip():      # only append if string isn't whitespace
                post[attr].append(list_input)
    elif attr == 'date' and post[attr] == None:  # uses existing date otherwise
        date_input = str(
            input('Enter the {} of the post (YYYY-MM-DD HH:MM): '.format(attr)))
        post[attr] = datetime.datetime.strptime(date_input, '%Y-%m-%d %H:%M')
    elif attr == 'date' and post[attr] != None:
        print('The event already has a date.')
        return post
    elif isinstance(post[attr], dict):
        print('Writing attributes for {}.'.format(attr))
        for key in post[attr]:
            post[attr] = write_attr(post[attr], key)
    else:
        input_data = str(input('Enter the {} of the post: '.format(attr)))
        post[attr] = override_default(post[attr], input_data)
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
        return '{}: {}\nOn {} at {} at {}\nEvent: {}'.format(
            get_type(post),
            post['title'],
            post['event']['date'].strftime("%-m %B"),
            post['event']['date'].strftime("%-I.%M%p"),
            post['event']['location'],
            post['event']['facebook_link'],
        )
    elif post_type == 'long':
        return '{}\nSLUGSoc {}: {}\nOn {} at {} at {}\nEvent details on Facebook at {}'.format(
            post['summary'],
            get_type(post),
            post['title'],
            post['event']['date'].strftime("%-m %B"),
            post['event']['date'].strftime("%-I.%M%p"),
            post['event']['location'],
            post['event']['facebook_link']
        )
    elif post_type == 'markdown':
        return '\n__{}__\n**{}**: __**{}**__\nOn **{}** at **{}** at **{}**\n{}\nRSVP here: {}'.format(
            post['summary'],
            get_type(post),
            post['title'],
            post['event']['date'].strftime("%-m %B"),
            post['event']['date'].strftime("%-I.%M%p"),
            post['event']['location'],
            post['content'],
            post['event']['facebook_link']
        )
    else:
        print('Please provide a correct parameter.')


def print_post(post):
    print(post)


def distribute_post(post, fb_post=False, dis_post=False, tw_post=False, site_post=True):
    # Share to Facebook
    if fb_post:
        try:
            graph = facebook_post.init_facebook()
            facebook_post.post_to_page(graph, format_post(post, 'long'))
            print('Posted to Facebook.')
        except KeyboardInterrupt:
            print('You cancelled posting to Facebook.')
        except:
            print('There was an error posting to Facebook.')
        # Posting to group - disabled in the Facebook Graph API v3 as of April 2018.
        # graph2 = facebook_post.init_facebook(os.environ['FACEBOOK_USER_ACCESS_TOKEN'])
        # facebook_post.post_to_group(graph2, format_post(post, 'long'))
    # Share to Twitter
    if tw_post:
        try:
            api = twitter_post.init_tweepy()
            twitter_post.update_status(api, format_post(post, 'short'))
            print('Posted to Twitter.')
        except KeyboardInterrupt:
            print('You cancelled posting to Twitter.')
        except:
            print('There was an error posting to Twitter.')
    # Share to Discord
    if dis_post:
        try:
            discord_post.post_announcement(format_post(post, 'markdown'))
            print('Posted to Discord.')
        except KeyboardInterrupt:
            print('You cancelled posting to Discord.')
        except:
            print('There was an error posting to Discord.')
    if site_post:
        try:
            website_post.create_announcement_file(post)
        except KeyboardInterrupt:
            print('You cancelled posting to the site.')
        except:
            print('There was an error posting to the site.')


graph2 = facebook_post.init_facebook(os.environ['SLUGS_ACCESS_TOKEN'])
event = facebook_event_retrieve.read_event(
    graph2, 'https://www.facebook.com/events/409928392815055/')
post = facebook_event_retrieve.process_event(event)
post = write_attrs(post)
distribute_post(post, True, True, True, True)
