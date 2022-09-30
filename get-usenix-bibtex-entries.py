#! /usr/bin/env python3

import requests

from bs4 import BeautifulSoup

#import bibtexparser

schedule_page = "https://www.usenix.org/conference/usenixsecurity22/technical-sessions"

def get_bibtex(req_url):
    resp = requests.get(req_url)

    page_soup = BeautifulSoup(resp.content, 'html.parser')

    bibtext = page_soup.find_all("div", "bibtex-text-entry bibtex-accordion-text-entry").pop().get_text()

    return bibtext

def __main__():
    #req_url = "https://www.usenix.org/conference/usenixsecurity22/presentation/cohen"
    #get_bibtex(req_url)

    technical_sessions_html = requests.get(schedule_page).content

    schedule_soup = BeautifulSoup(technical_sessions_html, 'html.parser')
    #session_title_tags = schedule_soup.find_all("h2", "node-title")
    #for title in session_title_tags:
    #    print(title.text.trim())
    papers = schedule_soup.find_all("article", "node-paper")

    base_url = "https://www.usenix.org"
    paper_urls = []

    for p in papers:
        links = p.find_all("a")
        paper_path_ext = links.pop().get("href")
        if "presentation" in paper_path_ext:
            paper_urls.append(base_url + paper_path_ext)
    
    #paper_titles = []
    #citations = []
    all_papers = open("/home/allison/Desktop/usenix-security-22.bib", "w")

    for u in paper_urls:
        bibtext = get_bibtex(u)
        all_papers.write(bibtext)
        #citations.append(bibtext)

    all_papers.close()
    

if __name__ == '__main__':
    __main__()
