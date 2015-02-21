mlbscoremap
===========

Filterable heat map of Major League Baseball scores written in Python

To test the script you can download the text file from http://www.retrosheet.org/gamelogs/gl2013.zip and unzip
Currently mlbscoremap.py will output a PDF file of the heatmap

Module Requirements
--------------------
* matplotlib
* numpy

Future considerations
----------------------
* Grab data straight from the web and unzip
* Filter scores by individual teams or leagues
* Add other categories as filterable (there are 170-ish total)
* Plot cells will have tooltips showing number of occurences of that score combination
