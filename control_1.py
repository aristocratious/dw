'''
Get the file from Google Drive
'''
global wholesale
global consumer
global selected_website
global count
count = 0
global filenum
filenum = 1
global append
append = ""
setupGoogleDrive()
response = input("\n\n\n\nType \'c\' for a consumer csv file or \'w\' for a wholesale one.  The default is consumer.")


wholesale = False
consumer = True
if response == "w":
    wholesale = True
    consumer = False
    selected_website = "Wholesale-"
    print("Exporting wholesale file.")
else:
    wholesale = False
    consumer = True
    selected_website = "Consumer-"
    print("Exporting retail/consumer file.")


################################################ OPENING A FILE TO WRITE TO
changes_only = None
valid_response = False
while valid_response==False:
    make_changes_or_complete_list = input("To create a complete CSV, type 'c'.  To make a CSV for changes, just hit enter.\n")
    if make_changes_or_complete_list == "c":
        changes_only = False
        make_csv(changes_only=changes_only, selected_website=selected_website)
        ask_to_quit("Created changes CSV")
        openCSV = csv.reader(open(get_recent_csv(changes_only=False),'r'))
        # openCSV = csv.reader(open("products_full_with_tags.csv",'r'))
        valid_response=True
    elif make_changes_or_complete_list == "":

        make_csv(selected_website=selected_website)

        ask_to_quit("Created full CSV")

        openCSV = csv.reader(open(get_recent_csv(changes_only=True),'r'))

        # openCSV = csv.reader(open(get_recent_changes(),'r'))
