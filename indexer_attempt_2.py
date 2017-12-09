# sources used for guidance
# https://www.python.org/doc/essays/graphs/
# http://aakashjapi.com/fuckin-search-engines-how-do-they-work/


import bs4, nltk, re
from nltk.corpus import stopwords
import nltk.stem.porter as p
import networkx as nx



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


# converts dat file to dictionary
def dat_to_dict(data):
    dict = eval(open(data, "r", encoding="UTF-8").read())
    return dict

# creates a directed graph representing the incoming and outgoing links of all indexed files.
# returns dictionary mapping urls to pageranks
def get_pageranks(dict):
    links_dict = dat_to_dict(dict)
    graph = {}

    # creates directed graph
    for key in links_dict.keys():
        to_links = get_internal_links(key)  # gets all internal links of current page
        # lists all links if they are links that are indexed in index.dat and not self loops
        filtered_list = [link for link in to_links if link in links_dict.values() and link != links_dict[key]]
        # adds filtered_list to a node's neighbors list
        graph[links_dict[key]] = filtered_list
        # makes a Directed graph out of the graph adjacency matrix
        nx_graph = nx.DiGraph(graph)

    # returns dictionary of pageranks for each node on graph
    return nx.pagerank(nx_graph)

#read index.dat - unused currently
def get_index_dat_items(dat):
    try:
        page = open(dat,"r")
        content = [item.split(" ") for item in page.readlines()]
        page.close()
        return content
    except:
        return ""
    return ""

def get_page_title(file):
    try:
        soup = bs4.BeautifulSoup(open("webpages/" + file, "r", encoding="UTF-8").read(),"lxml")
        return soup.title.string
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
        print(content)

        #sets inverted dictionary values and c ounts
        for word in list(set(content)):
            print([w for w in content if w == word])
            if word not in inverted_dict.keys():
                inverted_dict[word] = {}
                inverted_dict[word][file] = len([w for w in content if w == word])
            else:
                inverted_dict[word][file] = len([w for w in content if w == word])
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