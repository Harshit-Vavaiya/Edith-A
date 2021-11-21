import requests
import nltk
from sumy.summarizers.kl import KLSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

import trafilatura
import asyncio





def getSummary(url):
    webpage = trafilatura.fetch_url(url)
    text = trafilatura.extract(webpage)
    if not text: return ''
    summary = summarize(text)

    return summary


def summarizer(text):
    
    # list of stopwords
    stopwords = list(STOP_WORDS)

    # loading textmodel from spacy
    nlp = spacy.load('en_core_web_sm')

    # parsing the given text using model to 
    # This preprocesses the text
    # e.g. tokenizes words and sentences
    doc = nlp(text)

    # list of tokens
    tokens = [token.text for token in doc]

    # punctuations to avoid, new line is added to 
    # existing punctuations
    punctuation_ = str(punctuation)+'\n'
    
    # Count frequencies of word to find out importance
    # of each word in the given article,
    # this frequency will later help to score sentences
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation_:
                if word.text.lower() not in word_frequencies.keys():
                    word_frequencies[word.text.lower()] = 1
                else:
                    word_frequencies[word.text.lower()] += 1

    
    # most frequent word's value. highest frequency
    # this will help normalize frequency values
    max_freq = max(word_frequencies.values())

    # normalizing word frequency values
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_freq

    # sentence tokens
    sentence_tokens = [sent for sent in doc.sents]

    # score each sentence based on frequency of words it contains.
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    # number of sentences to select
    # here we are selecting 30% of actual content
    selected_length = int(len(sentence_tokens)*0.3)

    # making summary with 'n' highest scored sentences.
    summary = nlargest(selected_length,sentence_scores,key = sentence_scores.get)

    # making summary a single string
    final_summary = [word.text for word in summary]
    summary = '\n'.join(final_summary)

    return summary

def summarize(text):

    # summarizing text using summarizer function  
    summary = summarizer(text)
    return summary

def search(sentence):
  
    # q is a variable that stores query
    # of a user, in this case a sentence written
    q = sentence


    # google search api credentials
    apiKey =  'AIzaSyAnD8szm967WUs8Fbb3O32Fy-WCYlGfqkI'
    cx = '64138e78f5c16738e'
    url = 'https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s'%(apiKey,cx,q)
    
    # requesting the api with query
    res = requests.get(url)
    res = res.json()
    

    # if response is not what we expect than returning 
    # default value
    if not res:
        return { 'response' : 'I do not understand...'}
        


    result = []
    snip = ''
    used = set()
    for item in res['items']:
        if 'snippet' in item.keys():
            link = item['link']
            snippet = item['snippet'] 
            snip = snippet.replace('...','')
            used.add(link)
            result.append((link,snippet))
            break
    
    # result variable contains list of tuples,
    # (link, snippet) link of a page containing search result
    # snippet of that result.
    # we are taking only first web link from all the links
    # that google search api returns
    
    
    
    # url = result[0][0]
    # summary = getSummary(url)  
    # return { 'response' : 'answer: '+   str(url) }
    url = result[0][0]
    summary = getSummary(url)
    return { 'response' : summary+'\n\n Link:'+url }


