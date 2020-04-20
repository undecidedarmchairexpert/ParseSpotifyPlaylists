import time
import os
from collections import namedtuple
from datetime import date
from multiprocessing import Pool

from bs4 import BeautifulSoup
from selenium import webdriver


# Class to hold songs with proper naming for title, artists and album elements
class Song:
    def __init__(self, title="", artist="", album=""):
        self.title = title
        self.artist = artist
        self.album = album
        self.search = title + " " + artist

    # Create a method to generate a string containing the information of the song in a printable manner
    def get_song(self):
        return "Title: " + self.title + "\n" + "Artist: " + self.artist + "\n" + "Album: " + self.album + "\n" + "Search String:" + "\n" + self.title + " " + self.artist + "\n\n"

    # Create a method to generate a string containing the information about the song to easily search it
    def get_search(self):
        return self.search + "\n\n"


def get_playlist(listName, url):
    # Render page through Selenium and read innerHTML to variable
    browser = webdriver.Firefox(executable_path='geckodriver.exe',
                                service_log_path='nul')
    browser.get(url)
    time.sleep(5)
    innerHTML = browser.execute_script("return document.body.innerHTML")
    browser.quit()

    # Parse page with Beautiful Soup
    soup = BeautifulSoup(innerHTML, features="lxml")

    # Find the list element containing the playlist's songs
    tracklist_soup = soup.find_all("li", {"class": "tracklist-row"})

    # Create an empty list to store songs
    tracklist = []

    # Go through HTML list elements by tag and extract the song information looking their class with Beautiful Soup
    # Storying each object in our newly created list
    for tag in tracklist_soup:
        title = tag.find("div", {"class": "tracklist-name"}).text
        artist = tag.find("span", {"class": "TrackListRow__artists"}).text
        album = tag.find("span", {"class": "TrackListRow__album"}).text
        tracklist.append(Song(title, artist, album))

    fileName = listName + " - " + str(date.today()) + ".txt"
    songFile = open("Data/" + fileName, "w")

    fileName = listName + " - " + str(date.today()) + "_search" + ".txt"
    searchFile = open("Data/" + fileName, "w")

    # Write songs to a text file using the method i the class to create proper formatting
    for songs in tracklist:
        songFile.write(songs.get_song())
        searchFile.write(songs.get_search())


# Define main function as program in order to have required async main check
def program():
    if not os.path.isfile("./geckodriver.exe"):
        raise FileNotFoundError("This script requires Firefox & GeckoDriver to run. Please install Firefox and "
                                "download GeckoDriver into the same folder as the "
                                "script.\nhttps://github.com/mozilla/geckodriver/releases")
    # Open file consisting of url on one line and the name on following line
    # Split at new line in order to avoid readlines() leaving a trailing character
    toScrape = open("Data/toScrape.txt", 'r').read().split('\n')

    # Creating a list to store playlist tuples with Name and URL
    Playlist = namedtuple('Playlist', ['url', 'name'])
    playlists = []

    # Looping over file results to neatly store in the tuples list
    i = 0
    while (i < len(toScrape)):
        playlists.append(Playlist(toScrape[i], toScrape[(i + 1)]))
        i += 2

    # Creating a pool of 6 threads to call the get_playlist function 6 at a time
    pool = Pool(processes=12)

    # Loop over the playlist tuples list to scrape all playlists asynchronously using 6 threads
    for playlist in playlists:
        pool.apply_async(get_playlist, (playlist.name, playlist.url))

    # Wait for all threads to be finished and terminate
    pool.close()
    pool.join()


# Running async main check and then calling program
if __name__ == '__main__':
    program()