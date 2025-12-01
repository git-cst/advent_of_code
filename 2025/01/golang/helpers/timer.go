package helpers

import (
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

func (t *Timer) Elapsed() time.Duration {
	return time.Since(t.start)
}
