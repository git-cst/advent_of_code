package helpers

import (
	"fmt"
	"time"
)

type Timer struct {
	start time.Time
}

func NewTimer() *Timer {
	return &Timer{}
}

func (t *Timer) Start() {
	t.start = time.Now()
}

func (t *Timer) Stop() time.Duration {
	duration := time.Since(t.start)
	fmt.Printf("Runtime was %v\n", duration)
	return duration
}
