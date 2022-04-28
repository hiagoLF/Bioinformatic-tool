import pandas as pd

def createTableForProteinsFragments(proteinsIds, proteinsFragments, proteinsFragmentsSizes, fragmentsAminoacidFrequencies):
  newTable = pd.DataFrame({
    'Protein_ID': proteinsIds,
    'Fragment_Sequence': proteinsFragments,
    'Fragment_Size': proteinsFragmentsSizes,
    'Frequencies': fragmentsAminoacidFrequencies
  })

  print('3. Lines generated:' ,len(proteinsIds))

  newTable.to_csv('generated/tables/out.csv')

  print('4. out.csv file created')
