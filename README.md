# OneDrive-Sync
Small Python program to sync images located in a OneDrive cloud directory with a local directory, for linux distrubtions

# Requirements
* Python 2.7
* [Pyside 1.2.2 Python module](https://pypi.python.org/pypi/PySide) 
* [Requests Python module](http://www.python-requests.org/en/latest/) 

# Structure
The two main scripts are `maingui.py` and `onedrivesync.py`. `maingui.py` is used for authentication, `onedrivesync.py` is used for silent syncing.

# Configuration file
Before running anything, there is a file called `config` that contains a JSON with these values needing input:

	* filepath -> local directory to sync files with
	* client_secret -> client secret of your one drive application
	* client_id -> client id of you one drive application
	* cloud_filepath -> one drive directory containing files to sync (relative to root)

To obtain a one drive client id and secret, you need to create an app. [Instructions are here.](https://dev.onedrive.com/README.htm) 

# Authentication
The OneDrive API uses oauth authentication. This requires you to sign in, so some sort of GUI is neccesary. `maingui.py` is the script that authenticates your user account. This must be used at least once before using the non-gui script.

# Syncing files
Once you have authenticated your account, you don't need to run `maingui.py` everytime to sync your local files. You can then use `synconedrive.py` to forever sync your files. It uses the same configurations in `config`.


# Periodic Syncing
To sync files every so often, set up a cron job. To do this, use the crontab command in the terminal:

`crontab -e`

If you write the following line in the crontab, `synconedrive.py` will execute every minute:

`* * * * * absolute_path_to_synconedrive.py`

More about cronjobs [here](https://code.google.com/p/ncrontab/wiki/CrontabExamples).
