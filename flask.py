from flask import Flask, render_template, request, Response
from textwrap import dedent
# import wtf
import main
app = Flask(__name__)


def new_post():
    return {'title': None,
            'summary': None,
            'image': None,
            'image_description': None,
            'games': [],
            'categories': None,
            'event': {
                'date': None,
                'location': None
            }
            }


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


@app.route('/', methods=['GET', 'POST'])
def create_post_route():
    form = SitePostForm(request.POST)
    if request.method == 'POST' and form.validate():
        post = request.form.to_dict()
        post_header = """
        ---
        layout: post
        title: %s
        summary: %s
        prompt: Learn More
        image: %s
        image_description: %s
        games: [%s]
        categories: %s
        event:
          date: %s %s
          location: %s
        ---""" % (
            post['title'],
            post['summary'],
            post['image'],
            post['image_description'],
            post['games'],
            post['categories'],
            post['event[date]'],
            post['event[time]'],
            post['event[location]'])
        post_header = dedent(post_header)
        return Response(post_header, mimetype='text/markdown; charset=UTF-8')
    elif request.method == 'GET':
        return render_template('create_post.html')
    else:
        return 'Route undefined.'


if __name__ == '__main__':
    app.run()
