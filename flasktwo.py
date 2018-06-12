from textwrap import dedent
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField, BooleanField
from facebook_post import init_facebook
import facebook_event_retrieve
import os
import main
import re
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from dateutil.parser import parse
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


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
    elif isinstance(post[attr], dict):
        print('Writing attributes for {}.'.format(attr))
        for key in post[attr]:
            post[attr] = write_attr(post[attr], key)
    else:
        post[attr] = str(input('Enter the {} of the post: '.format(attr)))
    return post


def print_post(post):
    print(post)

# Flask routing


class ReusableForm(Form):
    title = TextField('title:', validators=[validators.required()])
    summary = TextField('summary:', validators=[validators.required()])
    image = TextField('image:', validators=[])
    image_description = TextField('image_description:', validators=[])
    games = TextField('games:', validators=None)
    categories = TextField('categories:', validators=[])
    content = TextAreaField('content:', validators=[])
    date = TextField('date:', validators=[validators.required()])
    location = TextField('location:', validators=[])
    facebook_link = TextField('facebook_link:', validators=[])
    ticket_link = TextField('ticket_link:', validators=[])
    lan_number = IntegerField('lan_number:', validators=[
                              validators.optional()])
    facebook_post = BooleanField('Post to Facebook?', validators=[])
    twitter_post = BooleanField('Post to Twitter?', validators=[])
    website_post = BooleanField('Post to SLUGSoc.co.uk?', validators=[])
    discord_post = BooleanField('Post to Discord?', validators=[])


@app.route("/", methods=['GET', 'POST'])
def hello():

    id = request.args.get('event_id')
    if id != None:
        fb = init_facebook(os.environ['FACEBOOK_PAGE_ACCESS_TOKEN'])
        fb2 = init_facebook(os.environ['SLUGS_ACCESS_TOKEN'])
        event = facebook_event_retrieve.read_event(fb2, id)
        event_post_data = facebook_event_retrieve.process_event(event)
        # Preprocess event here
        lan_number_search = re.findall('\\b\\d{2,3}\\b', 'LAN 70')
        if not not lan_number_search:
            event_post_data['lan_number'] = int(lan_number_search[0])
            event_post_data['categories'] = ['lan']
        # event_post_data['date'] = event_post_data['event']['date']
        # end event preprocessing
        form = ReusableForm(MultiDict(event_post_data))
    else:
        form = ReusableForm(request.form)
        event_post_data = facebook_event_retrieve.new_post()
    print(form.errors)
    if request.method == 'POST':
        title = request.form['title']

        if form.validate():
            # Save the comment here.
            flash('Post title is ' + title)
            event_post_data = form.data
            event_post_data['event'] = {
                'date': event_post_data['date'],
                'location': event_post_data['location'],
                'lan_number': event_post_data['lan_number'],
                'facebook_link': event_post_data['facebook_link'],
                'ticket_link': event_post_data['ticket_link'],
            }
            event_post_data.pop('date', None)
            event_post_data.pop('location', None)
            event_post_data.pop('lan_number', None)
            event_post_data.pop('facebook_link', None)
            event_post_data.pop('ticket_link', None)
            event_post_data.pop('facebook_post', None)
            event_post_data.pop('twitter_post', None)
            event_post_data.pop('discord_post', None)
            event_post_data.pop('website_post', None)
            event_post_data['event']['date'] = parse(
                event_post_data['event']['date'])
            print(event_post_data)
            fb = form.data['facebook_post']
            tw = form.data['twitter_post']
            web = form.data['website_post']
            dis = form.data['discord_post']
            main.distribute_post(event_post_data, fb, dis, tw, web)
        else:
            print('form.data:', form.data)
            print('form.errors:', form.errors)
            flash('All the form fields are required. ')

    return render_template('hello.html', form=form)


if __name__ == "__main__":
    app.run()
