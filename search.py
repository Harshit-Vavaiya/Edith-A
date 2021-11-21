import requests



from sumy.summarizers.kl import KLSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

import trafilatura






def getSummary(url):
    webpage = trafilatura.fetch_url(url)
    text = trafilatura.extract(webpage)
    if not text: return ''
    summary = summarize(text)

    return summary


def summarizer(text):
    parser =    PlaintextParser.from_string(text,Tokenizer('english'))
    kl_summarizer=KLSummarizer()
    kl_summary=kl_summarizer(parser.document,sentences_count=5)

    # get summary
    summary = ""

    for sentence in kl_summary:
        summary += str(sentence) + "\n"
    
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


