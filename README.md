# Jellyfin Media Admin
This Python script streamlines media management within Jellyfin by automating the organization of media files. Leveraging IMDb, it accurately identifies and categorizes media files (such as Movies, TV Shows, Children's Movies, or Children's Shows), ensuring they are organized in a Jellyfin-compatible structure.


## Key Features
- **Automated Unarchiving:** Extracts media files from archives, preparing them for use within Jellyfin.
- **Symbolic Link Creation:** Generates symbolic links for extracted media, placing them in the appropriate folder structure in Jellyfin's media library for accessible and organized media.
- **IMDb Integration:** Searches IMDb to efficiently categorize media into the correct folder and type. It prompts the user for input if the media type cannot be determined automatically, ensuring accurate classification.
- **Jellyfin library support**: Supports Movies and shows, organized in Jellyfin friendly folders. Example: A Fantastic Movie (2024), A Fantastic Series (2024)\Season 01\ 

This script is the initial version, with plans to refine and expand its capabilities based on user feedback and evolving needs.


## Note
Optimized for Linux-based systems due to native support for symbolic links. Future updates may include Windows support by adapting the script to create shortcuts, thus improving cross-platform utility.


## Usage
Execute the script by running `jelly_media_admin.py`.


## Configuration: `media.conf`
This configuration file specifies the paths to various media types in Jellyfin, supporting four default media types: Movies, Shows, Kids Movies, and Kids Shows.
If the file does not exist, it is created with default values. 

```
[media]
kidsmovies = /media/storage/media/KidsMovies/
kidsshows = /media/storage/media/KidsShows/
movies = /media/storage/media/Movies/
shows = /media/storage/media/Shows/
```


## Example of script output
```
NFO-file found
Processing file: /media/storage/downloads/A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.nfo
IMDb ID found in A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.nfo: ['tt012456']
Folder contains RAR archive: A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.rar
Extracting archive to /media/storage/media/Movies/'A Fantastic Movie (2024)'
Extracting A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.mkv to /media/storage/media/Movies/A Fantastic Movie (2024)/A.Fantastic.Movie.2024.1080p.BluRay.x264-hacker.mkv
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
