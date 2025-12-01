package solution

import (
	"fmt"
	"os"
	"strconv"
)

func turnLeftP1(currState, runningTotal, magnitude int) (int, int) {
	newState := (currState - magnitude) % 100
	if newState < 0 {
		newState += 100
	}

	if newState == 0 {
		runningTotal += 1
	}

	return newState, runningTotal
}

func turnRightP1(currState, runningTotal, magnitude int) (int, int) {
	newState := (currState + magnitude) % 100

	if newState == 0 {
		runningTotal += 1
	}

	return newState, runningTotal
}

func SolveP1(data []string) int {
	turnFuncs := make(map[string]func(int, int, int) (int, int))

	turnFuncs["L"] = turnLeftP1
	turnFuncs["R"] = turnRightP1

	runningTotal := 0
	currState := 50
	for _, instruction := range data {
		direction := instruction[:1]
		magnitude, err := strconv.Atoi(instruction[1:])
		if err != nil {
			fmt.Printf("Could not convert string %q to integer\n", instruction[1:])
			os.Exit(1)
		}

		currState, runningTotal = turnFuncs[direction](currState, runningTotal, magnitude)
	}

	return runningTotal
}
