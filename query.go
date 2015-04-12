package pdxcmd

import (
	"fmt"

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

//Run a generated ES Query string against ES and return the results
func QueryStmt(c *elastigo.Conn, index, type_str string, query map[string]interface{}) *elastigo.SearchResult {
	out, err := c.SearchUri(index, type_str, query)
	if err != nil {
		fmt.Printf("Failed to create search uri\n")
		return nil
	}
	return &out
}

/*
func QuerySpeech(speechText string) {

}
*/
