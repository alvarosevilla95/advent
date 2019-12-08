package util

import (
	"bufio"
	"os"
)

func ReadFileLines(url string) chan string {
	lines := make(chan string)
	go func() {
		defer close(lines)
		file, err := os.Open(url)
		if err != nil {
			panic(err)
		}
		defer file.Close()
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			lines <- scanner.Text()
		}
		if err := scanner.Err(); err != nil {
			panic(err)
		}
	}()
	return lines
}
