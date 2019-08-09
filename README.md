# product Catalog
This web application provides catalog to access product easily with web interface

## Project Description
This web application has been developed using python3, Flask, SQLite and basic HTML-CSS-Javascript.

Going deeper to the functionalities serve by this application, project_catalog aims to provide catalog for easier access to veried products categorised in many different category.
1. An anonymous user can view all categories and products easily
2. While an authenticated user can create catgeories and products
3. Also, an authenticated user can update or delete own products 
4. Most importantly, application uses Google signIn for application signIn

**Requirements**: 
Now moving towards how to use this web application we have two options for environment

Virtual machine environment:
1. Vagrant
2. Virtualbox
Virtual machine can be run using [Vagrant](https://www.vagrantup.com/downloads.html "Vagrant") and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1 "VirtualBox") which you can download and install from here. Find the version for your operating system. Also, VirtualBox does not require launch because Vagrant will do that. 
After successful installation, open Git Bash terminal then go to vagrant repository to start virtual machine. Command **vagrant init** will initialise virtual machine and will create Vagrantfile into vagrant repository. Then after running a command **vagrant up** will start virtual machine. Finally, once you are up with virtual machin you can log in using command **vagrant ssh**.

Or you can use enviornment of your choice. However, it should support and have running:
1. Python3
2. SQLite
3. Flask

Google SignIn App setup
As the application using Google SignIn for authentication you should have Google Account for developer login.
You will required to create Google API console project and client id to make this application sign in through google.
for information on how to configure project, access this doc [Google SignIn](https://developers.google.com/identity/sign-in/web/sign-in "Google SignIn configuration")
set application for using sign in feature and on the left side bar, under APIs and Services, access credential

In OAuth Consent screen >>
In Scopes for google APIs, keep scope as it is which will remain email, profile, openid

In Credential tab >>
In Authorized javascript origins set up http://localhost:5000 and
in Authorized redirect URIs set up two urls, one is http://localhost:5000/oauth2callback and second is http://localhost:5000/catalog

Get your client_id and go to code project-catalog/templates/login.html line5 which should be seeming as follow, and replace your client_id over there
<meta name="google-signin-client_id" content="YOUR_CLIENT_ID.apps.googleusercontent.com">

Also, you have to download json file of credential displaying under OAuth 2.0 client IDs list view. After download you will rename file to client_secret.json and place that file inside project-catalog folder.

**Project Setup**:
You can download this application and this will provide you project-catalog folder or you can download this repository and unzip the file so ultimately you will get project-catalog folder.
if you are using virtual machine then you can keep this folder inside virtual environment, exactly besides the file Vagrantfile. so, you can access it as /vagrant/project-catalog in git bash terminal.

Now, vagrant is all set to go, you will create database catalog by running as
$ python3 database_setup.py
then after you will add few dummy datas by running as
$ python3 insert_data.py
finally you will start application by running as
$ python3 app.py

you can access application through browser by accessing address http://localhost:5000/catalog
