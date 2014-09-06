package ops

import (
	"io/ioutil"
	"strings"
	"testing"

	"github.com/ropes/PDX-Council-Minutes-Data"
)

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
