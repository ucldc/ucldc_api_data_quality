#! /bin/bash
#set -x
. ~/.harvester-env  # COUCHDB_PASSWORD, other secrets? still a bit of risk?
. ./dq/bin/activate # all the goodies
ipython notebook --ip="0.0.0.0" --profile=nbserver ipynb &> nbserver.log &
echo $! > nbserver.pid
disown
