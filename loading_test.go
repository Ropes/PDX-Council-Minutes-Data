package ops

import (
	"fmt"
	"io/ioutil"
	"strings"
	"testing"

	"github.com/ropes/PDX-Council-Minutes-Data"
)

func datafile() string {
	d := pathfinder.EasyDate(2011, 1, 19)
	dir := pathfinder.MinutesDataDir(d)

	fi, err := ioutil.ReadFile("../" + dir + "/statements.csv")
	if err != nil {
		panic(err)
	}
	text := string(fi)
	return text
}

func TestFindData(t *testing.T) {
	d := pathfinder.EasyDate(2011, 1, 19)
	dir := pathfinder.MinutesDataDir(d)

	fi, err := ioutil.ReadFile("../" + dir + "/statements.csv")
	if err != nil {
		t.Error(err)
		panic(err)
	}
	text := string(fi)

	if len(text) < 500 {
		t.Errorf(text)
	}

	lines := strings.Split(text, "\n")
	test_index := 12
	if len(lines) < 100 {
		t.Errorf(lines[test_index])
	}

	split := strings.Split(lines[test_index], "::")
	if len(split) != 3 {
		t.Errorf("%#v\n", split)
	}

}

func TestTextParse(t *testing.T) {
	text := datafile()
	d := pathfinder.EasyDate(2011, 1, 19)

	c := make(chan []string)
	go ParseDoc(text, c)
	for s := range c {
		stmt := ParseTripleStmt(s, d)
		fmt.Println(stmt)
	}
	t.Errorf("allgood")

}
