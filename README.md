# Paragraph A Day

[View App on Heroku](https://paragraph-a-day.herokuapp.com/)

**Paragraph A Day** is a tool made for writers, designed to make the writing practice more enjoyable and motivating. The app provides users with a daily image for inspiration, and it allows users to save their writing as a "paragraph." There is a 500-character limit on each paragraph, which is designed to reduce pressure and increase motivation. There is also an option to share paragraphs anonymously with other users, which creates a sense of community without the pressure of judgment or evaluation.

**Features and Flow**: A new visitor can view example paragraphs on the home page, visit a page to learn more about the app, register as a new user, or log in as an existing user. Once logged in, the user is provided with the daily image prompt and a form to submit a paragraph. They can also visit a page to view their previously submitted paragraphs, or a page to view recent public paragraphs, including their own. On either of these pages, the user can click a button to edit or delete one of their own paragraphs. Additionally, on the public paragraphs page, the user can search for paragraphs created on a particular date; this feature is especially useful if the user is curious what other users wrote about an image that they also wrote about. 

**API Information**: When the first user of the day logs in, Paragraph A Day retrieves one random image from the [Unsplash API](https://unsplash.com/developers), which is then used as an image prompt for the rest of that day. There are many other endpoints developers can access when using the Unsplash API, which are described in the documentation, along with terms and guidelines. 

**Technology Stack**: Paragraph A Day utilizes HTML, CSS,  Bootstrap, Javascript/JQuery, PostgreSQL, SQLAlchemy, Flask, Python, and WTForms.