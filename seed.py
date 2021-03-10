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
    date_added = datetime.date(2021, 3, 7),
    photographer = "Anne Sack",
    credit_url = "https://unsplash.com/@anne_sack"
)

i2 = Image(
    image_url = "https://images.unsplash.com/photo-1614827141334-732badfbf72c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyMTIzOTh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MTUyOTEwNDk&ixlib=rb-1.2.1&q=80&w=200",
    date_added = datetime.date(2021, 3, 8), 
    photographer = "Jonny Auh",
    credit_url = "https://unsplash.com/@jonnyauh"
)

db.session.add_all([i1, i2])
db.session.commit()

p1 = Paragraph(
    title = "My first paragraph",
    content = "This is a test. I just really want to see approximately how long 100 words really is. I mean, if this is the limit I give people, how much will they actually be able to write? And how much space will it really take up on the page? I'm not really sure. So this should give me a better idea. I want to really see how much space this is going to take up. So far this is looking alright. We'll see how it goes! This is getting really close to 100 words. And here we are at 99!",
    public = True,
    user_id = 1,
    image_id = 1
)

p2 = Paragraph(
    title = "Inspired",
    content = "This is a test. I just really want to see approximately how long 100 words really is. I mean, if this is the limit I give people, how much will they actually be able to write? And how much space will it really take up on the page? I'm not really sure. So this should give me a better idea. I want to really see how much space this is going to take up. So far this is looking alright. We'll see how it goes! This is getting really close to 100 words. And here we are at 99!",
    public = True,
    user_id = 2,
    image_id = 1 
)

p3 = Paragraph(
    title = "The stormy night",
    content = "This is a test. I just really want to see approximately how long 100 words really is. I mean, if this is the limit I give people, how much will they actually be able to write? And how much space will it really take up on the page? I'm not really sure. So this should give me a better idea. I want to really see how much space this is going to take up. So far this is looking alright. We'll see how it goes! This is getting really close to 100 words. And here we are at 99!",
    public = True,
    user_id = 1,
    image_id = 2 
)

p4 = Paragraph(
    title = "Musings",
    content = "This is a test. I just really want to see approximately how long 100 words really is. I mean, if this is the limit I give people, how much will they actually be able to write? And how much space will it really take up on the page? I'm not really sure. So this should give me a better idea. I want to really see how much space this is going to take up. So far this is looking alright. We'll see how it goes! This is getting really close to 100 words. And here we are at 99!",
    user_id = 2,
    image_id = 2 
)


db.session.add_all([p1, p2, p3, p4])
db.session.commit()