package main

import (
	ctx "context"
	"errors"
	"log"
	"net/http"
	"time"

	"github.com/google/go-github/v33/github"
	"golang.org/x/oauth2"
)

// ClientInterface is for testing
type ClientInterface interface {
	ListRepositories(string) ([]string, error)
	ListPRs(string, []string, int) ([]PrList, error)
}

// Client is the custom handler for all requests
type Client struct {
	Client  *github.Client
	Context ctx.Context
}

// PullRequestDetails contains organization name
// and PrLists
type PullRequestDetails struct {
	Organization string   `json:"organization,omitempty"`
	PrRepoLists  []PrList `json:"prlists,omitempty"`
}

// PrList contains repository name
// and the associated PRs
type PrList struct {
	Repository string               `json:"repository,omitempty"`
	PRs        []github.PullRequest `json:"prs,omitempty"`
}

// NewClient creates a new instance of GitHub client
func NewClient() ClientInterface {
	token := getEnvOrDefault(GitHubToken, "")
	context := ctx.Background()
	if token == "" {
		return Client{
			Client:  github.NewClient(nil),
			Context: context,
		}
	}
	oauth2Client := oauth2.NewClient(context, oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: token},
	))
	return Client{
		Client:  github.NewClient(oauth2Client),
		Context: context,
	}
}

// ListRepositories returns the list of all repositories
func (c Client) ListRepositories(org string) ([]string, error) {
	listOfRepositories := []string{}
	listOption := &github.RepositoryListByOrgOptions{
		ListOptions: github.ListOptions{
			PerPage: 20,
		},
	}
	for {
		repositories, response, err :=
			c.Client.Repositories.ListByOrg(c.Context, org, listOption)
		if err != nil {
			return nil, err
		}
		log.Printf("Response: %v", response)
		if response.StatusCode != http.StatusOK {
			return nil, errors.New("Could not get the response")
		}
		for _, repository := range repositories {
			listOfRepositories = append(listOfRepositories, *repository.Name)
		}

		if response.NextPage == 0 {
			log.Println("Breaking from the loop of repositories")
			break
		}
		// assign next page
		listOption.Page = response.NextPage
	}
	return listOfRepositories, nil
}

// ListPRs returns the list of PRs for a given organization and repository
func (c Client) ListPRs(org string, repos []string, daysCount int) ([]PrList, error) {
	prListOptions := &github.PullRequestListOptions{
		State: "all",
		ListOptions: github.ListOptions{
			PerPage: 20,
		},
	}
	dayDiff := daysCount * -1
	var pullRequests []PrList

	for _, repo := range repos {
		var listPullRequests []github.PullRequest
		prDateReached := false
		for {
			prs, response, err := c.Client.PullRequests.List(c.Context, org, repo, prListOptions)
			if err != nil {
				return nil, err
			}
			log.Printf("Response: %v", response)
			if response.StatusCode != http.StatusOK {
				return nil, errors.New("Could not get the response")
			}

			for _, pr := range prs {
				timeStamp := pr.CreatedAt
				startDate := time.Now().AddDate(0, 0, dayDiff)
				log.Println("timestamp", timeStamp, "start date", startDate, " if condition", timeStamp.Before(startDate))
				if timeStamp.Before(startDate) {
					prDateReached = true
					break
				}
				if pr.ClosedAt != nil && pr.MergedAt == nil {
					continue
				}
				listPullRequests = append(listPullRequests, *pr)
			}
			if prDateReached {
				break
			}
			if response.NextPage == 0 {
				log.Println("Breaking from the loop of repositories - PRs")
				break
			}
			// assign next page
			prListOptions.Page = response.NextPage

		}
		if len(listPullRequests) != 0 {
			pullRequestElement := PrList{
				Repository: repo,
				PRs:        listPullRequests,
			}
			pullRequests = append(pullRequests, pullRequestElement)
		}

	}
	return pullRequests, nil

}
