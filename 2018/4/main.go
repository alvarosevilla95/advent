package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/alvarosevilla95/AOC2018/util"
)

type SleepCycle struct {
	Start time.Time
	End   time.Time
	Id    int
}
type Event struct {
	Type int
	Time time.Time
	Id   int
}
type Log []Event

func (l Log) Len() int           { return len(l) }
func (l Log) Less(i, j int) bool { return l[i].Time.Before(l[j].Time) }
func (l Log) Swap(i, j int)      { l[i], l[j] = l[j], l[i] }

func main() {
	var logs Log
	for line := range util.ReadFileLines("./input") {
		if strings.Contains(line, "shift") {
			line = line[1:]
			words := strings.Split(line, "]")
			t := parseTime(words[0])
			rest := words[1]
			idstr := strings.Split(rest, "#")[1]
			idstr = strings.Split(idstr, " ")[0]
			id, _ := strconv.Atoi(idstr)
			event := Event{
				Type: 0,
				Time: t,
				Id:   id,
			}
			logs = append(logs, event)
		}
		if strings.Contains(line, "falls") {
			line = line[1:]
			words := strings.Split(line, "]")
			t := parseTime(words[0])
			event := Event{
				Type: 1,
				Time: t,
			}
			logs = append(logs, event)
		}
		if strings.Contains(line, "wakes") {
			line = line[1:]
			words := strings.Split(line, "]")
			t := parseTime(words[0])
			event := Event{
				Type: 2,
				Time: t,
			}
			logs = append(logs, event)
		}
	}
	sc := make(map[int][]SleepCycle)
	var cur SleepCycle
	var curid int
	sort.Sort(logs)
	for _, e := range logs {
		switch e.Type {
		case 0:
			curid = e.Id
		case 1:
			cur = SleepCycle{
				Id:    curid,
				Start: e.Time,
			}
		case 2:
			cur.End = e.Time
			sc[curid] = append(sc[curid], cur)
		}
	}
	var maxid int
	var maxmin int
	var maxminvalue int
	for id, scs := range sc {
		var total time.Duration
		var minutes [60]int
		for _, s := range scs {
			total += s.End.Sub(s.Start)
			for i := s.Start.Minute(); i < s.End.Minute(); i++ {
				minutes[i] += 1
			}
		}
		mm := 0
		m := 0
		for i, v := range minutes {
			if v > m {
				mm = i
				m = v
			}
		}
		if m > maxminvalue {
			maxid = id
			maxmin = mm
			maxminvalue = m
		}
	}
	fmt.Println(maxid * maxmin)
	fmt.Println(maxid)
	fmt.Println(maxmin)
}

var layout = "2006-01-02 15:04"

func parseTime(str string) time.Time {
	t, _ := time.Parse(layout, str)
	return t
}
