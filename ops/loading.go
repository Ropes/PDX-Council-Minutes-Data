package ops

import (
	"fmt"
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
//TODO: Load data to ES

func mmain() {
	d := pathfinder.EasyDate(2011, 1, 19)
	dir := pathfinder.MinutesDataDir(d)

	fmt.Println(dir)
}
