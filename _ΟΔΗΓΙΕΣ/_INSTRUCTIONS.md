
# Βήματα (συγκεντρωμένα για win)
Ανοίγω Anaconda Powershell Promt
cd \\Mac\Home\Desktop\P-PO-BO
conda activate mailer
pyinstaller -F --hiddenimport xlrd -w -i mail.ico --add-data "Logo.png;." -n "Mass Mailer" send_emails_gui.py

# Βήματα για ενημέρωση github
Τερματικο.app
cd ~/Desktop/P-PO-BO
git add *
git commit -m "αριθμός"
git push


# Instructions to BUILD Mass Mailer

A full guide to build the mass mailer application using conda in various systems.

# Step 1: Make sure you have conda

The frist step is to download conda, which is a manager for python modules. Instructions to download conda can be found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) for various systems.

# Step 2: Create an environment

We will use conda to create an environment. An environement is a collection of modules with a specific version of python. We will only include the modules needed to run, debug, and build the mailer application on various operating systems. 

To create the environment go to a terminal in mac (or anaconda prompt in windows) navigate to the code directory and type:

```shell
$ conda env create -n mailer -f mailer.yml
```

Then activate the environment by typing

```shell
$ conda activate mailer
```

Now you have activated mailer! If all was done correctly you should see a ``(mailer)`` tag next to your terminal prompt.

# Step 3: Build the application

If needed on MAC ONLY install command line tools

```shell
$ xcode-select --install
```

# Step 4: Build the application

To build the application we will use the following command and a python module called pyinstaller that should be automatically installed in your environment.

To build for the architecture of the current computer (Mac, Windows, etc.) type the following command in the computer's terminal.

```shell
$ pyinstaller -F --hiddenimport xlrd -w -i mail.ico --add-data "Logo.png;." -n "Mass Mailer" send_emails_gui.py 
```

Gia MAC
```shell
$ pyinstaller -F --hiddenimport xlrd -w -i mail.ico --add-data "Logo.png:." -n "Mass Mailer" send_emails_gui.py 
``

make sure you are at the folder that contains the file ``send_emails_gui.py`` and that you have enabled the correct conda environment.

I can also write a batch file that does this for different operating systems if needed. 
