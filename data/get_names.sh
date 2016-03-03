#!/bin/bash

for xx in *; do temp="$(head -4 $xx | tail -1)"; echo ${temp:26:${#temp}-5}; done > ~/Desktop/vegetables.txt
