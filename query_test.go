package pdxcmd

import (
	"encoding/json"
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
