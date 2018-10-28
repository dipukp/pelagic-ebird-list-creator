Introduction
------------
Monitoring of pelagic birds from Indian coast was started in 2010 (Praveen 2013). The trips during the period 2010-2011 focused mainly on getting the logistics right, creating a species list, learning field identification and understanding the complexities of pelagic birding in general. During this time, a single list of bird species and the total number of birds sighted in a trip were maintained. These trips typically covered a distance of 50-150 km in a day and a single bird list for the complete trip results is a very coarse data, and may not be conducive for detailed analysis in the future. 

During 2012-2013, a more formal methodology was evolved based on Bailey(1968) to estimate the abundance of birds at various distances from the coast (Karuthedathu et al. 2012). This method relied on collecting the time and GPS location of each sighting along with the number of birds sighted and mapping these into distance bands. Analysis was done based on time slots spent in each distance bands. However, this soon met with exceptions for cases where the ship route was from one port to another following a constant distance from the coast. This made all sightings to fall in a single distance band thereby reducing its utility. In addition, analysis of this data was generally done using Microsoft Excel sheets and involved manual intervention. This added complexity that polarised the human resources who could carry out the analysis.  

Towards the beginning of 2014, eBird (www.eBird.org) started becoming popular in India as a tool to create birding lists and visualising trends of birds in space and time (Sullivan et al. 2014, Praveen & Quader 2015). The rapid uptake of eBird in the recent years has made it one of the biggest database of bird records in India (http://ebird.org/content/india/news/ebird-india-3-million/). Hence, instead of ad-hoc collection and analysis of pelagic trip data, it was decided that the pelagic bird lists shall also be entered in eBird enabling us to use the standard eBird visualisation to understand the spatio-temporal trends. This streamlines and simplifies both the data entry and analysis of pelagic data and makes it more similar to land birds. 

It must be mentioned that eBird also recommended a ‘Pelagic protocol’ that could be used in pelagic trips (http://help.ebird.org/customer/portal/articles/1375503-ebird-pelagic-protocol). It involves constant monitoring during the trip and creating appropriate lists based on changing scenarios in the trip like location, count period and movement of the boat. It also proposes ad-hoc eBird hotspots along well-known pelagic trails. However, dealing with an effort-intensive methodology and concepts like ad-hoc hot-spots may result in the same problem we initially faced. In other words, adoption of eBird pelagic protocol did not appear to be simple nor a step forward. Hence, we decided to devise our own protocol which is sufficiently complex and complete to cover all possible scenarios but still hide the complexity completely from the users through automation. 

eBird Concepts
--------------
Since the listing is heavily based on eBird, it is prudent that we explain some concepts of eBird for birders who are not used to this service. These concepts are used in the newly devised protocol and hence of relevance here.

Hotspot: Defined as any public area for birding. Hotspots enable clubbing data from multiple trips by multiple people to analyse data as clusters. See here for more details http://help.ebird.org/customer/portal/articles/1006824-what-is-an-ebird-hotspot

Complete Lists: eBird has a field which can indicate if all the species which a bird-watcher can identify were listed or not. If this question is answered in affirmative, then it is termed as a complete list. Complete lists are considered excellent for bird density analysis as it provides absence data in addition to presence. Please see below link for more details http://help.ebird.org/customer/portal/articles/1006361-are-you-reporting-all-species.

Stationary and Traveling Protocol: Every eBird list should select a protocol. As the name indicates, if the birder was stationary during the listing process, then stationary is correct protocol to select. If a birder was traveling in a path of any shape or direction, it falls under traveling protocol. There are other standard protocols in eBird which we do not use in our protocol and hence not covered here. Please visit below link for more details.  http://help.ebird.org/customer/portal/articles/974012-how-to-make-your-checklists-more-valuable

Principles & Protocol
---------------------
In the sea, a 10 km distance band was found reasonable for pelagic bird data analysis in India - distribution pattern does not change more drastically than that (compared to land based birding where the habitat change can be much drastic with such a distance band). Hence, the offshore/pelagic water can be divided into cells of 0.1 x 0.1 degree - roughly 11 km x 11 km. Every Lat/Long with a single decimal point can be considered as an eBird hotspot (e.g. 75.3, 12.1). All observations centered on such a cell of size 0.1 x 0.1 degree will go under that eBird hotspot.

With this definition in place, the following axioms were added  
<ul>
    <li>Each bird sighting can be uniquely assigned to a cell (hotspot) </li>
    <li>Each trip can be subdivided into multiple smaller lists based on cells where the boat was present </li>
    <li>Lists can be generated for each cell based on the following additional criteria that provides the right resolution for subdividing the time spent in each cell </li>
    <ul>
        <li> Lists with duration < 10 minutes and </li>  
        <ul>
            <li> has zero birds are dropped (i.e. no lists just for the sake of lists) </li>
            <li>has at least one bird </li>
            <ul>	
                <li>will have "All Species Reported" in eBird set to "No" (i.e. it is unlikely that you noticed all pelagic species in such a short duration) </li>  
                <li>and displacement < 0.1 km will have eBird Protocol = Stationary (i.e. boat was roughly stationary, say it was anchored)</li>
            </ul>
        </ul>
        <li>Lists with duration > 10 minutes and </li>
        <ul>
            <li>displacement < 0.1 km will have eBird Protocol = Stationary </li> 
            <li>displacement ≥ 0.1 km  will have eBird Protocol = Traveling </li>
        </ul>
        <li> A single list will have a max cutoff of 3 hours as time (Eg: if you stay in the same cell for a long duration, it will have multiple lists with each list maxing out at 3 hour) </li> 
        <li>If there are rough counts in the data sheet (e.g. 100 birds), the total number of birds in a given cell are adjusted to avoid "false precision" (See http://ebird.org/content/ebird/news/counting-201/) </li>
    </ul>
</ul>

Here is a worked out example showing how the lists can be created for a hypothetical trip using this protocol (Each list will contain the list of birds sighted during that duration)  
* Entered Cell/Hotspot 1 at 11:00 (few birds were seen)  
* Entered Cell/Hotspot 2 at 11:05   
* Entered Cell/Hotspot 1 again at 11:30  
* Entered Cell/Hotspot 3 at 12:30  
* Entered Cell/Hotspot 4 at 16:30  
* Entered Cell/Hotspot 5 at 17:30 (no birds seen)  
* Entered Cell/Hotspot 1 at 17:35, trip ends at 18:00  

Summary of generated lists (The actual hotspot naming will be based on the coordinates and the name of the sea/ocean):

Hotspot    Start Time    End Time    Duration(min)    Protocol      Complete List

List 1      1          11:00         11:04        5          Traveling     No

List 2      2          11:05         11:29        25         Traveling     Yes

List 3      1          11:30         12:29        60         Traveling     Yes

List 4      3          12:30         15:29        180        Traveling     Yes

List 5      3          15:30         16:29        60         Traveling     Yes

List 6      4          16:30         17:29        60         Traveling     Yes

List 7      1          17:35         18:00        25         Traveling     Yes


Protocol Execution
------------------
Certainly the protocol looks extremely complex on first look. However, all the complexity is subsumed in a freely downloadable python script (https://github.com/dipukp/pelagic-ebird-list-creator) which automatically generates these lists in a format that is supported by eBird for data uploads. Hence, the actual process of data recording and listing is much simpler for a pelagic birder. The steps are detailed as below.

Materials:
<ol>
    <li> A GPS enabled Android phone with GPSLogger software installed. This can be installed free from https://play.google.com/store/apps/details?id=com.mendhak.gpslogger&hl=en </li>
    <ol>
        <li> Configure GPSLogger to </li>
        <ol>
            <li> output GPS coordinates in .txt format </li>
            <li> set the interval of logging as “every 60 seconds” </li>
            <li> set the location source as Device GPS only (as the location from Wifi and Mobile towers may be coarse and will generate inaccurate locations)
        [The smartphone Location Services can also be configured to use only the device GPS as the sole provider, and not use the Wifi and Mobile towers] </li>
        </ol>
    </ol>
Note: Actually, the GPSLogger is not a mandatory requirement, but the actual requirement is a comma separated text file containing the following information in a specific format for each minute of the trip - Time of recording, Latitude and Longitude. The samples which show the actual format are present at https://github.com/dipukp/pelagic-ebird-list-creator. The GPSLogger software produces the output file in this format (with additional columns, which are not used by the script), hence it was selected as the tool for recording the coordinates.
    <li> A regular wrist watch with seconds precision </li>
    <li>Pencil/Pen and paper for data recording </li>
</ol>

Data Collection and Upload Process
<ol>
    <li> Switch On GPS logger at the start of the trip </li>
    <li> Align the timings of the wrist watch with the phone that has GPSLogger to the nearest minute & second. Also align (or take note of the difference in) the time between the cameras in the trip and the wrist watch for analysis and correlating images to the sightings </li>
    <li> For each bird sighting, record the </li>
    <ol>
        <li> Time of sighting </li>
        <li> Species and the number of individuals for each species </li>
    </ol>
    <li> After the trip, transfer this into an excel sheet in a predefined format as provided at https://github.com/dipukp/pelagic-ebird-list-creator </li>
    <li> Run the python script from https://github.com/dipukp/pelagic-ebird-list-creator giving the necessary inputs as documented in the above site </li>
    <li> The script automatically </li>
    <ol>
        <li> Identifies hotspots/cells based on GPS logger output </li>
        <li> Maps the time of bird sightings to the appropriate GPS location (based on actual or extrapolated GPS coordinates as appropriate, from GPS logger output) </li>
        <li> Uses the protocol principles, separates out the data into multiple ebird lists </li>
    </ol>
    <li> The script outputs these lists into an ebird-importable csv output file </li>
    <li> Import the data into eBird at http://ebird.org/ebird/import/upload.form?theme=ebird by selecting “eBird Checklist Format” </li>
</ol>

Uptake of this new methodology
------------------------------
Most pelagic birders have taken up this methodology in Kerala, Karnataka and Goa and have started uploading in eBird lists generated by the script. In Kerala, regular pelagic monitoring sponsored by the state forest department runs with this protocol. We were also able to convert older lists as the requirements for previous pelagic protocol remained the same - a kml file and a time-based species list. 

This methodology was also discussed with Marshall Iliff, eBIrd project leader, and his response was positive and agreed that this is indeed a step in positive direction. He specifically commented that  “This sounds like a very reasonable approach that addresses our main concerns that:  1) pelagic lists be broken into multiple lists, rather than one long day list; 2) species are associated with lat-longs that are roughly relevant to where they were seen; 3) it does not become so tedious as to not be fun anymore!” (Marshall Illiff in email dated 22 October 2014)

Realization and usage of script
-------------------------------
Python script to create ebird lists from pelagic data sheet and GPS Logger txt output files. The idea is to create separate lists based on .1x.1 degree grids with centre point as the (x.y,a.b) and add recorded birds into this.

Running of this script requires (curently tested versions in braces) 
 - Python (2.8)
 - compatible xlrd (xlrd-0.9.3) and xlwt (xlwt-0.7.5) packages (http://www.python-excel.org/)

Usage:
    GeneratePelagicEbirdLists.py [path to looger file] [path to data sheet xls] [path to ebird file xls]

Inputs
 - The data sheet in the specified format
 - The GPS points as expected in the sample file. The android application "GPS Logger" can generate the txt format that is exactly required by this script. If you are using some other tools to capture GPS points, that need to be converted into the expected format.
     - It is expected to take GPS coordinates at every 1 min interval, but if there are some gaps, script can take care of that using extrapolation!

Summary of the script logic:
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

Additional notes:
-----------------
- If you have a gpx file instead of a csv file (say from an external device like Garmin), this need to be converted to a simple csv file with 3 columns - time, lat and lon. There is a sample script here which converts a basic garmin GPX file into such csv file. If you have a different format of GPX file, then the script may need to be modified slightly.
- Using Python installer, a windows binary has also been created, which can be run on any new Windows machine. (This makes it easy for people to use the script/tool without explicitly installating python and other dependencies). 
 
 This package is available at 
     
          https://drive.google.com/open?id=0B7H2DYnIVIFkMzVHTHZoandtcWc

   Please feel free to use it to generate lists from Indian Coast. In case you plan to use it anwhere else in the world, the hotspot naming convention (and any other logic depending on GPS coordinates) will have to be tweaked as this has been tuned for Indian coast.
   
- The script currently generates the hotspot names considering the Indian coast only. 
- If the same has to be used in other places in the world, the hotspot naming logic has to be tweaked based on the geographical area by giving the appropriate sea/ocean names and the relevant coordinates. 
- Similarly, some of the configuration values used in the algorithm are fine-tuned for Indian conditions based on the previous surveys. These might need fine-tuning when porting the script to another region, where pelagic bird & birder densities are markedly different.
