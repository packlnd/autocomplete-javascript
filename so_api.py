import requests
import json
from BeautifulSoup import BeautifulSoup

base_url = "https://api.stackexchange.com/2.2"

def so_request(ep, params={}):
    url = "%s/%s" % (base_url, ep)
    if len(params) >= 1:
        url += '?'
        url += '&'.join(['%s=%s' % (k,v)
            for k,v in params.iteritems()])
    return requests.get(url).json()

def collect_ids(json_data):
    return [j['accepted_answer_id'] for j in json_data]

def filter_data(data):
    #TODO: Currently no filter
    return data

def get_questions(q):
    params = {
        'q':q,
        'views':100,
        'accepted':True,
        'site':'stackoverflow',
        'filter':'withbody',
        'sort':'relevance'
    }
    req = so_request("search/advanced", params)
    return req['items']#  Could limit to 10 here, but empty answers mess with that: [:10]

def get_answers(ids):
    format_ids = ';'.join([str(i) for i in ids])
    params = {
        'site':'stackoverflow',
        'filter':'withbody',
        'pagesize': 50
    }
    req = so_request('answers/' + format_ids, params)
    id_mapping = {item['answer_id']: item for item in req['items']}
    return [id_mapping[a_id] for a_id in ids if a_id in id_mapping]

def get_code(body):
    soup = BeautifulSoup(body)
    return [code.getText() for code in soup.findAll('code')]

def get_list_of_code(answers):
    code = [[a['answer_id'], get_code(a['body'])] for a in answers]
    return code

def prepare_query(q):
    return q.replace(' ', '%20')

def remove_empty(code):
    return [c for c in code if len(c[1]) > 0][:10]

def query_so(q):
    # Current approach gives answers to all SO questions matching search query
    q = prepare_query(q)
    json_data = get_questions(q)
    filtered = filter_data(json_data)
    # Return the ids of the accepted answers
    return collect_ids(filtered)

# Remove any ids from the SO results that we have from feedback
def reconcile_ids(f_ids, s_ids):
  f_id_set = set(f_ids)
  return f_ids + [s_id for s_id in s_ids if s_id not in f_id_set]

def query(q, feedback_ids):
    so_ids = query_so(q)
    ids = reconcile_ids(feedback_ids, so_ids)
    answers = get_answers(ids)
    return remove_empty(get_list_of_code(answers))
