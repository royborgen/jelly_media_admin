# jelly_media_admin
Script to automatically manage mediafiles in Jellyfin library.

The script will search imdb and identify a correct folder name and media type (Movies, Show, Kids Movie or Kids Show). 
It will place the media in correct media folder in a format that jellyfin likes. 

- The script will unrar mediafiles that are archived. 
- Create symbolic links to unarchived media under correct folderstructure in Jellyfins media library.
- If the script is unable to determin media type from IMDb, it will promt the user for needed inputs.

This the first iteration of this script. Further improvements to come


## Usage
The script is executed by running jelly_media_admin.py

# media.conf
This is the scripts configuration file. 
It contains the path to the various media types in Jellyfin. 
By defualt it supports 4 media types: Movies, Showes, Kids Movies and Kids Shows. 

```
[media]
kidsmovies = /media/storage/media/KidsMovies/
kidsshows = /media/storage/media/KidsShows/
movies = /media/storage/media/Movies/
shows = /media/storage/media/Shows/
```

## Example of script output
When running the script each Stantas child is cencored in the output. 
```
NFO-file found
Processing file: /media/storage/downloads/A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.nfo
IMDb ID found in japhson-rh.nfo: ['tt0098206']
Folder contains RAR archive: A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.rar
Extracting archive to /media/storage/media/Movies/'A Fantastic Movie (2024)'
Extracting japhson-rh.mkv to /media/storage/media/Movies/A Fantastic Movie (2024)/A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.mkv
Archive '/media/storage/downloads/A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker/A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.rar' successfully extracted to '/media/storage/media/Movies/A Fantastic Movie (2024)'.
```

## Requirements
- Python 3 
- requests library installed 
- sys library installed 
- json library installed
- os library installed
- configparser library installed
- re library installed
