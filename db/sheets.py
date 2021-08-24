import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import sqlite3
from database import AddContributor, AddContribution
import datetime

#https://collab-land.gitbook.io/collab-land/bots/discord
#https://wickbot.com/

class UserSheet:
    def __init__(self,owlID,sheetName,worksheetName):
        self.owlID = owlID
        self.sheetName = sheetName
        self.worksheetName = worksheetName
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
            ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("sheetCreds.json", scope) #access the json key you downloaded earlier 
        client = gspread.authorize(credentials) # authenticate the JSON key with gspread
        
        sheet = client.open(sheetName)
        self.contributionSheet = sheet.worksheet(worksheetName)
        
    
    def collectContributorSheet(self): #collects info from sheets and puts it in SingleContributor TABLE
        db = 'index_contribution.db'
        ranges = ['A3:F51']
        user_data = self.contributionSheet.batch_get(ranges)

        date = datetime.datetime.now()

        for outershell in user_data:
            for innershell in outershell:
                if len(innershell) > 2 and (innershell[5] == 'BD' or 'Product' or 'Treasury' or 'Creative & Design' or 'Dev/Engineering' or 'Growth' or 'Expenses' or 'MVI' or 'Analytics' or 'People Org & Community' or 'Institutional Business' or 'MetaGov' or 'Other'):
                    AddContribution(db, date.strftime("%m/%y"), innershell[0], innershell[1], innershell[2], innershell[3], innershell[4], innershell[5])

        print("We thank you for all your work and it has been recorded for review.")



class MasterControls:
    def __init__(self):
        scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name("sheetCreds.json", scope) #access the json key you downloaded earlier 
        client = gspread.authorize(credentials) # authenticate the JSON key with gspread

        sheet = client.open("discordTests")  #opens discordTests google sheets
        self.userInfoSheet = sheet.worksheet("Sheet2")
        self.masterSheet = sheet.worksheet("MasterSheet main") #access Sheet1
        self.businessDevSheet = sheet.worksheet("BD")
        self.productSheet = sheet.worksheet("Product")
        self.treasurySheet = sheet.worksheet("Treasury")
        self.creativeSheet = sheet.worksheet("Creative")
        self.developmentSheet = sheet.worksheet("Dev")
        self.growthSheet = sheet.worksheet("Growth")
        self.expenseSheet = sheet.worksheet("Expense")
        self.mviSheet = sheet.worksheet("MVI")
        self.analyticsSheet = sheet.worksheet("Analytics")
        self.peopleOrgSheet = sheet.worksheet("PeopleOrg")
        self.intBusinessSheet =  sheet.worksheet("Int Business")
        self.metaGovSheet = sheet.worksheet("MetaGov")
        self.otherSheet = sheet.worksheet("Other")


        self.functionalGroupSheets = [self.businessDevSheet, self.productSheet, self.treasurySheet, self.creativeSheet, self.developmentSheet, self.growthSheet, self.expenseSheet, self.mviSheet, self.analyticsSheet, self.peopleOrgSheet, self.intBusinessSheet, self.metaGovSheet, self.otherSheet]

        
    
    def collectAllOwlIDs(self): #collects all the users stored in Sheet2 of Owls and puts them into Contributor TABLE
        db = 'index_contribution.db'
        range = ['A2:C136']
        userInfoD = self.userInfoSheet.batch_get(range)

        for outershell in userInfoD:
            for innershell in outershell:
                AddContributor(db, innershell[0], innershell[1], innershell[2])
        print("We have collected all the OWl IDs")
        


    def updateMasterSheet(self): #updates the mastersheet.
        dbname = 'index_contribution.db'
        connection = sqlite3.connect(dbname)
        c = connection.cursor() 

        bd_data = []
        product_data = []
        treasury_data = []
        creative_data = []
        engineering_data = []
        growth_data = []
        expenses_data = []
        mvi_data = []
        analytics_data = []
        peopleOrgCom_data = []
        intBusiness_data = []
        metaGov_data = []
        other_data = []
       

        c.execute("SELECT USER_ID, DISCORD_NAME, CONTRIBUTION_INFO, LINKS, OTHER_NOTES, FUNCTIONAL_GROUP FROM SINGLECONTRIBUTION WHERE DATE = '08/21'")
        l = list(c.fetchall())
        newlist = list(map(list, l))
   
        for lists in newlist:
            for contribution in lists:
                if contribution == 'BD':
                    bd_data.append(lists)
                elif contribution == 'Product':
                    product_data.append(lists)
                elif contribution == 'Treasury':
                    treasury_data.append(lists)
                elif contribution == 'Creative & Design':
                    creative_data.append(lists)
                elif contribution == 'Dev/Engineering':
                    engineering_data.append(lists)
                elif contribution == 'Growth':
                    growth_data.append(lists)
                elif contribution == 'Expenses':
                    expenses_data.append(lists)
                elif contribution == 'MVI':
                    mvi_data.append(lists)
                elif contribution == 'Analytics':
                    analytics_data.append(lists)
                elif contribution == 'People Org & Community':
                    peopleOrgCom_data.append(lists)
                elif contribution == 'Institutional Business':
                    intBusiness_data.append(lists)
                elif contribution =='MetaGov':
                    metaGov_data.append(lists)
                elif contribution == 'Other':
                    other_data.append(lists)

        start = 4

        self.businessDevSheet.batch_update([{
            'range': f'A{start}',
            'values': bd_data,
        }])

        self.productSheet.batch_update([{
            'range': f'A{start}',
            'values': product_data,
        }])

        self.treasurySheet.batch_update([{
            'range': f'A{start}',
            'values': treasury_data,
        }])

        self.creativeSheet.batch_update([{
            'range': f'A{start}',
            'values': creative_data,
        }])

        self.developmentSheet.batch_update([{
            'range': f'A{start}',
            'values': engineering_data,
        }])

        self.growthSheet.batch_update([{
            'range': f'A{start}',
            'values': growth_data,
        }])

        self.expenseSheet.batch_update([{
            'range': f'A{start}',
            'values': expenses_data,
        }])

        self.mviSheet.batch_update([{
            'range': f'A{start}',
            'values': mvi_data,
        }])

        self.analyticsSheet.batch_update([{
            'range': f'A{start}',
            'values': analytics_data,
        }])

        self.peopleOrgSheet.batch_update([{
            'range': f'A{start}',
            'values': peopleOrgCom_data,
        }])

        self.intBusinessSheet.batch_update([{
            'range': f'A{start}',
            'values': intBusiness_data,
        }])

        self.metaGovSheet.batch_update([{
            'range': f'A{start}',
            'values': metaGov_data,
        }])

        self.otherSheet.batch_update([{
            'range': f'A{start}',
            'values': other_data,
        }])

        print("Updated Master Sheets Complete")


    #Clears last MasterSheet Data
    def clearLastMonthsData(self):
        for list in self.functionalGroupSheets:
            list.batch_clear(["A4:V115"])
        print("Clearing Last months data is complete")



#creates a contributor class
class Contributor:
    def __init__(self, owlId, username, walletAddress):
        self.username = username
        self.walletAddress = walletAddress
        self.owlId = owlId

