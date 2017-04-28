# -*- coding: utf-8 -*-
import os
import argparse
try:
    import configparser
except:
    import ConfigParser as configparser
import datetime
import csv
from get_solr_json import get_solr_json, create_facet_dict
import requests

solr_collection_query = {
    'q': '*:*',
    'facet': 'true',
    'facet.field': [
        'collection_url',
    ],
    'rows': 0,
    'facet.limit': -1,  # get them all
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('outdir',)
    argv = parser.parse_args()

    config = configparser.SafeConfigParser()
    config.read('report.ini')

    solr_url = config.get('new-index', 'solrUrl')
    api_key = config.get('new-index', 'solrAuth')

    couchdb_url = config.get('couchdb', 'url')

    solr_collection_json = get_solr_json(solr_url, solr_collection_query,
                                         api_key=api_key)
    solr_collection_facet = create_facet_dict(solr_collection_json,
                                              'collection_url')
    diffs = []
    couch_less = []
    for curl, count in solr_collection_facet.items():
        cid = curl.rsplit('/', 2)[-2]
        url_couchdb_count = ''.join(('{}/couchdb/ucldc/_design/',
                                     'all_provider_docs/_view/',
                                     'by_provider_name_count?',
                                     'key="{}"')).format(couchdb_url, cid)
        resp = requests.get(url_couchdb_count, verify=False)
        couch_count = resp.json()['rows'][0]['value']
        if count != couch_count:
            diffs.append((cid, count, couch_count))
            if couch_count < count:
                couch_less.append((cid, count, couch_count))
            print "{} SOLR:{} COUCH:{}".format(cid, count, couch_count)
    print "FOR {} COLLECTIONS, {} have different counts".format(
        len(solr_collection_facet), len(diffs))
    today = datetime.date.today()
    with open(os.path.join(argv.outdir, '{}-{}.csv'.format(today,
              'couch-solr-count-diffs')), 'w') as fileout:
        csvwriter = csv.writer(fileout)
        csvwriter.writerow(('Collection ID', 'Solr count', 'Couch count'))
        for c in diffs:
            csvwriter.writerow(c)
    if couch_less:
        for c in couch_less:
            print "PROBLEM LESS COUCH - CID:{} SOLR:{} COUCH:{}".format(
                c[0], c[1], c[2])

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
