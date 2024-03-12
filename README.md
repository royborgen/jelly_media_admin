# jelly_media_admin
Script to manage and organize mediafiles for Jellyfin. The script takes a download folder as input. 

The script will search imdb and identify a correct name and media type. 
It will place media in correct folder location for jellyfin. 

- The script will unrar mediafiles that are archived. 
- Create symbolic links to unarchived media under correct folderstructure in Jellyfin
- If the script is unable to determin media type from IMDb, it will promt the user for needed inputs.

This the first iteration of this script. Further improvements to come
