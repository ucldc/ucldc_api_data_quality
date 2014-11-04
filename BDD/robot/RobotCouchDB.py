from __future__ import print_function
import sys
import couchdb
class RobotCouchDB:
    def __init__(self, url, name):
        print('URL: {0} NAME:{1}'.format(url,name), file=sys.stderr)
        self.db = couchdb.Server(url)[name]

    def get_couch_doc(self, docid):
        return self.db.get(docid)
