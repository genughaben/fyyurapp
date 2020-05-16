
from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
from models import db, Venue, Artist, Show, format_datetime
from sqlalchemy.inspection import inspect
from forms import VenueForm
from flask import Blueprint
import pandas as pd
import sys

from pprint import pprint
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
        'num_upcoming_shows': len(Show.get_venues_upcoming_shows(venue_id=venue.id))
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

@venue_api.route('/search', methods=['POST'])
def search_venues():
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    response = {}
    error = False
    try:
      form_data = request.form
      search_term = form_data['search_term'].lower()
      search_term = f"%{search_term}%"

      venues_suggestions = Venue.query.filter(Venue.name.ilike(search_term)).all()

      response = {
        "count": len(venues_suggestions),
        "data" : []
      }

      venue_dict = {}
      for venue in venues_suggestions:
          venue_dict["id"] = venue.id
          venue_dict["name"] = venue.name
          venue_dict["num_upcoming_shows"] = venue.get_num_upcoming_shows()
          response["data"].append(venue_dict)

    except Exception as e:
      print(f"An error {e} occured.")
    finally:
      db.session.close()

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@venue_api.route('/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.filter_by(id=venue_id).first()

    upcoming_show_list = Show.get_venues_upcoming_shows(venue_id=venue.id)
    past_show_list = Show.get_venues_past_shows(venue_id=venue.id)

    data = {
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past_show_list,
      "upcoming_shows": upcoming_show_list,
      "past_shows_count": len(past_show_list),
      "upcoming_shows_count": len(upcoming_show_list)
    }

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
        image_link = form_data['image_link']
        genres = form_data.getlist('genres')
        website = url_valid_or_error(form_data['website'])
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
