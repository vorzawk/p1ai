#!/bin/bash
for numBlks in "10" "20"
do
	for numStks in "3" "5" "7" "10" "15"
	do
		echo Running tests for $numBlks blocks with $numStks stacks ...
		for i in {1..10}
		do
			echo Test $i summary
			timeout 4 ./randInitState.py $numBlks $numStks
			echo
		done
	done
done


