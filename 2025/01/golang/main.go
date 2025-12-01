package main

import (
	"advent_of_code/2025/01/helpers"
	"advent_of_code/2025/01/solution"
	"fmt"
	"os"
)

func main() {
	data, err := helpers.GetInput("../data.csv")
	if err != nil {
		_ = fmt.Errorf("%w", err)
		os.Exit(1)
	}

	timer := helpers.NewTimer()
	timer.Start()
	password := solution.SolveP1(data)
	fmt.Printf("Part 1 password: %d\n", password)
	timer.Stop()

	timer.Start()
	password = solution.SolveP2(data)
	fmt.Printf("Part 2 password: %d\n", password)
	timer.Stop()
}
