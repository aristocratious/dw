import csv, re, os, sys
from makeVariants import *
from compare import *

def main():
    global wholesale
    response = input("\n\n\n\nType \'c\' for a consumer csv file or \'w\' for a wholesale one.  The default is consumer.")
    if response == "w":
        wholesale = True
        print("Exporting wholesale file.")
    else:
        wholesale = False
        print("Exporting retail/consumer file.")
if __name__ == "__main__":
    main()

################################################ OPENING A FILE TO WRITE TO
valid_response = False
while valid_response==False:
    make_changes_or_complete_list = input("If you would like to create a complete CSV, type 'c'.  If you'd like to just make a CSV for changes, just hit enter.\n")
    if make_changes_or_complete_list == "c":
        openCSV = csv.reader(open("products_full_with_tags.csv",'r'))
        valid_response=True
    elif make_changes_or_complete_list == "":
        valid_response2 = False
        while valid_response2==False:
            fetch_now = input("Would you like to fetch changes now from Google Sheets? Y/N.\n")
            if fetch_now=="Y" or fetch_now=="y":
                make_changes_csv()

                valid_response2=True
            elif fetch_now=="N" or fetch_now=="n":
                valid_response2=True
        openCSV = csv.reader(open(get_recent_changes(),'r'))
        valid_response=True
products = []
for product in openCSV:
    products.append(product)

################################################ CREATING THE CSV FILE

count = 0
filenum = 1
append = ""
if wholesale == True:
    append = "wholesale"
else:
    append = "consumer"
if products[0][0] == "State+Unique":
    del products[0]
if len(products) > 0:
    reachedEnd=False
    for pro in products:
        pro_list = pro
        SKU = re.sub("[^0-9]", "", pro[0])
        title = pro_list[1]
        tags = pro_list[2]
        colorstring = pro_list[3]
        colors = {}
        colorFormatCorrect=True
        for c in colorstring.split("+"):
            if not ":" in c:
                #print("There is a format error in the Color column.  Please use ColorName:TTTTTTT format, separated by + signs.  Example: Black & Grey:TTTTTTT+Maroon & Gold:TTTTTTT.")
                colorFormatCorrect=False
            else:
                colors[c.split(":")[0].strip()] = c.split(":")[1].strip()

        if colorFormatCorrect:
            #The following creates a new shopify product for each color of a design
            for color in colors:
                #The following creates a list of variants that are turned on for each design.
                #print(color)
                mediums = trufalsy(colors[color])
                #print(mediums)
                variants = [print12x12, print18x24, palletart10x16, print12x12_frame_black, \
                print12x12_frame_white, print18x24_frame_black, print18x24_frame_white]
                for x in range(len(variants)):
                    if mediums[x] == False:
                        variants[x]="Remove"
                variants = remove_values_from_list(variants, "Remove")
                noVariants=False
                if len(variants) == 0:
                    noVariants = True
                    variants = [print12x12]
                firstVar = True
                for variant in variants:
                    if count % 40000 == 0 or count == 0:
                        csvWriter = csv.writer(open('exports/export-'+append+str(filenum)+'.csv', 'w', newline=''))
                        csvWriter.writerow(header)
                        filenum+=1
                    if firstVar:
                        #tags = tags+",Print,Pallet Art,Print + Frame (Black),Print + Frame (White)"
                        if noVariants:
                            published="FALSE"
                        else:
                            published = "TRUE"
                        product_img = "http://69.164.207.120/images/" + str(variant("code")) + ".jpg"
                        variant_img = ""
                        vendor = "DoWhimsy"
                        typevar = "Designed by DoWhimsy"
                        bodyHTML = 'Body HTML'
                        add_collection = title
                        title_temp = title+" | "+color
                    else:
                        tags = ""
                        published = ""
                        product_img = ""
                        variant_img = "http://69.164.207.120/images/" + str(variant("code")) + ".jpg"
                        vendor = ""
                        typevar = ""
                        bodyHTML = ""
                        add_collection = ""
                        title_temp = ""
                    handle = title.lower().replace(", ","-").replace(" ","-")+"-"+color.lower().replace("&","-and-").replace(" ","")
                    csvWriter.writerow([handle, title_temp, bodyHTML, \
                    vendor, typevar, tags, published, "Type", variant("type"), "Size", variant("size"), \
                    "Color", color, str(SKU)+"-"+str(variant("code"))+"-"+str(color),variant("grams"), "shopify", 10, "deny", \
                    variant("fulfiller"), variant("price", wholesale), " ", "TRUE", "TRUE", " ", product_img, " ", variant_img, " ", " ", add_collection])
                    firstVar = False
                    count += 1
                    reachedEnd=True
    if reachedEnd:
        print("Completed export.")
        saveLocalFile()
else:
    print("There are no changes to implement.")
