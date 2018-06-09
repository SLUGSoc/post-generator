from textwrap import dedent
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from facebook_event_retrieve import new_post
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


# @app.route('/', methods=['GET', 'POST'])
# def create_post_route():
#     form = SitePostForm(request.POST)
#     if request.method == 'POST' and form.validate():
#         post = request.form.to_dict()
#         post_header = """
#         ---
#         layout: post
#         title: %s
#         summary: %s
#         prompt: Learn More
#         image: %s
#         image_description: %s
#         games: [%s]
#         categories: %s
#         event:
#           date: %s %s
#           location: %s
#         ---""" % (
#             post['title'],
#             post['summary'],
#             post['image'],
#             post['image_description'],
#             post['games'],
#             post['categories'],
#             post['event[date]'],
#             post['event[time]'],
#             post['event[location]'])
#         post_header = dedent(post_header)
#         return Response(post_header, mimetype='text/markdown; charset=UTF-8')
#     elif request.method == 'GET':
#         return render_template('create_post.html')
#     else:
#         return 'Route undefined.'


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
    if request.method == 'POST':
        title = request.form['title']
        print(title)

        if form.validate():
            # Save the comment here.
            flash('Post title is ' + title)
        else:
            flash('All the form fields are required. ')

    return render_template('hello.html', form=form)


if __name__ == "__main__":
    app.run()
