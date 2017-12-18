import sys
import csv
from datetime import datetime, timedelta, time, date
import operator
import xlrd
import xlwt
from xlrd import open_workbook,cellname,xldate_as_tuple
from math import radians, cos, sin, asin, sqrt, floor

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
        on the earth (specified in decimal degrees). Return the result in kilometers
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
                        distance = GetDistance(origLat, origLon, cellList[myKey].origLat, cellList[myKey].origLon)
                        if distance > 5.0:
                                print("Looks like between 2 GPS readings [ " + cellList[myKey].origLat + "," + cellList[myKey].origLon +
                                      "  - " + origLat + "," + origLon + " :  " + str(myTime) + " ], more than 5km displacement is being shown. \n")
                                print("This tool considers this as an error (as pelagics are expected to be slow :) and hence aborting the processing. " +
                                      " Please check the GPS file for correctness, remove suspicious points and re-run the tool again. \n" +
                                      "In case you feel that this is a genuine case, contact the tool authors!\n");
                                sys.exit(1)                                
                        cellList[myKey].distance += distance
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
                print("Looks like some problem!!!! Key data : " + str(centrePoint) + "," + str(keyId) +
                      ", " + str(species) + ", " + str(count) + ", " + str(timeofSighting) + "\n")
                return 1
        myKey = "[" + centrePoint + ":" + str(keyId) + "]"
        for row in finalCellDataList:
                if(row["Cell Details"] == myKey):
                        if(timeofSighting >= row["Start Time"] and timeofSighting <= row["End Time"]):
                                if species in row:
                                        if not isinstance(count,(int,long)):
                                                row[species] = count
                                                row[species + "-RF"] = 0
                                        else:
                                                row[species] += count
                                                currentRF = row[species + "-RF"] 
                                                if(count > currentRF):
                                                        row[species + "-RF"] = GetRoundingFactor(count,currentRF)
                                else:
                                        #print (myKey + " --> " + str(timeofSighting) + ", " + str(row["Start Time"]) +
                                        #       ", " + str(row["End Time"]) + ", " + str(species) + ", " + str(count))
                                        row[species] = count
                                        row[species + "-RF"] = GetRoundingFactor(count,0)
                                return 1        
        return 0

def GetRoundingFactor(count, currentRF):
        #Check for rough estimates in order of 10,50,100,500,1000,5000
        #Find the highest applicable rouding Factor
        if not isinstance(count,(int,long)):
                return 0
        possibleRF = 0
        for f in [10,50,100,500,1000,5000,1000000]:
                if(count%f == 0):
                     possibleRF = f
        if(possibleRF > currentRF):
                #print("Identified a rough estimate in cell " + myKey + ": Updating estimation scale for " + str(species) + " in this cell as " + str(possibleRF))
                return possibleRF
        return currentRF

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
        print("\nUsage:\n\tGenerateList \"<path to loger file>\" \"<path to data sheet xls>\" \"<path of the output file - csv>\" \n")
        print("Sample:\n\tGenerateList 24-Sep-2011_Trip1-GPS.txt Datasheet_Trip1-24-Sep-2011.xls 2011-09-24-Trip1-ebird-lists.csv \n")
        print("\tIf you got this file as part of zip file form google drive, try reading the Readme.docx file in the same file to get more detailed instructions\n")
        sys.exit(1)

# Start Processing
print ("---------------------------------------------------------------")
print "NOTES: "
print "1. If the Datasheet contains both X and numbers for a given species, "
print "   tne results may be wrong for that species. This case is not handled by the script."
print "   Please ensure that the Datasheet either use only numbers or only X for a given species"
print "2. Ensure Datasheet is similar the included samples. It needs to have a sheet named Data"
print "3. Common mistakes in Datasheet are the time and date formats. Please follow the same"
print "   conventions as followed in the sample"
print "4. All the rows in the Datasheet needs to have a time value. If 2 rows have the same time,"
print "   copy the same value to both rows"
print "5. GPS file can have more columns than in the samples. The only mandatory columns are "
print "   the first 3 - time, lat, lon"
print "\n---------------------------------------------------------------"

# Open the data sheet, get start time and end time
wb = open_workbook(sys.argv[2])
dataSheet = wb.sheet_by_name("Data")
dataStartTime = time(*xlrd.xldate_as_tuple(dataSheet.cell(4,3).value, wb.datemode)[3:])
dataEndTime = time(*xlrd.xldate_as_tuple(dataSheet.cell(5,3).value, wb.datemode)[3:])
print ("Trip Start Time  : " + str(dataStartTime))
print ("Trip End Time    : " + str(dataEndTime))
print "---------------------------------------------------------------"
# Read the logger file and generate continuous stream of GPS points for every minute from start time to end.
# One key assumption is that the last GPS point in logger is after the last recorded sighing!

input_file = csv.DictReader(open(sys.argv[1], "rU")) # The 'rU' option will load files with unicode format strings without giving error on csv object.
prevRow = None
currentRow = {} 
timePoints = []
estimateDetected = 0
for row in input_file:
        timeDiff = 0
        time_key = filter((lambda x: "time" in x), row.keys())[0] # Fetching the the 'time' key with unicode escape characters. E.g.: '\xef\xbb\xbftime'
        dt = datetime.strptime(row[time_key],"%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(second=0)
        dt = dt + timedelta(hours=5,minutes=30)
        tripStartTime = datetime.combine(dt.date(), dataStartTime)
        tripEndTime = datetime.combine(dt.date(), dataEndTime)
        #print (dt, tripStartTime, tripEndTime)
        if dt < tripStartTime or dt > tripEndTime:
                # print ("Got a time stamp which is out of range")
                continue
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

# Now we have the continuos GPS points. Now go through it and separate into multiple cells
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
roundingFactorList = {}
print("List candidates are:\n")
for cell in sortedCellList:
        print(str(cell.key) + " -->     Start: " + str(cell.startTime) + "     End: " + str(cell.endTime))
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

print ("---------------------------------------------------------------")        
print ("Processing of Data Sheet started ...")

# Now get details from datashee, read the species list, and for each species, find the right cell and insert the species details into that list
state = dataSheet.cell(2,3).value
notes = "Pelagic Survey organised by "+dataSheet.cell(8,3).value+" from "+dataSheet.cell(0,3).value+"("+dataSheet.cell(1,3).value+")"+" Weather "+dataSheet.cell(6,3).value+".Photographs available with "+dataSheet.cell(11,3).value
allSpecies = dataSheet.cell(10,3).value
noObservers= str(dataSheet.cell(9,3).value).rstrip('0').rstrip('.')

dataStarted = 0;
for row_index in range(dataSheet.nrows):
        if(dataStarted == 0):                
                if(dataSheet.cell(row_index,0).value == "Time"):
                        dataStarted = 1
        else:
                species = dataSheet.cell(row_index,1).value.upper()
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
        # There are 7 fixed keys in every row - if there are no bird seen in that list, the count should be 7
        # such a list is decided to be discarded if effort is also less than 10 min
        if (len(row) == 7 and td.seconds < 600):
                continue
        else:
                columncnt += 1
                # Hotspot sea/ocean selection for Indian Coast
                # Bay Of Bengal	>78.92  >9.27
                # Arabian Sea	<77.55	>8.07
                # Else default to Indian Ocean (which should anyway be valid in Indina context
                if (float(row["Lon"]) > 78.92 and float(row["Lat"]) > 9.27):
                        sheet1.write(0, columncnt, "Bay Of Bengal: "+ row["Lat"] + "N " + row["Lon"] + "E")
                elif (float(row["Lon"]) < 77.55 and float(row["Lat"]) > 8.07):
                        sheet1.write(0, columncnt, "Arabian Sea: "+ row["Lat"] + "N " + row["Lon"] + "E")
                else:
                        sheet1.write(0, columncnt, "Indian Ocean: "+ row["Lat"] + "N " + row["Lon"] + "E")
                
                sheet1.write(1, columncnt, row["Lat"])
                sheet1.write(2, columncnt, row["Lon"])
                sheet1.write(3, columncnt, tripDate.strftime('%m/%d/%Y'))
                sheet1.write(4, columncnt, row["Start Time"].strftime('%H:%M'))
                sheet1.write(5, columncnt, state)
                sheet1.write(6, columncnt, "IN")
                if (float(row["Distance"]) < 0.1):
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
                    elif ("-RF" in key):
                        #skipping Rounding Factor
                        continue 
                    else:
                        # Apply Rounding Factor
                        rFactor = row[key + "-RF"]
                        finalValue = row[key]
                        if (rFactor > 0):
                                #print(key + " - " + str(row[key]) + ", RF=  " + str(roundingFactor))
                                finalValue = (int(row[key]/rFactor)*rFactor)
                                print(" --> Identified a rough estimate in the range " + str(rFactor) + "s for the species " + 
                                      key + " in cell " + row["Lat"] + "-" + row["Lon"] + "#" + row["Start Time"].strftime('%H:%M') +
                                      ". Final count adjusted from " + str(int(row[key])) + " to " + str(finalValue) +
                                      " accordingly... Please take note!")
                                estimateDetected = 1
                        sheet1.write(speciescnt, columncnt, str(finalValue).rstrip('0').rstrip('.'))
                        sheet1.write(speciescnt, 0, key)
                        speciescnt += 1
        book.save("c:\\temp\\eBirdTemp.xls")
	# Saved the file in a temporary excel sheet. Open and convert to csv.
        tmpbook = xlrd.open_workbook("c:\\temp\\eBirdTemp.xls")
        sheet = tmpbook.sheet_by_index(0)
        ebird_csv_file = open(sys.argv[3], 'wb')
        wr = csv.writer(ebird_csv_file) #, quoting=csv.QUOTE_ALL)
        for rownum in range(sheet.nrows):
                wr.writerow(sheet.row_values(rownum))
        ebird_csv_file.close()
        
print "\n... Processing of Data sheet completed !!!"
print ("---------------------------------------------------------------")
if(estimateDetected == 1):
        print "\n    IMPORTANT NOTE !!! "
        print ("    ------------------\nNote the messages above indicating identification of rough estimate, " +
               "read \"False Precision\" section at http://ebird.org/content/ebird/news/counting-201/ for details.")
        print ("\nThis is detected when the number of birds entered during a particular sighting falls exactly " +
               "as a multipe of 10, 50, 100, 500, 1000 or 5000. If this is detected, then the count for that species " +
               "in that cell would be updated to an estimated value to avoid False Precision. \n\nIf the original number " +
               "was not a rough estimate, but actual, exact number, please update the resultant csv file manually!!!")
        print ("\n---------------------------------------------------------------")
print ("Generated the CSV file '%s' that can be now imported to eBird." % (sys.argv[3]))
print ("Please check the contents of the file for correctness before importing.")
print ("---------------------------------------------------------------")
