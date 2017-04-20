try:
    import configparser
except:
    import ConfigParser as configparser
import json
import csv
import boto3

from get_solr_json import get_solr_json

if __name__ == "__main__":
    config = configparser.SafeConfigParser()
    config.read('report.ini')
    solr_url = config.get('new-index', 'solrUrl')
    api_key = config.get('new-index', 'solrAuth')
    print('SOLR: {}'.format(solr_url))
    cursorMark = '*'
    query = {
        'q': 'structmap_url:[* TO *]',
        'fl': 'id, structmap_url, collection_url',
        'rows': 1000,
        'cursorMark': cursorMark,
        'sort': 'id asc'
    }
    struct_map_urls = []
    num_read = 0
    solr_json = get_solr_json(solr_url, query, api_key=api_key)
    while len(solr_json['response']['docs']) > 0:
        cursorMark = solr_json['nextCursorMark']
        query['cursorMark'] = cursorMark
        struct_map_urls.extend(solr_json['response']['docs'])
        num_read += len(solr_json['response']['docs'])
        if (num_read % 5000) == 0:
            print(num_read)
        solr_json = get_solr_json(solr_url, query, api_key=api_key)
    with open('structmap_urls.json', 'w') as foo:
        json.dump(struct_map_urls, foo, indent=2)

    print('\n\n{} nuxeo objects in Solr\n\n'.format(num_read))
    print('\n\nGet object list from S3\n\n')

    s3 = boto3.resource('s3')
    # gather list of media json files "keys"
    # keys will be 'media_json/<UUID>-media.json'
    bucket = s3.Bucket('static.ucldc.cdlib.org')
    media_json_summary_objs = bucket.objects.filter(Prefix='media_json')
    media_json_keys = []
    count = 0
    for objsum in media_json_summary_objs:
        count += 1
        if (count % 5000) == 0:
            print(count)
        media_json_keys.append(objsum.key)

    print('\n\nTotal number of media_json in s3:'
          '{}\n\n'.format(len(media_json_keys)))

    bad_media = []
    count = 0
    bad_count = 0
    for row in struct_map_urls:
        count += 1
        # if (count % 1000) == 0:
        #    print('Processed: {}'.format(count))
        bucket, folder, key = row['structmap_url'].rsplit('/', 2)
        #x, bucket = bucket.rsplit('/', 1)
        s3key = '{}/{}'.format(folder, key)
        if s3key not in media_json_keys:
            bad_count += 1
            if (bad_count % 1000) == 0:
                print('{} bad so far'.format(bad_count))
            bad_media.append(row)

# this was REALLY slow
#        obj_summary = s3.ObjectSummary(bucket, '{}/{}'.format(folder, key))
#        try:
#            obj_summary.size
#        except botocore.exceptions.ClientError as e:
#            print('missing media: {}'.format(row))
#            bad_media.append(row)

    bad_media_sorted = sorted(bad_media, key=lambda x: x['collection_url'])

    print('{} missing media_json files'.format(len(bad_media_sorted)))
    with open('bad_media.json', 'w') as foo:
        json.dump(bad_media_sorted, foo, indent=2)

    with open('bad_media.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for obj in bad_media_sorted:
            writer.writerow((obj['collection_url'], obj['id'],
                             obj['structmap_url']))
