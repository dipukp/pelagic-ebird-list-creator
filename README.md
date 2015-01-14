# pelagic-ebird-list-creator
Python script to create ebird lists from pelagic data sheet and GPS Logger txt output files. The idea is to create separate lists based on .1x.1 degree grids with centre point as the (x.y,a.b) and add recorded birds into this.

Running of this script requires (curently tested versions in braces) 
 - Python (2.8)
 - compatible xlrd (xlrd-0.9.3) and xlwt (xlwt-0.7.5) packages (http://www.python-excel.org/)
