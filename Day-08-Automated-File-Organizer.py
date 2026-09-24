# Day 8 - Automated File Organizer

import os
import shutil  #add, move, update

folder_path = input("Enter folder path :")

for file_name in os.listdir(folder_path):

    file_path = os.path.join(folder_path,file_name)

    if os.path.isfile(file_path):

        extension = os.path.splitext(file_name)[1].lower()

        if extension in [".jpg", ".jpeg", ".png"]:
            folder_name = "Images"

        elif extension == ".pdf":
            folder_name = "PDFs"

        elif extension in [".docx", ".doc", ".txt"]:
            folder_name = "Documents"

        elif extension in [".xlsx", ".xls", ".csv"]:
            folder_name = "Spreadsheets"

        elif extension in [".mp4", ".mov", ".avi"]:
            folder_name = "Videos"

        else:
            folder_name = "Others"

        destination_folder = os.path.join(folder_path,folder_name)

        os.makedirs(destination_folder,exist_ok = True)

        destination_path = os.path.join(destination_folder,file_name)

        shutil.move(file_path,destination_path)

print("\nFiles organized successfully!")

