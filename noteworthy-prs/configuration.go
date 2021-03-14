package main

// Configuration reads the input config file
type Configuration struct {
	Organizations       []Organization `yaml:"organizations"`
	DaysCount           int            `yaml:"days"`
	FileName            string         `yaml:"filename"`
	PrettyPrintFileName string         `yaml:"prettyprintfile"`
}

// Organization represents GitHub organization
type Organization struct {
	Organization OrganizationStructure `yaml:"organization"`
}

// OrganizationStructure has information about particular
// GitHub Organization
type OrganizationStructure struct {
	Name string `yaml:"name"`
}
