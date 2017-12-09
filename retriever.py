import nltk
from nltk.corpus import stopwords as sw
import math

# used help from stack overflow to sort dictionary by Pagerank


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
    return final_results


# search interface, user enters search terms, results are retrieved and returned
def search():
    search_terms = input("Input search terms: ")
    tokenized_terms = nltk.word_tokenize(search_terms)
    stemmer = nltk.PorterStemmer()
    stemmed_terms = [stemmer.stem(token).lower() for token in tokenized_terms if token not in sw.words("english")]
    results = retrieve(stemmed_terms, "invindex.dat", "docs.dat")
    print(results)
    print(str(len(results)) + " results found.")
    return results


# -------------main ----------------------------
# print(open_json_dict("invindex.dat"))
# print(open_json_dict("docs.dat"))
# print(retrieve(["wadi"],"invindex.dat","docs.dat"))

search()
