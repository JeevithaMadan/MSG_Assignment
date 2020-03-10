#****************************************************
# Purpose: Generates the chart data using the public API
#          developed by BillBoard.
# Inputs:  strChartNames: one or more chart names to search for
#          strStartDate: chart date as string in YYYYMMDD format
#          strEndDate : chart date as string in YYYYMMDD format
# Returns: Stores the chart data for each chart names in 
#          JSON and CSV file format in the specified directory 
#          with naming convention
#****************************************************

import sys
import billboard
import json
import logging
import argparse
import datetime
import csv
import os


def main():
    args = len(sys.argv) - 2
    
    try: 
        parser = argparse.ArgumentParser()
        
        # parser to get the date arguments
        parser.add_argument('date', type=lambda s: datetime.datetime.strptime(s, '%Y%m%d'))
        if parser.parse_args([sys.argv[len(sys.argv) - 2]]) and parser.parse_args([sys.argv[len(sys.argv) - 1]]):
            startdate = datetime.datetime.strptime(sys.argv[len(sys.argv) - 2], '%Y%m%d').date()
            enddate =  datetime.datetime.strptime(sys.argv[len(sys.argv) - 1], '%Y%m%d').date()
            print('Start and End Date: {0} {1}'.format(startdate, enddate))
            getChartAPI(args,startdate,enddate)
    except ValueError as err:
        print("Value error: {0}".format(err))
    except SystemExit: 	
        print("Invalid input type entered, Date is required")

        
def getChartAPI(args,startdate,enddate):
    print('Calling Chart API')
    chartnames=[]
    # get the list of chartnames from the arguments
    for index in range(1,args):
        chartnames.append(sys.argv[index])
    print('Pulling Chart data from billboard for the chartnames as ',', '.join(chartnames))
    for chname in chartnames:
        date_array = \
            (startdate + datetime.timedelta(days=index) for index in range(0, (enddate - startdate).days))
        
        # parse through each date between start and end date to get the chart data  
        for date_object in date_array:
            date = date_object.strftime("%Y-%m-%d")
            chdata = billboard.ChartData(chname,date=date)
            writetojson(chdata.json(), chdata.name, startdate, enddate)
            writetocsv(chdata.json(), chdata.name, startdate, enddate)
        print("For {0} , stored the chart data in json and csv file format".format(chname))


def writetojson(jsondata,chartname,sdate,edate):
    # writing to json file
    epochtime = int(datetime.datetime.now().timestamp())

    filename = './source/' + chartname + '/' + chartname + '_' + str(sdate) + '_' + str(edate) + '_' + str(epochtime) + '.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # open a file for writing
    with open(filename, 'w') as json_file:
        json.dump(jsondata, json_file, indent = 4)  

def writetocsv(jsondata,chartname,sdate,edate):
    # writing to csv file
    json_parsed = json.loads(jsondata)
    json_data = json_parsed['entries']

    epochtime = int(datetime.datetime.now().timestamp())
    filename = './stage/' + chartname + '/' + chartname + '_' + str(sdate) + '_' + str(edate) + '_' + str(epochtime) + '.csv'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # open a file for writing
    csv_data = open(filename, 'w')

    # create the csv writer object
    csvwriter = csv.writer(csv_data)
    count = 0
    for chart in json_data:
        if count == 0:
            header = chart.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(chart.values())
    csv_data.close()

if __name__ == "__main__":
    main()

	
