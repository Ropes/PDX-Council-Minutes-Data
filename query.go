package pdxcmd

import (
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/mattbaird/elastigo/lib"
)

//Generate a json string which to query ES
func SpeakerQuery(speaker string) string {
	query := `{
		"query": {
			"term": { "Speaker": "%s" }
		}
	}`
	return fmt.Sprintf(query, speaker)
}

//Queries elasticsearch for statements containing a term
func StatementQuery(c *elastigo.Conn, index, term string, size int) *elastigo.SearchResult {
	textQ := fmt.Sprintf("Text:%s", term)
	fmt.Printf("\nTextq: '%s'\n", textQ)
	query := map[string]interface{}{"q": textQ, "size": strconv.Itoa(size)}
	out, err := c.SearchUri(index, "", query)
	if err != nil {
		fmt.Printf("Failed to query statements: %#v\n", err)
		return nil
	}
	return &out
}

//Get statement structs via function params
func GetStmts(esc *elastigo.Conn, index, term string, limit int) (*[]Statement, error) {
	out := StatementQuery(esc, index, term, limit)
	stmts := make([]Statement, 0)

	for _, h := range out.Hits.Hits {
		var stmt Statement
		err := json.Unmarshal([]byte(*h.Source), &stmt)
		if err != nil {
			fmt.Printf("Failed marshalling JSON: %#v\n", err)
			return nil, err
		}
		stmts = append(stmts, stmt)
	}
	return &stmts, nil
}

//Run a generated ES Query string against ES and return the results
func QueryStmt(c *elastigo.Conn, index, type_str string, query map[string]interface{}) *elastigo.SearchResult {
	out, err := c.SearchUri(index, type_str, query)
	if err != nil {
		fmt.Printf("Failed to create search uri\n")
		return nil
	}
	return &out
}
