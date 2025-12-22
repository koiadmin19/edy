#!/bin/bash

DIR=/home/dave/check-channels/

lines=`egrep -h -A 5 "\-$1[^0-9]" $DIR/{baoyu,nvwang,meigui,gongzhu}/touliang_upstream.conf | grep weight | wc -l`

if [ $lines -le 1 ]; then
  echo "不成扣"
  exit 0
fi

xin_value_check=`egrep -h "[^a-zA-Z]$1[^0-9]" $DIR/{baoyu,nvwang,meigui,gongzhu}/touliang_xin.conf | wc -l`

if [ $xin_value_check -le 1 ]; then
  echo "xin 冲突"
  exit 0
fi


full_deduction_check=`grep -h -A 5 $1 $DIR/{baoyu,nvwang,meigui,gongzhu}/touliang_upstream.conf | grep -A 1 不扣 | grep -v '#'`
no_deduction_check=`grep -h -A 5 $1 $DIR/{baoyu,nvwang,meigui,gongzhu}/touliang_upstream.conf | grep -A 1 扣量 | grep -v '#'`

if [[ -z $full_deduction_check ]]; then
  echo "全成扣"
  exit 0
fi

if [[ -z $no_deduction_check ]]; then
  echo "不成扣"
  exit 0
fi

output=`grep -h -A 5 $1 $DIR/{baoyu,nvwang,meigui,gongzhu}/touliang_upstream.conf | grep -A 1 '扣量' |grep weight | tail -n1 | cut -d= -f2 | cut -d';' -f1`

echo $output成
exit 0