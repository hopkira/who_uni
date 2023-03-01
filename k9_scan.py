import os
import shutil
 
# Get current working directory
cwd = os.getcwd()
 
# Create a counter to be used when copying files
k9_file_index = 1
 
# Loop through each file in the directory
for filename in os.listdir(cwd):
 
    # If the file ends in .txt
    if filename.endswith(".txt"):
 
        # Open the file
        with open(filename, 'r') as f:
            # Read the contents of the file
            contents = f.read()
 
            # If the word 'K9' is in the file
            if 'K9' in contents:
                # Create the new filename
                new_filename = 'k9_' + str(k9_file_index).zfill(3) + '.txt'
 
                # Increment the counter
                k9_file_index += 1
 
                # Copy the file
                shutil.copy(filename, new_filename)