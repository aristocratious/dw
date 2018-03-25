

header = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags','Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', \
'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker',	'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service', \
'Variant Price', 'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Alt Text', 'Variant Image', 'Variant Weight Unit','Variant Tax Code', 'Collection']

def trufalsy (mediums):
    medlist = []
    if len(mediums) != 7:
        print("Error because there were "+str(len(mediums))+" medium True/Falses and not 7.")
        return None
    for letter in mediums:
        if letter == "T":
            medlist = medlist + [True]
        elif letter == "F":
            medlist = medlist + [False]
        else:
            print("One of the letters in the mediums T/F column was not T or F.")
    return medlist

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]
'''
Type & size                         Code        Vendor      VariantGrams *not in use yet
Design Only, Digital File     -     110         DW          0
Print, 12" x 12"                    236         SP          3
Print, 18" x 24"                    241         SP          6
Pallet Art, 10" x 16"               381         AR          12
12" X 12" Print + Frame (Black)     790         SP+AR       13
12" x 12" Print + Frame (White)     791         SP+AR       13
18" x 24" Print + Frame (Black)     792         SP+AR       20
18" x 24" Print + Frame (White)     793         SP+AR       20
'''

def print12x12(requested_property, wholesale=False):

    if requested_property == "type":
        return "Print"
    elif requested_property == "size":
        return "12\" x 12\""
    elif requested_property == "code":
        return "236"
    elif requested_property == "price":
        if wholesale == True:
            return 9.6
        return "24"
    elif requested_property == "fulfiller":
        return "SP"
    elif requested_property == "grams":
        return 3
    else:
        return " "
def print18x24(requested_property, wholesale=False):
    if requested_property == "type":
        return "Print"
    elif requested_property == "size":
        return "18\" x 24\""
    elif requested_property == "code":
        return "241"
    elif requested_property == "price":
        if wholesale == True:
            return "14"
        return "35"
    elif requested_property == "fulfiller":
        return "SP"
    elif requested_property == "grams":
        return 6
    else:
        return " "

def palletart10x16(requested_property, wholesale=False):
    if requested_property == "type":
        return "Pallet Art"
    elif requested_property == "size":
        return "10\" x 16\""
    elif requested_property == "code":
        return "381"
    elif requested_property == "price":
        if wholesale == True:
            return 14
        return "35"
    elif requested_property == "fulfiller":
        return "AR"
    elif requested_property == "grams":
        return 12
    else:
        return " "

def print12x12_frame_black(requested_property, wholesale=False):
    if requested_property == "type":
        return "Print + Frame (Black)"
    elif requested_property == "size":
        return "12\" x 12\""
    elif requested_property == "code":
        return "790"
    elif requested_property == "price":
        if wholesale == True:
            return 19.6
        return "49"
    elif requested_property == "fulfiller":
        return "SP+AR"
    elif requested_property == "grams":
        return 13
    else:
        return " "
def print12x12_frame_white(requested_property, wholesale=False):
    if requested_property == "type":
        return "Print + Frame (White)"
    elif requested_property == "size":
        return "12\" x 12\""
    elif requested_property == "code":
        return "791"
    elif requested_property == "price":
        if wholesale == True:
            return 19.6
        return "49"
    elif requested_property == "fulfiller":
        return "SP+AR"
    elif requested_property == "grams":
        return 13
    else:
        return " "

def print18x24_frame_black(requested_property, wholesale=False):
    if requested_property == "type":
        return "Print + Frame (Black)"
    elif requested_property == "size":
        return "18\" x 24\""
    elif requested_property == "code":
        return "792"
    elif requested_property == "price":
        if wholesale == True:
            return 40
        return "100"
    elif requested_property == "fulfiller":
        return "SP+AR"
    elif requested_property == "grams":
        return 20
    else:
        return " "

def print18x24_frame_white(requested_property, wholesale=False):
    if requested_property == "type":
        return "Print + Frame (White)"
    elif requested_property == "size":
        return "18\" x 24\""
    elif requested_property == "code":
        return "793"
    elif requested_property == "price":
        if wholesale == True:
            return 40
        return "100"
    elif requested_property == "fulfiller":
        return "SP+AR"
    elif requested_property == "grams":
        return 20
    else:
        return " "
