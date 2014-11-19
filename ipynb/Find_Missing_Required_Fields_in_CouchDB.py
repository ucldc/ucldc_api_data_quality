# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Find missing data in UCLDC couchdb

# <markdowncell>

# This is a notebook that is a starting point for QA against the couchdb database currently used for storing UCLDC harvested records. Can add cells for checking other data values. There must be a "_value" QA view in couchdb for the functions below to work.

# <codecell>

#import some basic useful libraries and functions
from __future__ import print_function
import sys
import os

# <markdowncell>

# Connect to the couchdb database. The database name is 'ucldc' for our system.

# <codecell>

import couchdb
s=couchdb.Server('https://127.0.0.1/couchdb')
db=s['ucldc']

# <markdowncell>

# Create functions for finding missing field data.

# <codecell>

def get_missing_for_field(field_path, collection_id=None):
    '''Calls the couchdb view corresponding to <field_path>_value, using start/end key values to get only
    documents which are MISSING the field entirely.
    If no collection_id is given, it will work on all documents in the DB and could be very slow.
    '''
    viewname = 'qa_reports/{0}_value'.format(field_path)
    start_key = ["__MISSING__"]
    end_key = ["__MISSING__"]
    if collection_id:
        start_key.append(str(collection_id))
        end_key.append(str(collection_id))
    end_key.append({}) # empty dict
    view=db.view(viewname, startkey=start_key, endkey=end_key,group_level=3)
    missing_list = [r for r in view]
    return missing_list

def get_missing_for_field_in_collections(field_path, collection_ids):
    '''Get missings for a number of collections'''
    missing_list = []
    for cid in collection_ids:
        missing_list.extend(get_missing_for_field(field_path, collection_id=cid))
    return missing_list

# <markdowncell>

# Unfortunately, blank or "null" values need to be handled differently

# <codecell>

def get_null_for_field(field_path, collection_id=None):
    '''Calls the couchdb view corresponding to <field_path>_value, using start/end key values to get only
    documents which have null or blank string values for the field.
    If no collection_id is given, it will work on all documents in the DB and could be very slow.
    '''
    viewname = 'qa_reports/{0}_value'.format(field_path)
    start_key = []
    end_key = [""]
    if collection_id:
        start_key.append(str(collection_id))
        end_key.append(str(collection_id))
    end_key.append({}) # empty dict
    print("SKEY:{} EKEY:{}".format(start_key, end_key))
    view=db.view(viewname, startkey=start_key, endkey=end_key, group_level=3)
    null_list = [r for r in view]
    return null_list

def get_null_for_field_in_collections(field_path, collection_ids):
    '''Get null or blank for a number of collections'''
    missing_list = []
    for cid in collection_ids:
        null_list.extend(get_missing_for_field(field_path, collection_id=cid))
    return null_list

# <markdowncell>

# This will print out all the records found for the criteria. This could be a *very* long list.

# <codecell>

#now flag problems, there are certain items that should never be missing
def report_missing_for_field(field, collection_id=None):
    '''convenience function for reporting'''
    missing = get_missing_for_field(field, collection_id=collection_id)
    for row in missing:
        print('Missing {0}: {1}'.format(field, row['key'][2]), file=sys.stderr) #outputting to stderr make red bkgnd

# <codecell>

report_missing_for_field('dataProvider', collection_id=1675)

# <codecell>

missing = get_missing_for_field('sourceResource.identifier')
print('Number missing identifier:{}'.format(len(missing)))
collection_ids = [row['key'][1] for row in missing]
collection_ids = set(collection_ids) # this will give unique collection ids for missing id docs
print('Collection ids:{}'.format(collection_ids))
print('First 10:{}'.format([row['key'][2] for row in missing[:10]]), file=sys.stderr)

# <codecell>

report_missing_for_field('sourceResource.title')

# <codecell>

report_missing_for_field('isShownBy', collection_id=1675)

# <codecell>

report_missing_for_field('isShownBy')

# <codecell>

missing = get_missing_for_field_in_collections('isShownBy', (1675, 1750))
for row in missing:
    print('Missing "isShownBy" for {}'.format(row['key'][2]), file=sys.stderr)

# <codecell>

### missing = get_missing_for_field('sourceResource.collection.description')
### print('MISSING collection descrip:{}'.format(len(missing)))
null = get_null_for_field('sourceResource.collection.description')
print('null collection descrip:{}'.format(len(null)))
for i in null[:10]:
    print(i)

# <codecell>


