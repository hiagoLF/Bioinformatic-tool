def createProteinsDictionaryFromFasta(fastaProteins):
  proteinsList = fastaProteins.split('>')

  proteinSequencesDictionary = {}

  for protein in proteinsList:
    splitedFasta = protein.split('\n') 
    if(len(splitedFasta) > 1):
        proteinId = splitedFasta[0].split('|')[2].split(' ')[0].strip()
        splitedFasta.pop(0)
        proteinSequence = ''.join(splitedFasta)
        proteinSequencesDictionary[proteinId] = proteinSequence
  
  return proteinSequencesDictionary