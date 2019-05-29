from bs4 import BeautifulSoup
import requests
from requests_futures.sessions import FuturesSession
from progress.bar import IncrementalBar
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse, urlunparse
import code

top50 = "https://www.alexa.com/topsites"
top50 = requests.get(top50)
kbs = 'qwertyuiop asdfghjkl* zxcvbnm***'
lookalikes = 'l1i o0 pq bd zs nm yu'
kb = [ [ l for l in kbrow] for kbrow in kbs.split() ]

def find_kb_char(c):
    for r in range(len(kb)):
        if c in kb[r]:
            return ( r, kb[r].index(c) )
    return

def find_kb_neighbors(char):
    loc = find_kb_char(char)
    if loc is not None:
        reslist = []
        for r in range(loc[0] - 1, loc[0] + 2):
            if r >= 0 and r < len(kb):
                for c in range(loc[1] - 1, loc[1] + 2):
                    if c >= 0 and c < len(kb[r]) and (r, c) != loc:
                        reslist.append(kb[r][c])
        return reslist

def gen_mutated_strings(s):
    # iterate over letters, mutating each one
    prefix = 'www.' if s.find('www.') == 0 else ''
    postfix = s[s.rfind('.'):]
    s = s[len(prefix):len(s)-len(postfix)]
    mut = set()
    for l in range(len(s)):
        # Get keyboard neighbors
        kbnbrs = find_kb_neighbors(s[l])
        if kbnbrs is not None:
            # Generate mutation sets
            kbmuts = {s[0:l] + m + s[l+1:] for m in kbnbrs}
            delmut = {s[0:l] + s[l+1:]}
            dupmut = {s[0:l] + s[l]*2 + s[l+1:]}
            # Union with mutations
            mut |= kbmuts
            mut |= delmut
            mut |= dupmut
    return list({ prefix + a + postfix for a in mut if '*' not in a })

sitesoup = BeautifulSoup(top50.text, 'html.parser')
parentdivs = sitesoup.findAll("div", {"class": "DescriptionCell"})
toplinks = ["https://" + pdiv.find('p').find('a').text.lower() for pdiv in parentdivs]

def try_site(url):
    try:
        return requests.get(url, timeout = 5)
    except Exception:
        return
    
print ("Getting website details...")
with ThreadPool(20) as p:
    reqs = p.map(try_site, toplinks)

allurls = []
for req in reqs:
    if req is not None:
        allurls.append(req.url)

# Parsed urls
purls = [ urlparse(u) for u in allurls ]
# a is a link like <a> tags
mutdict = { a: gen_mutated_strings(a.netloc) for a in purls } 



code.interact(local=locals())
