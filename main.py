from operator import ge
import pandas as pd
import re
from collections import Counter
from matplotlib import pyplot as plt
import numpy as np
import aminoacids
from conversors import convertToPercentageList
from config import enviroment
from generate.table import generateTableWithDictionary
from predict.reasons import getReasonsBettweenAminoacidsFrequencies
from predictions import findProteinsInformations, getAminoacidsCoupleFrequencesInPercentage, getAminoacidsFrequencesInPercentage
from request import requestProteinsFromUniprot
from fasta import createProteinsDictionaryFromFasta
from tables import createTableForProteinsFragments

print('1. Readind file.csv')

file = pd.read_csv('input/file.csv' if enviroment == 'production' else 'input/file_test.csv')
proteinsIds = ' '.join(file['Protein_ID'])

print('2. Requesting', len(file['Protein_ID']), 'proteins from Uniprot')

fastaProteins = requestProteinsFromUniprot(proteinsIds)

proteinSequencesDictionary = createProteinsDictionaryFromFasta(fastaProteins)

[
   proteinsIds, 
   proteinsFragments, 
   proteinsFragmentsSizes, 
   fragmentsAminoacidFrequencies, 
   notFoundProteins, 
   proteinsRests
] = findProteinsInformations(file, proteinSequencesDictionary)

createTableForProteinsFragments(proteinsIds, proteinsFragments, proteinsFragmentsSizes, fragmentsAminoacidFrequencies)

print('5. Generating size frequencies graphic')
fragmentSizesDictionary = Counter(proteinsFragmentsSizes)
plt.bar(fragmentSizesDictionary.keys(), fragmentSizesDictionary.values())

plt.title('Tamanhos de fragmentos x Frequencias')
plt.xlabel("Tamanho")
plt.ylabel("Frequência")

plt.savefig('generated/graphics/sizes-frequencies.png')
print('6. sizes-frequencies.png file generated')

print('7. Generating aminoacid percentage graphic')
generalAminoacidCount = {}
for aminoacidFrequence in fragmentsAminoacidFrequencies:
   for aminoacid, frequency in aminoacidFrequence.items():
      if aminoacid in generalAminoacidCount:
         generalAminoacidCount[aminoacid] += frequency
      else:
         generalAminoacidCount[aminoacid] = frequency

plt.clf()
generalAminoacidCount = dict(sorted(generalAminoacidCount.items(), key=lambda item: item[1]))
percentagesList = convertToPercentageList(generalAminoacidCount.values())

plt.bar(generalAminoacidCount.keys(), percentagesList, align='edge')

plt.title('Aminoácidos nos fragmentos x Porcentagem')
plt.xlabel("Aminoácido")
plt.ylabel("Porcentagem")

plt.savefig('generated/graphics/aminoacid-frequencies.png')
print('8. aminoacid-frequencies.png file generated')

print('9. Generating aminoacids couple frequency graphics')

aminoacidsCouples = []
for aminoacidLetter in aminoacids.aminoacidsLettersList:
   for secondAminoacidLetter in aminoacids.aminoacidsLettersList:
      aminoacidsCouples.append(aminoacidLetter+secondAminoacidLetter)

fragmentAminoacidCoupleDictionary = {}
for aminoacidCouple in aminoacidsCouples:
   for fragmentKey, fragment in enumerate(proteinsFragments):
      currentFragmentLenth = len(fragment)
      for aminoacidKey, aminoacidLetter in enumerate(fragment):
         nextAminoacidLetter = fragment[aminoacidKey + 1] if currentFragmentLenth > aminoacidKey + 1 else ''
         if (aminoacidLetter + nextAminoacidLetter == aminoacidCouple):
            if(aminoacidCouple in fragmentAminoacidCoupleDictionary):
               fragmentAminoacidCoupleDictionary[aminoacidCouple] += 1
            else:
               fragmentAminoacidCoupleDictionary[aminoacidCouple] = 1         

plt.clf()
fragmentAminoacidCoupleDictionary = dict(sorted(fragmentAminoacidCoupleDictionary.items(), key=lambda item: item[1]))

percentagesList = convertToPercentageList(fragmentAminoacidCoupleDictionary.values())

plt.bar(list(fragmentAminoacidCoupleDictionary.keys())[-20: -1], percentagesList[-20: -1], align='edge')

plt.title('Frequencia de duplas de aminoácidos nas regiões transmembrana\ndas proteínas')
plt.xlabel("Dupla")
plt.ylabel("Frequência")

plt.savefig('generated/graphics/fragment-aminoacid-couple-frequency.png')
print('10. fragment-aminoacid-couple-frequency.png file generated')



proteinRestAminoacidCoupleDictionary = {}
for aminoacidCouple in aminoacidsCouples:
   for proteinRestKey, proteinRest in enumerate(proteinsRests):
      currentFragmentLength = len(proteinRest)
      for aminoacidKey, aminoacidLetter in enumerate(proteinRest):
         nextAminoacidLetter = proteinRest[aminoacidKey + 1] if currentFragmentLength > aminoacidKey + 1 else ''
         if (aminoacidLetter + nextAminoacidLetter == aminoacidCouple):
            if(aminoacidCouple in proteinRestAminoacidCoupleDictionary):
               proteinRestAminoacidCoupleDictionary[aminoacidCouple] += 1
            else:
               proteinRestAminoacidCoupleDictionary[aminoacidCouple] = 1         
plt.clf()
proteinRestAminoacidCoupleDictionary = dict(sorted(proteinRestAminoacidCoupleDictionary.items(), key=lambda item: item[1]))

percentagesList = convertToPercentageList(proteinRestAminoacidCoupleDictionary.values())

plt.bar(list(proteinRestAminoacidCoupleDictionary.keys())[-20: -1], percentagesList[-20: -1], align='edge')

plt.title('Frequencia de duplas de aminoácidos nos restos das proteínas')
plt.xlabel("Dupla")
plt.ylabel("Frequência")

plt.savefig('generated/graphics/rest-aminoacid-couple-frequency.png')
print('11. rest-aminoacid-couple-frequency.png file generated')

print('12. Generating amino acid reasos tables')

proteinsRestsAminoacidFrequencies = getAminoacidsFrequencesInPercentage(proteinsRests)
proteinsFragmentsAminoacidFrequencies = getAminoacidsFrequencesInPercentage(proteinsFragments)

aminoacidsReasons = getReasonsBettweenAminoacidsFrequencies(proteinsFragmentsAminoacidFrequencies, proteinsRestsAminoacidFrequencies)
generateTableWithDictionary(
   aminoacidsReasons, 
   'AMINO_ACID',
   'REASON',
   'aminoacids_reasons'
)


proteinsRestsAminoacidCoupleFrequencies = getAminoacidsCoupleFrequencesInPercentage(proteinsRests)
proteinsFragmentsAminoacidCoupleFrequencies = getAminoacidsCoupleFrequencesInPercentage(proteinsFragments)

aminoacidsReasons = getReasonsBettweenAminoacidsFrequencies(proteinsFragmentsAminoacidCoupleFrequencies, proteinsRestsAminoacidCoupleFrequencies)
generateTableWithDictionary(
   aminoacidsReasons, 
   'AMINO_ACID_COUPLE',
   'REASON',
   'aminoacids_couples_reasons'
)

print('13. Process Finished')

