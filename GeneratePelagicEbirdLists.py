import sys
import csv
import time
from datetime import datetime, timedelta
import operator
import xlrd
import xlwt
from xlrd import open_workbook,cellname,xldate_as_tuple
from math import radians, cos, sin, asin, sqrt

class CellDetails:
        def __init__(self):
                self.key = ""
                self.startTime = None
                self.endTime = None
                self.roundedLat = 0.0
                self.roundedLon = 0.0
                self.origLat = 0.0
                self.origLon = 0.0
                self.distance = 0.0
                self.duration = 0.0

def GetDistance(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 

        # 6367 km is the radius of the Earth
        km = 6367 * c
        return km 

def AddCellDetails(roundedLat, roundedLon, origLat, origLon, curKeyId, myTime, cellList):
        # Generate the key using rounded lat/lon values, check if it exists already,
        #       if not, add it
        #       if found, check if it is less than 3 hours and without gaps, if so, update the details
        #       else(gap or >3hrs), ignore, and return 0. Outer loop will generate new key ID and call again,
        #               will insert the new entry at that time.
        myKey = "[" + roundedLat + "-" + roundedLon + ":" + str(curKeyId) + "]"
        if myKey in cellList:
                diff = myTime - cellList[myKey].endTime
                if diff.total_seconds()/60 > 1:
                        # This is a reentry into the cell after a gap, so return 0 so that a new list is created
                        return 0
                diff = myTime - cellList[myKey].startTime
                if diff.total_seconds()/3600 > 3:
                        return 0                
                else:
                        cellList[myKey].endTime = myTime
                        cellList[myKey].distance += GetDistance(origLat, origLon, cellList[myKey].origLat, cellList[myKey].origLon)
                        cellList[myKey].origLat = origLat
                        cellList[myKey].origLon = origLon
                        cellList[myKey].duration += 1
                        return 1
        else:
                cellList[myKey] = CellDetails()
                cellList[myKey].key = myKey
                cellList[myKey].startTime = myTime
                cellList[myKey].endTime = myTime
                cellList[myKey].roundedLat = roundedLat
                cellList[myKey].roundedLon = roundedLon
                cellList[myKey].origLat = origLat
                cellList[myKey].origLon = origLon
                cellList[myKey].duration = 1
                return 1

def InsertIntoRightCell(finalCellDataList, centrePoint, keyId, timeofSighting, species, count):
        # Iterate through the list of cells and compare the cell identifier for current sighting
        # When a matching cell is found, check if species is already inserted,
        #       if it is not there, add the species into this cell list
        #       else, update the count
        if (keyId > 50):
                print("Looks like some problem!!!! Key data : ", centrePoint, keyId, species, count, timeofSighting, "\n")
                return 1
        myKey = "[" + centrePoint + ":" + str(keyId) + "]"
        for row in finalCellDataList:
                if(row["Cell Details"] == myKey):
                        if(timeofSighting >= row["Start Time"] and timeofSighting <= row["End Time"]):
                                if species in row:
                                        row[species] += count 
                                else:
                                        row[species] = count
                                return 1        
        return 0
        
def HandleSighting(timeOfSighting, species, count, finalCellDataList, timePoints):
        # Using the time of sighting, get the details of the sighting
        # Then, use these details to find and add this sighting to the right cell list.
        for line in timePoints:
                myKeyId = 1
                timePoint = line["time"]
                myLat = '%.1f' % round(float(line["lat"]), 1)
                myLon = '%.1f' % round(float(line["lon"]), 1)
                centrePoint = myLat + "-" + myLon
                if(timeOfSighting == timePoint):
                        keyId = 1
                        inserted = 0
                        while(inserted == 0):
                                inserted = InsertIntoRightCell(finalCellDataList, centrePoint, keyId, timeOfSighting, species, count)
                                keyId += 1

if (len(sys.argv) > 4 or len(sys.argv) < 4):
        print("\n    Usage: GenerateList.py \"<path to looger file>\" \"<path to data sheet xls>\" \"<path to ebird file xls>\" \n\n")
        sys.exit(1)

# Read the logger file and generate continuous stream of GPS points for every minute from start time to end.
# One key assumption is that the last GPS point in logger is after the last recorded sighing!
input_file = csv.DictReader(open(sys.argv[1]))
prevRow = None
currentRow = {} 
timePoints = []
for row in input_file:
        timeDiff = 0
        dt = datetime.strptime(row["time"],"%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(second=0)
        dt = dt + timedelta(hours=5,minutes=30)
        if prevRow is not None:
                diff = dt - prevRow["time"]
                timeDiff = diff.total_seconds()/60
        if timeDiff > 1:
                incrementLat = (float(row["lat"]) - float(prevRow["lat"]))/timeDiff
                incrementLon = (float(row["lon"]) - float(prevRow["lon"]))/timeDiff
                for x in range (1, int(timeDiff) + 1):
                        newLat = "{0:.6f}".format(float(prevRow["lat"]) + (incrementLat))
                        newLon = "{0:.6f}".format(float(prevRow["lon"]) + (incrementLon))
                        newTime = prevRow["time"] + timedelta(minutes=1)
                        currentRow = {"time":newTime,"lat":newLat,"lon":newLon}
                        timePoints.append(currentRow)
                        prevRow = currentRow
        if timeDiff < 2:
                lat = "{0:.6f}".format(float(row["lat"]))
                lon = "{0:.6f}".format(float(row["lon"]))
                currentRow = {"time":dt,"lat":lat,"lon":lon}
                timePoints.append(currentRow)
                prevRow = currentRow

# Now we have the continuos GPS points. Now go throug it and separate into multiple cells
# Rules used to consider a unique cell
# - A cell is [0.1 x 0.1 degrees]
# - A cell is considered unique for a period of 3 hours.
# - If boat enters the same cell before 3 hours from the starting time in the cell, it is considered as the same list
# - if boat enters the cell after 3 hours from the starting time, it is considered as a new list, identified with same coordinates, but different preceding number
cellList = {}
tripDate = None
for line in timePoints:
        if tripDate is None:
                tripDate = line["time"]
        curKeyId = 1
        roundedLat = '%.1f' % round(float(line["lat"]), 1)
        roundedLon = '%.1f' % round(float(line["lon"]), 1)
        inserted = 0
        while(inserted < 1):
                inserted = AddCellDetails(roundedLat, roundedLon, float(line["lat"]), float(line["lon"]), curKeyId, line["time"], cellList)
                curKeyId += 1

# Now we have list of cells. Create the final data structure, which is a list of dictionaries.
# Currently, fill it with list properties. Later we will add the bird details
tempCellList = []
for entry in cellList:
        tempCellList.append(cellList[entry])
sortedCellList = sorted(tempCellList, key=lambda CellDetails: CellDetails.startTime)

finalCellDataList = []
for cell in sortedCellList:
        print(cell.key, cell.startTime, cell.endTime)
        entry = cell.key
        if (cellList[entry].startTime == cellList[entry].endTime):
                cellList[entry].endTime = cellList[entry].endTime + timedelta(minutes=1)
        cellData = {}
        cellData["Cell Details"] = entry
        cellData["Start Time"]  = cellList[entry].startTime
        cellData["End Time"]    = cellList[entry].endTime
        cellData["Distance"]    = cellList[entry].distance
        cellData["Duration"]    = cellList[entry].duration
        cellData["Lat"]         = cellList[entry].roundedLat
        cellData["Lon"]         = cellList[entry].roundedLon
        finalCellDataList.append(cellData)
        

# Now open the data sheet, find the species list, and for each species, find the right cell and insert the species details into that list
wb = open_workbook(sys.argv[2])
dataSheet = wb.sheet_by_name("Data")

state = dataSheet.cell(2,3).value
notes = "Pelagic Survey organised by "+dataSheet.cell(8,3).value+" from "+dataSheet.cell(0,3).value+"("+dataSheet.cell(1,3).value+")"+" Weather "+dataSheet.cell(6,3).value+".Photographs available with "+dataSheet.cell(11,3).value
allSpecies = dataSheet.cell(10,3).value
noObservers= dataSheet.cell(9,3).value

dataStarted = 0;
for row_index in range(dataSheet.nrows):
        if(dataStarted == 0):                
                if(dataSheet.cell(row_index,0).value == "Time"):
                        dataStarted = 1
        else:
                species = dataSheet.cell(row_index,1).value
                count = dataSheet.cell(row_index,2).value
                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(dataSheet.cell(row_index,0).value, wb.datemode)
                sightingTime = datetime.strptime(str(hour) + ":" + str(minute), "%H:%M")

                dt = tripDate
                dt = dt.replace(hour=sightingTime.hour,minute=sightingTime.minute)
                HandleSighting(dt, species, count, finalCellDataList, timePoints)

# Now we can proceed to generating the ebird list from the current details.

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

date_format = xlwt.XFStyle()
date_format.num_format_str = 'mm/dd/yyyy'

time_format = xlwt.XFStyle()
time_format.num_format_str = 'h:mm'

sheet1.write(1, 0, "Latitude")
sheet1.write(2, 0, "Longitude")
sheet1.write(3, 0, "Date of Observation")
sheet1.write(4, 0, "Start Time")
sheet1.write(5, 0, "State")
sheet1.write(6, 0, "Country")
sheet1.write(7, 0, "Protocol")
sheet1.write(8, 0, "Number of Observers")
sheet1.write(9, 0, "Duration(Minutes)")
sheet1.write(10,0, "Reporting All Species")
sheet1.write(11, 0, "Distance Travelled(Miles)")
sheet1.write(12, 0, "Area Covered")
sheet1.write(13,0, "Notes")

speciescnt=14
columncnt = 1
for row in finalCellDataList:
        td = row["End Time"]-row["Start Time"]
        # there are 7 fixed keys in every row - if there are no bird seen in that list, the count should be 7
        # such a list is decided to be discarded if effort is also less than 10 min
        if (len(row) == 7 and td.seconds < 600):
                continue
        else:
                columncnt += 1
                sheet1.write(0, columncnt, "Pelagic HotSpot: "+ row["Lat"] + "-" + row["Lon"])
                sheet1.write(1, columncnt, row["Lat"])
                sheet1.write(2, columncnt, row["Lon"])
                sheet1.write(3, columncnt, tripDate.strftime('%m/%d/%Y'))
                sheet1.write(4, columncnt, row["Start Time"].strftime('%H:%M'))
                sheet1.write(5, columncnt, state)
                sheet1.write(6, columncnt, "IN")
                if (row["Distance"] == 0):
                        sheet1.write(7, columncnt, "Stationary")
                else:
                        sheet1.write(7, columncnt, "Traveling")
                sheet1.write(8, columncnt, noObservers)
                sheet1.write(9, columncnt, row["Duration"])
                # Valid lists with duration < 10 minutes will have "All Species Reported" set to "No"
                if(td.seconds < 600):
                        sheet1.write(10, columncnt, "N")
                else:
                        sheet1.write(10, columncnt, allSpecies)
                sheet1.write(11, columncnt, row["Distance"] * 0.621371)
                sheet1.write(13, columncnt, notes)
                for key in row:
                    if  (key == "Cell Details"):
                        continue 
                    elif  (key == "Lat"):
                        continue 
                    elif  (key == "Lon"):
                        continue 
                    elif  (key == "Start Time"):
                        continue 
                    elif  (key == "End Time"):
                        continue 
                    elif  (key == "Distance"):
                        continue 
                    elif  (key == "Duration"):
                        continue 
                    else:
                        sheet1.write(speciescnt, columncnt, row[key])
                        sheet1.write(speciescnt, 0, key)
                        speciescnt += 1
        book.save("c:\\temp\\eBirdTemp.xls")
	# Saved the file in a temporary excel sheet. Open and convert to csv.
        tmpbook = xlrd.open_workbook("c:\\temp\\eBirdTemp.xls")
        sheet = tmpbook.sheet_by_index(0)
        ebird_csv_file = open(sys.argv[3], 'wb')
        wr = csv.writer(ebird_csv_file, quoting=csv.QUOTE_ALL)
        for rownum in range(sheet.nrows):
                wr.writerow(sheet.row_values(rownum))
        ebird_csv_file.close()
