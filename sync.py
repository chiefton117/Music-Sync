
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
from filecmp import dircmp
import os.path
from shutil import copytree
import tkinter as tk
from tkinter import filedialog

def main():

	source = tk.Tk()
	source.withdraw()

	# Select two guaranteed existing source directories
	print("Please select a source directory | back up from here");
	source = filedialog.askdirectory(title="--Select Source Directory--", mustexist = True)

	print("Please select a destination directory | back up to here");
	destination = filedialog.askdirectory(title="--Select Destination Directory--", mustexist = True)

	print("Back up from " + source + " ----> " + destination);
	return None if tolower(input("Y/N")) != "y";

	#source = input("")
	dir1 = "E:\\Music";
	dir2 = "C:\\Users\\Luna\\Music";
	comp = dircmp(dir1,dir2); # Create the comparison object
	for a in comp.left_only:
		print(os.path.join(comp.left,a))

# Converts your music to a logical artist->album->song structure, given the metadata of songs in your directories
# For each artist, recursively find subdirectories until we hit a file
#def cleanStructure():



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

main();