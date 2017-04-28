# -*- coding: utf-8 -*-
import argparse
try:
    import configparser
except:
    import ConfigParser as configparser
from get_solr_json import get_solr_json
import requests

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('collection_id')
    parser.add_argument(
        'outdir',
        nargs=1, )
    argv = parser.parse_args()
    config = configparser.SafeConfigParser()
    config.read('report.ini')

    solr_url = config.get('new-index', 'solrUrl')
    api_key = config.get('new-index', 'solrAuth')

    couchdb_url = config.get('couchdb', 'url')
    cid = argv.collection_id
    url_couchdb_collection_ids = '{}/couchdb/ucldc/_design/all_provider_docs' \
        '/_view/by_provider_name?key="{}"'.format(couchdb_url, cid)
    print("URL:{}".format(url_couchdb_collection_ids))
    #may need to do paging here
    resp = requests.get(url_couchdb_collection_ids, verify=False)
    rows = resp.json()['rows']
    couchdb_ids = [x['id'] for x in rows]

    solr_url = config.get('new-index', 'solrUrl')
    api_key = config.get('new-index', 'solrAuth')

    #get solr ids
    solr_query = {
        'rows': 100,
        'sort': 'id asc',
        'fl': 'harvest_id_s',
        'q':
        'collection_url:"https://registry.cdlib.org/api/v1/collection/{}/"'.
        format(cid),
        'cursorMark': '*'
    }
    solr_ids = []
    while 1:
        solr_json = get_solr_json(solr_url, solr_query, api_key=api_key)
        solr_docs = solr_json['response']['docs']
        if not solr_docs:
            break
        solr_query['cursorMark'] = solr_json['nextCursorMark']
        solr_ids.extend([x['harvest_id_s'] for x in solr_docs])

    not_in_solr = []
    for couchid in couchdb_ids:
        if couchid not in solr_ids:
            not_in_solr.append(couchid)

    print(not_in_solr)

# Copyright © 2016, Regents of the University of California
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the University of California nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
