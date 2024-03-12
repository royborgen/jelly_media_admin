#!/usr/bin/python3
import requests
import json
import sys
import os
import re
import rarfile

def query_imdb_api(movie_id):
    url = "https://graph.imdbapi.dev/v1"
    query = {
        "query": """
        {
          title(id: "%s") {
            id
        primary_title
            type
            start_year
           # plot
            genres
           # rating {
           #   aggregate_rating
           #   votes_count
           # }
          }
        }
        """ % movie_id
    }

    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=query, headers=headers)
        if response.status_code == 200:
            return response.json()  # Successfully got response, return as JSON
        else:
            # API did not return a successful response
            return {"error": f"API returned non-200 status code: {response.status_code}", "data": None}
    except requests.exceptions.RequestException as e:
        # Handle exceptions raised by the requests library
        return {"error": f"Request failed: {e}", "data": None}

def checkfolder(folder_path):

    season_pattern = re.compile(r'(?:^|\D)(?:s|season)\.?(0*[1-9][0-9]?)(?!\d)', re.IGNORECASE)
    match = season_pattern.search(folder_path)
    if match:
        season_number = match.group(1).zfill(2)
    else:
        season_number = False
    
    # Regex to check for imdb url in nfo
    imdb_id_pattern = re.compile(r"imdb\.com/title/(tt\d+)/?", re.IGNORECASE)
    imdb_id = []
    nfo_file_found = False
    archive = False

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".nfo"):
                print(f"NFO-file found")
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")  # Explicitly confirm file processing
                with open(file_path, 'r', encoding='ISO-8859-1') as file_search:
                    contents = file_search.read()
    
                matches = imdb_id_pattern.findall(contents)
                if matches:
                    nfo_file_found = True
                    print(f"IMDb ID found in {file}: {matches}")
                else:
                    print(f"No IMDb ID found in {file}.")
                imdb_id.extend(matches)

            if file.lower().endswith(".rar"):
                archive = file
                print(f"Folder contains RAR archive: {file} ")

    if not nfo_file_found:
        print(f"No NFO-file found in {folder_path}")

    return imdb_id, archive, season_number


def is_for_kids(json_data):
    if json_data: 
        genres = json_data["data"]["title"]["genres"]
        if "Animation" in genres:
            return True  # It's for kids
        else:
            return False  # Not for kids


def set_destination_path(media_type, kids_media):
    #setting default storage location to folder Movies
    storage_location = "/home/roy/test/Movies/"

    KidsMovies = "/media/storage/media/KidsMovies/"
    KidsShows = "/media/storage/media/KidsShows/"
    Movies = "/media/storage/media/Movies/"
    Shows = "/media/storage/media/Shows/"

    #KidsMovies = "/home/roy/test/KidsMovies/"
    #KidsShows = "/home/roy/test/KidsShows/"
    #Movies = "/home/roy/test/Movies/"
    #Shows = "/home/roy/test/Shows/"


    if kids_media == False:
        if media_type == "tvSeries": 
            storage_location = Shows
        if media_type == "movie":
            storage_location = Movies
    if kids_media == True: 
        if media_type == "tvSeries": 
            storage_location = KidsShows
        if media_type == "movie":
            storage_location = KidsMovies

    return storage_location 


def create_folder(folder_name, destination_path, season_number):    
    try:
        # Use os.makedirs() to create the directory; exist_ok=True means no error if the directory already exists
        if season_number: 
            season_number = f"Season {season_number}"
            destination_path = os.path.join(destination_path, folder_name, season_number)
            os.makedirs(destination_path, exist_ok=True)
            print(f"Folder '{destination_path}' created successfully or already exists.")
        else:
            destination_path = os.path.join(destination_path, folder_name, season_number) 
            os.makedirs(destination_path, exist_ok=True)
            print(f"Folder '{destination_path}'{folder_name}' created successfully or already exists.")
    except Exception as e:
        # Catch any exception that might occur and print it
        print(f"An error occurred: {e}")


def unarchive(archive_path, destination_folder):
    try:
        # Check if the archive file exists
        if os.path.exists(archive_path):
            # Get the total number of files in the archive
            with rarfile.RarFile(archive_path, 'r') as rf:
                total_files = len(rf.infolist())

            # Initialize progress variables
            files_extracted = 0

            # Extract the archive
            with rarfile.RarFile(archive_path, 'r') as rf:
                for file in rf.namelist():
                    # Construct the destination path for the file
                    destination_path = os.path.join(destination_folder, os.path.basename(file))
                    print(f"Extracting {file} to {destination_path}")

                    # Extract the file to the destination folder
                    rf.extract(file, destination_folder)
                    
                    # Update progress
                    files_extracted += 1
                    progress = (files_extracted / total_files) * 100
                    print(f"Progress: {progress:.2f}%")

            print(f"Archive '{archive_path}' successfully extracted to '{destination_folder}'.")
        else:
            print(f"Error: Archive '{archive_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



def create_symlink (source_path, link_path): 
    try:
        os.symlink(source_path, link_path)
        print(f"Symbolic link created from {source_path} to {link_path}")
    except OSError as e:
        print(f"Failed to create symbolic link: {e}")

    return True

    
def main():
# Check if the script has been given the right number of arguments
    if len(sys.argv) != 2:
        print("Usage: script.py <ID>")
        sys.exit(1)

    folder_path = sys.argv[1]  # Replace 'your/folder/path' with the actual folder path

    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        sys.exit(1)

    #Call function that checked the source folder for season number, if media is archived and fetches IMDb ID from NFO-file
    imdb_id, archived, season_number = checkfolder(folder_path)
       
    #check if IMDb ID was found, if not we ask the user to enter one   
    if imdb_id:  
        movie_id = imdb_id[0]
    else:
        movie_id = input("No IMDb ID found.\n\nPlease enter the IMDb ID (enter blank for manual entry): ")

    
    #fetching imdb-info
    result = query_imdb_api(movie_id)
    if "errors" in result: 
        print(f"Error fetching data for IMDb ID")
        valid_foldername = False
        while valid_foldername == False:
            foldername = input("Please provide a foldername in the format 'Media name (year)': ")
            if foldername == "": 
                print("Invalid folder name. Please try again!")
            else: 
                valid_foldername = True
                foldername = foldername.strip()

        media_type = input(f"Is this a movie? [Y/n] ").strip().lower()
        if media_type in ["", "y"]:
            media_type = "movie"
        elif media_type in ["n"]:
            media_type = "tvSeries"
            print(season_number)
            if season_number == False:
                valid_season_number = False
                while not valid_season_number:  
                    season_number = input("Please provide a two digit season number: ")
                    # Check if the input is a two-digit number
                    if not (season_number.isdigit() and len(season_number) == 2):
                        print("Invalid season number provided. Season number needs to be a two digit number (i.e. 01)")
                    else:
                        valid_season_number = True
                                        
        else: 
            print("Invalid input. Please enter 'y' or 'n'.")
        kids_media = input(f"Is this kids media? [y/N] ").strip().lower()
        if kids_media in ["", "n"]:
            kids_media  = False
        elif kids_media in ["y"]:
            kids_media  = True
        else: 
            print("Invalid input. Please enter 'y' or 'n'.")
    #if successfully fetched IMDb data
    else:
        imdb_title = result['data']['title']
        foldername = f"{imdb_title['primary_title']} ({imdb_title['start_year']})"
        media_type = result["data"]["title"]["type"]
        kids_media = (is_for_kids(result))
    
   
    #sets correct destination path based on media type
    destination_path = set_destination_path(media_type, kids_media)    
    
    if archived: 
        if season_number: 
            create_folder(foldername, destination_path, season_number)
            print(f"Extracting archive to " + os.path.join(destination_path, foldername, f"Season {season_number}"))
            unarchive(os.path.join(folder_path, archived), os.path.join(destination_path, foldername, f"Season {season_number}"))
            
        else:  
            print(f"Extracting archive to {destination_path}'{foldername}'")
            unarchive(os.path.join(folder_path, archived), os.path.join(destination_path, foldername))

    else:
        if season_number: 
            create_folder(foldername, destination_path, "")
            symlink_dest = os.path.join(destination_path, foldername, f'Season {season_number}')
            print(f"Creating symbolic link from {folder_path} to {symlink_dest}")
            create_symlink (folder_path, symlink_dest)
        else:
           symlink_dest = os.path.join(destination_path, foldername)
           print(f"Creating symbolic link from {folder_path} to {symlink_dest}")
           create_symlink (folder_path, symlink_dest) 
            
if __name__ == "__main__":
    main()

