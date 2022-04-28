import pandas as pd

def generateTableWithDictionary(aminoacidsReasons: dict, keyColumnName, valueColumnName, fileTitle):
  dataFrame = {}
  dataFrame[keyColumnName] = aminoacidsReasons.keys()
  dataFrame[valueColumnName] = aminoacidsReasons.values()
  
  newTable = pd.DataFrame(dataFrame)

  newTable.to_csv('generated/tables/'+fileTitle+'.csv')