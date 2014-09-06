package ops

import (
	"io/ioutil"
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

	if len(fi) < 500 {
		t.Errorf(string(fi))
	}
}
