# Parse Spotify Playlists

Script allowing to render the web page for Spotify playlists and grab the tracklist.

This is not dependent on the Spotify API as it renders the web pages out in a browser and grabs the information form the page source.

***NOTE: This was made to get comfortable with Python and as an example to using Beautiful Soup and should not be actively used.***

## Usage

To use the script, make sure Gecko driver is in the same folder as the script.

Create a new folder called `Data` in the script folder. This should contain a text file called `toScrape.txt` which will be a list of the playlists to scrape.
The list should be the URL for the playlist on one line followed by the name you want to assign on the following line. There should be no whitespace between playlists.

The script will create two files for each playlist. Both files are dated with today's date in order to avoid the script overwriting past files.
The first, standard, file will contain listings for the song title, artist and album which will be all labeled.
The second, postfixed `_search` contains a string which allows for easily searching the song online.

## Prerequisites

This script utilises selenium and is made to work with Mozilla's webdriver (Gecklo/Firefox). Therefore, this requires downloading `geckodriver.exe` into the same folder as the Python script.