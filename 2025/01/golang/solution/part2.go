package solution

import (
	"fmt"
	"strconv"
)

func turnLeftP2(currState, runningTotal, magnitude int) (int, int) {
	newState := currState - magnitude

	if newState <= 0 {
		if currState != 0 {
			runningTotal += (-newState / dialLimit) + 1
		} else {
			runningTotal += -newState / dialLimit
		}
	}

	newState %= dialLimit
	if newState < 0 {
		newState += dialLimit
	}
	return newState, runningTotal
}

func turnRightP2(currState, runningTotal, magnitude int) (int, int) {
	newState := currState + magnitude

	if newState > (dialLimit - 1) {
		runningTotal += newState / dialLimit
	}

	return newState % dialLimit, runningTotal
}

func SolveP2(data []string) (int, error) {
	turnFuncs := make(map[string]func(int, int, int) (int, int))

	turnFuncs["L"] = turnLeftP2
	turnFuncs["R"] = turnRightP2

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
