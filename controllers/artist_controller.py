
from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
from models import db, Venue, Artist, Show
from sqlalchemy.inspection import inspect
from forms import ArtistForm
from flask import Blueprint
import pandas as pd
import sys

from controllers.util import url_valid_or_error

artist_api = Blueprint('artist_api', __name__)


#  Artists
#  ----------------------------------------------------------------
@artist_api.route('/')
def artists():
  artist_list = Artist.query.order_by(Artist.name.asc()).all()
  data = []
  print(artist_list)
  for artist in artist_list:
      arist_dict = {}
      arist_dict['id'] = artist.id
      arist_dict['name'] = artist.name
      data.append(arist_dict)

  return render_template('pages/artists.html', artists=data)

@artist_api.route('/search', methods=['POST'])
def search_artists():
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

    response = {}
    error = False
    try:
        form_data = request.form
        search_term = form_data['search_term']
        search_term = f"%{search_term}%"

        artist_suggestions = Artist.query.filter(Artist.name.ilike(search_term)).all()

        response = {
          "count": len(artist_suggestions),
          "data" : []
        }

        artist_dict = {}
        for artist in artist_suggestions:
            artist_dict["id"] = artist.id
            artist_dict["name"] = artist.name
            artist_dict["num_upcoming_shows"] = artist.get_num_upcoming_shows()
            response["data"].append(artist_dict)

    except Exception as e:
        print(f"An error {e} occured.")
    finally:
        db.session.close()

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@artist_api.route('/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id

  data = Artist.query.filter_by(id=artist_id).first()
  genres = []
  if len(data.genres[0]) > 1:
      for genre in data.genres:
          genres.append(genre)
  else:
      genres = [data.genres]

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@artist_api.route('/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@artist_api.route('/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@artist_api.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

  #  Create Artist
  #  ----------------------------------------------------------------

@artist_api.route('/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@artist_api.route('/create', methods=['POST'])
def create_artist_submission():

    error = False
    try:
        form_data = request.form
        name = form_data['name']
        city = form_data['city']
        state = form_data['state']
        phone = form_data['phone']
        image_link = form_data['image_link']
        facebook_link = url_valid_or_error(form_data['facebook_link'])
        website = url_valid_or_error(form_data['website'])
        genres = form_data.getlist('genres')

        new_artist = Artist(
            name = name,
            city = city,
            state = state,
            phone = phone,
            image_link = image_link,
            facebook_link = facebook_link,
            website = website,
            genres = genres,
            seek_performance = False,
            seek_performance_text = '',
        )
        db.session.add(new_artist)
        db.session.commit()
    except Exception as e:
        flash('Invalid Artist ' + form_data['name'] + ' could not be listed.', 'error')
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Artist ' + form_data['name'] + ' could not be listed.', 'error')
        abort(400)
    flash('Artist ' + form_data['name'] + ' was successfully listed!', 'success')
    return render_template('pages/home.html')


    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
