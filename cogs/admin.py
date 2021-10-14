import data
import datetime
import discord
from discord.ext import commands
from git import Repo
import fileinput
import json
import os
import time


# Opens Json File to check for Admin Id
with open("./config.json") as f:
    configData = json.load(f)

AdminId = configData["Admin"]

#sets the admin owner of the bot.
def is_owner():
    async def predicate(ctx):
        return ctx.author.id == AdminId
    return commands.check(predicate)


class Admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    #Activates the bot to accept submissions
    @commands.command(name='activate')
    @is_owner()
    async def activate(self, ctx):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for Submissions| !help'))
        self.bot.unload_extension(f"cogs.events") 
        self.bot.load_extension(f"cogs.contributor")
        await ctx.send(f"Hooty is now taking in Contribution submissions")


    # Deactivates the Bot
    @commands.command(name='deactivate')
    @is_owner()
    async def deactivate(self, ctx):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Closed for Submissions'))
        self.bot.unload_extension("cogs.contributor")
        self.bot.load_extension("cogs.events") 
        await ctx.send("Hooty is no longer taking in Contribution submissions.")


    #enable different cogs while bots running 
    # !loadclog classname
    @commands.command(name='loadcog')
    @is_owner()
    async def loadcog(self, ctx, cog):
        self.bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} file has been enabled.")

    #disable different cogs while bots running
    # !unloadcog {classname} 
    @commands.command(name='unloadcog')
    @is_owner()
    async def unloadcog(self, ctx, cog):
        self.bot.unload_extension(f"cogs.{cog}") 
        await ctx.send(f"{cog} file has been disabled.")

    #Updates Master Sheet with current months data inside database
    #!updateMaster
    @commands.command(name='updateMaster')
    @is_owner()
    async def updateMaster(self, ctx):
        send = data.MasterControls()
        send.updateMasterSheet()
        await ctx.send("MasterSheet has been updated.")

    #GoogleSheet Commands
    #!Clear
    @commands.command(name='clearMaster')
    @is_owner()
    async def clear(self, ctx):
        send = data.MasterControls()
        send.clearLastMonthsData()
        await ctx.send("Master Sheet has been cleared.")

    #changes wallet address of user in Database
    #!changeWallet "OwlID" "New Wallet Address"
    @commands.command(name='changeWallet')    
    @is_owner()
    async def changeWallet(self, ctx, arg1, arg2):
        userInfo = data.MasterControls()
        userInfo.changeWallet(arg1, arg2)
        await ctx.send(f'Owl ID: {arg1} wallet address has been changed to {arg2}.')

    @changeWallet.error
    async def changeWallet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Command failed. \n Please make sure to type: !changeWallet "Owl Id" "New Wallet Address"')

    #Admin Help Command
    @commands.command(name='adminHelp')
    @is_owner()
    async def adminHelp(self, ctx):

        embed = discord.Embed(
            title = 'Admin Bot Commands',
            description = 'List of commands only for the Administrator',
            colour = discord.Colour.blue()
        )
        
    
        embed.add_field(name='!activate', value= '- Activates bot for Submissions', inline = False)
        embed.add_field(name='!deactivate', value= '- Dectivates bot for Submissions', inline = False)
        embed.add_field(name='!updateMaster', value= '- Updates Master Sheet with current months contribution', inline = False)
        embed.add_field(name='!changeWallet', value= '- Changes wallet address of user. \n - Command syntax: !changeWallet "owlID" "new wallet address"', inline = False)
        embed.add_field(name='!clearMaster', value= '- Clears Master Sheet Data', inline = False)
        # embed.add_field(name='!loadcog className', value= '- Enables different class functions', inline = False)
        # embed.add_field(name='!unloadcog className', value= '- Disables different class functions', inline = False)z
        embed.add_field(name='!adminHelp', value= '- Displays list of Admin controls', inline = False)
        embed.set_footer(text = 'If there is any problems with the bot, please contact TeeWhy')
        
        await ctx.send(embed=embed)

    #Throws Error if non admin tries to access adminHelp command.
    @adminHelp.error
    async def adminHelp_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Your account does not have Admin privlages. If you are trying to submit contribution documents, please type !help for a list of commands to assist you. ')


    #Command to make a pull request to upload institutional PDFs to https://github.com/IndexCoop/indexcoop.github.io
    #!pdf {file attatchment.pdf}
    @commands.command(name='pdf')    
    @is_owner()
    async def upload_pdf_file(self, ctx, *args):
        pdf_name = ctx.message.attachments[0].filename
        working = '/Users/tylercranmer/Dev/indexcoop.github.io'
        repo = Repo(working)
        assert not repo.bare
        index_html = '/Users/tylercranmer/Dev/indexcoop.github.io/index.html'


        try:
            if not ctx.message.attachments[0].filename.endswith('.pdf'):
                await ctx.send('The file you provided was NOT recorded. Please make sure to send a the file in a .pdf format. \n \n Example:    filename.pdf')
                return

            else:

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

                # if both the year and month path exist, insert new pdf into month directory. 
                if os.path.exists(new_abs_path_month):
                    pdf_file = os.path.abspath(f'{new_abs_path_month}/{ctx.message.attachments[0].filename}')
                    pdf_file = pdf_file.lower().replace("'", "")
                    await ctx.message.attachments[0].save(pdf_file)

                    print(f'Current {year} and {month} folder exists. inserted {ctx.message.attachments[0].filename} \n')
                    
                    if os.path.exists(pdf_file):
                        html_line = f'<a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/2021/{pdf_name}" target="_blank" class="link-11">Learn <span>More</span></a>'
                        with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                            for line in f:
                                if 'link-11' in line:
                                    print(html_line, end = '\n')
                                else:
                                    print(line, end='')  

                        # repo.git.add(all=True)
                        # repo.git.commit(f'add {pdf_name} and uploaded html link')
                    
                    elif not os.path.exists(pdf_file):
                        print("pdf file path was not found. time sleep for 10 sec")
                        time.sleep(10)
                        if os.path.exists(pdf_file):
                            html_line = f'<a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/2021/{pdf_name}" target="_blank" class="link-11">Learn <span>More</span></a>'
                            with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                                for line in f:
                                    if 'link-11' in line:
                                        print(html_line, end = '\n')
                                    else:
                                        print(line, end='')  
                            # repo.git.add(all=True)
                            # repo.git.commit(f'add {pdf_name} and uploaded html link')
                        else:
                            print("pdf file path not found")

                    #NEED TO MERGE branch and Commit

                    await ctx.send(f'{ctx.message.attachments[0].filename} has been uploaded to github')

                # if year directory exsist but not the month directory, create new month directory and insert new pdf into month path
                elif os.path.exists(new_abs_path_year) and not os.path.exists(new_abs_path_month):
                    #create new_month folder
                    os.mkdir(new_abs_path_month)
                    pdf_file = os.path.abspath(f'{new_abs_path_month}/{ctx.message.attachments[0].filename}')
                    pdf_file = pdf_file.lower().replace("'", "")
                    await ctx.message.attachments[0].save(pdf_file)


                    #NEED TO MERGE branch and Commit

                    await ctx.send(f'{ctx.message.attachments[0].filename} has been uploaded to github')

                    #TO DO insert arg into new months folder
                    print(f'current {year} folder exists. Created a {month} folder and inserted {ctx.message.attachments[0].filename}')
                    
                    
                    if os.path.exists(pdf_file):
                        html_line = f'<a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/2021/{pdf_name}" target="_blank" class="link-11">Learn <span>More</span></a>'
                        with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                            for line in f:
                                if 'link-11' in line:
                                    print(html_line, end = '\n')
                                else:
                                    print(line, end='')  

                        # repo.git.add(all=True)
                        # repo.git.commit(f'add {pdf_name} and uploaded html link')
                    
                    elif not os.path.exists(pdf_file):
                        print("pdf file path was not found. time sleep for 10 sec")
                        time.sleep(10)
                        if os.path.exists(pdf_file):
                            html_line = f'<a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/2021/{pdf_name}" target="_blank" class="link-11">Learn <span>More</span></a>'
                            with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                                for line in f:
                                    if 'link-11' in line:
                                        print(html_line, end = '\n')
                                    else:
                                        print(line, end='')  
                            # repo.git.add(all=True)
                            # repo.git.commit(f'add {pdf_name} and uploaded html link')
                        else:
                            print("pdf file path not found")                   


                # if the current year path doesnt exist, create new year/month directory. Insert new pdf into month directory. 
                elif not os.path.exists(new_abs_path_year):
                    #create new year folder
                    os.mkdir(new_abs_path_year)
                    os.mkdir(new_abs_path_month)
                    pdf_file = os.path.abspath(f'{new_abs_path_month}/{ctx.message.attachments[0].filename}')
                    pdf_file = pdf_file.lower().replace("'", "")
                    await ctx.message.attachments[0].save(pdf_file)

                    #NEED TO MERGE branch and Commit

                    await ctx.send(f'{ctx.message.attachments[0].filename} has been uploaded to github')

                    #TO DO insert arg into new months folder
                    print(f'created a {year}/{month}folder and inserted {ctx.message.attachments[0].filename}')

                    if os.path.exists(pdf_file):
                        html_line = f'<a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/2021/{pdf_name}" target="_blank" class="link-11">Learn <span>More</span></a>'
                        with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                            for line in f:
                                if 'link-11' in line:
                                    print(html_line, end = '\n')
                                else:
                                    print(line, end='')  

                        repo.git.add(all=True)
                        repo.git.commit(f'add {pdf_name} and uploaded html link')
                    
                    elif not os.path.exists(pdf_file):
                        print("pdf file path was not found. time sleep for 10 sec")
                        time.sleep(10)
                        if os.path.exists(pdf_file):
                            html_line = f'<a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/2021/{pdf_name}" target="_blank" class="link-11">Learn <span>More</span></a>'
                            with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                                for line in f:
                                    if 'link-11' in line:
                                        print(html_line, end = '\n')
                                    else:
                                        print(line, end='')  
                            repo.git.add(all=True)
                            repo.git.commit(f'add {pdf_name} and uploaded html link')
                        else:
                            print("pdf file path not found")


        except IndexError:
            await ctx.send('I did not see a file uploaded with the !pdf command. Please drag the pdf file into the chat and type !pdf inside the ADD A COMMENT forum.')
            


def setup(bot):
    bot.add_cog(Admin(bot))