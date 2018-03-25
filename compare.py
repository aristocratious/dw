# from __future__ import print_function
# import httplib2
# import os
# import glob
# import csv
# import datetime
# from apiclient import discovery
# from oauth2client import client
# from oauth2client import tools
# from oauth2client.file import Storage
# from get_xlsx import *
# import control_xlsx
#
# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
# CLIENT_SECRET_FILE = 'client_secret.json'
# APPLICATION_NAME = 'Google Sheets API Python Quickstart'

#
# def get_recent_csv(changes_only=True):
#     changes_directory = 'changes/'
#     full_directory = 'full/'
#     if changes_only:
#         list_of_files = glob.glob('changes/*.csv') # * means all if need specific format then *.csv
#         print("Using the changes-only CSV.")
#     else:
#         list_of_files = glob.glob('full/*.csv') # * means all if need specific format then *.csv
#         print("Using the full, complete CSV.")
#     latest_file = max(list_of_files, key=os.path.getctime)
#     return(latest_file)

# def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # home_dir = os.path.expanduser('~')
    # credential_dir = os.path.join(home_dir, '.credentials')
    # if not os.path.exists(credential_dir):
    #     os.makedirs(credential_dir)
    # credential_path = os.path.join(credential_dir,
    #                                'sheets.googleapis.com-python-quickstart.json')
    #
    # store = Storage(credential_path)
    # credentials = store.get()
    # if not credentials or credentials.invalid:
    #     flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    #     flow.user_agent = APPLICATION_NAME
    #     if flags:
    #         credentials = tools.run_flow(flow, store, flags)
    #     else: # Needed only for compatibility with Python 2.6
    #         credentials = tools.run(flow, store)
    #     print('Storing credentials to ' + credential_path)
    # return credentials
# def initiate():
    # credentials = get_credentials()
    # http = credentials.authorize(httplib2.Http())
    # discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
    # service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    #
    # spreadsheetId = '1kAl6FbZoa4PhHEJbO_l0CoVtyzjvBbfYpziaKXD7qPs'
    # rangeName = 'Published Products!A:E'
    # result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
    # global values
    # values = result.get('values', [])

# def validate():
    # if not values:
    #     print('No data found.')
    # else:
    #     valid=True
    #     for row in values[1:]:
    #         if len(row[0]) < 1:
    #             valid=False
    #             print("There is a SKU entry that is blank.")
    #             break
    #         if len(row[1]) < 1:
    #             valid=False
    #             print("There is a Series entry that is blank.")
    #             break
    #         if not ":" in row[3]:
    #             print("There is a format error in the Color column.  Please use ColorName:TTTTTTT format, separated by + signs.  Example: Black & Grey:TTTTTTT+Maroon & Gold:TTTTTTT.")
    #             print(row[3])
    #             valid=False
    #             break
    # return(valid)

# def setLocalSheet():
#     local_csv = csv.reader(open(get_recent_local_copy(),'r'))
#     #print(get_recent_local_copy())
#     global local_sheet
#     local_sheet = []
#     for row in local_csv:
#         local_sheet.append(row)
# def saveLocalFile():
#     if deletions > 0 or changes > 0:
#         print("Saving new local copy for future comparisons in the local_product_list folder.\n\n\n\n")
#         today = str(datetime.datetime.today().year)+'-'+str(datetime.datetime.today().month)+'-'+str(datetime.datetime.today().day)+' '+str(datetime.datetime.today().hour)+'-'+str(datetime.datetime.today().minute)
#         csvLocalWriter = csv.writer(open('local_product_list/local_'+ today +'.csv', 'w', newline=''))
#         for row in values:
#             csvLocalWriter.writerow(row)

# def make_csv(changes_only=True, selected_website="Consumer-"):
#     print("Getting live sheet from local storage")
#     live_sheet = get_XLSX_as_list(xfile="live",test=False)
#     today = str(datetime.datetime.today().year)+'-'+str(datetime.datetime.today().month)+'-'+str(datetime.datetime.today().day)+' '+str(datetime.datetime.today().hour)+'-'+str(datetime.datetime.today().minute)
#
#     if not changes_only:
#         csvChangeWriter = csv.writer(open('full/full_'+ today +'.csv', 'w', newline=''))
#         for live_sheet_row in live_sheet:
#             csvChangeWriter.writerow(live_sheet_row)
#         return
#
#     # setLocalSheet()
#
#     print("Getting local sheet to make comparisons")
#     local_sheet = get_XLSX_as_list(xfile="local", test=False)
#
#
#     csvChangeWriter = csv.writer(open('changes/changes_'+ today +'.csv', 'w', newline=''))
#     # csvChangeWriter.writerow(values[0])
#
#     global changes
#     changes=0
#     global deletions
#     deletions=0
#
#     temp_published_index = control_xlsx.indices[selected_website+"Published"]
#     temp_state_plus_unique_index = control_xlsx.indices[selected_website+"State+Unique"]
#
#     completed_products = []
#     for index, live_sheet_row in enumerate(live_sheet):
#         if live_sheet_row[temp_state_plus_unique_index] in completed_products:
#             #skip it
#             continue
#         if live_sheet_row not in local_sheet:
#             #there has been a change of some sort
#             if live_sheet_row[temp_published_index] == "FALSE":
#                 #an item was turned-off so we must grab all lines of same SKU and write to CSV
#                 temp_turned_off_state_plus_unique = live_sheet_row[temp_state_plus_unique_index]
#                 foundStart = False
#                 index_delta = 0
#                 index_start = None
#                 while foundStart == False:
#                     index_delta += 1
#                     if not temp_turned_off_state_plus_unique == live_sheet[index-index_delta][temp_state_plus_unique_index]:
#                         index_start = index - index_delta + 1
#                         foundStart = True
#                 index_delta = 0
#                 index_end = None
#                 while foundEnd == False:
#                     index_delta += 1
#                     if not temp_turned_off_state_plus_unique == live_sheet[index+index_delta][temp_state_plus_unique_index]:
#                         index_end = index + index_delta - 1
#                         foundEnd = True
#                 for row in live_sheet[index_start:index_end]:
#                     csvChangeWriter.writerow(row)
#                 completed_products.append(live_sheet_row[temp_state_plus_unique_index])
#                 deletions+=1
#                 continue
#             #print("Changed/added item", live_sheet_row[0])
#             csvChangeWriter.writerow(live_sheet_row)
#             changes+=1
#     print("\n\n\n\nFound "+str(changes)+" row changes in the live Google Drive XLSX file.")



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



# if __name__ == '__main__':
#     main()
