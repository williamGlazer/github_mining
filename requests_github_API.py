#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% IMPORTS

import requests
import time
from requests.auth import HTTPBasicAuth


#%% GET DATA FROM REQUEST

def get_requests(url, user, passwd):
    """
    makes a GET request to the github API
    user and passwd required to have 5000 request limit

    :Returns:
        - dictionnary of the json data
    """
    
    #get
    r = requests.get(url, auth=HTTPBasicAuth(user, passwd))
    
    #if timout
    if r.status_code == 403:
        print("LIMIT EXCEEDED")
        print("WAIT AN HOUR")
        i=1
        while r.status_code != 200:
            time.sleep(60)
            r = requests.get(url, auth=HTTPBasicAuth(user, passwd))
            print("{} MINUTES ELAPSED".format(i))
            i+=1
    elif r.status_code != 200:
        print(r.status_code)
        return []
    #return data
    data = r.json()
    return data


#%% PROG FCT
                
def progress(current, total):
    print("Currently at {:.2f}%".format(current/total*100))
    
    
#%% GET LIST OF FORKS
def get_forks(repo_url, user, passwd):
    """
    repo_url is formatted as AUTHOR/REPO
    user and passwd required to have 5000 request limit

    :Returns:
        - list of dict of forks
    """
    
    #auth for 5000 request/h limitprint("\nINPUT GITHUB AUTH TO GET BETTER REQUEST LIMIT")
    if user=='' or passwd=='':
        user = input('username : ')
        passwd = input('passwd :   ')

    #repo url
    github_fork_url = "https://api.github.com/repos/{}/forks?sort=stargazers&per_page=100&page="
    url = github_fork_url.format(repo_url)

    #fetch all pages
    forks = []
    i=1
    eop = False
    while not eop:
        print("\n\nFECTHING PAGE {}".format(i))
        data = get_requests(url+str(i), user, passwd)
        forks = forks + data
        i+=1
        if len(data) != 100:
            eop = True
    
    #reject private ones
    temp = forks
    for fork in temp:
        if fork['private'] == True:
            forks.remove(fork)
    print("{} private forks".format(len(temp)-len(forks)))

    return forks
    

#%% GET PULL REQUESTS
def get_pullReq(repo_url, user, passwd):
    """
    repo_url is formatted as AUTHOR/REPO
    user and passwd required to have 5000 request limit

    :Returns:
        - list of dict of pullreq
    """
    
    #auth for 5000 request/h limitprint("\nINPUT GITHUB AUTH TO GET BETTER REQUEST LIMIT")
    if user=='' or passwd=='':
        user = input('username : ')
        passwd = input('passwd :   ')

    #repo url
    github_pullReq_url = "https://api.github.com/repos/{}/pulls?state=all&per_page=100&page="
    url = github_pullReq_url.format(repo_url)

    #fetch all pages
    pullReq = []
    i=1
    eop = False
    while not eop:
        print("\n\nFECTHING PAGE {}".format(i))
        data = get_requests(url+str(i), user, passwd)
        pullReq = pullReq + data
        i+=1
        if len(data) != 100:
            eop = True
    
    return pullReq    


#%% GET COMMITS OF PULL REQ
    
def get_pullReq_commits(pullreq_url, user, passwd):
    """
    pullreq_url is from the dictionnary  outputted by get_pullreq
    dict['_links']['commits']['href']
    user and passwd required to have 5000 request limit

    :Returns:
        - list of dict of commits
    """
    
    #auth for 5000 request/h limitprint("\nINPUT GITHUB AUTH TO GET BETTER REQUEST LIMIT")
    if user=='' or passwd=='':
        user = input('username : ')
        passwd = input('passwd :   ')

    #fetch 250 max commits
    pullReq_commits = get_requests(pullreq_url, user, passwd)

    return pullReq_commits    
