#!/usr/bin/env python

import os
from openpyxl import Workbook
from openpyxl import load_workbook

WorkingDirectory = 'C:\\Documents\\!-Synced\\OneDrive\\!!-Github_Repositories\\Misc-Junk\\Python_Pandas'
SourceData = 'C:\\Documents\\!-Synced\\OneDrive\\!!-Github_Repositories\\Misc-Junk\\Python_Pandas\\DocProperties.csv'

os.chdir(WorkingDirectory)

workbook = load_workbook(filename = WorkingDirectory + '\\DataSummary.xlsx')
workbook.sheetnames
#['SourceData']

sheet = workbook.active
print(sheet)

print(sheet.title)
