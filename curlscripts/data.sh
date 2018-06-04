#!/bin/bash

for id in {1000..1002}; do

	for n in {1..10}; do
		curl --header "Content:application/json" --data '{"id":'"$id"',"data":49}'  http:\//localhost:8080/
	done
done

