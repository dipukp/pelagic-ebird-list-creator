Problem Statement
-----------------
Pelagic trips cover a large distance in a days trip. A single bird list for the complete trip results in a very coarse data, and may not be conducive for detailed analysis in future. 

Concept
-------
Along our coast, a 10km distance band is found reasonable for pelagic birds - distribution pattern does not change more drastically than that. Hence, the coastal area can be divided into cells of 0.1 x 0.1 degree - roughly 11km x 11km. Every Lat/Long with a single decimal point is a hotspot (e.g. 75.3, 12.1). All observations centered on such a cell of size 11x11 will go into that hotspot.

With this concept in place, 
- each bird sighting can be assigned to a cell
- The complete trip can be subdivided into multiple smaller list based on cells
- eBird lists can be generated for each cell based on the following additional criteria
Point 1: Lists with duration < 10 species and has zero birds are dropped.
Point 2: Lists with duration < 10 minutes and has atleast one bird will have "All Species Reported" set to "No"
Point 3: Lists with duration < 10 minutes and has atleast one bird and distance = 0 will have Protocol = Stationary (boat was roughly stationaly, say during a lunch stop)
Point 4: Lists with duration > 10 minutes and distance = 0 will have Protocol = Stationary.
Point 5: Lists with duration > 10 minutes and distance >0  will have Protocol = Traveling
Point 6: A single lists will have a max cutoff of 3 hours as time (Eg: if you stay in the same 
Point 7: If there are rough counts in the data sheet, adjust total number in a given cell to avoid "false precision" issue (see http://ebird.org/content/ebird/news/counting-201/)

Eg:
- Enter Cell 1 at 10:00
- Enter Cell 2 at 11:00
- Enter Cell 1 again at 11:30
- Enter Cell 3 at 12:30
- Enter Cell 4 at 16:30
- Enter Cell 5 at 17:30 (no birds seen)
- Enter cell 1 at 17:35, trip ends at 18:00

Output will be:
List 1:  Name: Cell 1, Start Time: 10:00, Duration:   60 minutes
List 2:  Name: Cell 2, Start Time: 11:00, Duration:   30 minutes
List 3:  Name: Cell 1, Start Time: 11:30, Duration:   60 minutes
List 4:  Name: Cell 3, Start Time: 12:30, Duration:   180 minutes
List 5:  Name: Cell 3, Start Time: 15:30, Duration:   60 minutes
List 6:  Name: Cell 4, Start Time: 16:30, Duration:   60 minutes
List 7:  Name: Cell 1, Start Time: 17:30, Duration:   25 minutes

##########################################################################
Currently proposed Solution
---------------------------
1. Take the GPS output in a specific format during the trip (Curerntly GPSLogger app on Android phones is used which can output the points in csv format, this formate is used as it is today)
2. For each bird sighting, record the time of sighting species and the number of individuals for each species
(The above xls should be in the predefined format)
3. Run a python script giving the GPS logger output and the data xls file.
4. The script automatically
- identifies hotspots/cells based on GPS logger output
- maps the time of bird sightings to the appropriate GPS location (based on actual or extrapolated GPS coordinates as appropriate, from GPS logger ouput) 
- based on criteria mentioned above, separates out the data into multiple ebird lists and create the ebird-importable csv output file (checklist format).
5. Import the data into eBird (if there are errors in bird names/time format etc., correct and try upload again)

##########################################################################
Realization
-----------

# pelagic-ebird-list-creator
Python script to create ebird lists from pelagic data sheet and GPS Logger txt output files. The idea is to create separate lists based on .1x.1 degree grids with centre point as the (x.y,a.b) and add recorded birds into this.

Running of this script requires (curently tested versions in braces) 
 - Python (2.8)
 - compatible xlrd (xlrd-0.9.3) and xlwt (xlwt-0.7.5) packages (http://www.python-excel.org/)

Usage:
    GeneratePelagicEbirdLists.py <path to looger file> <path to data sheet xls> <path to ebird file xls>

Inputs
 - The data sheet in the specified format
 - The GPS points as expected in the sample file. The android application "GPS Logger" can generate the txt format that is exactly required by this script. If you are using some other tools to capture GPS points, that need to be converted into the expected format.
     - It is expected to take GPS coordinates at every 1 min interval, but if there are some gaps, script can take care of that using extrapolation!

##########################################################################
Summary of the logic:
---------------------
 - Go through the GPS points and create a per minute GPS track
     - use simple linear extrapolation if a reading is not available for a particular minute
     - use only those readings which are between the start and end time
 - Iterate through the track and find out the grids that has been traversed during this trip
     - A grid is of size 0.1x0.1 degree size with centre as the corresponding x.y,a.b. Eg: A grid with name "Pelagic HotSpot: 11.9-75.3" is a grid of 0.1x0.1 degree with centre point as (lat 11.9, lon 75.3)
     - Also note other details of the grid like time of entry/time of exit, approx distance travelled in the grid etc
     - If a grid is re-entered, it is marked as a new grid entry
 - Once we have all the grids traversed ready, go through the data sheet, get each sighting, check the time and coordinate and add the entry into the appropriate grid entry
 - Now we have a list of Grid entries including the birds seen in that grid
 - Create corresponding lists considering the constraints mentioned in the "Concept" section above
 - Name hotspots using a standard covention, separating broadly into 3 categories - Arabian Sea, Bay Of Bengal and Indian Ocean
 - Write the results into a csv file which can be directly imported into eBird.

##########################################################################
Additional notes:
 - Using Python installer, a windows binary has also been created, which can be run on any new Windows machine. (This make it easy for people to use this without explicitly installating python and other dependencies. This package is available at 
     
          https://drive.google.com/open?id=0B7H2DYnIVIFkMzVHTHZoandtcWc

   Please feel free to use it to generate lists from Indian Coast. In case you plan to use it anwhere else in the world, the hotspot naming convention (and any other logic depending on GPS coordinates) will have to be tweaked as this has been tuned for Indian coast.
