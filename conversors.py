def convertToPercentageList(numbersList):
   total = 0
   for currentNumber in numbersList:
      total += currentNumber
   
   percentageNumbersList = []
   for numberToConvert in numbersList:
      percentageNumbersList.append((numberToConvert / total) * 100)
   return percentageNumbersList


def convertDictionaryValuesToPercentage(dictionaryPercentages):
   total = 0
   for dictKey, dictValue in dictionaryPercentages.items():
      total += dictValue
   percentagesDictionary = {}
   for dictKey, dictValue in dictionaryPercentages.items():
      percentagesDictionary[dictKey] = (dictValue / total) * 100
   return percentagesDictionary