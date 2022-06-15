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


# Sample Requests

Next, visit http://127.0.0.1:5000/employee to create an account. A user is required to enter username, password, and verify if they are an admin or not. After the account is created, the user will receive a token of 20 characters long upon signing in which they can use it to access other routes. This token will expire after 90 minutes. 
<br>

![create employee](https://user-images.githubusercontent.com/49329136/173753044-9af697c9-7832-4edf-850b-6a3ae2cb262e.png)
<br>


![image](https://user-images.githubusercontent.com/49329136/173754131-49f8de71-7929-459f-aaa6-fda9dbec83ed.png)
<br>

![image](https://user-images.githubusercontent.com/49329136/173754750-abb221e8-bd0a-4206-af0d-cd63b59cce8a.png)


# Test Results

Every endpoint has been tested using Postman, please refer to the following link: <br>
https://drive.google.com/file/d/1mZRyBekf1CaMxB3HbHEGvCJVQaJgGgSX/view?usp=sharing
