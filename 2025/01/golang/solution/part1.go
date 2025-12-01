package solution

import (
	"fmt"
	"strconv"
)

func turnLeftP1(currState, runningTotal, magnitude int) (int, int) {
	newState := (currState - magnitude) % dialLimit
	if newState < 0 {
		newState += dialLimit
	}

	if newState == 0 {
		runningTotal += 1
	}

	return newState, runningTotal
}

func turnRightP1(currState, runningTotal, magnitude int) (int, int) {
	newState := (currState + magnitude) % dialLimit

	if newState == 0 {
		runningTotal += 1
	}

	return newState, runningTotal
}

func SolveP1(data []string) (int, error) {

	turnFuncs := make(map[string]func(int, int, int) (int, int))

	turnFuncs["L"] = turnLeftP1
	turnFuncs["R"] = turnRightP1

	runningTotal := 0
	currState := initialState
	for _, instruction := range data {
		direction := instruction[:1]
		magnitude, err := strconv.Atoi(instruction[1:])
		if err != nil {
			return 0, fmt.Errorf("could not convert string %q to integer", instruction[1:])
		}

		currState, runningTotal = turnFuncs[direction](currState, runningTotal, magnitude)
	}

	return runningTotal, nil
}
