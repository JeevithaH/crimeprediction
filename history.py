import pandas as pd

pd.set_option('display.max_columns', 100)


def get_history(crime, state, district, year):
    result = crime[(crime['STATE/UT'] == state) & (crime['DISTRICT'] == district) & (crime['YEAR'] == year)][
        ['STATE/UT', 'DISTRICT', 'YEAR', 'MURDER', 'ATTEMPT TO MURDER',
         'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER', 'KIDNAPPING & ABDUCTION',
         'DACOITY',
         'PREPARATION AND ASSEMBLY FOR DACOITY', 'ROBBERY', 'BURGLARY', 'THEFT',
         'AUTO THEFT', 'OTHER THEFT', 'RIOTS', 'CRIMINAL BREACH OF TRUST',
         'CHEATING', 'OTHER IPC CRIMES', 'TOTAL IPC CRIMES']]
    if len(result) == 0:
        result_dict = "Data not Available for the requested params"
    else:
        result_dict = result.to_dict()
        result_dict = {key: list(value.values())[0] for key, value in result_dict.items()}
    return result_dict
