#!/bin/bash
List=(
https://manhua.dmzj.com/qwnjtyldtzm
https://manhua.dmzj.com/newgame
https://manhua.dmzj.com/jiabailideduoluo
)
for i in ${List[@]}
do dcdownloader $i &
done
wait
