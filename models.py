from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date

db = SQLAlchemy()

def setup_database(app):
    app.config.from_object('config')
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

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


    def get_num_upcoming_shows(self):
        t = Venue.query.filter_by(id=Venue.id).filter(Show.date < date.today()).count()
        # print(f"shows count: {t}")
        return t
      

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=False)
    webpage_link = db.Column(db.String(500), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    seek_performance = db.Column(db.Boolean, nullable=False, default=False)
    seek_performance_text = db.Column(db.Text, nullable=False, default='')
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
