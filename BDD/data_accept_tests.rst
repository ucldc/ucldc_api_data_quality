want to do data comparisons on raw data to couchdb & solr outputs


When "LAPL MARC record <id>" field 260$c is 'X' then the couchdb <id> should be 'Y'

table like fitnesse looks cool

Tools found but rejected:
-------------------------
Avignon - out of date
Arbiter - out of date
madcow - web testing
Thucydides - web testing
jasmine - for javascript

Tools in running
----------------

TextTest - http://texttest.sourceforge.net/
FitNesse - http://www.fitnesse.org/FrontPage - java but python plugin
easyb - http://easyb.org/ - groovy
concordion - http://concordion.org/ has python wrapper
behave - https://github.com/behave/behave python
robotframework - http://robotframework.org/ python - 
lettuce - http://lettuce.it/ python
cucumber - http://cukes.info/ ruby more complete than lettuce


So take MARC record file (in json or xml) and dump of same doc in couchdb and solr.

Just do flat file comparisons, can worry about the test data syncing later.

going to take an OAC xml starting record and compare to it's couchdb and solr versions.

Let's select a good one:

honeyman-collection-the-robert-b-honeyman-jr-colle--http://ark.cdlib.org/ark:/13030/tf9580129n   - settlers woodcut?

http://dsc.cdlib.org/search?facet=type-tab&style=cui&raw=1&relation=ark:/13030/tf9p3012wq&docsPerPage=1&startDoc=659

https://54.84.142.143/couchdb/ucldc/honeyman-collection-the-robert-b-honeyman-jr-colle--http%3A%2F%2Fark.cdlib.org%2Fark%3A%2F13030%2Ftf9580129n

http://107.21.228.130:8080/solr/dc-collection/select?q=id%3A*tf9580129n*&wt=json&indent=true

ericson-photograph-collection--http://ark.cdlib.org/ark:/13030/ft958006cj - cyclists

http://dsc.cdlib.org/search?facet=type-tab&style=cui&raw=1&relation=ark:/13030/tf3489n5x0&startDoc=194&docsPerPage=1

https://54.84.142.143/couchdb/ucldc/ericson-photograph-collection--http%3A%2F%2Fark.cdlib.org%2Fark%3A%2F13030%2Fft958006cj

http://107.21.228.130:8080/solr/dc-collection/select?q=id%3Aericson-photograph-collection--*ft958006cj&wt=json&indent=true


honeyman-collection-the-robert-b-honeyman-jr-colle--http://ark.cdlib.org/ark:/13030/tf8h4nb84g - early redlands

http://dsc.cdlib.org/search?facet=type-tab&style=cui&raw=1&relation=ark:/13030/tf9p3012wq&docsPerPage=1&startDoc=299

https://54.84.142.143/couchdb/ucldc/honeyman-collection-the-robert-b-honeyman-jr-colle--http%3A%2F%2Fark.cdlib.org%2Fark%3A%2F13030%2Ftf8h4nb84g

http://107.21.228.130:8080/solr/dc-collection/select?q=id%3Ahoneyman-collection-the-robert-b-honeyman-jr-colle--*tf8h4nb84g&wt=json&indent=true

Some Results
------------

robotframework - http://robotframework.org/ python
==================================================

Got something workly quickly, but syntax is unfriendly


FitNesse - http://www.fitnesse.org/FrontPage - java but python plugin
=====================================================================

Can't get python plugin to work.....
tried python 2 style, now will go for python3
