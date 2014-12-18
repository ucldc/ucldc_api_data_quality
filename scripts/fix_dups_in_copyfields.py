import os, sys
import shutil
import time
import PIL
import PIL.Image as Image
import boto
from boto.s3.key import Key
import solr

URL_SOLR = os.environ.get('URL_SOLR', 'http://107.21.228.130:8080/solr/dc-collection/')
#this is the list of acceptable input to solr index, needed because the 
#doc returned by solrpy has additional fields that err out on update.
INPUT_DOC_KEYS = ('id', 'collection_name', 'campus', 'repository',
                  'identifier', 'title', 'contributor', 'coverage',
                  'creator', 'date', 'description', 'format', 'identifier',
                  'language', 'publisher', 'relation', 'rights', 'source',
                  'subject', 'type', 
                  )
EXCLUDE_DOC_KEYS = ('score', 'timestamp')


def update_doc_from_solr_result_doc(solr_result_doc, exclude_doc_keys=EXCLUDE_DOC_KEYS):
    '''Convert a solr results document into on suitable for updating the record.
    Solr returns some extra data that makes the raw response document faile
    on update. Subset the fields and return a docuemtn suitable for updating 
    the index.
    '''
    solr_update_doc = {}
    for key, val in solr_result_doc.items():
        if key not in exclude_doc_keys:
            if key[-3:] != '_ss':
                solr_update_doc[key] = val
    return solr_update_doc

solr_db = solr.Solr(URL_SOLR)
resp = solr_db.select('*:*', sort='timestamp asc')
while(resp):
    for doc in resp.results:
        u = update_doc_from_solr_result_doc(doc)
        solr_db.add(u)
    solr_db.commit() #commit the 10 in the batch
    print u['id']; sys.stdout.flush() #check in every batch
    #NOTE: this does not work because of update to 
    # to timestamp. need to get head of results each time
    #### resp = resp.next_batch()
    resp = solr_db.select('*:*', sort='timestamp asc')
