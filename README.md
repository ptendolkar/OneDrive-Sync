# OneDrive-Sync
Small Python program to sync images on OneDrive cloud with a local directory for linux distrubtions

# Requirements
* Python 2.7
* [Pyside 1.2.2 Python module](https://pypi.python.org/pypi/PySide) 
* [Requests Python module](http://www.python-requests.org/en/latest/) 

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
Once you have authenticated your account, you don't need to run `maingui.py` everytime to sync your local files. You can then use `synconedrive.py` to forever sync your files. It uses the same configurations in `config`.

I set up a cron job to sync up files every minute. To do this, use the crontab command:

`crontab -e`

And write the following line:

`* * * * * absolute_path_to_synconedrive.py`
