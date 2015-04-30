package pdxcmd

import (
	"encoding/json"
	"fmt"
	"strings"
	"testing"
)

type QStruct struct {
	Query struct {
		Term struct {
			Speaker string `json:"Speaker"`
		} `json:"term"`
	} `json:"query"`
}

func TestSpeakerQuery(t *testing.T) {
	speaker := "Adams"
	x := SpeakerQuery(speaker)
	dec := json.NewDecoder(strings.NewReader(x))

	var QS QStruct
	if err := dec.Decode(&QS); err != nil {
		t.Errorf("Error unmarshalling json: %#v \n", err)
	}
	//fmt.Printf("%#v \n", QS.Query.Term.Speaker)
	if s := QS.Query.Term.Speaker; s != "Adams" {
		t.Errorf("Speaker value incorrect: %v \n", s)
	}
}

func TestQueryUri(t *testing.T) {
	//speaker := "Adams"
	esc := ESConnect("localhost")
	out, err := esc.SearchUri("wat", "", map[string]interface{}{"q": `Speaker:Adams`, "size": `4`})
	if err != nil {
		t.Errorf("Error querying ES DSL: %#v\n", err)
	}

	fmt.Printf("Query Search: %#v \n\n\n ", out)
	for i, h := range out.Hits.Hits {
		marsh, err := json.Marshal(&h.Source)
		if err != nil {
			t.Errorf("Failed marshalling JSON: %#v\n", err)
		}
		fmt.Printf("Query %s: %d %#v\n", "Adams", i, string(marsh))
	}
}

func TestQueryStmt(t *testing.T) {
	q := "portland"
	esc := ESConnect("localhost")
	out := StatementQuery(esc, "wat", q, 500)

	stmts := make([]Statement, 0)

	fmt.Printf("%s\n", q)
	for i, h := range out.Hits.Hits {

		var stmt Statement
		err := json.Unmarshal([]byte(*h.Source), &stmt)
		if err != nil {
			t.Errorf("Failed marshalling JSON: %#v\n", err)
		}
		fmt.Printf("%d Speaker %s\n", i, string(stmt.Speaker))
		stmts = append(stmts, stmt)
	}
}
