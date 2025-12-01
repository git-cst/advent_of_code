package main

import (
	"advent_of_code/2025/01/helpers"
	"advent_of_code/2025/01/solution"
	"fmt"
	"log"
)

func main() {
	data, err := helpers.GetInput("../data.csv")
	if err != nil {
		log.Fatal(err)
	}

	timer := helpers.NewTimer()
	timer.Start()
	password, err := solution.SolveP1(data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 1 password: %d\nRuntime was %v\n", password, timer.Elapsed())

	timer.Start()
	password, err = solution.SolveP2(data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 2 password: %d\nRuntime was %v\n", password, timer.Elapsed())
}
