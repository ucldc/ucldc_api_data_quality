# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# CouchDb Data Sampler notebook
# =============================
# 
# This should provide a base for creating random samples of documents in a collection in Couch DB.
# It will create a new db **`ucldc_samples_from_<cid>_<date>`** in couchdb for use in QA.

# <codecell>

from __future__ import print_function
import os
import json
import random
import datetime
import couchdb

# <codecell>

collection_id = '1678' # NOTE: is a string, not a number though numeric data
sample_size = 3
SAMPLE_DB_NAME_TEMPLATE = 'ucldc_samples_from_{}_{}'

# <codecell>

# NOTE: the calls below get the results from https://54.84.142.143/couchdb/ucldc/_design/all_provider_docs/_view/by_provider_name?key="1678"
server = couchdb.Server()
server.resource.credentials = ('admin', os.environ['COUCHDB_PASSWORD'])
cdb = server['ucldc']

# <codecell>

def get_collection_ids(couchdb, collection_id):
    v = cdb.view('all_provider_docs/by_provider_name',
             key=collection_id)
    doc_ids = []
    for row in v:
        doc_ids.append(row['id'])
    return doc_ids

# <codecell>

def get_sample_ids(collection_ids, sample_size):
    population_size = len(collection_ids)
    sample_ids = set()
    # NOTE: Each time this is run, a different sample set will be generated. Remember that notebooks cache results!
    # It may also take more than sample_size loops, if collisions in random ids occur set will not grow
    while len(sample_ids) < sample_size:
        rand_index = random.randint(0, population_size - 1)
        sample_ids.add(collection_ids[rand_index])
    return sample_ids

# <codecell>

def create_samples_db(sourcedb, collection_id, sample_size=3):
    collection_ids = get_collection_ids(sourcedb, collection_id)
    sample_ids = get_sample_ids(collection_ids, sample_size)
    sample_db = server.create(SAMPLE_DB_NAME_TEMPLATE.format(collection_id, datetime.date.today()))
    for doc_id in sample_ids:
        sample_db[doc_id] = sourcedb[doc_id]
    return 'Created db {} with docs {}'.format(sample_db, sample_ids)

# <codecell>

print(create_samples_db(cdb, '1678'))

# <codecell>

# Takes a while, big collections will be slow
print(create_samples_db(cdb, '26094', sample_size=50))

# <codecell>


