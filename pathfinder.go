package pathfinder

import (
	"path/filepath"
	"strconv"
	"time"
)

func MinutesDataDir(date time.Time) string {
	y, m, d := date.Date()
	return filepath.Join("data", strconv.Itoa(y),
		strconv.Itoa(int(m)), strconv.Itoa(d))
}
