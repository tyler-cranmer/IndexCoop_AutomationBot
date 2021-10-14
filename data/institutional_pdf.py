import os
import discord
import fileinput
from git import Repo
import datetime

# file_name = os.path.abspath('./index.html')
# new_arg = 'link/FLI_One_Pager.arg'
# html_line = f'<a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/2021/{new_arg}" target="_blank" class="link-11">Learn <span>More</span></a>'
# with fileinput.FileInput(file_name, inplace = True, backup ='.bak') as f:
#     for line in f:
#         if 'link-11' in line:
#             print(html_line, end = '\n')
#         else:
#             print(line, end='')


# def update_arg(file):
#     #create branch
#     #create new folder of the month. 
#     #insert arg into folder
#     file_path = os.path.abspath(f'./{file}')
#     html_line = f'<a href="{file_path}" target="_blank" class="link-11">Learn <span>More</span></a>'
#     with fileinput.FileInput(file_path, inplace = True, backup ='.bak') as f:
#         for line in f:
#             if 'link-11' in line:
#                 print(html_line, end = '\n')
#             else:
#                 print(line, end='')
# class Automate:
#     def __init__(self):
#         working = '/Users/tylercranmer/Dev/indexcoop.github.io'
#         repo = Repo(working)
#         assert not repo.bare

#         #repo.git.checkout('-b', 'testing_automate')

#     def add_directories(arg):
#         pdf = str(arg)
#         date = datetime.date.today()
#         year = date.strftime("%Y")
#         month = date.strftime("%m")

#         calendar = {'1' : 'January', '2': 'February', '3': 'March', '4': 'April', 
#             '5': 'May', '6': "June", '7': 'July', '8': 'August',
#                 '9': 'September', '10': 'October', '11': 'November', '12': 'December'}

#         for key in calendar:
#             if key == month:
#                 month = calendar[key]
        
#         #create new folder of the year. 
#         script_path = os.path.realpath('/Users/tylercranmer/Dev/indexcoop.github.io/assets')
#         new_abs_path_year = os.path.join(script_path, year)
#         new_abs_path_month = os.path.join(new_abs_path_year, month)

#         if os.path.exists(new_abs_path_month):
#             #TO DO insert arg into current months folder
#             print('Current year and month folder exists. \n')
#             print('#TO DO insert arg into current months folder')
#             arg_abs_path = os.path.join(new_abs_path_month, pdf)
#             os.mkdir(arg_abs_path)
#         elif os.path.exists(new_abs_path_year) and not os.path.exists(new_abs_path_month):
#             #create new_month folder
#             os.mkdir(new_abs_path_month)
#             arg_abs_path = os.path.join(new_abs_path_month, pdf)
#             os.mkdir(arg_abs_path)
#             #TO DO insert arg into new months folder
#             print('current year folder exists, Created a new month folder')
#             print("#TO DO insert arg into newly created months folder")
#         elif not os.path.exists(new_abs_path_year):
#             #create new year folder
#             os.mkdir(new_abs_path_year)
#             os.mkdir(new_abs_path_month)
#             arg_abs_path = os.path.join(new_abs_path_month, pdf)
#             os.mkdir(arg_abs_path)
#             #TO DO insert arg into new months folder
#             print('created a new year and month folder')
#             print("#TO DO insert arg into newly created months folder")



class Automate:
    def __init__(self):
        working = '/Users/tylercranmer/Dev/indexcoop.github.io'
        repo = Repo(working)
        assert not repo.bare

        #repo.git.checkout('-b', 'testing_automate')

    async def add_directories(file_name,file_content):
        
        date = datetime.date.today()
        year = date.strftime("%Y")
        month = date.strftime("%m")

        calendar = {'1' : 'January', '2': 'February', '3': 'March', '4': 'April', 
            '5': 'May', '6': "June", '7': 'July', '8': 'August',
                '9': 'September', '10': 'October', '11': 'November', '12': 'December'}

        for key in calendar:
            if key == month:
                month = calendar[key]
        
        #create new folder of the year. 
        script_path = os.path.realpath('/Users/tylercranmer/Dev/indexcoop.github.io/assets')
        new_abs_path_year = os.path.join(script_path, year)
        new_abs_path_month = os.path.join(new_abs_path_year, month)

        if os.path.exists(new_abs_path_month):
            #TO DO insert arg into current months folder
            print('Current year and month folder exists. \n')
            print('#TO DO insert arg into current months folder')
            pdf_file = os.path.abspath(f'{new_abs_path_month}/{file_name}')
            pdf_file = temp_file.lower().replace("'", "")
            await file_content.save(pdf_file)

        elif os.path.exists(new_abs_path_year) and not os.path.exists(new_abs_path_month):
            #create new_month folder
            os.mkdir(new_abs_path_month)
            pdf_file = os.path.abspath(f'{new_abs_path_month}/{file_name}')
            pdf_file = temp_file.lower().replace("'", "")
            await file_content.save(pdf_file)
            #TO DO insert arg into new months folder
            print('current year folder exists, Created a new month folder')
            print("#TO DO insert arg into newly created months folder")
        elif not os.path.exists(new_abs_path_year):
            #create new year folder
            os.mkdir(new_abs_path_year)
            os.mkdir(new_abs_path_month)
            pdf_file = os.path.abspath(f'{new_abs_path_month}/{file_name}')
            pdf_file = temp_file.lower().replace("'", "")
            await file_content.save(pdf_file)
            #TO DO insert arg into new months folder
            print('created a new year and month folder')
            print("#TO DO insert arg into newly created months folder")


