
####				  	  ####
#						 	 #
#  Music Synchronizer V1.0   #
#						 	 #
####				  	  ####

##
## This script backs up or synchronizes two directories of music
## Each directory should have an artist->album->song folder structure, and each will be checked for their string values
## Arguments given will be the function(backup, sync), source and destination directories
##
import sys
import cli_ui
import math
from filecmp import dircmp
import os.path
from shutil import copytree
import tkinter as tk
from tkinter import filedialog

def main():

	source = tk.Tk()
	source.withdraw()

	cli_ui.setup(title="Music_Sync_V1.0")

	cli_ui.info(asciibox("Music Sync V1.0", "#"))

	cli_ui.info_section("Music_Sync_V1.0")

	print(asciibox("abcdefgkjhf\nkjlashdfjk", "9"))

	options = ["Backup", "Synchronize"];
	fctn = cli_ui.ask_choice(["Select a function"], choices = options);
	print(fctn)

	# asciibox("Music Synchronizer V1.0", "#")
	# asciibox("aaaaaaaaaa", "a")
	# asciibox("ferrets r cool", "/")

	# # Select two guaranteed existing source directories
	# print("Please select a source directory | back up from here");
	# source = filedialog.askdirectory(title="--Select Source Directory--", mustexist = True)
	# if(len(source) < 1): 
	# 	print("Cancelling...");
	# 	sys.exit();

	# print("Please select a destination directory | back up to here");
	# destination = filedialog.askdirectory(title="--Select Destination Directory--", mustexist = True)
	# if(len(destination) < 1): 
	# 	print("Cancelling...");
	# 	sys.exit();

	# print("Back up from " + source + " ----> " + destination);
	# sys.exit() if input("Y/N: ").lower() != "y" else backup(source, destination);
	
	

	#dir1 = "E:\\Music";
	#dir2 = "C:\\Users\\Luna\\Music";
	#comp = dircmp(dir1,dir2); # Create the comparison object
	#for a in comp.left_only:
	#	print(os.path.join(comp.left,a))

# Backup from one directory to another, given two guaranteed existing directories in these steps:
# 1. Copy all artists only existing in source to directory
# 2. For all common artists, go one layer down
#	2a. Copy all albums existing only in source but not the destination

def backup(s, d):
	
	artists = 0;
	art_error = 0;
	albums = 0;
	alb_error = 0;

	print("Staring Backup! Comparing Directories....")
	comp = dircmp(s,d); # Create the comparison object

	print("Found " + len(comp.common_dirs) + " common artists\n")
	print("Backing up " + len(comp.left_only) + " artists...\n")

	for left in comp.left_only: # Move all new artists over

		try:
			shutil.copytree(os.path.join(comp.left,left), comp.right);
			artists = artists + 1;
		except:
			art_error = art_error + 1;
			print("Artist Error | " + left);

	for artist in comp.common_dirs:	# For all common artists, move new albums over

		# Compare artist directories for new albums
		comp_com = dircmp(os.path.join(comp.left,artist), os.path.join(comp.right,artist));

		for album in comp_com.left_only:
			l_path = os.path.join(comp_com.left, album);
			try:
				shutil.copytree(l_path, comp_com.right);
				albums = albums + 1;
			except:
				alb_error = alb_error + 1;
				print("Album Error | " + album);
		
	accuracy = {
	artist: [artist, art_error, round(float(art_error/(artist+art_error)), 2) + "%"],
	album: [albums, alb_error, round(float(alb_error/(albums+alb_error)), 2) + "%"]
	}
	print("{:<8} {:<15} {:<10} {:<10}".format('Format', 'Success','Error','Accuracy'))
	for k, v in accuracy.items():
		form, success, error, acc = v
		print ("{:<8} {:<15} {:<10} {:<10}".format(form, success, error, acc))


	print(len(comp.funny_files) + " Anomalies Found! Listing...")
	for funny in comp.funny_files:
		print(funny)


# Synchronize two guaranteed existing directories
#def synchronize(s, d):

def asciibox(text, symbol):

	padding = 3; # Space from end of longest word to border
	longest = text; # Find the longest line to base size from
	words = [];

	if "\n" in text: # If there are many lines, split to print all
		words = text.split("\n"); # Define an array either way to iterate through
		longest = max(words, key=len);
	else:
		words = [text];
	

	length = len(longest) + (2 * padding); # An empty line will have this many spaces
	space = " ";

	sign = ((symbol * 5) + (space * (len(longest)-2)) + (symbol * 5) + "\n");
	sign += (symbol + (space * length) + symbol) + "\n";

	for line in words:
		line_pad = math.floor(int((length-len(line))/2));
		#if line_pad % 2 != 0: line_pad = line_pad + 1; # Adjust for odd numbered lines
		sign += (symbol + (space*line_pad) + line + (space*line_pad) + symbol) + "\n";
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