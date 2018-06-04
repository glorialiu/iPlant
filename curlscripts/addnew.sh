#!/bin/bash -x

for n in {1000..1002}; do
	curl --header "Content:application/json" --data '{"id":'"$n"'}' http:\//localhost:8080/new
done

