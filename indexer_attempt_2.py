# --------------------------sources used for guidance-----------------------------
# https://www.python.org/doc/essays/graphs/
# http://aakashjapi.com/fuckin-search-engines-how-do-they-work/
# graphs and page rank:
# networkx documentation: https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html#directed-graphs
#                         https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html#edges
#                         https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html#networkx.algorithms.link_analysis.pagerank_alg.pagerank
# BeautifulSoup documentation for getting page title:https: //www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start


import bs4, nltk, re
from nltk.corpus import stopwords
import nltk.stem.porter as p
import networkx as nx
import lxml.html, os



# reads local html page and returns a tokenized and stemmed list of words
def read_file(file):
    try:
        with open("webpages/"+file,"r",encoding="UTF-8") as f:
            content = f.read()
            tokenization = nltk.word_tokenize(content)
            # set(to)
            removed_stopwords = [word.lower() for word in tokenization if word not in stopwords.words("english") and word.isalnum()]
            stemmer = p.PorterStemmer()
            stemmed_words = [stemmer.stem(token) for token in removed_stopwords]
        return stemmed_words
    except:
        return "p"
    return "p"

# reads a files content
def read_file_content(file):
    try:
        with open("webpages/" + file, "r", encoding="UTF-8") as f:
            content = f.read()
            return content
    except:
        return ""
    return""

# get all iinternal links from a webpage
def get_internal_links(html):
    file = open("webpages/" +html,"r",encoding="UTF-8")
    f_content = file.read()
    file.close()
    links_in_page = re.findall(r'[/][w][i][k][i][/]+[a-zA-z()-_]*', f_content)
    internal_links = []
    for link in links_in_page:
        if link !="/wiki/":
            base_url = "https://www.wikipedia.org"
            new_url = base_url + link.replace(" ","_")
            internal_links.append(new_url)
        #  print(new_url)
    return list(set(internal_links))


# # gets ALL internal links from a given webpage's content, converts relative links to full links
# def get_all_links(page_content):
#     parsed = lxml.html.fromstring(page_content)
#     valid_links = []
#     for link in parsed.xpath('//a/@href'):
#         # convert relative link to full link
#         if "http://" not in link and "https://" not in link and "www." not in link:
#             baseurl = "https://" + str(os.path.basename(page_content))
#             newurl = baseurl + link.replace(" ", "")
#             # add link to list of potentially valid links
#             valid_links.append(newurl)
#         # select the url in href for all a tags(links)
#         else:
#             # appends a full link to list of valid links
#             valid_links.append(link)
#     # returns list of links on the page
#     return valid_links

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
            #baseurl = "http://" + str(os.path.basename(url))
            newurl = url + link.replace(" ", "")
            # add link to list of potentially valid links
            valid_links.append(newurl)
        # select the url in href for all a tags(links)
        else:
            # appends a full link to list of valid links
            valid_links.append(link)
    return valid_links


# converts dat file to dictionary
def dat_to_dict(data):
    dict = eval(open(data, "r", encoding="UTF-8").read())
    return dict

# creates a directed graph representing the incoming and outgoing links of all indexed files.
# returns dictionary mapping urls to pageranks
# decided to  calculate pagerank index before retrieval to save time during retrieval
def get_pageranks(dict):
    links_dict = dat_to_dict(dict)
    graph = {}

    # creates directed graph
    for key in links_dict.keys():
        content = read_file_content(key)
        to_links = change_relative_to_absolute(get_all_links(content), links_dict[key])
        #to_links = get_all_links(key)  # gets all internal links of current page
        # lists all links if they are links that are indexed in index.dat and not self loops
        filtered_list = [link for link in to_links if link in links_dict.values() and link != links_dict[key]]
        # adds filtered_list to a node's neighbors list
        graph[links_dict[key]] = filtered_list
        # makes a Directed graph out of the graph adjacency matrix
        nx_graph = nx.DiGraph(graph)

    print("page ranks calculated")
    print(graph)
    # returns dictionary of pageranks for each node on graph
    return nx.pagerank(nx_graph)


# readsand retrieve'sa web page's title
def get_page_title(file):
    try:
        soup = bs4.BeautifulSoup(open("webpages/" + file, "r", encoding="UTF-8").read(),"lxml")
        title = soup.title.string
        # remove most special characters from title, used because result would not show up if something  like
        # ™ is in the title
        title = re.sub(r'[^a-zA-z0-9:. |]', '', title)
        return title
    except:
        print("error")

# indexes page contents and url information
def indexer():
    file_urls = dat_to_dict("index.dat")  # reads index.dat as dictionary
    # stores each document's data in format : {"file": {"url": "www.com", "pagerank": 0.5, "count": 2424},"file2": ...}
    docs_dat = {}
    # stores each document's data in format : {"word": {"file1": 2, "file2": 324, "file3": ...}, "word2": ...}
    inverted_dict = {}
    pageranks = get_pageranks("index.dat") # gets pageranks of each dictionary
    count = 0  # for console, to see progress of indexing
    for item in file_urls.keys():
        file = item
        url = file_urls[item]
        content = read_file(file)
        # sets value for document attributes
        docs_dat[file] = {}
        docs_dat[file]["url"] = url
        docs_dat[file]["count"] = len(content)
        docs_dat[file]["pagerank"] = pageranks[url]
        docs_dat[file]["title"] = get_page_title(file)

        #sets inverted dictionary values and c ounts
        for word in list(set(content)):
            print([w for w in content if w == word])
            if word not in inverted_dict.keys():
                inverted_dict[word] = {}
                inverted_dict[word][file] = len([w for w in content if w == word])
            else:
                inverted_dict[word][file] = len([w for w in content if w == word])
        count += 1
        print("Files indexed: " + str(count))
    # saves inverted index to invindex.dat
    with open("invindex.dat","w",encoding="UTF-8") as invindex_dat:
        invindex_dat.write(str(inverted_dict))
    # saves document data to docs.dat
    with open("docs.dat","w",encoding="UTF-8") as docs:
        docs.write(str(docs_dat))

    # returns inverted index
    return inverted_dict


# -------------main ----------------------------
print(indexer())

#get_page_title("1.html")
#print(get_internal_links("1.html"))

#print(make_graph("index.dat"))