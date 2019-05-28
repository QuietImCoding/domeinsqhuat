from bs4 import BeautifulSoup
import requests
from progress.bar import IncrementalBar
from urllib.parse import urlparse, urlunparse
import code

top50 = "https://www.alexa.com/topsites"
top50 = requests.get(top50)
kbs = 'qwertyuiop asdfghjkl* zxcvbnm***'
kb = [ [ l for l in kbrow] for kbrow in kbs.split() ]

def find_kb_char(c):
    for r in range(len(kb)):
        if c in kb[r]:
            return ( r, kb[r].index(c) )
    return

sitesoup = BeautifulSoup(top50.text, 'html.parser')
parentdivs = sitesoup.findAll("div", {"class": "DescriptionCell"})
toplinks = ["https://" + pdiv.find('p').find('a').text.lower() for pdiv in parentdivs]

def try_site(url):
    try:
        return requests.get(url, timeout = 5)
    except Exception:
        print("\nRequest timed out for " + url)
        return
    
reqs = []
with IncrementalBar("Making requests", max = len(toplinks)) as pb:
    for l in toplinks:
        reqs.append(try_site(l))
        pb.next()

allurls = []
for req in reqs:
    if req is not None:
        print(req.url + ':')
        allurls.append(req.url if req.history == [] else req.history[-1].url)
        for el in req.history:
            print('\tRedirected to: ' + el.url)

prsdurls = [ urlparse(u) for u in allurls ] 

code.interact(local=locals())
