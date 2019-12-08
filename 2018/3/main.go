package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/alvarosevilla95/AOC2018/util"
)

type Grid [1000][1000]int

type Value struct {
	Id   int
	X    int
	Y    int
	XLen int
	YLen int
}

func main() {
	var values []*Value
	grid := new(Grid)
	for line := range util.ReadFileLines("./input") {
		values = append(values, readLineValue(line))
	}

	fmt.Println(fillGrid(values, grid))

	for _, v := range values {
		if isIsolated(v, grid) {
			fmt.Println(v.Id)
		}
	}
}

func fillGrid(values []*Value, grid *Grid) int {
	totalDups := 0
	for _, v := range values {
		for i := v.X; i < v.X+v.XLen; i++ {
			for j := v.Y; j < v.Y+v.YLen; j++ {
				if grid[i][j] == 1 {
					totalDups += 1
				}
				grid[i][j] += 1
			}
		}
	}
	return totalDups
}

func isIsolated(value *Value, grid *Grid) bool {
	for i := value.X; i < value.X+value.XLen; i++ {
		for j := value.Y; j < value.Y+value.YLen; j++ {
			if grid[i][j] != 1 { //its own
				return false
			}
		}
	}
	return true
}

func readLineValue(line string) *Value {
	words := strings.Split(line, " ")
	idWord := words[0]
	idWord = idWord[1:] // skip #
	id, _ := strconv.Atoi(idWord)

	// skip words[1] ('@')

	crdWord := words[2]
	crds := strings.Split(crdWord, ",")
	x, _ := strconv.Atoi(crds[0])
	y, _ := strconv.Atoi(crds[1][:len(crds[1])-1]) //Remove ':'

	lenWord := words[3]
	lens := strings.Split(lenWord, "x")
	xlen, _ := strconv.Atoi(lens[0])
	ylen, _ := strconv.Atoi(lens[1])

	return &Value{
		Id:   id,
		X:    x,
		Y:    y,
		XLen: xlen,
		YLen: ylen,
	}

}
