package pdxcmd

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
	"testing"
)

func datafile() string {
	d := EasyDate(2011, 1, 19)
	dir := MinutesDataDir(d)

	fi, err := ioutil.ReadFile(dir + "/statements.csv")
	if err != nil {
		panic(err)
	}
	text := string(fi)
	return text
}

func TestFindData(t *testing.T) {
	d := EasyDate(2011, 1, 19)
	dir := MinutesDataDir(d)

	fi, err := ioutil.ReadFile(dir + "/statements.csv")
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
	d := EasyDate(2011, 1, 19)

	c := make(chan []string)
	go ParseDoc(text, c)
	for s := range c {
		stmt := ParseTripleStmt(s, d)
		fmt.Println(stmt)
	}
	//t.Errorf("allgood")

}

func TestESLoad(t *testing.T) {
	text := datafile()
	d := EasyDate(2011, 1, 19)
	//testIndex := "pdxcmd_test"

	var stmts []Statement
	//stmts := make([]Statement, 0)
	c := make(chan []string)
	go ParseDoc(text, c)
	for s := range c {
		stmt := ParseTripleStmt(s, d)
		fmt.Println(stmt)
		stmts = append(stmts, stmt)
	}

	fmt.Printf("%#v\n", c)

	esc := ESConnect("localhost")
	blkindxr := esc.NewBulkIndexerErrors(10, 60)
	blkindxr.Start()
	for i, s := range stmts {
		//TODO: Insert elasticsearch
		blkindxr.Index("wat", "user", strconv.Itoa(s.Index), "", &s.Date, s, true)
		fmt.Printf("%#v %#v\n", i, s)
	}
	blkindxr.Stop()
}
