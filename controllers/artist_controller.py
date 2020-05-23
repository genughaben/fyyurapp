
from datetime import datetime
from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
from models import db, Venue, Artist, Show, format_datetime
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
        search_term = form_data['search_term'].lower()
        search_term = f"%{search_term}%"

        artist_suggestions = Artist.query.filter(Artist.name.ilike(search_term)).all()

        response = {
          "count": len(artist_suggestions),
          "data" : []
        }

        for artist in artist_suggestions:
            artist_dict = {}
            artist_dict["id"] = artist.id
            artist_dict["name"] = artist.name
            artist_dict["num_upcoming_shows"] = len( [ s.start_time > datetime.now() for s in artist.shows ])
            response["data"].append(artist_dict)

    except Exception as e:
        print(f"An error {e} occured.")
    finally:
        db.session.close()

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@artist_api.route('/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id

  artist = Artist.query.filter_by(id=artist_id).first()

  upcoming_show_list = Show.get_artists_upcoming_shows(artist_id=artist.id)
  past_show_list = Show.get_artists_past_shows(artist_id=artist.id)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "website": artist.website,
    "seek_performance": artist.seek_performance,
    "seek_performance_text": artist.seek_performance_text,
    "past_shows": past_show_list,
    "upcoming_shows": upcoming_show_list,
    "past_shows_count": len(past_show_list),
    "upcoming_shows_count": len(upcoming_show_list)
   }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@artist_api.route('/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.filter_by(id=artist_id).first()
    form = ArtistForm()
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.website.data = artist.website
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.seek_performance.data = True if artist.seek_performance else False
    form.seek_performance_text.data = artist.seek_performance_text
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@artist_api.route('/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    error = False
    try:
        data = request.form
        artist.name = data['name']
        artist.city = data['city']
        artist.state = data['state']
        artist.phone = data['phone']
        artist.genres = data.getlist('genres')
        artist.image_link = data['image_link']
        artist.facebook_link = data['facebook_link']
        artist.website = data['website']
        artist.seek_performance = True if data['seek_performance_text'] != '' else False
        artist.seek_performance_text = data['seek_performance_text']

        db.session.commit()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash(f'An error occurred. Artst could not be changed.')
    if not error:
        flash(f'Venue was successfully updated!')
        return redirect(url_for('artist_api.show_artist', artist_id=artist_id))
    else:
        return render_template('errors/404.html')

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
        genres = form_data.getlist('genres')
        website = url_valid_or_error('website', form_data)
        image_link = form_data['image_link']
        facebook_link = url_valid_or_error('facebook_link', form_data)
        seek_performance_text = form_data['seek_performance_text']

        new_artist = Artist(
            name = name,
            city = city,
            state = state,
            phone = phone,
            genres = genres,
            website = website,
            image_link = image_link,
            facebook_link = facebook_link,
            seek_performance = True if seek_performance_text != '' else False,
            seek_performance_text = seek_performance_text,
        )
        print(new_artist)
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
