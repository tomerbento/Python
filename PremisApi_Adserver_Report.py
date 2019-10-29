# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 19:01:12 2019

@author: tomerb
"""

import requests
import json
import sys
from time import sleep
import datetime
from datetime import date, timedelta


#print ("start")
#sleep(5)
#print("continue")
ver = "1.0.0.0"
ApiUnameTest = "Investing2test_API";
ApiPassTest = "c1265fa1a53b06ded1a48444c6907c85";



BaseLink = "https://console.primis.tech/UI/php/responders/apiResponder.php";
Method = "method=authentication";
Version = "version=2.11";
TokenUser = "apiUserName=Investing2test_API";
TokenPass = "apiUserCode=c1265fa1a53b06ded1a48444c6907c85";

ApiUname = "Investing_API";
ApiPass = "764478046227";


#ApiUname = ApiUname;
#ApiPass = ApiPass;
#Investing_API
#764478046227




#amout of days back from today to pull report
delta_interval = 3 
start_date = (datetime.datetime.now()- timedelta(delta_interval)).date()
end_date = datetime.datetime.now().date()
delta = timedelta(days=1)




print ("today is :"+  end_date.strftime("%Y-%m-%d"))
print("start from  : "+ start_date.strftime("%Y-%m-%d"))

#authentication to get the token (valid for 1 hour)
params = (
        (' method', 'authentication'),
        ('apiUserName', ApiUname),
        ('apiUserCode', ApiPass),
        ('version', '2.11'),
            )


    
response = requests.post(BaseLink, params=params);
JsonDump = json.dumps(response.json());
#store the response token
Token =json.loads(JsonDump)["token"];
print("the token is : "+Token)

    





#set the dim for report
Dim = '["placement","campaign","browser","country","deviceType","domain","timeInterval"]'
#Dim = '["timeInterval"]'


#set the metrics for the report
Metric =    '["id","name","video_ad_imps","video_ad_ecpm","video_ad_revenue","video_ad_imps_viewability_rate","video_ad_attempts","video_ad_starts","video_ad_completion_rate","video_ad_fillrate","adserver_serving_fee"]'


#enter a loop from start date to end and pull each day seperatly
while start_date <= end_date:
        DateInterval = start_date.strftime('%Y-%m-%d') # the current iteration date that will be set to start and end
        startDate = DateInterval
        endDate =DateInterval
        
        #set the report parameters
        AdServerData ="""[
              {
                "name": "reportType",
                "data": "adServer"
              },
              {
                "name": "timeInterval",
                "data": "date"
              },
              {
                "name": "fromDay",
                "data":  \"%s\"
              },
              {
                "name": "toDay",
                "data":  \"%s\"
              },
              {
                "name": "dimensions",
                "data": %s
              },
              {
                "name": "period",
                "data": "custom"
              },
              {
                "name": "metrics",
                "data": %s
              }
            ]"""% (startDate,endDate,Dim,Metric)
              
        JsonData = {
              'token': Token ,
              'version': '2.11',
              'method': 'publisherReport',
              'data': AdServerData
                  } 
        
        
            #print the current iteration date
        print (start_date.strftime("%Y-%m-%d"))
        
        response = requests.post(BaseLink, data=JsonData);
        JsonDump = json.dumps(response.json());
        
        #store the reprot id request for later use to check if ready
        ReportId =json.loads(JsonDump)["reportId"];
        print("the reportid is : "+ ReportId)
           
            
        
            
            
        i=1
        
        #set the interval in seconds for evry wait before checking if report is ready
        ReportFetchInterval = 30
        #enter a loop until the report is ready
        while True  :
                        ReportJsonData = {
                          'token': Token ,
                          'version': '2.11',
                          'method': 'publisherReport',
                          'reportId' : ReportId
                        }
            
                
          
                        response = requests.post(BaseLink, data=ReportJsonData);
        
                        
                        
                        if response.status_code==454 :
                            print(str(i)+ "Report "+ ReportId+ " not ready yet , trying again in "+ str(ReportFetchInterval) + " seconds")
                    
                        elif response.status_code==200:
                            print("ready , fetching report ")
                            FileName ='D:/DATA_LAKE_INGESTION_US/Primis/Adserver_Report/Primis_adServer_Report_'+DateInterval+'.json' 
                            break
                        else:
                            print(response.status_code)
                            break
                        i+=1           
                        sleep(ReportFetchInterval)
        
                    
                
            #store the report into json file    
        with open(FileName, 'w') as f:
             json.dump(response.json(), f, ensure_ascii=False)
             print("file "+FileName + " Saved")
                    
        

    
    
        
    #move one day and repeat
        start_date += delta

print("All files saved")


    
