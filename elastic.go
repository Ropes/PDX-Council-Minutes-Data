package pdxcmd

import (
	"flag"
	"log"

	"github.com/shutej/elastigo/lib"
)

var (
	host *string = flag.String("host", "localhost", "Local ES")
)

func ESConnect(host string) *elastigo.Conn {
	c := elastigo.NewConn()
	log.SetFlags(log.LstdFlags)
	c.Domain = host
	return c
}
