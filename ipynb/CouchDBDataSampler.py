# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# CouchDb Data Sampler notebook
# =============================
# 
# This should provide a base for creating random samples of documents in a collection in Couch DB.
# It will create a new db "collection_sample_<cid>_<date>" in couchdb for use in QA.

# <codecell>

from __future__ import print_function
import json
import random
import datetime
import couchdb

# <codecell>

collection_id = '1678' # NOTE: is a string, not a number though numeric data
sample_size = 3

# <codecell>

# NOTE: the calls below get the results from https://54.84.142.143/couchdb/ucldc/_design/all_provider_docs/_view/by_provider_name?key="1678"
server = couchdb.Server()
cdb = server['ucldc']
v = cdb.view('all_provider_docs/by_provider_name',
             key=collection_id)
doc_ids = []
for row in v:
    doc_ids.append(row['id'])
print('Docs in collection:{}'.format(len(doc_ids)))

# <codecell>

population_size = len(doc_ids)
sample_ids = []
# NOTE: Each time this is run, a different sample set will be generated. Remember that notebooks cache results!
for i in range(0, sample_size):
    rand_index = random.randint(0, population_size - 1)
    sample_ids.append(doc_ids[rand_index])
print(sample_ids)

# <codecell>

# create new db for sample data
db_name = 'collection_sample_{}_{}'.format(collection_id, datetime.date.today())
sample_db = server.create(db_name)

# <codecell>


