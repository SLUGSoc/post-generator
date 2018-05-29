import facebook
import os
import webbrowser


def init_facebook():
    return facebook.GraphAPI(
        access_token=os.environ['FACEBOOK_PAGE_ACCESS_TOKEN'], version="2.7")


def post_to_page(graph, content):
    graph.put_object(parent_object=os.environ['FACEBOOK_PAGE_ID'], connection_name='feed',
                     message=content)


def get_permissions(graph):
    app_id = os.environ['FACEBOOK_APP_ID']
    canvas_url = None
    perms = ['manage_pages', 'publish_pages']
    fb_login_url = graph.auth_url(app_id, canvas_url, perms)
    webbrowser.open(fb_login_url, new=0, autoraise=True)
    print(fb_login_url)


# graph = init_facebook()
# get_permissions(graph)
