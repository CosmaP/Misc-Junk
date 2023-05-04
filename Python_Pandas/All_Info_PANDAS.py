#!/usr/bin/env python

import os
import pandas as pd

WorkingDirectory = 'C:\\Documents\\!-Synced\\OneDrive\\!!-Github_Repositories\\Misc-Junk\\Python_Pandas'
SourceData = 'C:\\Documents\\!-Synced\\OneDrive\\!!-Github_Repositories\\Misc-Junk\\Python_Pandas\\DocProperties.csv'
OutputData = 'C:\\Documents\\!-Synced\\OneDrive\\!!-Github_Repositories\\Misc-Junk\\Python_Pandas\\DataSummary.xlsx'

os.chdir(WorkingDirectory)

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(OutputData, sheet_name='RawData')

# Edit a value in the DataFrame
df.loc[0, 'Column1'] = 'New Value'

# Save the modified DataFrame back to the Excel file
with pd.ExcelWriter(OutputData) as writer:
    df.to_excel(writer, sheet_name='RawData', index=False)
