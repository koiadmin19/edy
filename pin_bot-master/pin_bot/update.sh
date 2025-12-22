#!/bin/bash

DIR="/pin"
shadow_file="domains.yaml_shadow"
date_test=`date +%H`
shadow_test=`find $shadow_file -mtime +1`
if [[ $? -ne 0 ]]; then
  echo "no file, copying domains.yaml"
  cd $DIR && cp domains.yaml domains.yaml_shadow
fi
if [[ -n $shadow_test ]] && [[ $date_test -eq 22 ]]; then
  echo "old file, copying domains.yaml"
  cd $DIR && cp domains.yaml domains.yaml_shadow
fi

cd $DIR && git pull && ./pin_update.py 15431 20858 -1001680490161