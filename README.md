# Cross Note
#### Video Demo: [Here](https://youtu.be/dMGQOj-YH_Y)
#### Description:
Cross Note is a website I created using Python Flask, HTML, CSS, JavaScript, and SQLite 3, along with Bootstrap. The website is designed for storing notes, similar to those on the App Store. The key difference is that most note apps on mobile devices can only be accessed on mobile, and the same goes for laptops or PCs. My project uses databases and accounts on the web to allow you to create notes on any device and access them easily, no matter where you are or what device you are currently using, without needing to sync multiple devices through numerous steps.
##### So first file is the flask_session.
*This file can be ignored as it was made automatically by Flask.
##### Second file is my static file.
This file contains either script file or assets.
* Background.png: This is a free-to-use multi-color fractal. I chose it because I wanted the background to be new and fresh, so my main color scheme was lighter colors with high saturation.
* favicon.ico: To be honest, I just chose a random icon because, for some reason, my Flask wasn't able to run my HTML file without a favicon.
* script.js: This is my JavaScript file. I have both JavaScript in this file and also direct scripts in the HTML itself. The first line is just to ensure it runs. Then I name my main div—`the contenteditable div`—for later use. I created an error function to not only return any errors when users make a mistake but also to use it for alerts or notifications by making it appear at the very bottom of the page. The next function is a saving function using JSON to send whatever note the user inputted back to Python.
* styles.css: My CSS file. As I mentioned, I wanted to create a modern and clean look, so Bootstrap helped with the responsive design. I made a smaller white div than the actual page to make it look like a piece of paper. I had a lot of problems using overflow, but I think it turned out great. I used mainly pink and white for the **"piece of paper"** so it is easier on the eyes. I am currently thinking about adding a dark mode, but maybe sometime later.
##### Third is my templates file.
This folder is used to store all the HTML files.
* layout.html: just so i don't need to recode the page every time. This html file have the error message javascript inside of it to made it available for any other html files. I used a container which used a nav for the navbar like _Home_, _User_, _Logout_ or if they didn't login, it would show _Login_ and _Register_ instead.
* index.html: the page where the user spend the most time on, this is the main page for user to type whatever they want and save it. The file have a content editable div and a **save button** which is detected using javascript.
* login and register html: it pretty clear what these does. i do a a **login_required** function in python at it will redirect first-timers to login.html. The files have _POST method form_ to send data to the backend.
* change.html: or account.html. It basically show your username and you can also change your name-which is unique or change your password. This file is essentially 2 files because the first time it would show you whether you would want to change your password or username and then it would show a form for you to input.
##### Fourth is my app.py. My python script.
* I use libraries such as:
  * flask
  * flask_session
  * cs50
  * werkzeug.security: for hashing a detect hashing.
  * functools-which i didn't actually use.
  * markupsafe-which i didn't actually use.
* i made a **login_required** inspired by the finance problem set. my **"/"** route use the database to load whatever save content that the user typed before and load it for them, if they are a first-timer, it would load the default in index.html instead. **"/login" and "/register"** which use database and check for all possible error cases (i hope). **"/logout"** which is self explained. **"/save"** which used the JSON to put users input into their respective row in the database. And finally **"/change"** which is by far the most complex. use post to determine whether the user want to change thier _password_ or _user name_ and then post again to change it in thr database. I also check for error cases. Finally is just debug and run.
##### Fifth is my note.db AKA my database.
* i have two table inside my database. One is user which contains a unique ID,username and a password hash. The other is called note which contains the user's id and their notes and it also have a default timestamp call _time_.
##### Last is my requirements.txt which is just habit.
Originally, i wanted for it to have an anchor link when the user input a url but i gave up after realizing that i need to check its inner HTML which mess with my contenteditable. I also want to have picture be able to drop in the contenteditable which you can freely drag around and resize but it is way to complex for me.
