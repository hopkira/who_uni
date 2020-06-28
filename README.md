# Doctor Who Universe - a backstory for K9

A basic set of tools to create a set of files to upload to IBM Watson - and a simple Cloud Function to interrogate the result.

## Step 1 - Download Wikipedia Pages as XML
Download the relevant pages in XML format from [Wikipedia Export Page](Wikipedia,https://en.wikipedia.org/wiki/Special:Export).  I used the Categories of ‘First doctor serials’ and ‘Ninth doctor episodes’ onwards to generate a list of all Doctor Who stories by page (I had to manually delete the series headers).  I could then export all the stories as XML.

## Step 2 - Distill XML pages into MediaWiki Story extracts
The resulting XML file includes all sorts of details about the stories, but I only want the functional plot. As a result I needed to process the resulting downloaded XML file and using the **process_wiki.py** program and direct its output to a new file called *clean.mw*.  This will create a new mediawiki format file with just the Plot or Synopsis elements.

## Step 3 - Split each Story into a separate text file
Process the resulting *clean.mw* mediawiki file into a sequence of story.txt files using the split_files.py program.

## Step 4 - Convert the text files into UTF-8 PDFs
Use the **word2pdf.py** file to convert these 'latin-1' plain text story files into equivalent 'utf-8' PDF files.

## Step 5 - Upload training set to Knowledge Studio and create dictionaries
I then uploaded a subset of the files (14 of them) to create a document set in the Watson Knowledge Studio.  There I also created a number of Entities based on Wikipedia pages, including Villains, Henchmen, Assistants, Monsters and Robots.

## Step 6 - Create Ground Truth and train machine learning model
I then manually marked up all of the 14 uploaded Doctor Who stories that include K9.  This subset created the Ground Truth for training and testing purposes.  I then used these documents to create a model that can be used to understall *all* the Doctor Who stories.

## Step 7 - Load all stories and model into Watson Discovery
The resulting model and all of the Story files are then loaded into Watson Discovery.  The custom model is incorporated as an enrichment for Entity Extraction and Relation Extraction.  The stories can now be queried using the Discovery APIs

## Step 8 - Query Discovery using a KNative Cloud Function
To make the stories easily accessible to my robots, I created a Python Cloud Function **discovery.py**.
This Function is created in a virtualenv Python environment and then zipped up with its dependencies and uploaded to IBM Cloud.  The basic function will take a search string and return the closest matching passage in the closest matching story.  The response also includes the entities and relationships that the machine learning model extracted from that story.
Further Cloud Functions will massage the returned data into a set of phrases for the robot to speak.

## Step 9 - Incorporate Cloud Function into Watson Assistant
To complete the capability, when someone asks the robot to tell a story or explain a Doctor Who term, a 'story' Intent is triggered in Watson Assistant and the Cloud Function is triggered.