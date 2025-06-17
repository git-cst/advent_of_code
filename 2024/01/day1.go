package main

import (
	"fmt"
	"math"
	"os"
	"sort"
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

	return strings.Split(data, "\n"), nil
}

func solve(data []string) (float64, float64) {
	var arr1 []int
	var arr2 []int
	var distance float64
	var similarity float64

	hashmap := make(map[int]int)

	for _, s := range data {
		arrParts := strings.Split(s, ",")
		arr1val, err := strconv.Atoi(arrParts[0])
		if err != nil {
			return 0.0, 0.0
		}

		arr2val, err := strconv.Atoi(arrParts[1])
		if err != nil {
			return 0.0, 0.0
		}

		arr1 = append(arr1, arr1val)
		arr2 = append(arr2, arr2val)
		hashmap[arr2val] += 1
	}

	sort.Slice(arr1, func(i, j int) bool { return arr1[i] < arr1[j] })
	sort.Slice(arr2, func(i, j int) bool { return arr2[i] < arr2[j] })

	for i := 0; i < len(arr1); i++ {
		val := arr1[i] - arr2[i]
		distance += math.Abs(float64(val))
		similarity += float64(arr1[i] * hashmap[arr1[i]])
	}

	fmt.Printf("Distance is %v\n", distance)
	fmt.Printf("Similarity is %v\n", similarity)
	return distance, similarity
}

func main() {
	timer := newTimer()
	data, err := getInput("/home/csteenberg/projects/advent_of_code/2024/01/day1_input.csv")
	if err != nil {
		return
	}

	solve(data)
	timer.Stop()
}
