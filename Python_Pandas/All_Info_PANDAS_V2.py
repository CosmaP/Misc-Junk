#!/usr/bin/env python

import os
import pandas as pd

WorkingDirectory = '.\\'
SourceData = '.\\Lottery_Powerball_Winning_Numbers__Beginning_2010.csv'
OutputData = '.\\Lottery_Powerball_Modified.csv'

os.chdir(WorkingDirectory)

# Create a new DataFrame with some data
#data = ({'Data': ['']})
#df = pd.DataFrame(data)

# Read the CSV file into a new DataFrame
df = pd.read_csv(SourceData)
#df = pd.DataFrame(df)

# Set row lookup (index) to date column or any unique col.  Otherwise it will be there when you export
df = df.set_index('Draw Date')

print(df) 

# Print the row where the index is the date '10/10/2020'
print(df.loc['10/10/2020'])

# Add an extra column
#df['Test Col'] = 5

# Remove any rows that have more than 2 null value columns.  Produce 'clean' data
clean = df.dropna(thresh=2, axis='columns').dropna(how='any')

print(clean)

# Write to csv
df.to_csv('Lottery_Numbers.csv')
df.to_json('Lottery_Numbers.json')

# Print column list
print(df.columns)

# Create a new Excel file and save the DataFrame to a new sheet called 'rawdata'
with pd.ExcelWriter(OutputData) as writer:
    df.to_excel(writer, sheet_name='Raw Data', index=False)


# Open the Excel file and select the 'rawdata' sheet
#with pd.ExcelWriter(OutputData) as writer:   #, mode='a'
#    #workbook = writer.book
#    workbook = writer.cur_sheet
#    worksheet = workbook['Raw Data']
#    
#    # Write the CSV data to the 'rawdata' sheet
#    start_row = worksheet.max_row + 2
#    csv_df.to_excel(writer, sheet_name='Raw Data', startrow=start_row, index=False)
