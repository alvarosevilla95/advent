package main

import (
	"fmt"
	"strings"
	"unicode"

	"github.com/alvarosevilla95/AOC2018/util"
)

func main() {
	input := <-util.ReadFileLines("./input")
	fmt.Println(len(eval(input)))
	fmt.Println(optimize(input))
}

func eval(input string) string {
	data := []byte(input)
	for i := 0; i < len(data)-1; i++ {
		if data[i]^data[i+1] == 32 {
			data = append(data[:i], data[i+2:]...)
			if i -= 2; i < -1 {
				i = -1
			}
		}
	}
	return string(data)
}

func optimize(input string) int {
	min := len(input)
	for i := 0; i < 26; i++ {
		u := rune('a' + byte(i))
		data := strings.Replace(input, string(u), "", -1)
		data = strings.Replace(data, string(unicode.ToUpper(u)), "", -1)
		length := len(eval(data))
		if length < min {
			min = length
		}
	}
	return min
}
