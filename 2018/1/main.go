package main

import (
	"fmt"
	"strconv"

	"github.com/alvarosevilla95/AOC2018/util"
)

func main() {
	GetTotalFreq()
	GetFirstDupFreq()
}

func GetTotalFreq() {
	total := 0
	for _, v := range getFreqValues() {
		total += v
	}
	fmt.Println(total)
}
func GetFirstDupFreq() {
	seen := make(map[int]bool)
	total := 0
	seen[0] = true
	for {
		for _, value := range getFreqValues() {
			total += value
			_, ok := seen[total]
			if ok {
				fmt.Println(total)
				return
			}
			seen[total] = true
		}
	}
}

func getFreqValues() []int {
	var values []int
	lines := util.ReadFileLines("./freq.txt")
	for line := range lines {
		value, _ := strconv.Atoi(line)
		values = append(values, value)
	}
	return values
}
