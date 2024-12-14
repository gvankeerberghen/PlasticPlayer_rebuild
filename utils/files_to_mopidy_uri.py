import os
import urllib.parse

FOLDER = '/Users/guillaume/Desktop/musique_gus/20241214/'
OUTPUT_FILE_NAME = 'uris.txt'
OUTPUT_FILE = FOLDER + OUTPUT_FILE_NAME

def encode_file_paths(input_folder = FOLDER, output_file = OUTPUT_FILE):
    try:
        with open(output_file, 'w') as output:
            for root, dirs, files in os.walk(input_folder):
                for file in files:
                  print(f"Found file: {file}")
                  if file is not OUTPUT_FILE_NAME:
                      encoded_path = urllib.parse.quote(file)
                      output.write('local:track:' + encoded_path + '\n')
    except Exception as e:
        print(f"An error occurred: {e}")

encode_file_paths()
