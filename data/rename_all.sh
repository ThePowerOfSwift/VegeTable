#!/bin/bash

cd all_data/
pwd

ii=0
for xx in *;
do
mv $xx food_${ii}.csv
((ii++))
done

