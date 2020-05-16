
from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
from models import db, Venue, Artist, Show
from sqlalchemy.inspection import inspect
from forms import VenueForm
from flask import Blueprint
import pandas as pd
import sys

from controllers.util import url_valid_or_error

venue_api = Blueprint('venue_api', __name__)

#  Venues
#  ----------------------------------------------------------------
from collections import defaultdict

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

@venue_api.route('/')
def venues():
    venues_list = Venue.query.order_by(Venue.city.asc()).order_by(Venue.state.asc()).all()

    data = []
    entry = {
      'city': venues_list[0].city,
      'state': venues_list[0].state,
      'venues': []
    }
    for venue in venues_list:
      venue_entry = {
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': venue.get_num_upcoming_shows()
      }
      if venue.city == entry['city'] and venue.state == entry['state']:
        entry['venues'].append(venue_entry)
      else:
        data.append(entry)
        entry = {
          'city': venue.city,
          'state': venue.state,
          'venues': [venue]
        }
    data.append(entry)

    return render_template('pages/venues.html', areas=data)

from pprint import pprint

@venue_api.route('/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  error = False
  try:
      form_data = request.form
      pprint(from_data)
      search_term = form_data['search_term']

      venues_suggestions = Venue.query.filter(func.lower(Venue.name) == func.lower(f"{search_term}"))

      response = {
        "count": len(venues_suggestion),
        "data" : []
      }

      venue_dict = {}
      for venue in venues_suggestions:
          venue_dict["id"] = venue.id
          venue_dict["name"] = venue.name
          venue_dict["num_upcoming_shows"] = venue.get_num_upcoming_shows
          response["data"].append(venue_dict)

  except e:
      print(f"An error {e} occured.")
  finally:
      db.session.close()

  pprint(response)
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@venue_api.route('/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data1={
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
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  data = Venue.query.filter_by(id=venue_id).first()
  print(data)
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------
#

# Show GETted Create Form
@venue_api.route('/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


# def check_duplicate_addresses(address_to_check):
#     Venue.query.filter_by(address=address_to_check)
#
#
#     pass
#
# def check_sense(value):
#     if()
#     pass
#
# def check_url(maybe_url):

def error_handling():
    error = True
    db.session.rollback()
    flash('Invalid url ' + form_data['name'] + ' could not be listed.', 'error')
    print(sys.exc_info())
    return error

# Process users data POSTed via Create From
@venue_api.route('/create', methods=['POST'])
def create_venue_submission():

    error = False
    try:
        form_data = request.form
        name = form_data['name']
        city = form_data['city']
        state = form_data['state']
        address = form_data['address']
        phone = form_data['phone']
        genres = form_data.getlist('genres')
        website = url_valid_or_error(form_data['website_link'])
        facebook_link = url_valid_or_error(form_data['facebook_link'])
        new_venue = Venue(
          name = name,
          city = city,
          state = state,
          address = address,
          phone = phone,
          genres = genres,
          website = website,
          facebook_link = facebook_link
        )
        db.session.add(new_venue)
        db.session.commit()
    except InvalidUrlException:
        error = error_handling()
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Venue ' + form_data['name'] + ' could not be listed.', 'error')
        abort(400)
    flash('Venue ' + form_data['name'] + ' was successfully listed!', 'success')
    return render_template('pages/home.html')
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success

### flash('Venue ' + request.form['name'] + ' was successfully listed!')


  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

### return render_template('pages/home.html')


@venue_api.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))


@venue_api.route('/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None
