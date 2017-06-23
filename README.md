# kipartman

Development in progress.

Coming in the first release:

  * Organize and manage your team parts inside a part database 
  * Group equivalent parts to allow easy parts replacement
  * Download your parts specifications and pricing from Octopart
  * Download you parts symbols and footprints from SnapEDA
  * Create your BOM and chose your parts providers

## Installing

The server part is delivered as a docker-compose file, it is installed throug this command:

  docker compose up --build

By default the database and file repository are searched in the current folder, this can be modified by editing the ''.env'' file and changing the ''KIPARTBASE_PATH'' variable.
Copy the ''db.sqlite3 file'' in the destination folder.

The client part is installed through pip

  pip install kipartman

