#!/bin/bash
OLDIFS=$IFS
IFS=","
FQDN=$2
USER=$3
while read cloneaddr description
 do
	 python3 pygog.py --cloneaddr $cloneaddr --fqdn $FQDN -o $USER --description $description
 done < $1
 IFS=$OLDIFS
