def getReasonsBettweenAminoacidsFrequencies(firstsFrequencies, secondsFrequencies):
  aminoacidsReasons = {}
  
  for aminoacidFromFirst, aminoacidFromFirstFrequency in firstsFrequencies.items():
    for aminoacidFromSecond, aminoacidFromSecondFrequency in secondsFrequencies.items():
      if aminoacidFromFirst == aminoacidFromSecond:
        aminoacidsReasons[aminoacidFromFirst] = aminoacidFromFirstFrequency / aminoacidFromSecondFrequency

  return aminoacidsReasons