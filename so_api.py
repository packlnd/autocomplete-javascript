import requests
import json

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

def get_answers(ids):
    format_ids = ';'.join([str(i) for i in ids])
    params = {
        'site':'stackoverflow'
    }
    answs = so_request('questions/' + format_ids + '/answers', params)
    for a in answs['items']:
        print a

def query_so(q):
    params = {
        'q':q,
        'accepted':'true',
        'site':'stackoverflow'
    }
    json_data = so_request("search/advanced", params)['items']
    filtered = filter_data(json_data)
    ids = collect_ids(filtered)
    answers = get_answers(ids)
    print answers

query_so("python")
