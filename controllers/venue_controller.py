
from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
from models import db, Venue, Artist, Show, format_datetime
from datetime import datetime
from sqlalchemy.inspection import inspect
from forms import VenueForm
from flask import Blueprint
import pandas as pd
import sys

from pprint import pprint
from controllers.util import InvalidUrlException, url_valid_or_error

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

      for venue in venues_suggestions:
          venue_dict = {}
          venue_dict["id"] = venue.id
          venue_dict["name"] = venue.name
          venue_dict["num_upcoming_shows"] = len( [ s.start_time > datetime.now() for s in venue.shows ])
          response["data"].append(venue_dict)

      print(response.data)

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
def create_venue_form(form_data=None):

    form = VenueForm()
    if form_data:
        return render_template('forms/new_venue.html', form=form, venue=form_data)
    else:
        return render_template('forms/new_venue.html', form=form)

def error_handling(e):
    error = True
    db.session.rollback()
    flash(f'Error: {e}', 'error')
    print(sys.exc_info())
    return error

# Process users data POSTed via Create From
@venue_api.route('/create', methods=['POST'])
def create_venue_submission():

    error = False
    invalid = False
    exists = False
    try:
        form_data = request.form
        name = form_data['name']
        city = form_data['city']
        state = form_data['state']
        address = form_data['address']
        phone = form_data['phone']
        image_link = url_valid_or_error('image_link', form_data)
        genres = form_data.getlist('genres')
        website = url_valid_or_error('website', form_data)
        facebook_link = url_valid_or_error('facebook_link', form_data)
        seeking_description = form_data['seeking_description']
        new_venue = Venue(
          name = name,
          city = city,
          state = state,
          address = address,
          phone = phone,
          genres = genres,
          website = website,
          facebook_link = facebook_link,
          image_link = image_link,
          seeking_talent = True if seeking_description != '' else False,
          seeking_description = seeking_description
        )
        exists = db.session.query(Venue.id).filter_by(name=name).scalar() is not None
        if not exists:
            db.session.add(new_venue)
            db.session.commit()
    except InvalidUrlException as e:
        invalid = error_handling(e)
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Venue ' + form_data['name'] + ' could not be listed.', 'error')
        abort(400)
    if exists:
        flash('Not added, there is already a Venue with name ' + form_data['name'] + ' present in the database.', 'success')
        return render_template(url_for('venue_api.create_venue_form', form_data=form_data))
    if invalid:
        flash('Not added, there is already a Venue with name ' + form_data['name'] + ' present in the database.', 'success')
        return render_template(url_for('venue_api.create_venue_form', form_data=form_data))
    flash('Venue ' + form_data['name'] + ' was successfully listed!', 'success')
    return render_template('pages/home.html')

@venue_api.route('/<int:venue_id>/edit', methods=['POST', 'GET'])
def edit_venue_submission(venue_id):
    if request.method == 'GET':
        venue = Venue.query.filter_by(id=venue_id).first()
        form = VenueForm()
        form.name.data = venue.name
        form.genres.data = venue.genres
        form.address.data = venue.address
        form.city.data = venue.city
        form.state.data = venue.state
        form.phone.data = venue.phone
        form.website.data = venue.website
        form.facebook_link.data = venue.facebook_link
        form.seeking_talent.data = True if venue.seeking_description else False
        form.seeking_description.data = venue.seeking_description
        form.image_link.data = venue.image_link
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    if request.method == 'POST':
        venue = Venue.query.filter_by(id=venue_id).first()
        error = False
        try:
            data = request.form
            venue.name = data['name']
            venue.city = data['city']
            venue.state = data['state']
            venue.address = data['address']
            venue.phone = data['phone']
            venue.genres = data.getlist('genres')
            venue.image_link = data['image_link']
            venue.facebook_link = data['facebook_link']
            venue.website = data['website']
            venue.seeking_talent = True if data['seeking_description'] != '' else False
            venue.seeking_description = data['seeking_description']

            db.session.commit()

        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            flash(f'An error occurred. Venue could not be changed.')
        if not error:
            flash(f'Venue was successfully updated!')
        return redirect(url_for('venue_api.show_venue', venue_id=venue_id))
    else:
        return render_template('errors/404.html')


@venue_api.route('/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        db.session.delete(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash(f'Error: venue with id: {venue_id} could not be deleted.')
    if not error:
        flash(f'Success: venue with id: {venue_id} was deleted.')

    return render_template('pages/home.html')
