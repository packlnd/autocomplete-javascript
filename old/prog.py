from parse_xml import get_data
from BeautifulSoup import BeautifulSoup as BSHTML

"""
    Current design is
    posts list of maps: [{'id':4828, 'title': ...}, ...]
    qna is map from question ID to list of answer IDs: {482828: [24i482, 24828, 824828, ...]}
"""

""" Code is between <code> tags. """
def get_code(desc):
    bs = BSHTML(desc)
    return bs.code

def get_attrib(post, att):
    return post.attributes[att].value if\
        att in post.attributes.keys() else '-1'

def is_question(t):
    return t == '1'
def is_answer(t):
    return t == '2'

""" Extracts relevant information from Stack Overflow dictionary"""
def extract_relevant(data):
    posts = {}
    for post in data:
        posts[post.attributes['Id'].value] = {
            'id': get_attrib(post, 'Id'),
            'title': get_attrib(post, 'Title'),
            'body': get_attrib(post, 'Body'),
            'type': get_attrib(post, 'PostTypeId'),
            'answer': get_attrib(post, 'AcceptedAnswerId'),
            'parent': get_attrib(post, 'ParentId'),
            'score': get_attrib(post, 'Score'),
            'views': get_attrib(post, 'ViewCount'),
            'tags': get_attrib(post, 'Tags'),
            'favorite_count': get_attrib(post, 'FavoriteCount')
        }
    return posts

""" Group questions and answers together """
def group(posts):
    qna = {}
    for i,post in posts.iteritems():
        if is_question(post['type']):
            if not post['id'] in qna:
                qna[post['id']] = []
        elif is_answer(post['type']):
            if not post['parent'] in qna:
                qna[post['parent']] = []
            qna[post['parent']].append(post['id'])
    return qna

print 'Parsing xml...'
data = get_data('Posts.xml')
print '...done'

print 'Parsing xml to dictionary...'
posts = extract_relevant(data)
data = None
print '...done'
print 'Grouping questions and answers...'
qna = group(posts)
print '...done'
print qna
