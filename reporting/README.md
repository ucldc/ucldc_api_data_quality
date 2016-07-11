# ucldc\_api\_data\_quality/reporting

These scripts are used to produce QA spreadsheets comparing the candidate Solr index being built to the existing index which powers Calisphere.

## Linux & Mac install

Have a version of python available on your machine.
It's probably best to make a `virtualenv` though not necessary.

Then 

	git clone https://github.com/mredar/ucldc_api_data_quality.git
	cd ucldc_api_data_quality/reporting
	# mkvirtualenv if you want
	pip install -r requirements.txt

## Windows install

http://conda.pydata.org/miniconda.html  <-- python 2.7

http://git-scm.com/download/win

#### initial setup
only do this once
```dos
conda create -n myenv python
activate myenv
git clone https://github.com/mredar/ucldc_api_data_quality.git
cd ucldc_api_data_quality/reporting
pip install -r requirements.txt
```

#### run again

```dos
activate myenv
cd ucldc_api_data_quality/reporting
```
if you need to update the code

```
git pull origin master
```

# Setup the data sources

The "calisphere" entry will be for the existing index to compare to, the "new-index" is the index being compared. You can actually compare any 2 Solr indexes that have the Calisphere schema by changing these URLs.

Now copy `report.ini.tmpl` to `report.ini` in the reporting directory and edit:

in `report.ini`:

```ini
[calisphere]
solrUrl = {{ solr for calisphere hostname}}/solr/query
solrAuth = {{ api_key }}

[new-index]
solrUrl = {{ hostname }}/{{ solr root path}}/query
solrAuth = {{ api_key }}
```

# Run Reports

From the `ucldc_api_data_quality/reporting` directory:

Main QA spreadsheet for counts comparison:

```shell
python qa_counts_new_calisphere_index.py {{ out directory }}
```

Will create a spreadsheets in the `{{ out directory }}` named YYYY-MM-DD-production-to-new.xlsx

Duplicates and missing QA spreadsheet: 

```shell
python qa_duplicates_and_missing_solr_index.py {{ out directory }}
```

Will create a spreadsheets in the `{{ out directory }}` named YYYY-MM-DD-duplicates_and_missing_fields.xlsx


# Tool for finding CouchDB data from Calisphere ID

This is something that needs to be done often when debugging data problems. We often find image or metadata problems for items in the stage environment (should work from production as well). This tool will display some information from the CouchDB document for an object with a given Calisphere ID. It can also save the corresponding Solr document and the corresponding CouchDB document for deeper analysis.

First, add an "index-stg" section to your report.ini:

```ini
[stg-index]
solrUrl = {{ stage hostname }}/{{ solr_root_path}}/solr_api/query
solrAuth = <api_key>
```

Activate your virtualenv setup for this project, then run:

`python get_couchdata_for_calisphere_id.py <calisphere id>`

This will display the following:

```text
===========================================================================
Calisphere/Solr ID: ark:/13030/kt8r29p8vp
CouchDB ID: 16289--http://ark.cdlib.org/ark:/13030/kt8r29p8vp
isShownAt: http://ark.cdlib.org/ark:/13030/kt8r29p8vp
isShownBy: http://content.cdlib.org/ark:/13030/kt8r29p8vp/hi-res
object?: fdfac47caec9e2be18c63d5c15aab637
===========================================================================
```

To save the full Solr doc, add the option --save_solr_doc
To save the full CouchDB doc, add the option --save_couch_doc

