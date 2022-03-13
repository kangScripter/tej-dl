import os
import json
import subprocess
import argparse
import sys

print("Tej Widevine Downloader")
print("V 0.0.1")

arguments = argparse.ArgumentParser()
arguments.add_argument("-l", "--mpd", dest="mpd", help="mpd link")
arguments.add_argument("-k","--key", dest="key",  help="key")
arguments.add_argument("-o", "--output", dest="output", help="File Name")

args = arguments.parse_args()

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)

ytdlp = dirPath + '/bin/yt-dlp.exe'
aria2c = dirPath + '/bin/aria2c.exe'
mp4decrypt = dirPath + '/bin/mp4decrypt.exe'
mkvmerge = dirPath + '/bin/mkvmerge.exe'

output = str(args.output)

mpd = str(args.mpd)
KEY = str(args.key)
 


print("\n Downloading..")
subprocess.run([ytdlp, '-k', '--allow-unplayable-formats', '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', '--no-check-certificate', '-F', mpd])
video_id = input("Input Video ID : ")
audio_id = input("Input Audio ID : ")
subprocess.run([ytdlp, '-k', '--allow-unplayable-formats','--no-check-certificate', '-f', audio_id, '--fixup', 'never', mpd, '-o', 'Encrypted.Audio.m4a', '--external-downloader', aria2c, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
subprocess.run([ytdlp, '-k', '--allow-unplayable-formats', '--no-check-certificate', '-f', video_id, '--fixup', 'never', mpd, '-o', 'Encrypted.Video.mp4', '--external-downloader', aria2c, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
  
print("\n\n")  
print("\n\nDecrypt Video & Audio...")
print("\nDone..")

subprocess.run(f'{mp4decrypt} --key {KEY} --show-progress Encrypted.Audio.m4a Decrypted.Audio.m4a')
subprocess.run(f'{mp4decrypt} --key {KEY} --show-progress Encrypted.Video.mp4 Decrypted.Video.mp4')
print()
print("\n Merging..")

subprocess.run([mkvmerge, '--ui-language' ,'en', '--output', output +'.mkv', '--language', '0:und', '--default-track', '0:yes', '--compression', '0:none', 'Decrypted.Video.mp4', '--language', '0:und', '--default-track', '0:yes', '--compression' ,'0:none', 'Decrypted.Audio.m4a','--language', '0:id'])

print("\n Cleaning...")
os.remove("Decrypted.Video.mp4")
os.remove("Decrypted.Audio.m4a")
os.remove("Encrypted.Video.mp4")
os.remove("Encrypted.Audio.m4a")






