#!/bin/bash
IN=$1
csvcut -c 2 $IN | sed 's/\"//' | sed 's/\(.*\)\"$/\1/' | sed 's/\"\"/\"/g'
