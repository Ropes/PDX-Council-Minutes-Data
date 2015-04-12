package pdxcmd

import "fmt"

func SpeakerQuery(speaker string) string {
	query := `{
		"query": {
			"term": { "Speaker": "%s" }
		}
	}`
	return fmt.Sprintf(query, speaker)
}

/*
func QuerySpeech(speechText string) {

}
*/
