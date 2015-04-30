package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/mattbaird/elastigo/lib"
	"github.com/ropes/PDX-Council-Minutes-Data"
)

var esc *elastigo.Conn

func QueryStatements(w http.ResponseWriter, r *http.Request) {
	out, err := pdxcmd.GetStmts(esc, "wat", "portland", 15)
	if err != nil {
		fmt.Fprintf(w, "Whoops %s didn't work!", r.URL.Path[1:])
	}
	j, err := json.Marshal(out)
	if err != nil {
		fmt.Fprintf(w, "JSON Marshaling failed: %#v", err)
	}
	fmt.Fprintf(w, "%s", string(j))
}

func main() {
	esc = pdxcmd.ESConnect("localhost")

	http.HandleFunc("/stmt", QueryStatements)
	http.ListenAndServe(":8080", nil)

}
