# OneDrive-Sync
Small Python program to sync images on OneDrive cloud with a local directory for linux distros

# Requirements
* Python 2.7 or higher
* Pyside 1.2.2 Python module (this will probably require installing QT)
* Requests Python module

# Configuration file
Before running anything, there is a file called `config` that needs to be editted with these values:
	filepath -> local directory to sync files with
	client_secret -> client secret of your one drive application
	client_id -> client id of you one drive application
	cloud_filepath -> one drive directory containing files to sync (relative to root)

To obtain a one drive client id and secret, you need to create an app. [Instructions are here.](https://dev.onedrive.com/)

# Authentication
The OneDrive API uses oauth authentication. This requires you to sign in, so some sort of GUI is neccesary. `maingui.py` authenticates your user account. 

# Syncing files
You can use 
