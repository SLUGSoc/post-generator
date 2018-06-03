from flask import Flask, render_template, request, Response
from textwrap import dedent
from facebook_event_retrieve import new_post
# import wtf
import main
app = Flask(__name__)


# Flask routing


@app.route('/', methods=['GET', 'POST'])
def create_post_route():
    form = SitePostForm(request.POST)
    if request.method == 'POST' and form.validate():
        post = request.form.to_dict()
        main.distribute_post(post, True, True, True, True)
        return Response('Done!', mimetype='text/plain; charset=UTF-8')
    elif request.method == 'GET':
        return render_template('create_post.html')
    else:
        return 'Route undefined.'


if __name__ == '__main__':
    app.run()
