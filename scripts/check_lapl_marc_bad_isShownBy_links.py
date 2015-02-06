import os
import json
import urllib
from delay_decorator import pause_2b_nice
import datetime

@pause_2b_nice
def get_url(url):
    return urllib.urlretrieve(url)

j=json.load(open('isShownBy?startkey=[%22lapl-photos-marc%22,%20%22__MISSING__%22]&endkey=[%22lapl-photos-marc%22,%20%7B%7D]&group_level=3'))
rows=j['rows']
missing = []
bad_link_data = []
n=0
for r in rows:
    n += 1
    if not r['key'][1].startswith('http'):
        missing.append((r['key'][2], r['key'][1]))
    else:
        try:
            fname, headers = get_url(r['key'][1])
            os.remove(fname)    
        except Exception, e:
            bad_link_data.append((r['key'][2], r['key'][1]))
    if n % 1000 == 0:
        print("{} processed.".format(n))

print('BAD LINKS:{}'.format(bad_link_data))
print('MISSING LINKS:{}'.format(missing))

with open('bad_links', 'w') as foo:
    for x in bad_link_data:
        foo.write('{}\n'.format(x))
with open('missing', 'w') as foo:
    for x in missing:
        foo.write('{}\n'.format(x))
