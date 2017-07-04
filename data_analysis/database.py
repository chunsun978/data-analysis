from os import path

from sqlalchemy import (create_engine,
                        Column,
                        String,
                        Integer,
                        Boolean,
                        Table,
                        ForeignKey)

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

database_filename = 'twitter.sqlite3'

directory = path.abspath(path.dirname(__file__))
database_filepath = path.join(directory, database_filename)

engine_url = 'sqlite:///{}'.format(database_filepath)

engine = create_engine(engine_url)

# Our database class objects are going to inherit from 
# this class
Base = declarative_base(bind=engine)

# Session class
Session = sessionmaker(bind=engine, autoflush=False)

# Create a Session
session = Session()



hashtag_tweet = Table('hashtag_tweet', Base.metadata,
        Column('hashtag_id', Integer, ForeignKey('hashtags.id'), nullable=False),
        Column('tweet_id', Integer, ForeignKey('tweets.id'), nullable=False)
        )

class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    tid = Column(String(100), nullable=False)
    tweet = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable =False)
    coordinates = Column(String(50), nullable=True )
    user = relationship('User', backref='tweets')
    created_at = Column(String(100), nullable=False)
    favorite_count = Column(Integer)
    in_reply_to_screen_name = Column(String)
    in_reply_to_status_id = Column(Integer)
    lang = Column(String)
    quoted_status_id = Column(Integer)
    source = Column(String)
    is_retweet = Column(Boolean)
    hashtags = relationship ('Hashtag',
                            secondary='hashtag_tweet',
                            back_populates='tweets')
    
    def __repr__(self):
        return '<Tweet {}>'.format(self.id)
    
class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    tweets = relationship('Tweet',
                          secondary='hashtag_tweet',
                          back_populates='hashtags')

    def __repr__(self):
        Base.metadata.create_all()

def init_db():
    Base.metadata.create_all()

if not path.isfile(database_filepath):
    init_db()

