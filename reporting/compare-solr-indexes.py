# -*- coding: utf-8 -*-
import os
import re
import argparse
import requests
import csv

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

date_match = re.compile(r'(\d\d\d\d)-\1')

url_solr_new_collection = 'https://harvest-stg.cdlib.org/solr_api/select?' \
        'wt=json&q=collection_url:"https://registry.cdlib.org/api/v1/' \
        'collection/{}/"&rows=100&sort=id asc&cursorMark={}'

url_solr_prod_doc = 'https://solr.calisphere.org/solr/select?wt=json&q=id:"{}"'


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(
            past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] == self.current_dict[o])


def compare_collection(cid,
                       new_solr=url_solr_new_collection,
                       old_solr=url_solr_prod_doc,
                       api_key=None):
    print('---- working on : {} ----'.format(cid))
    cid = cid.strip()
    headers = {'X-Authentication-Token': api_key}
    next_cursorMark = '*'  # * is starting cursorMark
    n = 0
    changes = []
    added = []
    removed = []
    print('URLSSS:{}'.format(url_solr_new_collection))
    while 1:
        solr_query = url_solr_new_collection.format(cid, next_cursorMark)
        print("QUERY: {}".format(solr_query))
        resp = requests.get(solr_query, headers=headers, verify=False)
        resp.raise_for_status()
        resp_obj = resp.json()
        next_cursorMark = resp_obj['nextCursorMark']
        docs = resp_obj['response']['docs']
        if not len(docs):
            print('--- {} : {} items ---'.format(cid, n))
            break
        for doc in docs:
            n += 1
            prod_query = url_solr_prod_doc.format(doc['id'])
            resp = requests.get(prod_query, headers=headers, verify=False)
            resp_obj = resp.json()
            prod_doc = resp_obj['response']['docs'][0]
            if doc != prod_doc:
                d = DictDiffer(doc, prod_doc)
                changed = d.changed()
                for k in changed:
                    if k not in (
                            '_version_',
                            'timestamp', ):
                        changes.append((doc['id'], doc['harvest_id_s'], k,
                                        prod_doc[k], doc[k]))
                        print("{} {} CHANGED - {} OLD:{} NEW:{}".format(doc[
                            'id'], doc['harvest_id_s'], k, prod_doc[k], doc[
                                k]))

                if d.added() or d.removed():
                    print('{} {} ADDED:{} REMOVED:{}'.format(doc['id'], doc[
                        'harvest_id_s'], d.added(), d.removed()))
                    if d.added():
                        added.append(
                            (doc['id'], doc['harvest_id_s'], d.added()))
                    if d.removed():
                        removed.append(
                            (doc['id'], doc['harvest_id_s'], d.removed()))
        print('--- Processed {} docs. ---'.format(n))
        print('--- Changed values: {} ---'.format(len(changes)))
        print('--- Added values: {} ---'.format(len(added)))
        print('--- Removed values: {} ---'.format(len(removed)))
    if changes:
        with open('{}-changed.csv'.format(cid), 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(('ID', 'HARVEST ID', 'field', 'old value',
                                'new value'))
            for row in changes:
                csvwriter.writerow(row)
    if added:
        with open('{}-added.csv'.format(cid), 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(('ID', 'HARVEST ID', 'added'))
            for row in added:
                csvwriter.writerow(row)
    if removed:
        with open('{}-removed.csv'.format(cid), 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(('ID', 'HARVEST ID', 'removed'))
            for row in removed:
                csvwriter.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cid', help='Collection ID')
    parser.add_argument('--api_key', help='Solr API KEY')
    args = parser.parse_args()

    api_key = args.api_key if args.api_key else os.environ['SOLR_API_KEY']

    compare_collection(args.cid, api_key=api_key)

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
