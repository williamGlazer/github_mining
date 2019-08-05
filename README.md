# github_mining
Functions to mine from the github HTML page and the github API

Requires [Selenium](https://pypi.org/project/selenium/) python package
Requires [geckodriver](https://www.softwaretestinghelp.com/geckodriver-selenium-tutorial/) which is a proxy for the FireFox web browser (incidentally, you also need FireFox)

---

## Scraper

#### get_depends(github_urls)
Mines the HTML from the github.com projects and returns a their dependants and dependencies ([ref](https://help.github.com/en/articles/listing-the-projects-that-depend-on-a-repository))

---

## Resquests

#### get_forks/pullreq/pullreq_commits(repo_url, user, passwd)
Sends a GET request to the github api which return a list of all forks/pullreq.commits

