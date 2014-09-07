package ops

import (
	"fmt"
	"strings"
	"time"

	"github.com/ropes/PDX-Council-Minutes-Data"
)

//Statement contains fields for speaker and what they said
//as well as the statements index in the document and date.
type Statement struct {
	Speaker string
	Text    string
	index   int
	date    time.Time
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
		c <- split
	}
	close(c)
}

//TODO: Load data to ES

func main() {
	d := pathfinder.EasyDate(2011, 1, 19)
	dir := pathfinder.MinutesDataDir(d)

	fmt.Println(dir)
}
