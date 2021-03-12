# Seed data to create the database and add/commit a few users, images and paragraphs

from app import app
from models import db, User, Paragraph, Image
import datetime

db.drop_all()
db.create_all()

u1 = User.register(
    username = "firsttestuser",
    password ="wu9r324ir3",
    email = "firsttestuser@email.com"
)

u2 = User.register(
    username = "secondtestuser",
    password ="wu9wetwerr324ir3",
    email = "secondtestuser@email.com"
)

db.session.add_all([u1, u2])
db.session.commit()

i1 = Image(
    image_url = "https://images.unsplash.com/photo-1613993729048-84d5639ac8c1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyMTIzOTh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MTUyOTA4NTA&ixlib=rb-1.2.1&q=80&w=200",
    date_added = datetime.date(2021, 3, 11),
    photographer = "Anne Sack",
    credit_url = "https://unsplash.com/@anne_sack"
)

i2 = Image(
    image_url = "https://images.unsplash.com/photo-1614827141334-732badfbf72c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyMTIzOTh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MTUyOTEwNDk&ixlib=rb-1.2.1&q=80&w=200",
    date_added = datetime.date(2021, 3, 12), 
    photographer = "Jonny Auh",
    credit_url = "https://unsplash.com/@jonnyauh"
)

i3 = Image(
    image_url = "https://images.unsplash.com/photo-1615136611564-465f782c859b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyMTIzOTh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MTU1NjIxMTA&ixlib=rb-1.2.1&q=80&w=200",
    date_added = datetime.date(2021, 3, 13),
    photographer = "Dave Weatherall",
    credit_url = "https://unsplash.com/@thattravelblog"
)

i4 = Image(
    image_url = "https://images.unsplash.com/photo-1613847397435-900a256196df?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyMTIzOTh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MTU1NjQ5NDI&ixlib=rb-1.2.1&q=80&w=200",
    date_added = datetime.date(2021, 3, 14),
    photographer = "Egor Ivlev",
    credit_url = "https://unsplash.com/@ger46"
)

i5 = Image(
    image_url = "https://images.unsplash.com/photo-1610601683621-2770eeb5e232?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyMTIzOTh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MTU1NjUwNTI&ixlib=rb-1.2.1&q=80&w=200",
    date_added = datetime.date(2021, 3, 15),
    photographer = "Alen Kajtezovic",
    credit_url = "https://unsplash.com/@alenkajtezovic"
)

db.session.add_all([i1, i2, i3, i4, i5])
db.session.commit()

p1 = Paragraph(
    title = "My first paragraph",
    content = "This is a test 1. Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis quo ipsa labore iure fuga saepe nulla at illo esse repudiandae dolore similique, aspernatur sequi officia porro maxime! Sit, velit fugiat!",
    public = True,
    user_id = 1,
    image_id = 1
)

p2 = Paragraph(
    title = "Inspired",
    content = "This is a test 2. Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis quo ipsa labore iure fuga saepe nulla at illo esse repudiandae dolore similique, aspernatur sequi officia porro maxime! Sit, velit fugiat!",
    public = True,
    user_id = 2,
    image_id = 1 
)

p3 = Paragraph(
    title = "The stormy night",
    content = "This is a test 3. Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis quo ipsa labore iure fuga saepe nulla at illo esse repudiandae dolore similique, aspernatur sequi officia porro maxime! Sit, velit fugiat!",
    public = True,
    user_id = 1,
    image_id = 2 
)

p4 = Paragraph(
    title = "Musings",
    content = "This is a test 4. Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis quo ipsa labore iure fuga saepe nulla at illo esse repudiandae dolore similique, aspernatur sequi officia porro maxime! Sit, velit fugiat!",
    user_id = 2,
    image_id = 2 
)

p5 = Paragraph(
    title = "A Great Image",
    content = "This is a test 5. Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis quo ipsa labore iure fuga saepe nulla at illo esse repudiandae dolore similique, aspernatur sequi officia porro maxime! Sit, velit fugiat!",
    public = True,
    user_id = 1,
    image_id = 4 
)

p6 = Paragraph(
    title = "A Story to Tell",
    content = "This is a test 6. Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis quo ipsa labore iure fuga saepe nulla at illo esse repudiandae dolore similique, aspernatur sequi officia porro maxime! Sit, velit fugiat!",
    public = True,
    user_id = 2,
    image_id = 5 
)

db.session.add_all([p1, p2, p3, p4, p5, p6])
db.session.commit()