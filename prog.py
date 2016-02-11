from parse_xml import get_data
from BeautifulSoup import BeautifulSoup as BSHTML

""" Code is between <code> tags. """
def get_code(desc):
    bs = BSHTML(desc)
    return bs.code

data = get_data('PostsMin.xml')
post = data[0]
desc = post.attributes['Body'].value
code = get_code(desc)
print code
