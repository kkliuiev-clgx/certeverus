'''CPT code mapping- run on actuals '''

import pandas as pd

def get_cpt_dictionary():
    ''' This method creates a dictionary for mapping CPT codes to Categories '''
    # actdf = pd.read_csv(r"./Data/DataFHMSActuals.csv")
    cptdf = pd.read_csv(r"./Data/CPT lookup table.csv")

    # cptdict = cptdf.to_dict('split')
    # print('\n\nCPTDICT:\n\n',cptdict)
    # cptdict2 = cptdict['data']
    # finaldict = {d[0]: d[1] for d in cptdict2}
    # print('\n\nFINAL\n\n',finaldict)
    # newact = actdf.replace(finaldict)
    # newact.to_csv('CPT_test.csv')

    cptdict3 = cptdf.set_index('CPT Code').to_dict()['Category'] #might be simpler - lets discuss
    # print('\n\nREVISED:\n\n',cptdict3)
    return cptdict3

print(get_cpt_dictionary())

