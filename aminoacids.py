aminoacidsLettersList = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V' ]

def getAminoacidCouples():
  aminoacidsCouples = []
  for aminoacidLetter in aminoacidsLettersList.aminoacidsLettersList:
    for secondAminoacidLetter in aminoacidsLettersList.aminoacidsLettersList:
        aminoacidsCouples.append(aminoacidLetter+secondAminoacidLetter)

