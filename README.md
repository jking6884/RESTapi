###Installation

####Step 1:Clone the project to your application folder.

    git clone git@github.com:jking6884/RESTapi.git YourAppFolderName && cd YourAppFolderName

####Step 2: Install the requirements and add your Database configuration details.

    docker-compose build

    vim config.py
    #Fill in your database username, password, name, host etc

#### Step 3 : Declare your Resource and it's fields in a YAML file as follows

For a list of supported fields please see https://github.com/Leo-g/Flask-Scaffold/wiki/Fields

    vim scaffold/blog.yaml
    posts:
     - title:string
     - body:text
     - author:string
     - creation_date:date
     - published:boolean
    comments:
     - author:string
     - body:text
     - author_url:url
     - created_on:date
     - approved:boolean
    authors:
     - name:string
     - profile:text
     - url:url

#### Step 4 : Run the Scaffolding  and database migrations script

    python scaffold.py scaffold/blog.yaml
    python db.py db init
    python db.py db migrate
    python db.py db upgrade

###Tests

####For unit testing with python Unit tests

    For a Single module

    python app/<module_name>/test_<module_name>.py

    For all modules

    bash tests.bash

###API

API calls can be made to the following URL

Note: This example is for a Post module

| HTTP Method  | URL  | Results |
| :------------ |:---------------:| -----:|
| GET      | http://localhost:5000/api/v1/posts.json | Returns a list of all Posts |
| POST     | http://localhost:5000/api/v1/posts.json      |   Creates a New Post |
| GET | http://localhost:5000/api/v1/posts/1.json      | Returns details for the a single Post |
| PATCH | http://localhost:5000/api/v1/posts/1.json      | Update a Post |
| DELETE | http://localhost:8001/api/v1/posts/1.json      | Delete a Post |

The JSON format follows the spec at jsonapi.org and a sample is available in the sample.json   file

For details on how the API is built read 	http://techarena51.com/index.php/buidling-a-database-driven-restful-json-api-in-python-3-with-flask-flask-restful-and-sqlalchemy/

###Directory Structure
        Project-Folder
            |-- config.py
            |--run.py
            |--requirements.txt
            |--conf.js
            |__ /venv
            |-- db.py
            |__ /scaffold
            |-- scaffold.py
            |-- tests.bash    #Tests for all modules
            |__ app/
                |-- __init__.py
                +-- module-1
                    |-- __init__.py
                    |-- models.py
                    |-- test_module-1.py  # Unit Tests for module 1
                    |-- views.py
                        
                +-- module-2
                    |-- __init__.py
                    |-- models.py
                    |-- test_module-2.py  # Unit Tests for module 2
                    |-- views.py
                |__ templates
                   |-- index.html
                   |-- login.html
                   |-- home.html
                   +-- static
                          + -- js
                                 |-- app.js
                                 |-- login.js
                          |-- css
                          |-- images
                   +-- module-1
                                   |-- _form.html
                                   |-- index.html
                                   |-- add.html
                                   |-- update.html
                                   |-- controller.js
                                   |--conf.js
                                   |--spec.js
                   +-- module-2
                                   |-- _form.html
                                   |-- index.html
                                   |-- add.html
                                   |-- update.html
                                   |-- controller.js
                                   |-- conf.js
                                   |-- spec.js


