# Toy Store API

A simple Python REST API with Bearer Token Authentication of 20 characters long that can be used to create, get, and delete admin, employee and item records. The application is built with Python, Flask, and is connected to a database using Flask-SQLAlchemy.


# Basic Overview 

Toy Store API is built based on a simple business logic where:
* Only Admins(shop owner and/or team leaders) can administer(create, get, and delete) their Employees and 
* Both Admins and Employees can create, get, and delete their toy Items.

# Setting Up

```shell
$ git clone https://github.com/anp-tech/toystoreapi.git
$ cd toystoreapi
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip
$ pip install -r requirements.txt
$ python3 run.py

``` 

# Test Results

Every endpoint has been tested using Postman, please refer to the following link: <br>
https://drive.google.com/file/d/1mZRyBekf1CaMxB3HbHEGvCJVQaJgGgSX/view?usp=sharing


