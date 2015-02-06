==================
Data Quality Notes
==================

What I want to do in QA test
============================

Statements such as:


Given the Lapl 245 is "A Nice Title" for <docid>
when I get the corresponding couchdb document
then the couchdb sourceResource.title should contain "A Nice Title"

This is to verify that the code correctly maps and transforms data values.


Some tools looked at
====================

dataprofiler -- http://sourceforge.net/projects/dataquality/
    not useful, aimed at sql dbs couldn't start without a db connect

talend os -


DataCleaner - http://datacleaner.org/get_datacleaner_ce#

radi - http://radi-testdir.sourceforge.net/Radi_Home.html

testlink - http://www.testlink.org/

DPLA metadata profile v4
========================

Currently, just trying to validate that we have the required fields for records.

REQUIRED FIELDS:
in dpla:sourceResource
    Collection.title, collection.description
    Creator
    Date - original source date-unparsed, begin, end parse
    Format
    Language
    Place
    Publisher
    Rights
    Subject
    Title
    Type

in edm:WebResource
    Standerdized Rights Statement 

in ore:Aggregation
    DataProvider
    IsShownAt
    Object -- currently md5 but should become full url to UCLDC image access
    Preview


Notes on couchdb data source
============================

couchdb is not the best fit, mongo looks better -- this is not driving a specific app....
Need to have a script that checks for missing on required data points.

@id is bogus - need scheme of ids for solr index

urlencoded query:

https://54.84.142.143/couchdb/ucldc/_design/qa_reports/_view/isShownBy?startkey=[%22lapl-photos-marc%22,%22__MISSING__%22]&endkey=[%22lapl-photos-marc%22,{}]&group_level=3

un encoded:
https://54.84.142.143/couchdb/ucldc/_design/qa_reports/_view/isShownBy?startkey=["lapl-photos-marc","__MISSING__"]&endkey=["lapl-photos-marc",{}]&group_level=3

this gives lapl itesm where missing isShownBy which is derived from:

856$u

Notes on solr index
===================

http://107.21.228.130:8080/solr/dc-collection/select?q=*%3A*&rows=0&wt=json&indent=true&facet=true&facet.missing=true&facet.limit=100&facet.offset=0&facet.sort=count&facet.field=reference_image_md5  -- shows duplicate downloaded images

And using results from above, can find the problem documents:

http://107.21.228.130:8080/solr/dc-collection/select?q=reference_image_md5%3A12daf1784ea44975a0bb170dbe58238b&rows=3&wt=json&indent=true&facet=true&facet.query=true&facet.field=reference_image_md5


This will give unique values for a field in a given collection:

https://registry.cdlib.org/solr/query?q=*:*&fq=collection:"https://registry.cdlib.org/api/v1/collection/26094"&rows=1&wt=json&indent=true&facet=true&facet.query=true&facet.field=description_ss
