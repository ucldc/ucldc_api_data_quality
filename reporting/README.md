# ucldc\_api\_data\_quality/reporting

These scripts are used to produce QA spreadsheets comparing the candidate solr index being built to the existing index which powers Calisphere.

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

The "calisphere" entry will be for the existing index to compare to, the "new-index" is the index being compared. You can actually compare any 2 solr indexes that have the Calisphere schema by changing these URLs.

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

