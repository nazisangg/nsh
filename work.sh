#!/bin/bash 
# a is the group size
# i is how many round of game you would like to run.


for (( a = 2; a < 10; a++ )); do
	#statements
	echo $a
	for (( i = 0; i < 30; i++ )); do
		#statements
		echo $i
		python3 testNPlayers.py st qlearning 1 50 5 1 1 $a 1 $i
	done
done

