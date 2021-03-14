package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
	"text/template"

	yaml "gopkg.in/yaml.v2"
)

const (
	// ConfigFile env variable that can be overridden
	ConfigFile = "CONFIG_FILE"
	// GitHubToken env variable
	GitHubToken = "GITHUB_TOKEN"
	// PrettyPrintFilePath env variable
	PrettyPrintFilePath = "PRETTY_PRINT_FILE_PATH"
)

func readConfiguration() Configuration {

	log.Println("Reading the configuration file")
	var config Configuration
	var configFile string = getEnvOrDefault(ConfigFile, "config.yaml")
	fileContents, err := ioutil.ReadFile(configFile)
	if err != nil {
		log.Fatalf("Couldn't read the config file %v, Err: %v", configFile, err)
	}
	err = yaml.Unmarshal(fileContents, &config)
	if err != nil {
		log.Fatalf("Error while parsing the config file %v, Err: %v", configFile, err)
	}
	return config
}

func main() {

	config := readConfiguration()
	client := NewClient()
	log.Println("Listing repositories for each organization")
	var expectedPrList []PullRequestDetails
	for _, organization := range config.Organizations {
		repos, err := client.ListRepositories(organization.Organization.Name)
		if err != nil {
			log.Fatalf("Err: %v", err)
			return
		}
		log.Printf("List for %v is : %v", organization, repos)
		pRs, err := client.ListPRs(organization.Organization.Name, repos, config.DaysCount)
		if err != nil {
			log.Fatalf("Err: %v", err)
			return
		}

		expectedPrs := PullRequestDetails{
			Organization: organization.Organization.Name,
			PrRepoLists:  pRs,
		}

		expectedPrList = append(expectedPrList, expectedPrs)
	}
	err := saveIntoFile(expectedPrList, config.FileName)
	if err != nil {
		log.Fatalf("Err: %v", err)
		return
	}
	err = prettyPrint(expectedPrList, getEnvOrDefault(PrettyPrintFilePath, config.PrettyPrintFileName))
	if err != nil {
		log.Fatalf("Err: %v", err)
	}
}

func getEnvOrDefault(env, defaultValue string) string {
	value, isPresent := os.LookupEnv(env)
	if isPresent {
		return value
	}
	return defaultValue
}

func saveIntoFile(pRs []PullRequestDetails, fileName string) error {
	fileContents, err := json.MarshalIndent(pRs, "", "")
	if err != nil {
		return err
	}
	return ioutil.WriteFile(fileName, fileContents, 0644)
}

func prettyPrint(expectedPrs []PullRequestDetails, fileName string) error {

	t, err := template.ParseFiles("static/template.html")
	if err != nil {
		return err
	}

	f, err := os.Create(fileName)
	if err != nil {
		return err
	}
	err = t.Execute(f, expectedPrs)
	return err
}
