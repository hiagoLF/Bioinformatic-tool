import re
from collections import Counter

from conversors import convertDictionaryValuesToPercentage

def findProteinsInformations(file, proteinSequencesDictionary):
  proteinsIds = []
  proteinsFragments = []
  proteinsFragmentsSizes = []
  fragmentsAminoacidFrequencies = []
  notFoundProteins = []
  proteinsRests = []

  for proteinIdIndex, proteinId in enumerate(file['Protein_ID']):
    if proteinId in proteinSequencesDictionary:
        intervals = re.findall(r'\d+', file['TM_Segment_Helix'][proteinIdIndex])
        
        proteinsIds.append(proteinId)
        proteinsFragments.append(proteinSequencesDictionary[proteinId][int(intervals[2]):int(intervals[3])])
        proteinsRests.append(proteinSequencesDictionary[proteinId][0:int(intervals[2])-1] + proteinSequencesDictionary[proteinId][int(intervals[3])+1:-1])
        proteinsFragmentsSizes.append(int(intervals[3]) - int(intervals[2]))

        fragmentsAminoacidFrequencies.append(dict(Counter(proteinSequencesDictionary[proteinId][int(intervals[2]):int(intervals[3])])))
    else:
        notFoundProteins.append(proteinId)
    
  if len(notFoundProteins) > 0:
    print('Warning: Proteins not found:')
    print('--> ', notFoundProteins)

  return [
    proteinsIds,
    proteinsFragments,
    proteinsFragmentsSizes,
    fragmentsAminoacidFrequencies,
    notFoundProteins,
    proteinsRests
  ]

def getAminoacidsFrequencesInPercentage(sequences):
  aminoacidsFrequenciesDictionary = {}
  
  for sequence in sequences:
    for aminoacid in sequence:
      if aminoacid in aminoacidsFrequenciesDictionary:
        aminoacidsFrequenciesDictionary[aminoacid] += 1
      else:
        aminoacidsFrequenciesDictionary[aminoacid] = 1
  
  return convertDictionaryValuesToPercentage(aminoacidsFrequenciesDictionary)

