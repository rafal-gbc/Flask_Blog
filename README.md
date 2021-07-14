# Flask Blog
Simple blog made with Flask.

## Project description
This is a simple blog created using Python and Flask.
SQLlite is used as a lightweight relational database to store objects.


* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [More detailed information about modules](#more-detailed-information-about-modules)
* [Application view](#application-view)


## General info
<details>
<summary>Click here to see general information about <b>Flask Blog</b>!</summary>
<b>Flask Blog</b>. Basic blog website where you can register, login and create/delete/update your blog posts,
and read, comment other users posts.
This project is a start for anyone that want to develop a blog web app using Flask framework.<br/>
A user login and register system is created to securely store user data and preferences in a SQLlite database
and also to securely restore user password using TimedJSONWebSignatureSerializer.
</details>

## Technologies
<ul>
<li>Python</li>
<ul>
<li>WTF-Forms</li>
<li>Pillow</li>
</ul>
<li>Flask</li>
<ul>
<li>Flask-SQLAlchemy ORM for SQLlite</li>
<li>Flask-Login</li>
<li>Flask-WTF</li>
<li>Flask-Login</li>
<li>Flask-Mail</li>
</ul>
<li>Bootstrap</li>
<li>HTML</li>
<li>CSS</li>
<li>Javascript</li>
</ul>


## Setup
Download or clone repository from ```git clone https://github.com/rafal-gbc/flaskblog.git``` <br/>
Install libraries from requirements.txt, to do this open your terminal and type:
```
pip install -r requirements.txt
```
After this edit the ```config.py``` file:
```
SECRET_KEY = 'YOUR SECRET KEY'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
MAIL_SERVER = 'smtp server'
MAIL_PORT = 2525
MAIL_USERNAME = 'user name'
MAIL_PASSWORD = 'password'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
```
### Examples for Google Mail service and Mailtrap service:
__Google Mail Example__ <br/>
https://support.google.com/mail/answer/7126229?hl=en
```
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_USERNAME = "your_username@gmail.com"
MAIL_PASSWORD = "your_password"
```

__Mailtrap Example__ <br/>
https://mailtrap.io <br/>
```
MAIL_SERVER = 'smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = 'YOUR USERNAME' 
MAIL_PASSWORD = 'YOUR PASSWORD'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
```

### Start application:
Open your terminal in project folder and type:
   
Unix Bash (Linux, Mac):
```
$ export FLASK_DEBUG=1
$ export FLASK_APP=app
$ flask run
```

Windows CMD:
```
> set FLASK_DEBUG=1
> set FLASK_APP=app
> flask run
```
Windows PowerShell:
```
> $env:FLASK_DEBUG=1 
> $env:FLASK_APP="app" 
> flask run
```
 FLASK_DEBUG=1 is not necessary. It allows to restart the server automatically after code changes.


## Application view
### Home Page
![home_page](https://user-images.githubusercontent.com/85440091/125602316-fa855f5c-3aa7-4dc4-8395-3fec798ffb6e.png)
### Register Page
![register_page](https://user-images.githubusercontent.com/85440091/125604507-f7f76046-66f1-43f3-805c-32048f4096b1.png)
### Add Post Page
![add_post_page](https://user-images.githubusercontent.com/85440091/125604856-42072dd7-3ff8-4363-8539-a1cb866210b3.png)
### All Posts Page
![all_posts_page](https://user-images.githubusercontent.com/85440091/125605051-9399c5c2-9053-4418-9bd2-678f476331ce.png)


