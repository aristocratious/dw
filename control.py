'''

'''
from __future__ import print_function
import csv, re, os, sys, httplib2, glob, datetime
# from makeVariants import *
# from compare import *
#from get_xlsx import *
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from openpyxl import load_workbook

header = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags','Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', \
'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker',	'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service', \
'Variant Price', 'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Alt Text', 'Variant Image', 'Variant Weight Unit','Variant Tax Code', 'Collection']


indices = {
            "Order": 0,
            "Simple Product Code": 1,
            "State+Unique": 2,
            "Product Code": 3,
            "Variant SKU" : 4,
            "Series": 5,
            "Option1 Value": 6,
            "Color": 7,
            "Title": 8,
            "Consumer-Body (HTML)":9,
            "Consumer-Vendor":10,
            "Consumer-Handle":11,
            "Consumer-Type":12,
            "Type/Option": 13,
            "Size": 14,
            "Consumer-Tags":15,
            "Consumer-Published":16,
            "Consumer-Variant Grams":17,
            "Consumer-Variant Inventory Qty":18,
            "Consumer-Variant Inventory Policy":19,
            "Consumer-Variant Fulfillment Service":20,
            "Consumer-Variant Price":21,
            "Consumer-Variant Compare At Price":22,
            "Consumer-Variant Requires Shipping":23,
            "Consumer-Variant Taxable":24,
            "Consumer-Variant Barcode":25,
            "Consumer-Image Src":26,
            "Consumer-Image Position":27,
            "Consumer-Image Alt Text":28,
            "Consumer-Gift Card":29,
            "Consumer-Google Shopping / MPN":30,
            "Consumer-Google Shopping / Age Group":31,
            "Consumer-Google Shopping / Gender":32,
            "Consumer-Google Shopping / Google Product Category":33,
            "Consumer-SEO Title":34,
            "Consumer-SEO Description":35,
            "Consumer-Google Shopping / AdWords Grouping":36,
            "Consumer-Google Shopping / AdWords Labels":37,
            "Consumer-Google Shopping / Condition":38,
            "Consumer-Google Shopping / Custom Product":39,
            "Consumer-Google Shopping / Custom Label 0":40,
            "Consumer-Google Shopping / Custom Label 1":41,
            "Consumer-Google Shopping / Custom Label 2":42,
            "Consumer-Google Shopping / Custom Label 3":43,
            "Consumer-Google Shopping / Custom Label 4":44,
            "Consumer-Variant Image":45,
            "Consumer-Variant Weight Unit":46,
            "Consumer-Variant Tax Code":47,
            "Wholesale-Body (HTML)":48,
            "Wholesale-Vendor":49,
            "Wholesale-Handle":50,
            "Wholesale-Type":51,
            "Wholesale-Tags":52,
            "Wholesale-Published":53,
            "Wholesale-Variant Grams":54,
            "Wholesale-Variant Inventory Qty":55,
            "Wholesale-Variant Inventory Policy":56,
            "Wholesale-Variant Fulfillment Service":57,
            "Wholesale-Variant Price":58,
            "Wholesale-Variant Compare At Price":59,
            "Wholesale-Variant Requires Shipping":60,
            "Wholesale-Variant Taxable":61,
            "Wholesale-Variant Barcode":62,
            "Wholesale-Image Src":63,
            "Wholesale-Image Position":64,
            "Wholesale-Image Alt Text":65,
            "Wholesale-Gift Card":66,
            "Wholesale-Google Shopping / MPN":67,
            "Wholesale-Google Shopping / Age Group":68,
            "Wholesale-Google Shopping / Gender":69,
            "Wholesale-Google Shopping / Google Product Category":70,
            "Wholesale-SEO Title":71,
            "Wholesale-SEO Description":72,
            "Wholesale-Google Shopping / AdWords Grouping":73,
            "Wholesale-Google Shopping / AdWords Labels":74,
            "Wholesale-Google Shopping / Condition":75,
            "Wholesale-Google Shopping / Custom Product":76,
            "Wholesale-Google Shopping / Custom Label 0":77,
            "Wholesale-Google Shopping / Custom Label 1":78,
            "Wholesale-Google Shopping / Custom Label 2":79,
            "Wholesale-Google Shopping / Custom Label 3":80,
            "Wholesale-Google Shopping / Custom Label 4":81,
            "Wholesale-Variant Image":82,
            "Wholesale-Variant Weight Unit":83,
            "Wholesale-Variant Tax Code":84
           }



FILE_ID = "1g8HA8dGM9d4OMTg5jGEmOALFled5yj8c"
#LOCAL_FILE_NAME = "local_product_list/product_list.xlsx"
LIVE_FILE_NAME = "live_product_list/live_product_list.xlsx"
FIRST_SHEET = "Sheet1"

# Set up Google Drive API
# http://pythonhosted.org/PyDrive/filemanagement.html#download-file-content
def getGoogleDriveFile():
    print("Saving copy from Google Drive")
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        print("Google Drive authenticated.")
        gfile = drive.CreateFile({'id': FILE_ID})
        gfile.GetContentFile(LIVE_FILE_NAME) # Download file as 'catlove.png'.
        print("Saved to",LIVE_FILE_NAME)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


    return LIVE_FILE_NAME

def LOCAL_FILE_NAME():
    list_of_files = glob.glob('local_product_list/*.xlsx') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return(latest_file)

# Start accessing using OpenPyxl
def get_XLSX_as_list(xfile, test=False, xsheet=FIRST_SHEET):
    if xfile=="live":
        xfile = LIVE_FILE_NAME
    elif xfile == "local":
        xfile = LOCAL_FILE_NAME()
    print("Get XLSX", str(xfile))
    wb = load_workbook(filename=xfile, read_only=True)
    ws = wb[xsheet]
    big_list = []
    index = 0
    for row in ws.rows: #use the whole file, without headers
        if index < 5:
            index+=1
            continue
        big_list.append([str(cell.value) for cell in row])
    return cleanseList(big_list)


def get_recent_csv(changes_only):
    changes_directory = 'changes/'
    full_directory = 'full/'
    if changes_only==True:
        list_of_files = glob.glob('changes/*.csv') # * means all if need specific format then *.csv
        print("Using the changes-only CSV.")
    else:
        list_of_files = glob.glob('full/*.csv') # * means all if need specific format then *.csv
        print("Using the full, complete CSV.")
    latest_file = max(list_of_files, key=os.path.getctime)
    print(str(latest_file))
    return(latest_file)

def setSelectedWebsite():
    response = input("Type \'c\' for a consumer csv file or \'w\' for a wholesale one.  The default is consumer.")
    if response == "w":
        wholesale = True
        consumer = False
        selected_website = "Wholesale-"
        return selected_website
        #print("Selected wholesale file.")
    else:
        wholesale = False
        consumer = True
        selected_website = "Consumer-"
        return selected_website
        #print("Exporting retail/consumer file.")

def setChangesVar():
    valid_response = False
    while valid_response==False:
        make_changes_or_complete_list = input("To create a complete CSV, type 'c'.  To make a CSV for changes, just hit enter.\n")
        if make_changes_or_complete_list == "c":
            #print("Making a complete .csv file")
            changes_only = False
            #xlsx_to_csv(changes_only=changes_only, selected_website=selected_website)
            valid_response=True
            return False
        elif make_changes_or_complete_list == "":
            #print("Making a changes-only .csv file")
            changes_only = True
            #xlsx_to_csv(selected_website=selected_website)
            valid_response=True
            return True

def printNumNotMatches(old, new):
    print(str(len([x for x in old if x not in new]))+" differences local->live.", str(len([x for x in new if x not in old]))+" differences live->local.")

def returnAreChanges(old,new):
    foundChanges = False
    for x in new:
        if foundChanges == False:
            if x not in old:
                foundChanges = True
                return True
    if foundChanges == False:
        return False

def cleanseRow(row):
    return [cell if cell != "None" else "" for cell in row]
def cleanseList(row):
    all_Nones = True
    for cell in row:
        if cell != "None":
            all_Nones=False
    return [z for z in row if all_Nones==False]


def xlsx_to_csv(changes_only, selected_website):
    today = str(datetime.datetime.today().year)+'-'+str(datetime.datetime.today().month)+'-'+str(datetime.datetime.today().day)+' '+str(datetime.datetime.today().hour)+'-'+str(datetime.datetime.today().minute)
    if changes_only == False:
        csvChangeWriter = csv.writer(open('full/full_'+ today +'.csv', 'w', newline=''))
        live_sheet = get_XLSX_as_list(xfile="live",test=False)
        for live_sheet_row in live_sheet:
            csvChangeWriter.writerow(cleanseRow(live_sheet_row))
        print("...done!  Saved the .csv file to the full/ folder.")

    elif changes_only == True:
        print("Getting live sheet from local storage")
        live_sheet = get_XLSX_as_list(xfile="live",test=False)
        # setLocalSheet()
        print("Getting local sheet to make comparisons")
        local_sheet = get_XLSX_as_list(xfile="local", test=False)


        #printNumNotMatches(local_sheet,live_sheet)
        if returnAreChanges(local_sheet,live_sheet) == False:
            print("There are no changes to add to a CSV.")
        else:
            csvChangeWriter = csv.writer(open('changes/changes_'+ today +'.csv', 'w', newline=''))
            # csvChangeWriter.writerow(values[0])

            global changes
            changes=0
            global deletions
            deletions=0
            if selected_website == None:
                setSelectedWebsite()
            temp_published_index = indices[selected_website+"Published"]
            temp_state_plus_unique_index = indices["State+Unique"]


            completed_products = []
            changed_SKUs = []
            for index, live_sheet_row in enumerate(live_sheet):
                if live_sheet_row[temp_state_plus_unique_index] in completed_products:
                    #skip it
                    continue
                if live_sheet_row not in local_sheet:
                    #there has been a change of some sort
                    # if live_sheet_row[temp_published_index] == "FALSE":
                    #     #an item was turned-off so we must grab all lines of same SKU and write to CSV
                    #     temp_turned_off_state_plus_unique = live_sheet_row[temp_state_plus_unique_index]
                    #     foundStart = False
                    #     index_delta = 0
                    #     index_start = None
                    #     while foundStart == False:
                    #         index_delta += 1
                    #         if not temp_turned_off_state_plus_unique == live_sheet[index-index_delta][temp_state_plus_unique_index]:
                    #             index_start = index - index_delta + 1
                    #             foundStart = True
                    #     index_delta = 0
                    #     index_end = None
                    #     while foundEnd == False:
                    #         index_delta += 1
                    #         if not temp_turned_off_state_plus_unique == live_sheet[index+index_delta][temp_state_plus_unique_index]:
                    #             index_end = index + index_delta - 1
                    #             foundEnd = True
                    #     for row in live_sheet[index_start:index_end]:
                    #         csvChangeWriter.writerow(cleanseRow(row))
                    #     completed_products.append(live_sheet_row[temp_state_plus_unique_index])
                    #     deletions+=1
                    #     continue
                    changed_SKUs.append(live_sheet_row[temp_state_plus_unique_index]) #add the SKU of any changed row

                    #print("Changed/added item", live_sheet_row[0])

                    changes+=1
            for row in live_sheet:
                if row[temp_state_plus_unique_index] in changed_SKUs:
                    csvChangeWriter.writerow(row)
            print("\n\n\n\nFound "+str(changes)+" row changes in the live Google Drive XLSX file.")



            # print("Not checking for deletions")
            # local_skus = [item[3] for item in local_sheet] #3 is the VARIANT SKU
            # live_skus = [item[3] for item in live_sheet] #3 is the VARIANT SKU
            #for sku in local_skus:
            #    if sku not in live_skus:
            #
            #        csvChangeWriter.writerow(live_sheet_row)
            #        deletions+=1
            # for row in local_sheet:
            #     if row[0] not in live_skus:
            #         row[14] = "FALSE" #Unpublish Row
            #         row[48] = "FALSE"
            #         csvChangeWriter.writerow(row)
            #         deletions+=1
            # print("Found "+str(deletions)+" row deletions in the live Google Drive sheet.\n\n\n\n")
            print("...done!  Saved the .csv file to the changes/ folder.")


def get_recent_csv(changes_only):
    changes_directory = 'changes/'
    full_directory = 'full/'
    if changes_only:
        list_of_files = glob.glob('changes/*.csv') # * means all if need specific format then *.csv
        print("Using the changes-only CSV.")
    else:
        list_of_files = glob.glob('full/*.csv') # * means all if need specific format then *.csv
        print("Using the full, complete CSV.")
    latest_file = max(list_of_files, key=os.path.getctime)
    return(latest_file)

def ask_to_quit(accomplishment):
    quit = input(str(accomplishment)+" Hit enter to continue or \"q\" to quit.")
    if quit == "q":
        from sys import exit
        exit("Ending program.")

def export_row_to_CSV(row, selected_website, first_of_product=False):
    if row[2] == "None":
        return("End of sheet")
    # if row[indices[selected_website+"Published"]] == "FALSE":
    #     return None #Is not published, so don't post it.


    #first_of_product=True
    # if count % 40000 == 0 or count == 0:
    #     csvWriter = csv.writer(open('exports/export-'+append+str(filenum)+'.csv', 'w', newline=''))
    #     csvWriter.writerow(header)
    #     filenum+=1


    #for row in rows_as_list:
    published = row[indices[selected_website+"Published"]]

    #if published:
    SKU = row[indices["Variant SKU"]]
    title = str(row[indices["Series"]])+" ("+str(row[indices["Color"]])+")"
    tags = row[indices[selected_website+"Tags"]]
    handle = row[indices[selected_website+"Handle"]]
    series = row[indices["Series"]]
    vtype = row[indices["Type/Option"]]
    vsize = row[indices["Size"]]
    vcode = row[indices["Product Code"]]
    vgrams = row[indices[selected_website+"Variant Grams"]]
    vfulfiller = row[indices[selected_website+"Variant Fulfillment Service"]]
    vprice = row[indices[selected_website+"Variant Price"]]
    color = row[indices["Color"]]



    if first_of_product:
        # product_img = "http://69.164.207.120/images/" + str(variant("code")) + ".jpg"
        product_img = row[indices[selected_website+"Image Src"]]
        variant_img = ""
        vendor = row[indices[selected_website+"Vendor"]]
        typevar = row[indices[selected_website+"Type"]]
        bodyHTML = row[indices[selected_website+"Body (HTML)"]]
        add_collection = series
        first_of_product=False
    else:
        tags = ""
        published = ""
        product_img = ""
        # variant_img = "http://69.164.207.120/images/" + str(variant("code")) + ".jpg"
        variant_img = row[indices[selected_website+"Variant Image"]]
        if variant_img == "None":
            variant_img = row[indices[selected_website+"Image Src"]]
        vendor = ""
        typevar = ""
        bodyHTML = ""
        add_collection = ""
        title = ""
    # handle = title.lower().replace(", ","-").replace(" ","-")+"-"+color.lower().replace("&","-and-").replace(" ","")
    return([handle, title, bodyHTML, \
    vendor, typevar, tags, published, "Type", vtype, "Size", vsize, \
    "Color", color, SKU,\
    vgrams, "shopify", 10, "deny", \
    vfulfiller, vprice, " ", "TRUE", \
    "TRUE", " ", product_img, " ", variant_img, " ", " ", add_collection])
    #lines_printed+=1
    # count += 1
    # reachedEnd=True
    #
    # if reachedEnd:
    #     print("Completed export.")
    # saveLocalFile()

#1 get Google drive live file
def getLiveFile():
    count = 0
    filenum = 1
    append = ""

    getGoogleDriveFile()



    #3
#2 make changes CSV
def makeChangesCSV(changes_only, selected_website):
    # changes_only = None
    # valid_response = False
    # while valid_response==False:
    #     make_changes_or_complete_list = input("To create a complete CSV, type 'c'.  To make a CSV for changes, just hit enter.\n")
    #     if make_changes_or_complete_list == "c":
    #         changes_only = False
    #         xlsx_to_csv(changes_only=changes_only, selected_website=selected_website)
    #         #ask_to_quit("Created changes CSV")
    #         openCSV = csv.reader(open(get_recent_csv(changes_only=False),'r'))
    #         # openCSV = csv.reader(open("products_full_with_tags.csv",'r'))
    #         valid_response=True
    #     elif make_changes_or_complete_list == "":
    #
    #         xlsx_to_csv(selected_website=selected_website)
    #
    #         #ask_to_quit("Created full CSV")
    #
    #         openCSV = csv.reader(open(get_recent_csv(changes_only=True),'r'))
    #
    #         # openCSV = csv.reader(open(get_recent_changes(),'r'))
    if changes_only == None:
        changes_only =  setChangesVar()
    if selected_website == None:
        selected_website = setSelectedWebsite()
    print("Changes_only",changes_only,"Selected website",selected_website)
    xlsx_to_csv(changes_only, selected_website=selected_website)
#3 make the shopify import csv
def makeShopifyCSV():
    changes_only = setChangesVar()
    openCSV = csv.reader(open(get_recent_csv(changes_only),'r'))

    products = list(openCSV) #gets rid of headers

    # for product in openCSV:
    #     products.append(product)
    print("Added all lines from CSV to list")
    print(str(len(products)))
    ################################################ CREATING THE CSV FILE
    selected_website = setSelectedWebsite()
    if selected_website == "Wholesale-":
        append = "wholesale"
    elif selected_website == "Consumer-":
        append = "consumer"
    # if products[0][0] == "State+Unique":
    #     del products[0]
    if len(products) == 0:
        exit("There are no rows in opened CSV.")
    reachedEnd=False
    completed_products = []
    #index = 0
    #for row in products:
    filenum = 1
    csvWriter = csv.writer(open('exports/export-'+append+str(filenum)+'.csv', 'w', newline=''))
    csvWriter.writerow(header)



    for index, row in enumerate(products):
        if row[indices[selected_website+"Published"]] == "FALSE":
            continue  #don't do anything with turned-off lines (yet)
        StatePlusUnique = row[indices["State+Unique"]]
        if StatePlusUnique not in completed_products and StatePlusUnique is not "None":
            # first_of_product = True
            csvWriter.writerow(export_row_to_CSV(row, selected_website, first_of_product=True))
            completed_products.append(StatePlusUnique)
        else:
            csvWriter.writerow(export_row_to_CSV(row, selected_website, first_of_product=False))
    for row in products:
        StatePlusUnique = row[indices["State+Unique"]]
        if StatePlusUnique not in completed_products: # it hasn't been completed because it is turned off
            csvWriter.writerow(export_row_to_CSV(row, selected_website, first_of_product=True))
            print("Printed turned off product.")
            completed_products.append(StatePlusUnique)
        else:
            #turned-off rows only need one line with Published = FALSE
            pass
        # group_of_rows_representing_same_product = []
        # index_delta = 0
        #
        # checking_if_next_rows_are_same_product = True
        # csvWriter.writerow(export_row_to_CSV(row, selected_website, first_of_product=True))
        # while checking_if_next_rows_are_same_product == True:
        #     index_delta+=1
        #     try:
        #         #print(index_delta)
        #         #group_of_rows_representing_same_product.append(row)
        #         temp_subsequent_row = products[index+index_delta]
        #         if temp_subsequent_row[indices["State+Unique"]] == StatePlusUnique:
        #             if export_row_to_CSV(temp_subsequent_row, selected_website, first_of_product=False) == "end":
        #                 exit("Reached end of row on line "+str(index))
        #             #group_of_rows_representing_same_product.append(products[index+index_delta])
        #         else:
        #             checking_if_next_rows_are_same_product = False #the next row is not a new product
        #     except IndexError:
        #         checking_if_next_rows_are_same_product = False
        #         pass
        #     except Exception as e:
        #         checking_if_next_rows_are_same_product = False
        #         print(str(e))

        #export_row_to_CSV(group_of_rows_representing_same_product)


def main():
    global wholesale
    global consumer
    global selected_website
    selected_website = None
    global count
    global filenum
    global append
    global csvWriter
    global make_changes_or_complete_list
    global changes_only
    changes_only = None
    make_changes_or_complete_list = None

    cont = True
    while cont:
        startWhere = int(input("Choose: [1] Get live Google Drive file, [2] convert XLSX to CSV (with or without changes), or [3] make Shopify CSV file."))
        if startWhere == 1:
            #
            getLiveFile()
        elif startWhere == 2:
            #
            makeChangesCSV(changes_only=changes_only, selected_website=selected_website)
        elif startWhere == 3:
            #
            makeShopifyCSV()
        else:
            continue
        answer = input("Task completed.  Would you like to do another task? [y] for yes, [n] for no.  Default is yes.")
        if answer == "n":
            cont = False
        else:
            continue

if __name__ == "__main__":
    main()
