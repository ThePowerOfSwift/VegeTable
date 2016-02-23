#!/bin/bash
RANGE_START=2815
RANGE_END=8232

for i in `seq $RANGE_START $RANGE_END`;
do
	curl -O "ndb.nal.usda.gov/ndb/foods/show/$i?format=Abridged&reportfmt=csv"
done
