# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import print_function
import couchdb
s=couchdb.Server('https://127.0.0.1/couchdb')
db=s['ucldc']

# <codecell>

def histogram_field_value(field_path):
    viewname = 'qa_reports/{0}_value'.format(field_path)
    view=db.view(viewname, group_level=2)
    reduced_list = [r for r in view]
    reduced_list.sort(key=lambda row: -int(row['value']))
    return reduced_list

# <codecell>

hist_list = histogram_field_value('sourceResource.subject.name')
for row in hist_list:
    if row['value'] > 1000:
        print(row)

# <codecell>


