#!/bin/bash

echo 'Starting program'
./data_collection_c.o  $1 $2
echo ''
echo 'Data collection finished, write 0000 to characteristic'
sleep 20
./data_collection_stop.sh
