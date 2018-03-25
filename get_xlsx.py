# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from openpyxl import load_workbook
# import glob, os
#
# FILE_ID = "1KqjcT3H3tF73taZX4GEAw6NHvoyFeXps"
# #LOCAL_FILE_NAME = "local_product_list/product_list.xlsx"
# LIVE_FILE_NAME = "live_product_list/live_product_list.xlsx"
# FIRST_SHEET = "Sheet1"
#
# # Set up Google Drive API
# # http://pythonhosted.org/PyDrive/filemanagement.html#download-file-content
# def getGoogleDriveFile():
#     print("Saving copy from Google Drive")
#     try:
#         gauth = GoogleAuth()
#         gauth.LocalWebserverAuth()
#         drive = GoogleDrive(gauth)
#         print("Google Drive authenticated.")
#         gfile = drive.CreateFile({'id': FILE_ID})
#         gfile.GetContentFile(LIVE_FILE_NAME) # Download file as 'catlove.png'.
#         print("Saved to",LIVE_FILE_NAME)
#     except:
#         print("Unexpected error:", sys.exc_info()[0])
#         raise
#
#
#     return LIVE_FILE_NAME
#
# def LOCAL_FILE_NAME():
#     list_of_files = glob.glob('local_product_list/*.xlsx') # * means all if need specific format then *.csv
#     latest_file = max(list_of_files, key=os.path.getctime)
#     return(latest_file)
#
# # Start accessing using OpenPyxl
# def get_XLSX_as_list(xfile, test=False, xsheet=FIRST_SHEET):
#     if xfile=="live":
#         xfile = LIVE_FILE_NAME
#     elif xfile == "local":
#         xfile = LOCAL_FILE_NAME()
#     print("Get XLSX", str(xfile))
#     wb = load_workbook(filename=xfile, read_only=True)
#     ws = wb[xsheet]
#     big_list = []
#
#     if test:
#         for row in ws.rows: #set it to just a snippet of the full file
#             big_list.append([str(cell.value) for cell in row])
#     else:
#         for row in ws.rows: #use the whole file
#             big_list.append([str(cell.value) for cell in row])
#     return(big_list)
#
