package helpers

import (
	"fmt"
	"os"
	"strings"
)

func GetInput(path string) ([]string, error) {
	dat, err := os.ReadFile(path)
	if err != nil {
		return []string{}, fmt.Errorf("error whilst reading file, %v", err)
	}

	data := string(dat[:])

	return strings.Split(data, "\r\n"), nil
}
