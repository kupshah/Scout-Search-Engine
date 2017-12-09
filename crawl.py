import urllib.request,re

# crawl crawls Wikipedia pages, by depth-first search implementation.

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


# joins two lists, disregarding duplicate items
def union(a, b):
    for link in b:
        if link not in a:
            a.append(link)


# generates list of many many many wikipedia links starting from a seed
def crawl_web(seed, max_pages): # depth-first crawl implementation
    queue = [seed]  # links that have not been visited
    visited = []  # links that have been visited
    dat_content = {}
    while queue and len(visited) < max_pages:  # while there are items in queue
        page = queue.pop()  # remove top item in queue
        if page not in visited:  # if that item has not been visited
            page_content = read_page(page)  # reads page
            file_path = "webpages/" + str(len(visited) + 1) + ".html"  # generates file name to save content to
            file_out = open(file_path, "w", encoding="utf-8")  # opens file
            file_out.write(page_content)  # writes page content to file
            file_out.close()  # closes file
            dat_content[str(len(visited) + 1) + ".html"] = page  # str(len(visited) +1) +".html" + " " + page + "\n"
            union(queue, get_internal_links(page_content))  # add links from that page to the queue
            visited.append(page)  # add the page to the list of visited links
    dat_file = open("index.dat", "w", encoding="utf-8")  # opens index.dat
    dat_file.write(str(dat_content))  # "saves info for all generated files"
    dat_file.close()  # closes dat file
    return visited  # returns list of visited pages


# ------------------main----------------------

# saves 100 urls from web crawl
crawl_web("https://en.wikipedia.org/wiki/Star_Wars", 500)

#print(get_all_links(read_page("https://www.google.com")))