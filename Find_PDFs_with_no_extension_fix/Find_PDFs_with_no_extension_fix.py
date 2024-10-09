#!/usr/bin/python

import os
import shutil

def add_pdf_extension(folder_path):
    """Iterate through files in the given folder"""
    # Iterate through files in the given folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Check if the file has no extension
            if '.' not in filename:
                # Check if the file is a PDF by examining its content 
                # (you can adjust this check if needed)
                with open(file_path, 'rb') as file:
                    header = file.read(4)

                if header.startswith(b'%PDF'):
                    # Add .pdf extension to the file
                    new_file_path = os.path.join(folder_path, f'{filename}.pdf')
                    shutil.move(file_path, new_file_path)
                    print(f"Renamed {filename} to {filename}.pdf")

# Replace 'your_folder_path' with the actual path to the folder you want to check
folder_to_check = 'C:\Data\Test'
add_pdf_extension(folder_to_check)
