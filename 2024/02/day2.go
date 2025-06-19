package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

type Timer struct {
	start time.Time
}

func newTimer() *Timer {
	return &Timer{start: time.Now()}
}

func (t *Timer) Stop() time.Duration {
	duration := time.Since(t.start)
	fmt.Printf("Runtime was %v\n", duration)
	return duration
}

func getInput(path string) ([]string, error) {
	dat, err := os.ReadFile(path)
	if err != nil {
		return []string{}, fmt.Errorf("error whilst reading file, %v", err)
	}

	data := string(dat[:])

	return strings.Split(data, "\r\n"), nil
}

func convertStrArrToIntArr(strArr []string) ([]int, error) {
	intArr := make([]int, len(strArr))
	for i, val := range strArr {
		intVal, err := strconv.Atoi(val)
		if err != nil {
			return []int{}, err
		}
		intArr[i] = intVal
	}

	return intArr, nil
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	timer := newTimer()

	workingDirectiory, err := os.Getwd()
	if err != nil {
		os.Exit(1)
	}

	inputFile := filepath.Join(workingDirectiory, "day2_input.csv")
	inputData, err := getInput(inputFile)
	if err != nil {
		os.Exit(1)
	}

	convertedData := make([][]int, len(inputData))
	for i, arr := range inputData {
		intArr, err := convertStrArrToIntArr(strings.Split(arr, " "))
		if err != nil {
			os.Exit(1)
		}
		convertedData[i] = intArr
	}

	count := 0
	for _, arr := range convertedData {
		valid := true
		directionality := 0
		for i := len(arr) - 1; i >= 1; i-- {
			currVal := arr[i]
			nextVal := arr[i-1]
			difference := currVal - nextVal
			if abs(difference) > 3 || difference == 0 {
				valid = false
				break
			}

			if i == len(arr)-1 {
				if (currVal - nextVal) < 0 {
					directionality = -1
				} else {
					directionality = 1
				}
			}

			if currVal-nextVal > 0 && directionality == -1 {
				valid = false
				break
			} else if currVal-nextVal < 0 && directionality == 1 {
				valid = false
				break
			}
		}

		if valid {
			count++
		}
	}

	fmt.Printf("Count of safe arrays: %d\n", count)
	timer.Stop()
}
