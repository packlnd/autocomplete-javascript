import requests
import json
from BeautifulSoup import BeautifulSoup

prefix = "https://api.stackexchange.com/2.2"

def so_request(ep, params={}):
    url = "%s/%s" % (prefix, ep)
    if len(params) >= 1:
        url += '?'
        url += '&'.join(['%s=%s' % (k,v)
            for k,v in params.iteritems()])
    print url
    return requests.get(url).json()

def collect_ids(json_data):
    ids = []
    for j in json_data:
        ids.append(j['question_id'])
    return ids

def filter_data(data):
    #TODO: Currently no filter
    return data

def get_questions(q):
    params = {
        'q':q,
        'views':100,
        'accepted':'true',
        'site':'stackoverflow',
        'filter':'withbody',
        'sort':'relevance'
    }
    req = so_request("search/advanced", params)
    return req['items']

def get_answers(ids):
    format_ids = ';'.join([str(i) for i in ids])
    params = {
        'site':'stackoverflow',
        'filter':'withbody'
    }
    req = so_request('questions/' + format_ids + '/answers', params)
    return req['items']

def get_code(body):
    soup = BeautifulSoup(body)
    return soup.findAll('code')

def print_code(answers):
    for answer in answers:
        code = get_code(answer['body'])
        print str(code)
        print '\n'

def prepare_query(q):
    return q.replace(' ', '+')

def query_so(q):
    # Current approach gives answers to all SO questions matching search query
    q = prepare_query(q)
    json_data = get_questions(q)
    filtered = filter_data(json_data)
    ids = collect_ids(filtered)
    answers = get_answers(ids)
    print_code(answers)

query_so("get query parameters")
