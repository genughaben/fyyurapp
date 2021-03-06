from datetime import datetime

import babel
import dateutil.parser
from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# from flask_basicauth import BasicAuth

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)

# app.config['BASIC_AUTH_USERNAME'] = 'admin'
# app.config['BASIC_AUTH_PASSWORD'] = 'udacity'
app.config['BASIC_AUTH_FORCE'] = True
app.config.from_object('config')

# basic_auth = BasicAuth(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# def setup_database(app):
#     app.config.from_object('config')
#     db.init_app(app)
#     migrate = Migrate(app, db)
#     return db

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.Text, nullable=False, default='')
    image_link = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __str__(self):
        _str = ""
        _str += f"name: {self.name}\n"
        _str += f"genres: {self.genres}\n"
        _str += f"address: {self.address}\n"
        _str += f"city: {self.city}\n"
        _str += f"state: {self.state}\n"
        _str += f"phone: {self.phone}\n"
        _str += f"website: {self.website}\n"
        _str += f"facebook_link: {self.facebook_link}\n"
        _str += f"seeking_talent: {self.seeking_talent}\n"
        _str += f"seeking_description: {self.seeking_description}\n"
        _str += f"image_link: {self.image_link}\n"
        _str += f"shows: {self.shows}\n"
        return _str


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    website = db.Column(db.String(500), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    seek_performance = db.Column(db.Boolean, nullable=False, default=False)
    seek_performance_text = db.Column(db.Text, nullable=False, default='')
    shows = db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

    @staticmethod
    def extract_show_venue_info(show_result):
        show_list = []
        for show in show_result:
            show_dict = {}
            show_dict['venue_image_link'] = show.venue.image_link
            show_dict['venue_id'] = show.venue.id
            show_dict['venue_name'] = show.venue.name
            show_dict['start_time'] = show.start_time.strftime('%Y-%m-%d %H:%M:%S')
            show_list.append(show_dict)
        return show_list

    @staticmethod
    def get_artists_upcoming_shows(artist_id):
        show_result = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).all()
        return Show.extract_show_venue_info(show_result)

    @staticmethod
    def get_artists_past_shows(artist_id):
        show_result = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time < datetime.now()).all()
        return Show.extract_show_venue_info(show_result)

    @staticmethod
    def extract_show_artist_info(show_result):
        show_list = []
        for show in show_result:
            show_dict = {}
            show_dict['artist_image_link'] = show.artist.image_link
            show_dict['artist_id'] = show.artist.id
            show_dict['artist_name'] = show.artist.name
            show_dict['start_time'] = show.start_time.strftime('%Y-%m-%d %H:%M:%S')
            show_list.append(show_dict)
        return show_list

    @staticmethod
    def get_venues_upcoming_shows(venue_id):
        show_result = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time > datetime.now()).all()
        return Show.extract_show_artist_info(show_result)

    @staticmethod
    def get_venues_past_shows(venue_id):
        show_result = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time < datetime.now()).all()
        return Show.extract_show_artist_info(show_result)
