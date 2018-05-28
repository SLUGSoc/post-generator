from flask import Flask, render_template, request
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


@app.route('/', methods=['GET', 'POST'])
def create_post_route():
    print(request.method)
    if request.method == 'POST':
        print_post(new_post())
        print_post(request.form.to_dict())
        # print(request.data)
        # dict = request.form
        # for key in dict:
        #     print(key, dict[key])
        return 'Submitted'
    elif request.method == 'GET':
        return render_template('create_post.html')
    else:
        return 'Route undefined.'


if __name__ == '__main__':
    app.run()
