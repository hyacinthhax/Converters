import os
import sys
import time


y_list = ["yes", "y", "ya", ""]
files_remove = input("Would you like to remove the files?  \n>")
input_dir = input("Enter the Path to MP3's... \n>")
output_dir = input("Enter the Output Path... \n>")
mp3_files = [x for x in os.listdir(input_dir) if x.split(".")[1] == "mp3"]

for files in mp3_files:
	file = files.split("/")[-1]
	flag = 0
	if input_dir.split()[-1] == "/":
		files = input_dir + files
	elif input_dir.split()[-1] != "/":
		files = input_dir + "/" + files

	if file[-4:] == ".wav":
		os.remove(files)

	base_name = file.split(".")[0]
	if output_dir.split()[-1] == "/":
		wav_file = output_dir + base_name + ".wav"
	elif output_dir.split()[-1] != "/":
		wav_file = output_dir + "/" + base_name + ".wav"

	if os.path.exists(wav_file):
		pass

	else:
		ffmpeg_command = f"ffmpeg -y -i {files} {wav_file}"
		print(f"Converting: {files} --> {wav_file}")
		os.system(ffmpeg_command)
		time.sleep(10)
		if files_remove in y_list:
			print(f"Removing Original: {files}")
			os.remove(files)

print(f"All conversions completed...  ")