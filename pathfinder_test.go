package pdxcmd

import (
	"testing"
	"time"
)

func TestPathing(t *testing.T) {
	d := time.Date(2011, 1, 19, 0, 0, 0, 0, time.UTC)
	mdd := MinutesDataDir(d)
	if mdd != "data/2011/1/19" {
		t.Errorf("Path incorrect! %+v\n", mdd)
	}

}
