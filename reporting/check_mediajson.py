import sys
import os
try:
    import configparser
except:
    import ConfigParser as configparser
import logging
# import json
import datetime
import argparse
import csv
import boto3

from get_solr_json import get_solr_json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_solr_docs(solr_url, api_key, query=None):
    '''Get just the documents for a given query'''
    cursorMark = '*'
    if not query:
        query = {
            'q': 'structmap_url:[* TO *]',
            'fl': 'id, structmap_url, collection_url, type_ss',
            'rows': 1000,
            'cursorMark': cursorMark,
            'sort': 'id asc'
        }
    docs = []
    num_read = 0
    solr_json = get_solr_json(solr_url, query, api_key=api_key)
    while len(solr_json['response']['docs']) > 0:
        cursorMark = solr_json['nextCursorMark']
        query['cursorMark'] = cursorMark
        docs.extend(solr_json['response']['docs'])
        num_read += len(solr_json['response']['docs'])
        if (num_read % 5000) == 0:
            logger.info(num_read)
        solr_json = get_solr_json(solr_url, query, api_key=api_key)
    return docs


def get_summary_objects(s3, bucket, prefix):
    bucket = s3.Bucket(bucket)
    return bucket.objects.filter(Prefix=prefix)


def get_media_json_keys(s3):
    # gather list of media json files "keys"
    # keys will be 'media_json/<UUID>-media.json'
    media_json_object_summaries = get_summary_objects(
        s3, 'static.ucldc.cdlib.org', 'media_json')
    media_json_keys = []
    count = 0
    for objsum in media_json_object_summaries:
        count += 1
        if (count % 5000) == 0:
            logger.info(count)
        media_json_keys.append(objsum.key)
    return media_json_keys


# this was REALLY slow
#        obj_summary = s3.ObjectSummary(bucket, '{}/{}'.format(folder, key))
#        try:
#            obj_summary.size
#        except botocore.exceptions.ClientError as e:
#            logger.info('missing media: {}'.format(row))
#            missing_media.append(row)


def missing_media_json(s3, solr_docs):
    missing_media = []
    count = 0
    bad_count = 0
    media_json_keys = get_media_json_keys(s3)
    for row in solr_docs:
        count += 1
        bucket, folder, key = row['structmap_url'].rsplit('/', 2)
        s3key = '{}/{}'.format(folder, key)
        if s3key not in media_json_keys:
            bad_count += 1
            if (bad_count % 1000) == 0:
                logger.info('{} bad so far'.format(bad_count))
            missing_media.append(row)
    return missing_media


def get_jp2000_file_sizes(s3):
    '''Get the sizes and UUID for all of the jp2000 files on s3
    Return a dictionary indexed by UUID'''
    jp2000_object_summaries = get_summary_objects(s3, 'ucldc-private-files',
                                                  'jp2000')
    uuid_sizes = {}
    for objsum in jp2000_object_summaries:
        folder, UUID = objsum.key.rsplit('/', 1)
        uuid_sizes[UUID] = objsum.size
    return uuid_sizes


def get_missing_jp2000_docs(s3, solr_docs):
    '''
    Build a list of all the docs with missing or 0 size jp2000
    '''
    uuid_sizes = get_jp2000_file_sizes(s3)
    problems = []
    for doc in solr_docs:
        print('checking doc : {}'.format(doc['id']))
        if doc.get('type_ss') == ['text']:
            continue
        UUID = doc['id']
        if not uuid_sizes.get(UUID):
            if uuid_sizes.get(UUID) is None:
                doc['size'] = -1
            else:
                doc['size'] = uuid_sizes[UUID]
            problems.append(doc)
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--outdir',
        default='reports',
        help='out directory for reports (defaults to reports)')
    parser.add_argument(
        '--inisection',
        default='new-index',
        help='section of report.ini to get Solr server info')

    if argv is None:
        argv = parser.parse_args()

    config = configparser.SafeConfigParser()
    config.read('report.ini')
    solr_url = config.get(argv.inisection, 'solrUrl')
    api_key = config.get(argv.inisection, 'solrAuth')
    print('SOLR: {}'.format(solr_url))
    nuxeo_solr_docs = get_solr_docs(solr_url, api_key)
    #with open('nuxeo_solr_docs.json', 'w') as foo:
    #    json.dump(nuxeo_solr_docs, foo, indent=2)

    print('\n\n{} nuxeo objects in Solr\n\n'.format(len(nuxeo_solr_docs)))

    print('\n\nGet object list from S3\n\n')
    s3 = boto3.resource('s3')
    media_json_keys = get_media_json_keys(s3)
    print('\n\nTotal number of media_json in s3:'
          '{}\n\n'.format(len(media_json_keys)))

    missing_media = missing_media_json(s3, nuxeo_solr_docs)
    missing_media_sorted = sorted(
        missing_media, key=lambda x: x['collection_url'])

    print('{} missing media_json files'.format(len(missing_media_sorted)))
    #with open('missing_media.json', 'w') as foo:
    #    json.dump(missing_media_sorted, foo, indent=2)

    today = datetime.date.today()
    fileout = os.path.join(argv.outdir, '{}-{}-{}.csv'.format(
        today, 'missing-media-json', argv.inisection))
    with open(fileout, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for obj in missing_media_sorted:
            writer.writerow((obj['collection_url'], obj['id'],
                             obj['structmap_url'], obj.get('type_ss')))

    missing_jp2000 = get_missing_jp2000_docs(s3, nuxeo_solr_docs)
    missing_jp2000_sorted = sorted(
        missing_jp2000, key=lambda x: x['collection_url'])
    print('{} missing jp2000 files'.format(len(missing_media_sorted)))
    #with open('missing_jp2000.json', 'w') as foo:
    #    json.dump(missing_jp2000_sorted, foo, indent=2)
    fileout = os.path.join(argv.outdir, '{}-{}-{}.csv'.format(
        today, 'missing-jp2000', argv.inisection))
    with open(fileout, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for obj in missing_jp2000_sorted:
            writer.writerow(
                (obj['collection_url'], obj['id'], obj['structmap_url'],
                 obj.get('type_ss'), obj['size']))


if __name__ == "__main__":
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    sys.exit(main())
