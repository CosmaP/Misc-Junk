#!/usr/bin/env python

import os
import pandas as pd

WorkingDirectory = '.\\'
SourceData = '.\\DocProperties.csv'
OutputData = '.\\DataSummary.xlsx'

os.chdir(WorkingDirectory)

# Create a new DataFrame with some data
#data = ({'Data': ['']})
#df = pd.DataFrame(data)

# Read the CSV file into a new DataFrame
csv_df = pd.read_csv(SourceData)
#df = pd.DataFrame(csv_df)

# Create a new Excel file and save the DataFrame to a new sheet called 'rawdata'
with pd.ExcelWriter(OutputData) as writer:
    csv_df.to_excel(writer, sheet_name='Raw Data', index=False)


# Open the Excel file and select the 'rawdata' sheet
#with pd.ExcelWriter(OutputData) as writer:   #, mode='a'
#    #workbook = writer.book
#    workbook = writer.cur_sheet
#    worksheet = workbook['Raw Data']
#    
#    # Write the CSV data to the 'rawdata' sheet
#    start_row = worksheet.max_row + 2
#    csv_df.to_excel(writer, sheet_name='Raw Data', startrow=start_row, index=False)
