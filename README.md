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
 
Summary of the logic:
 - Go through the GPS points and create a per minute GPS track (using extrapolation if required)
 - Iterate through the track and find out the grids that has been traversed during this trip
     - A grid is of size 0.1x0.1 degree size with centre as the corresponding x.y,a.b. Eg: A grid with name "Pelagic HotSpot: 11.9-75.3" is a grid of 0.1x0.1 degree with centre point as (lat 11.9, lon 75.3)
     - Also note other details of the grid like time of entry/time of exit, approx distance travelled in the grid etc
     - If a grid is re-entered, it is marked as a new grid entry
 - Once we have all the grids traversed ready, go through the data sheet, get each sighting, check the time and coordinate and add the entry into the appropriate grid entry
 - Now we have a list of Grid entries including the birds seen in that grid
 - Create corresponding lists considering the following additional constraints
     - Lists with duration < 10 species and has zero birds are dropped.
     - Lists with duration < 10 minutes and has atleast one bird will have "All Species Reported" set to "No"
     - Lists with duration < 10 minutes and has atleast one bird and distance = 0 will have Protocol = Stationary.
     - Lists with duration > 10 minutes and distance = 0 will have Protocol = Stationary.
     - Lists with duration > 10 minutes and distance > 0  will have Protocol = Traveling
     
The result is a csv file which can be directly imported into eBird.
