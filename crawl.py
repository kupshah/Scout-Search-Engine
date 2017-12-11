# Final Project - crawl
# Kunaal Shah


# --------------------------sources used for guidance-----------------------------
# help from http://buildsearchengine.blogspot.com/ for inspiration on data structures and traversal methods
# for web crawlers
# Lecture slides presented in I-427 Search Informatics
# Instructors Brad Demarest and Rahul Raghatate


import urllib.request,re
import lxml.html
import os


# reads webpage, returns page contents
def read_page(url):
    try:
        # req = requests.Request(url, headers={'User-Agent': 'IUB-I427-kupshah'})
        page = urllib.request.urlopen(url)
        contents = page.read().decode(errors="replace")
        page.close()
        return contents
    except:
        return ""
    return ""


# gets all internal "/wiki/" pages in a web page's content
def get_internal_links(page_content):
    # finds all wiki links
    links_in_page = re.findall(r'[/][w][i][k][i][/]+[a-zA-z()-_]*', page_content)
    internal_links = []
    for link in links_in_page:
        # sets relative wiki path to absolute path
        if link != "/wiki/":
            base_url = "https://www.wikipedia.org"
            new_url = base_url + link.replace(" ","_")
            internal_links.append(new_url)
        #  print(new_url)
    return list(set(internal_links))


# gets ALL internal links from a given webpage's content, converts relative links to full links
def get_all_links(page_content):
    parsed = lxml.html.fromstring(page_content)
    valid_links = parsed.xpath('//a/@href')
    # returns list of links on the page
    return valid_links


# given a list and a url, changes relative links to full links
def change_relative_to_absolute(links,url):
    valid_links = []
    for link in links:
        # change relative links to full links
        if "http://" not in link and "https://" not in link and "www." not in link:
            newurl = url + link.replace(" ", "")
            # add link to list of potentially valid links
            valid_links.append(newurl)
            print("changed " + link + " to " + newurl)
        # select the url in href for all a tags(links)
        else:
            # appends a full link to list of valid links
            valid_links.append(link)
    return valid_links


# joins two lists of links, disregarding duplicate items
def union(a, b):
    for link in b:
        if link not in a:
            a.append(link)


# generates list of many many many links starting from a seed, using depth first traversal
def dfs_crawl_web(seed, max_pages): # depth-first crawl implementation
    queue = [seed]  # links that have not been visited
    visited = []  # links that have been visited
    dat_content = {}
    while queue and len(visited) < max_pages:  # while there are items in queue
        page = queue.pop()  # remove top item in queue
        if page not in visited:  # if that item has not been visited
            try:
                print("Visiting " + page)
                page_content = read_page(page)  # reads page
                file_path = "webpages/" + str(len(visited) + 1) + ".html"  # generates file name to save content to
                file_out = open(file_path, "w", encoding="utf-8")  # opens file
                file_out.write(page_content)  # writes page content to file
                file_out.close()  # closes file
                dat_content[str(len(visited) + 1) + ".html"] = page  # str(len(visited) +1) +".html" + " " + page + "\n"
                union(queue, change_relative_to_absolute(get_all_links(page_content),
                                                         page))  # add links from that page to the queue
                visited.append(page)  # add the page to the list of visited links
                print("added " + page)
            except:
                print("Error reading" + page)
    dat_file = open("index.dat", "w", encoding="utf-8")  # opens index.dat
    dat_file.write(str(dat_content))  # "saves info for all generated files"
    dat_file.close()  # closes dat file
    print(visited)  # prints list of visited pages


# generates list of many many many links starting from a seed, using breadth-first first traversal
def bfs_crawl_web(seed, max_pages):  # depth-first crawl implementation
    queue = [seed]  # links that have not been visited
    visited = []  # links that have been visited
    dat_content = {}

    while queue and len(visited) < max_pages:  # while there are items in queue
        page = queue[0]  # get first page in queue
        if page not in visited:  # if that page has not been visited
            try:
                print("visiting" + page)
                page_content = read_page(page)  # reads page
                file_path = "webpages/" + str(len(visited) + 1) + ".html"  # generates file name to save content to
                file_out = open(file_path, "w", encoding="utf-8")  # opens file
                file_out.write(str(page_content))  # writes page content to file
                file_out.close()  # closes file
                dat_content[str(len(visited) + 1) + ".html"] = page  # str(len(visited) +1) +".html" + " " + page + "\n"
                union(queue, change_relative_to_absolute(get_all_links(page_content), page))  # add links from that page to the queue
                visited.append(page)  # add the page to the list of visited links
            except:
                print("error reading" + page)
        del queue[0] # remove the visited page from queue
    dat_file = open("index.dat", "w", encoding="utf-8")  # opens index.dat
    dat_file.write(str(dat_content))  # "saves info for all generated files"
    dat_file.close()  # closes dat file
    print(visited)  # prints list of visited pages


# user inputs seed, type of traversal (dfs or bfs) and max _pages to visit,
def crawl(seed, traversal, n):
    if traversal == "dfs":
        bfs_crawl_web(seed,n)
    elif traversal == "bfs":
        dfs_crawl_web(seed,n)
    else:
        return "Invalid traversal type"


# ------------------main----------------------


# saves 200 urls from web crawl
bfs_crawl_web(200,"http://www.imdb.com")
#crawl("http://www.starwars.com","bfs",200)

