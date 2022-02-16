
####				  	  	 	  ####
#					     			 #
#  	   Music Synchronizer V1.0	     #
#					     			 #
####				  	  		  ####

##
## This script backs up or synchronizes two directories of music
## Each directory should have an artist->album->song folder structure, and each will be checked for their string values
## Arguments given will be the function(backup, sync), source and destination directories
##
import sys
import cli_ui
import re
import math
from filecmp import dircmp
import os.path
#from shutil import copy, copytree
import shutil
import tkinter as tk
from tkinter import filedialog

def main():

	source = tk.Tk()
	source.withdraw()

	cli_ui.setup(title="Music Sync 1.1")

	cli_ui.info_section("Music Sync 1.1")



	options = ["Backup", "Synchronize"];
	fctn = cli_ui.ask_choice("Select a function", choices = options);

	# Select two guaranteed existing source directories
	print("Please select a source directory | back up from here");
	source = filedialog.askdirectory(title="--Select Source Directory--", mustexist = True)
	if(len(source) < 1): 
		print("Cancelling...");
		sys.exit();

	print("Please select a destination directory | back up to here");
	destination = filedialog.askdirectory(title="--Select Destination Directory--", mustexist = True)
	if(len(destination) < 1): 
		print("Cancelling...");
		sys.exit();

	if(fctn == options[0]):
		print("Back up from " + source + " ----> " + destination);
		sys.exit() if input("Y/N: ").lower() != "y" else backup(source, destination);
	if(fctn == options[1]):
		print("Synchronize " + source + " <---> " + destination);
		sys.exit() if input("Y/N: ").lower() != "y" else backup(source, destination);


# Backup from one directory to another, given two guaranteed existing directories in these steps:
# 1. Copy all artists only existing in source to directory
# 2. For all common artists, go one layer down
#	2a. Copy all albums existing only in source but not the destination
def backup(s, d):
	
	artists = 0;
	art_error = 0;
	albums = 0;
	alb_error = 0;
	files = 0;

	print("Staring Backup! Comparing Directories....")
	comp = dircmp(s,d); # Create the comparison object

	print("Found " + str(len(comp.common_dirs)) + " common artists\n")


	for left in comp.left_only: # Move all new artists over

		# Update working directory to os standard convention
		cl = re.sub(r"[\/\\]", str(os.sep + os.sep), str(comp.left))
		start = os.path.join(cl, left);

		cr = re.sub(r"[\/\\]", str(os.sep + os.sep), str(comp.right))
		end = os.path.join(cr, left)

		try:
			if(os.path.isdir(start)):
				shutil.copytree(start,end);
				artists = artists + 1;
			else:
				shutil.copy(start,end);
				files = files + 1;
		except:
			art_error = art_error + 1;
			print("Artist Error | " + left);

	for artist in comp.common_dirs:	# For all common artists, move new albums over
		
		# Compare artist directories for new albums
		comp_com = dircmp(os.path.join(comp.left,artist), os.path.join(comp.right,artist));

		for album in comp_com.left_only:

			# Update working directory to os standard convention
			ccl = re.sub(r"[\/\\]", str(os.sep + os.sep), str(comp_com.left))
			start = os.path.join(ccl, album);

			cr = re.sub(r"[\/\\]", str(os.sep + os.sep), str(comp_com.right))
			end = os.path.join(cr,album)

			try:

				if(os.path.isdir(start)):
					shutil.copytree(start,end);
					albums = albums + 1;
				else:
					shutil.copy(start,end);
					files = files + 1;

			except:
				alb_error = alb_error + 1;
				print("Album Error | " + album);
	
	resultTable(artists, art_error, albums, alb_error, files)


	anomalies = len(comp.funny_files);
	if(anomalies > 0):
		print(str(anomalies) + " Anomalies Found!")
		print("Listing...")
		for funny in comp.funny_files:
			print(funny);


#Synchronize two guaranteed existing directories
def synchronize(s, d):
	backup(s,d);
	backup(d,s);

def resultTable(artists, art_error, albums, alb_error, files):

	print()
	if artists + art_error == 0:
		are = 0.00
	else:
		# Artist error rate
		are = round(1-float(art_error/(artists+art_error)), 2) * 100

	if albums + alb_error == 0:
		ale = 0.00
	else:
		# Album error rate
		ale = round(1-float(alb_error/(albums+alb_error)), 2) * 100

	# Dictionary containing artist/album table
	# accuracy = {
	# artist: ["artist", str(artists+art_error), str(art_error), str(are) + "%"],
	# album: ["album", str(albums+alb_error), str(alb_error), str(ale) + "%"]
	# }
	accuracy = [
	["artist", str(artists+art_error), str(art_error), str(are) + "%"],
	["album", str(albums+alb_error), str(alb_error), str(ale) + "%"],
	["other", str(files), "N/A", "N/A"]
	]
	print("{:<8} {:<10} {:<10} {:<15}".format('Format', 'Total', 'Error','Accuracy'))
	for v in accuracy:
		form, total, error, acc = v
		print ("{:<8} {:<10} {:<10} {:<15}".format(form, total, error, acc))

def asciibox(text, symbol):

	padding = 3; # Space from end of longest word to border
	longest = text; # Find the longest line to base size from
	words = [];

	if "\n" in text: # If there are many lines, split to print all
		words = text.split("\n"); # Define an array either way to iterate through
		longest = max(words, key=len);
	else:
		words = [text];
	
	print(str(len(longest)) + " " + longest)

	length = len(longest) + (2 * padding); # An empty line will have this many spaces
	space = " ";

	sign = ((symbol * 5) + (space * (len(longest)-2)) + (symbol * 5) + "\n");
	sign += (symbol + (space * length) + symbol) + "\n";

	for line in words:
		#line_pad = math.floor(int((length-len(line))/2));

		pad_value = math.floor((length-len(line))/2); # Generalized pad value that may be subject to change
		pad_left = pad_value;
		pad_right = pad_value if len(longest)-len(line) <= 0 else pad_value + 1;
		
		#line_pad = length-len(line)>0?length-len(line)/2:;
		#math.floor(int((length-len(line))/2));

		#if line_pad % 2 != 0: line_pad = line_pad + 1; # Adjust for odd numbered lines
		sign += (symbol + (space*pad_left) + line + (space*pad_right) + symbol) + "\n";
		#sign += (symbol + (space*padding) + line + (space*padding) + symbol) + "\n";
	

	sign += (symbol + (space * length) + symbol) + "\n";
	sign += ((symbol * 5) + (space * (len(longest)-2)) + (symbol * 5)) + "\n";

	return sign;

	# Optional print from fctn code
	# print((symbol * 5) + (space * (len(text)-2)) + (symbol * 5))
	# print(symbol + (space * length) + symbol)
	# print(symbol + (space*3) + text + (space*3) + symbol)
	# print(symbol + (space * length) + symbol)
	# print((symbol * 5) + (space * (len(text)-2)) + (symbol * 5))

main();
