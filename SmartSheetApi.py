# Import.
import smartsheet
import requests
import json
import sys
from time import sleep
import datetime
from datetime import date, timedelta
#this is the new version
smartsheet = smartsheet.Smartsheet('s4l9x10ccm9k1roexm5qx0awgg')
action = smartsheet.Sheets.list_sheets(include_all=False)

# Instantiate smartsheet and specify access token value.
i=0;

for single_sheet in action.data:
    SheetName = single_sheet.name;
    SheetId = single_sheet.id ;
    #print(SheetName)
    if SheetName.find("remnant_team_") == 0 :
        #print(i)
        SheetResponse = smartsheet.Sheets.get_sheet_as_csv(SheetId,"D:/DATA_LAKE_INGESTION_US/SmartSheet/")
        i+=1
        #store the report into json file    
        #print("saved "+SheetName);
        # Get all columns.
        #action = smartsheet.Sheets.get_columns(SheetId, include_all=True)
        #columns = action.data
        #print(SheetResponse)
        
        
        
        
        
        
        
        
        
        
        
        
sys.exit();
        
        
        
      