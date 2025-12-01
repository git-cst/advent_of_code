package solution

import (
	"fmt"
	"os"
	"strconv"
)

func turnLeftP2(currState, runningTotal, magnitude int) (int, int) {
	newState := currState - magnitude

	if newState <= 0 {
		if currState != 0 {
			runningTotal += (-newState / 100) + 1
		} else {
			runningTotal += -newState / 100
		}
	}

	newState %= 100
	if newState < 0 {
		newState += 100
	}
	return newState, runningTotal
}

func turnRightP2(currState, runningTotal, magnitude int) (int, int) {
	newState := currState + magnitude

	if newState > 99 {
		runningTotal += newState / 100
	}

	return newState % 100, runningTotal
}

func SolveP2(data []string) int {
	turnFuncs := make(map[string]func(int, int, int) (int, int))

	turnFuncs["L"] = turnLeftP2
	turnFuncs["R"] = turnRightP2

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
