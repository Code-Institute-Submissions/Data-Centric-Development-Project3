# LogIt - The Virtual Dive Log
## Data-Centric-Development-Project3

## DEMO

A live demo website can be found here : <https://bh-logit.herokuapp.com/>

![Responsive](/resources/responsive.JPG)

## Context
LogIt is a mobile-responsive web app that has a focus on the data-centric approach development. 

In a nutshell, LogIt is to challenge the way how Divers keep their dive logs conventionally using a physical log book. 

With the use of a database, User will be able to store and access all their dive logs information online, and even create a 
sighting log with photo attached if they spot some interesting marine life during the dive! 

# UX
### STRATEGY
* Target audience
    - Divers who keep a dive log
    - Divers who are interested in sharing their dives and sightings with their friends
    - Users looking to find out more information about certain dive sites, from other divers dive logs
    - Users looking to find out more about a certain marine specie sightings
* Goals
	- to digitalise conventional phyiscal dive logs
	- to allow User to post photos on the sightings
	- User to be able to Create,Read,Update,Delete (CRUD) 
	- User to be able to perform a search on Country, DiveSite, Species

### SCOPE
* User Story
    - I am a diver, I want to store all my dive logs and sightings online
	- I am a diver, I am interested to see other divers dive logs on a particular dive site
	- I am a diver, I am interested to see all the sightings of my favourite marine specie with photos
* Requirements
	- User to be able to Create, Read, Update and Delete (Profile, Dive Logs, Sightings)
	- User to be able to search for Country, Dive Site or a marine Specie
	- If no photos are uploaded for profile and sightings, a default one will be inserted instead

### Sitemap/Wireframes
The sitemap was created to help me conceptualise the User Flow when visiting the website. It can be viewed [here](resources/sitemap.jpg).

The wireframe helps me to visualise the page layout. It can be viewed [here](resources/wireframe.png).

# FEATURES

The core functionalities of a database **Create , Read, Update, Delete (CRUD)** are presented in this project. 
These functions are as follows:

### 1. Create
* When a user enters a new email address that is not yet saved in the database, the user will be prompted with a form to create a User 
Profile. The submitted information will then be saved in the database together with a display photo (optional), and user will be able to access
the created profile when the same email is entered. If no display photo is uploaded, the app will auto assign a default display photo. 

* From the User profile page, user will be able to create a new Dive Log.  The dive log created will be tied to the particular User. 

* From each specific dive log, user will be able to create sightings spotted for that particular dive. The sighting created will be tied to 
the User and the specific dive log.

### 2. Read
* When an existing email address is entered in the "Profile" section, the app will read and display all the information from the database 
with the email address. 

* Clicking on "See all dives for User", all the User dive logs created will be read and display from database. 

* User can choose to read and display all the sightings tied to the User, or can individually see all the sightings per dive log created.

### 3. Update
* User will be able to click on the "Edit" button on each dive log and edit the information on it. The database will update and overwrite
the existing with the new information. 

* Each sightings can also be updated with new information. A new sighting photo can be updated as well. 

### 4. Delete
* A delete confirmation page will be prompted when User decides to delete either a sighting, dive log or the User profile itself.

* To maintain data integrity, the app has been set up as such:
    - Delete Sightings - deletes just the Sighting 
    - Delete Dive Log - and all the Sightings related to this Dive Log
    - Delete User Profile - and all the Dive Logs, Sightings related to this User

### 5. Additional FEATURES
* On the Home page, a table of 5 of the latest sightings will be shown. This is updated based on the last 5 Sightings data that were 
saved on the database. 
* Clicking on any of the latest sightings, the app will automatically run a search and dispay all the Sightings for the particular Species
on the database. 

* A search bar is available for User to search for all Dive Logs for a Country, or a Dive Site. User will be able to search for a Species sighted.


## FUTURE FEATURES
* User password verification

* User to be able to search by User, and see all the User's activity

* An interactive map that plots out all of the User's dives and sightings

* An interactive map that plots out all of the dives and sightings on the database

* User to be able to like, comment and follow other Users

# TECHNOLOGIES USED
* HTML5
* CSS3
* Bootstrap4
* Javascript
* jQuery
* Python
* Flask
* Jinja2
* MongoDB
* [UploadeCare](https://uploadcare.com/) - User to upload photos (limited to 1MB per upload for free account)
* Git and Gitpod
* Heroku
* Am I Responsive(<http://ami.responsivedesign.is/>)
* Screen To Gif(<https://www.screentogif.com/>)
* Google fonts (<https://fonts.google.com/>)

# TESTING
### Manual Testing

|Test Description| Results|
|------ | ------ |
| Latest Sightings on Home Page to update when new sightings are posted | Pass |
| Search to automatically run  | Pass |
| Search by Country (eg. Thailand) on search bar | Pass |
| Search by Dive Site (eg. Redang) on search bar | Pass |
| Search by Sepcies (eg. White Tip) on search bar | Pass |
| Search by invalid on search bar | Pass |
| Prompts a User information form when new email address is entered in Profile | Pass |
| Creates a new User Profile after submitting User Informaton | Pass |
| Uploads a user display photo (smaller than 1MB file size) | Pass |
| Delete User | Pass |
| Add new dive log for user | Pass |
| Add new sightings per dive log | Pass |
| Edit dive log and sightings | Pass |
| Display all dive logs and sightings | Pass |
| Display all sightings related to a specific dive log | Pass |
| Delete Dive Logs and Sightings | Pass |
| Pagination | Pass |
| Mobile Responsive mode | Pass |


### KNOWN BUGS
 * Unable to create a single "Back to Profile" button on both "All Dive Logs" and "Sightings" page. Error : InvalidOperation: cannot set options after executing query
 * Workaround
    - Created button in each iteration of the Table "For" loop


# DEPLOYMENT
This site is hosted using Heroku, deployed directly from the master branch. This site can be viewed [here](https://bh-logit.herokuapp.com/). 
The deployed site will update automatically upon new commits from the master branch.

To run locally, clone this repository directly into the editor of your choice by pasting git clone 
`heroku git:clone -a bh-logit` into your terminal.


# CREDITS
* Images
    - Default User Profile image (https://www.pond5.com)
    - Default Sightings image (https://www.pexels.com/photo/person-diving-on-ocean-3257802/)

* Logos
    - https://www.freelogodesign.org/


# Acknowledgements
* Forms Templates reference from - https://www.codeply.com/p/xjn4SoQjD6


**This is for educational use** 