#!/usr/bin/env python3
print("Content-Type: text/html")    
print()                             
 
import cgi,cgitb
import nltk
import math
from nltk.corpus import stopwords as sw
#nltk.download('stopwords')
#nltk.download('punkt')

cgitb.enable() #for debugging

# converts dat file to dictionary
def dat_to_dict(data):
    dict = eval(open(data, "r", encoding="UTF-8").read())
    return dict


# takes in search query, inverted index, and doc maps, returns the urls of all files that the word is in
def retrieve(words, invindex, docs):
    inv_index_dict = dat_to_dict(invindex)
    docs_dict = dat_to_dict(docs)

    # stores the urls for the results
    page_results = {}

    # search for each word in inverted index, if a word belongs to file(s) all files are stores in the results array
    for word in words:
        if word in inv_index_dict.keys():
            for hit in inv_index_dict[word].keys():
                if hit not in page_results.keys():
                    page_results[hit] = {}
                    page_results[hit]["url"] = docs_dict[hit]["url"]
                    tf = (inv_index_dict[word][hit]/docs_dict[hit]["count"])
                    idf = 1/(1 + math.log10(docs_dict[hit]["count"]))
                    tf_idf = tf * idf
                    page_results[hit]["word_relevance"] = tf_idf
                    page_results[hit]["title"] = docs_dict[hit]["title"]
                    page_results[hit]["rank"] = page_results[hit]["word_relevance"] * docs_dict[hit]["pagerank"]
                else:
                    tf = (inv_index_dict[word][hit] / docs_dict[hit]["count"])  # calculate term frequency for word
                    idf = 1 / (1 + math.log10(docs_dict[hit]["count"]))  # calculate document frequency for word
                    tf_idf = tf * idf  # calculate tf-idf
                    page_results[hit]["word_relevance"] += tf_idf
                    page_results[hit]["title"] = docs_dict[hit]["title"]
                    page_results[hit]["rank"] = page_results[hit]["word_relevance"] * docs_dict[hit]["pagerank"]
    # sorts results by page rank, results in list of ".html" files
    sorted_results = sorted(page_results.keys(), reverse = True, key=lambda x: (page_results[x]["rank"]))
    # returns the url for each result in the file
    final_results = [[page_results[hit]["url"],page_results[hit]["title"],page_results[hit]["rank"]] for hit in sorted_results]
    print("<p>" + str(len(docs_dict.keys())) + " webpages searched.</p>")
    return final_results


# search interface, user enters search terms, results are retrieved and returned
def search(words):
    tokenized_terms = nltk.word_tokenize(words)
    stemmer = nltk.PorterStemmer()
    stemmed_terms = [stemmer.stem(token).lower() for token in tokenized_terms if token not in sw.words("english")]
    results = retrieve(stemmed_terms, "invindex.dat", "docs.dat")
    return results

form = cgi.FieldStorage()
query = form.getfirst("query", "test_default").lower() 
#query = form.getvalue('query')
print ("<html>")
print ("<head>")
print ("<title>" + query + " - ScOut Results</title>")
print ("</head>")
print ('<body style="background-image:url(stars.png);background-size:contain">')
print ('<div style = "border:5px thin #888182; padding: 30px 30px 30px 30px; margin: 30px 30px 30px 30px; background-color: rgba(219,243,243,0.7);">')
print ('<img src="scoutlogo.png" width="400" height="120">')
results = search(query)
print ("<p>" + str(len(results)) + " results found for search query: "+ query+"</p>")
print ('<hr width="400px" align="left">')
print ('<div style="padding-top: 25px">')
for result in results:
    unknown_pages = 1
    if result[1] is None:
        print("<p> <a href='" + result[0]+"'>"+ "Unknown Page " + str(unknown_pages)+"</a> | Rank = " + str(result[2]) +"</p><br>")
        unknown_pages += 1
    else:
        print("<p> <a href='" + result[0]+"'>"+result[1] +"</a> | Rank = " + str(result[2]) +"</p><br>")
print ('</div>')
#print ("<h2> %s </h2>" % (query))
print ("</div>")
print ("</body>")
print ("</html>")
