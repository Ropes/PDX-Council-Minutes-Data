package pdxcmd

import (
	"fmt"
	"strconv"
	"strings"
	"time"

	"github.com/shutej/elastigo/lib"
)

//Statement contains fields for speaker and what they said
//as well as the statements index in the document and date.
type Statement struct {
	Speaker string
	Text    string
	Index   int
	Date    time.Time
}

//TODO: Find file locations based on date
//TODO: Read in files

func ParseDoc(text string, c chan []string) {
	lines := strings.Split(text, "\n")
	test_index := 12
	if len(lines) < 100 {
		panic(lines[test_index])
	}

	for _, v := range lines {
		split := strings.Split(v, "::")
		//fmt.Printf("%#v\n", split)
		c <- split
	}
	close(c)
}

func ParseTripleStmt(s []string, t time.Time) Statement {
	index, err := strconv.Atoi(s[0])
	if err != nil {
		panic(err)
	}
	stmt := &Statement{s[1], s[2], index, t}

	return *stmt
}

//Load statement data to ES
func LoadStatments(stmts *[]Statement, esc *elastigo.Conn, index, user string) error {
	blkindxr := esc.NewBulkIndexerErrors(10, 60)
	blkindxr.Start()
	for _, s := range *stmts {
		blkindxr.Index(index, user, strconv.Itoa(s.Index), "", &s.Date, s, true)
	}
	blkindxr.Stop()
	return nil
}

func mmain() {
	d := EasyDate(2011, 1, 19)
	dir := MinutesDataDir(d)

	fmt.Println(dir)
}
