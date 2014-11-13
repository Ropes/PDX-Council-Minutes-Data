package pdxcmd

import (
	"path/filepath"
	"strconv"
	"time"
)

//Returns a time.Date object based on the Year, Month, and Date only
func EasyDate(year, month, date int) time.Time {
	return time.Date(year, time.Month(month), date, 0, 0, 0, 0, time.UTC)
}

//Returns a path from the projects main directory to a meeting date's
//data directory. Formatted as follows
//project_dir/data/
//    2014/
//        /<month/
//            /<day of filing>/
//                minutes.pdf
//                log?
//                processed_data_files
func MinutesDataDir(date time.Time) string {
	y, m, d := date.Date()
	return filepath.Join("data", strconv.Itoa(y),
		strconv.Itoa(int(m)), strconv.Itoa(d))
}
