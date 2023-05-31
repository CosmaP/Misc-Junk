#!/usr/bin/env python


# Quick and dirty to convert between formats

import os
# import pandas
import tablib

import pprint as pprint

# pip install "tablib[xls]
# pip install "tablib[pandas]
# pip install "tablib[html]

WorkingDirectory = '.\\'
SourceData = '.\\Lottery_Powerball_Winning_Numbers__Beginning_2010.csv'
OutputData = '.\\Lottery_Powerball_Modified.csv'

os.chdir(WorkingDirectory)

ds = tablib.Dataset()

# collection of names
names = ['Kenneth Reitz', 'Bessie Monke']

for name in names:
    # split name appropriately
    fname, lname = name.split()

    # add names to Dataset
    ds.append([fname, lname])

ds.headers = ['First Name', 'Last Name']

print(ds.dict)

ds.append_col([22, 20], header='Age')

print(ds.dict)

imported_data = tablib.Dataset().load(open(SourceData).read())

print(imported_data)

print(imported_data.export('json'))

print(imported_data.export('csv'))

with open('fred.csv', 'w') as f:
    f.write(ds.export('csv'))

with open('fred.json', 'w') as f:
    f.write(ds.export('json'))

with open('fred.html', 'w') as f:
    f.write(ds.export('html'))

# Does not work
# with open ('fred.xlsx','w') as f:
#    f.write(ds.export('xlsx'))


#  Read a CSV

with open(SourceData) as f:
    data = f.read()
    ds2 = tablib.Dataset().load(data)

print(ds2.json)
print(ds2.csv)
print(ds2.html)


with open('fred2.html', 'w') as f:
    f.write(ds2.export('html'))

print(ds2.headers)

# Remove a col
del ds2['Multiplier']
print(ds2.headers)

#pprint(ds2.csv)
