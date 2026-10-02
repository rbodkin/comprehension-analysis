import json,urllib.request,sys
C='2588573f-daa3-4130-9bce-e60ba5db04c1'
def dql(q):
    r=urllib.request.Request(f'https://api.docent.transluce.org/rest/dql/{C}/execute',data=json.dumps({"dql":q}).encode(),headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r,timeout=600))
