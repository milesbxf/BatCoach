#BatCoach
BatCoach is a web app for managing a virtual online cricket team on [Battrick](http://www.battrick.org/), tracking stats and player attributes. Data is parsed from HTML files saved from the Battrick website and maintained in a database.

##Release plan
- v0.1 - imports players and club information from a selectable local directory or file upload. Tracks player attributes and highlights training 'pops' (attribute increases), records club information and tracks leagues and league positions.

#Specification
##Set up
Upon startup, the frontend checks whether a config has already been set at `api/config/check`, which checks whether the database has been initialised. If the database hasn't been created, a set up page is displayed, inviting the user to import a Pavilion.html file with club information. This is the main team which will be tracked. Future versions will support tracking of multiple teams, but currently only one is supported.

##Importing files
On the frontend, the main import page lists all the HTML files in the current import directory, getting these from `api/import/listfiles`. If no files are found, a warning message is displayed to the user. If the import directory is invalid a HTTP 500 server error is sent and an error displayed to the user. The files can then be selected and filenames (not full path) are sent to the backend to process at `api/import/importfiles`. An import results page is then displayed showing which files were successfully imported.

The import directory can be selected through a folder browser on the frontend. Users can enter a path in a textbox. A list of subdirectories (from `api/folders/list` with subdirectory name or `..`, indicating parent directory as a parameter) and the option to go to the parent directory is shown. Folders can be clicked on to navigate; once the desired import directory is found, the user clicks a button and the import directory is changed via `api/import/changedir` with the current directory and requested subdirectory. 
