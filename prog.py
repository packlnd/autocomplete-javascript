from parse_xml import get_data

""" Code is between <code> tags. """
def get_code(desc):
    raise NotImplementedError

data = get_data('PostsMin.xml')
post = data[0]
desc = post.attributes['Body'].value
get_code(desc)
