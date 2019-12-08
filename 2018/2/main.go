package main

import (
	"fmt"

	"github.com/alvarosevilla95/AOC2018/util"
)

func main() {
	fmt.Println(GetChecksum())
	fmt.Println(GetMatch())
}

func GetChecksum() int {
	var total2s, total3s int
	for id := range util.ReadFileLines("./boxes.txt") {
		has2, has3 := getCounts(id)
		if has2 {
			total2s += 1
		}
		if has3 {
			total3s += 1
		}
	}
	return total2s * total3s
}

func getCounts(id string) (bool, bool) {
	counts := make(map[rune]int)
	for _, c := range id {
		counts[c] += 1
	}
	var has2, has3 bool
	for _, v := range counts {
		if v == 2 {
			has2 = true
		}
		if v == 3 {
			has3 = true
		}
	}
	return has2, has3
}

func GetMatch() string {
	var ids []string
	for id := range util.ReadFileLines("./boxes.txt") {
		for _, seen := range ids {
			cnt, common := getMismatch(id, seen)
			if cnt == 1 {
				return common
			}
		}
		ids = append(ids, id)
	}
	return ""
}

func getMismatch(id1, id2 string) (int, string) {
	ms := 0
	var common []byte
	for i := range id1 {
		if id1[i] != id2[i] {
			ms += 1
		} else {
			common = append(common, id1[i])
		}
	}
	return ms, string(common)
}
