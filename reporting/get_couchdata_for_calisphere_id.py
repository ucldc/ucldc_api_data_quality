#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Use this to get data from the couchdb instance for a record from calisphere
# defaults to the staging environment
import sys
import os.path
import argparse
import urllib
import ConfigParser
import json
import requests

from get_solr_json import get_solr_json

DIR_SCRIPT = os.path.abspath(os.path.split(__file__)[0])

url_couchdb = 'https://harvest-stg.cdlib.org/couchdb/ucldc/'

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main(objid, save_solr_doc=False, save_couch_doc=False):
    config = ConfigParser.SafeConfigParser()
    config.read(DIR_SCRIPT+'/report.ini')
    solr_url = config.get('stg-index', 'solrUrl')
    api_key = config.get('stg-index', 'solrAuth')

    query = { 'q': objid }
    resp = get_solr_json(solr_url, query, api_key=api_key)
    doc = resp['response']['docs'][0]
    if save_solr_doc:
        with open('solr_doc_{}.json'.format(objid.replace('/','-')), 'w') as foo:
            json.dump(doc, foo)

    url_couch_doc=url_couchdb+urllib.quote(doc['harvest_id_s'], safe='')

    couch_doc = requests.get(url_couch_doc, verify=False).json()
    if save_couch_doc:
        with open('couch_doc_{}.json'.format(objid.replace('/','-')), 'w') as foo:
            json.dump(doc, foo)
    print
    print '==========================================================================='
    print 'Calisphere/Solr ID: {}'.format(objid)
    print 'CouchDB ID: {}'.format(doc['harvest_id_s'])
    print 'isShownAt: {}'.format(couch_doc['isShownAt'])
    print 'isShownBy: {}'.format(couch_doc.get('isShownBy', None))
    print 'object: {}'.format(couch_doc.get('object', None))
    print 'preview: https://calisphere.org/clip/500x500/{}'.format(couch_doc.get('object', None))
    print '==========================================================================='

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('objid', nargs=1,)
    parser.add_argument('--save_solr_doc', action='store_true',
            help='Save the solr doc to solr_doc_<id>.json')
    parser.add_argument('--save_couch_doc', action='store_true',
            help='Save the couch doc to couch_doc_<id>.json')
    argv = parser.parse_args()
    sys.exit(main(argv.objid[0], save_solr_doc=argv.save_solr_doc,
            save_couch_doc=argv.save_couch_doc))


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

