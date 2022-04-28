import urllib.parse
import urllib.request
from config import apiRequesUrl

def requestProteinsFromUniprot(proteinsIds):
  params = {
    "format": "fasta",
    "columns": 'id,entry_name,reviewed',
    "from": "ID",
    "to": "ACC",
    "query": proteinsIds,
  }

  data = urllib.parse.urlencode(params)
  data = data.encode('utf-8')
  req = urllib.request.Request(apiRequesUrl, data)
  with urllib.request.urlopen(req) as f:
    response = f.read()
  fastaProteins = response.decode('utf-8')
  return fastaProteins