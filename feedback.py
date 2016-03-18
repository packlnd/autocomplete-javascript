from elasticsearch import Elasticsearch
from flask import Flask
from flask import request
import json
import so_api

app = Flask(__name__)

@app.route('/feedback')
def record_feedback():
    query = request.args.get('query', None)
    docid = request.args.get('docid', -1)
    token = request.args.get('token', None)
    if query is None or docid < 0 or token != 'cse504':
        return 'Query and docid must be set.'

    es = get_es()

    # Need to get the document if it exists, and update
    # the keywords field
    curr_feedback = es.get(index='feedback', doc_type='event', id=docid, ignore=[404])

    body = [query]
    if curr_feedback['found']:
        body.append(curr_feedback['_source']['keywords'])

    event = {
        'keywords': ' '.join(body)
    }

    es.index(
        index='feedback',
        doc_type='event',
        id=docid,
        body=event
    )

    return 'OK'

@app.route('/inspect')
def inspect_document():
    docid = request.args.get('docid', -1)
    token = request.args.get('token', None)
    if docid < 0 or token != 'cse504':
        return 'Docid must be set.'

    es = get_es()

    # Need to get the document if it exists, and update
    # the keywords field
    curr_feedback = es.get(index='feedback', doc_type='event', id=docid, ignore=[404])

    if curr_feedback['found']:
        return str(curr_feedback['_source']['keywords'])
    else:
        return 'Not found'

def get_es():
    return Elasticsearch(
        [
            {
                'host': 'localhost',
                'port': 9292
            }
        ],
        http_auth=('cse504', 'JNPP@ss1')
    )

@app.route('/test')
def test():
    return 'Hello world!'

@app.route('/search')
def search_feedback():
    query = request.args.get('query', None)
    token = request.args.get('token', None)
    only_raw = request.args.get('raw', 'False') == True

    if query is None or token != 'cse504':
        return 'Query cannot be empty.'

    ids = []
    if not only_raw:
        es = get_es()
    
        search = {
            'query': {
                'match': {
                    'keywords': query
                }
            }
        }
    
        results = es.search(index='feedback', doc_type='event', body=search, size=5, _source=False)
    
        ids = [int(res['_id']) for res in results['hits']['hits']]

    # Now query SO for more results
    return json.dumps(so_api.query(query, ids))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
