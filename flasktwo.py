from textwrap import dedent
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from facebook_post import init_facebook
import facebook_event_retrieve
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
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
    content = TextField('content:', validators=[])
    date = TextField('date:', validators=[validators.required()])
    location = TextField('location:', validators=[])
    facebook_link = TextField('facebook_link:', validators=[])
    ticket_link = TextField('ticket_link:', validators=[])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    id = request.args.get('event_id')
    if id != None:
        fb = init_facebook(os.environ['SLUGS_ACCESS_TOKEN'])
        event = facebook_event_retrieve.read_event(graph)
        event_post_data = facebook_event_retrieve.process_event(event)
    if request.method == 'POST':
        title = request.form['title']

        if form.validate():
            # Save the comment here.
            flash('Post title is ' + title)
        else:
            print("test post:", event_post_data)
            form.image.data = event_post_data['image']
            print('form.data:', form.data)
            flash('All the form fields are required. ')

    return render_template('hello.html', form=form)


if __name__ == "__main__":
    app.run()
