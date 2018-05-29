import facebook


def init_facebook():
    return facebook.GraphAPI(
        access_token=os.environ['FACEBOOK_PAGE_ACCESS_TOKEN'], version="2.7")


def post_to_page(graph, content):
    graph.put_object(parent_object=os.environ['FACEBOOK_PAGE_ID'], connection_name='feed',
                     message=content)


graph = init_facebook()
post_to_page(graph, 'Hello world!')
