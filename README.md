# Paragraph A Day

[View App on Heroku](https://paragraph-a-day.herokuapp.com/)

**Paragraph A Day** is a tool made for writers, designed to make the writing practice more enjoyable and motivating. The app provides users with a daily image for inspiration, and it allows users to save their writing as a "paragraph." There is a 500-character limit on each paragraph, which is designed to reduce pressure and increase motivation. There is also an option to share paragraphs anonymously with other users, which creates a sense of community without the pressure of judgment or evaluation.

**Features and Flow**: A new visitor can view example paragraphs on the home page, visit a page to learn more about the app, register as a new user, or log in as an existing user. Once logged in, the user is provided with the daily image prompt and a form to submit a paragraph. They can also visit a page to view their previously submitted paragraphs, or a page to view recent public paragraphs, including their own. On either of these pages, the user can click a button to edit or delete one of their own paragraphs. Additionally, on the public paragraphs page, the user can search for paragraphs created on a particular date; this feature is especially useful if the user is curious what other users wrote about an image that they also wrote about. 

**API Information**: When the first user of the day logs in, Paragraph A Day retrieves one random image from the [Unsplash API](https://unsplash.com/developers), which is then used as an image prompt for the rest of that day. There are many other endpoints developers can access when using the Unsplash API, which are described in the documentation, along with terms and guidelines. 

**Technology Stack**: Paragraph A Day utilizes HTML, CSS,  Bootstrap, Javascript/JQuery, PostgreSQL, SQLAlchemy, Flask, Python, and WTForms.

**Project Setup**: If you clone this repository and would like to run the app on your local machine, these steps will help you get started. This project uses [Python](https://www.python.org/downloads/) and [PostgreSQL](https://www.postgresql.org/download) which you will need to download. You may find this [documentation for PostgreSQL](https://www.postgresql.org/docs/current/tutorial.html)  and [documentation for Python](https://docs.python.org/3/using/index.html) helpful for installation. In developing this app, I used [Git Bash](https://git-scm.com/downloads) for my command line interface, though you may choose to use a different tool. Once these basics are in place, you're ready for project setup at the command line: 

- Create a database for the project, as well as a test database for testing. These can be created by running the following commands:
     - `createdb paragraph_db`
     - `createdb paragraph_test_db`
- Create a virtual environment within the project directory and then activate that virtual environment with the following commands:
     - `python -m venv venv`
     - `. venv/Scripts/activate`
- Install all the dependencies required for this project with this command:
     - `pip install -r requirements.txt`
- Before running the app, at a minimum you will need to run a basic seed file to create all the tables in the database. Alternatively, you may wish to run a seed file that will add some users and paragraphs to the database, so that the app already has some content in it when you launch it locally. Before running a seed file, first move into the /prep directory with this command:
     - `cd prep`
- Then to run a seed file, you'll need to set three environmental variables. The first is the PYTHONPATH, which tells flask where to find the app.py file. The second is the ACCESS\_KEY, which can be obtained by creating a developer account at [Unsplash](https://unsplash.com/documentation#creating-a-developer-account). The third is a SECRET_KEY, which you can set to be anything you wish for your local version. 
     - `PYTHONPATH=.. SECRET_KEY="your_secret_key" ACCESS_KEY="your_access_key" python seed_basic.py`
     - `PYTHONPATH=.. SECRET_KEY="your_secret_key" ACCESS_KEY="your_access_key" python seed.py`
     - `PYTHONPATH=.. SECRET_KEY="your_secret_key" ACCESS_KEY="your_access_key" python seed_two.py`
- Now move back into the main directory and then set SECRET\_KEY and ACCESS_KEY as environmental variables to run flask and launch the app:
     - `cd ..`
     - `SECRET_KEY="your_secret_key" ACCESS_KEY="your_access_key" flask run`
- Following this command, a URL will be provided where you can now access the app. To stop flask from running at any time, you can press CTRL-C. 
- If you would like to run the tests that were used in developing the app, you can do so with the following command:
     - `SECRET_KEY="your_secret_key" ACCESS_KEY="your_access_key" python -m unittest tests.py`