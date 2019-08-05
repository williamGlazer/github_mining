#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% IMPORTS

import time
import os
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options


#%%
def init_browser(headless=False):
    """
    Initialize selenium browser
    NEEDS TO BE CLOSED ( *.quit() )

    :Returns:
        - webdriver element
    """

    dirname = os.path.dirname(__file__)
    gecko_driver_path = os.path.join(dirname, 'geckodriver')
    options = Options()
    options.headless = headless
    browser = webdriver.Firefox(options=options, executable_path=gecko_driver_path)
    return browser


#%%
def get_depends(github_urls):
    """
    Gets dependents & dependencies from list of github_url of form AUTHOR/REPO

    :Returns:
        - dictionnary of Array of Array of dependents & dependencies
    """

    PAGE_CAP = 100

    pages_visited = 1
    depend_dict = {'dependents':[], 'dependencies':[]}
    n_urls = len(github_urls)

    if n_urls != 0:
        browser = init_browser(headless=True)
        for url in github_urls:
            #Shutdown browser to avoid memory cap after 100 tabs
            if pages_visited % PAGE_CAP == 0:
                browser.quit()
                browser = init_browser(headless=True)
            dep = get_depend(browser, url, dependencies=False)
            depend_dict['dependents'].append(dep['dependents'])
            depend_dict['dependencies'].append(dep['dependencies'])
            pages_visited += 1
            progress(pages_visited, n_urls)
        browser.quit()

    return depend_dict


#%%
def get_depend(browser, github_url, dependencies=False, dependants=False):
    """
    Gets dependencies ID from github_url

    :Returns:
        - Dict of depend
    """

    #get URL
    url = "https://github.com/PATH/network/DEP"
    url = url.replace('PATH', github_url)

    #recursive call
    if dependencies == dependants:
        dependencies = get_depend(browser, github_url, dependencies=True)
        dependants = get_depend(browser, github_url, dependants=True)
        return {'dependencies':dependencies, 'dependants':dependants}

    #otherwise
    elif dependencies:
        url = url.replace('DEP', 'dependencies')
    elif dependants:
        url = url.replace('DEP', 'dependents')

    #open browser & wait loading
    browser.get(url)
    time.sleep(.2)

    #verify if 404
    page_404 = browser.find_elements_by_xpath("//title[contains(text(),\'Page not found\')]") != []
    if page_404:
        depend = '404'

    #scrape HTML
    else:
        depend = []
        pages_left = True
        while pages_left:
            #find all links
            links = browser.find_elements_by_xpath(
                "//a[contains(@data-hovercard-type,\'repository\')\
                and (contains(@class,\'text-bold\') \
                 or contains(@data-octo-click,\'dep_graph_package\')\)]")
            for link in links:
                url = link.get_attribute("href")
                dep = url[19:] #remove 'github.com'
                if dep not in depend:
                    depend.append(dep)
            #get next button href
            buttons = browser.find_elements_by_xpath(
                "//a[contains(@class,\'btn btn-outline BtnGroup-item\')]")
            for b in buttons:
                if b.text == 'Next':
                    next_button = b
            try:
                url = next_button.get_attribute("href")
            #if none left, exit
            except:
                pages_left = False
            #if pages left, go to next
            else:
                browser.get(url)

    return depend


#%%
def progress(current, total):
    """
    Prints current progress
    """
    print("Currently at {:.2f}%".format(current/total*100))
