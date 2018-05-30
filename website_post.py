from textwrap import dedent
import sys
import subprocess
import os


def open_file(filepath):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filepath))
    elif os.name == 'nt':
        os.startfile(filepath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', filepath))


def create_announcement_file(post):
    post_header = """
        ---
        layout: post
        title: %s
        summary: %s
        prompt: Learn More
        image: %s
        image_description: %s
        games: %s
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
        ' '.join(post['categories']),
        post['event']['date'].strftime("%Y-%m-%d"),
        post['event']['date'].strftime("%H:%M"),
        post['event']['location'])
    post_header = dedent(post_header)
    md_file = open('generated_post.md', 'w')
    md_file.write(post_header)
    md_file.close()
    open_file('generated_post.md')
