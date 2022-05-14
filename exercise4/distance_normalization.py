import numpy as np

def normalizeDistances(dict, target=1.0):
   new_dict= {}
   
   for k in dict:
      
      minVal = min(dict[k].values())
      maxVal = max(dict[k].values())
      new_dict[k] = {key: (value-minVal)/(maxVal-minVal) for key,value in dict[k].items()}
   return new_dict
