# kipartman

Kipartman is a tool designed to help Kicad user managing their BOM efficiently. 
It relies on both Octopart (https://octopart.com/) and SnapEDA (https://www.snapeda.com/) to manage parts and associated footprints.

With kipartman you will be able to:

  * Organize and manage your team parts inside a part database 
  * Group equivalent parts to allow easy parts replacement
  * Manage your part stock
  * Download your parts specifications and pricing from Octopart
  * Download you parts symbols and footprints from SnapEDA
  * Create your BOM
  * Prepare your buying order from your BOM by chosing the best prices

Kipartman is a combination of a database and file server (kipartbase) and a graphical tool to manage it (kipartman).

Note: in the future kipart base will allow multi-user simultaneous usage but this is not yet ready and may lead to database corrupt.

Note: kipartman is still in active development phase, some functionalities may not be yet available.

## Prerequisites

On Ubuntu systems you need to install some packages before installing kipartman:

<code>
sudo apt-get install build-essential libgtk-3-dev libwebkitgtk-3.0-dev libwxgtk3.0-dev libwxgtk-media3.0-dev libwebkitgtk-dev libboost-dev
</code>

## Installing

Kipartman is available through pip:

<code>
pip install kipartman
</code>

Note: wxPython can be quite long to install as it is built from sources.

## Configuration

By default the database is a sqlite database and is installed in ```~/.kipartbase```, you can change this destination folder by setting the ```KIPARTBASE_PATH``` environment variable.
If you want to use postgres, mysql or any other database please read the django documentation (https://docs.djangoproject.com/en/1.11/ref/settings/)

## Run the server

The server can be run manually or through a docker-compose.

  * To run it manually just use the command:

```
kipartbase
```

  * You can also run it through a docker-compose from the git repository:

```
git clone  https://github.com/turdusmerula/kipartman
cd kipartman
docker-compose up --build
```

## Octopart

Octopart is a search engine for electronic parts, you will need to configure an api key to allow kipartman to interact with it.

Create an account on the website https://octopart.com/ and create an api key at https://octopart.com/api/dashboard.

Edit the file ```~/.kipartman/configure.json``` and put your newly created api key:

```
{
    "kipartbase": "http://localhost:8100",
    "octopart_api_key": "<your api key>"
}
```

## SnapEDA

SnapEDA is a database containing a huge pool of footprints and schematic symbols, you will need an account to download files on their website.

Create an account on the website https://www.snapeda.com/account/signup/?next=/.

Edit the file ```~/.kipartman/configure.json``` and put your SnapEDA credentials:
```
{
    "snapeda_password": "xxxxxxxx",
    "snapeda_user": "john.doe@gmail.com"
}
```

Note: works with the SnapEDA team is in progress to improve support for Kicad.

## Kipartman

You can launch kipartman by simply calling it from the console:

```
kipartman
```

## TODO list

  * Add filtering from parts parameters in part view
  * Improve sorting of non string columns in treeview and listviews
  * Refresh kipart libraries and footprint from database
  * Add backup and restore
  * Add tutorials

 
