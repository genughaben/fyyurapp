from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
from models import db, Venue, Artist, Show
from sqlalchemy.inspection import inspect
from forms import ShowForm
from flask import Blueprint
import pandas as pd
import sys

from controllers.util import url_valid_or_error

show_api = Blueprint('show_api', __name__)

#  Shows
#  ----------------------------------------------------------------

@show_api.route('/')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.order_by(Show.date.asc()).all()

  show_list = []
  show_entry = {}
  for show in shows:
      show_entry['venue_id'] = show.venue_id
      show_entry['venue_name'] = show.venue.name
      show_entry['artist_id'] = show.artist_id
      show_entry['artist_name'] = show.artist.name
      show_entry['artist_image_link'] = show.artist.image_link
      show_entry['start_time'] = show.date.strftime("%Y-%m-%dT%H:%M:%S")
      show_list.append(show_entry)

  data = show_list
  return render_template('pages/shows.html', shows=data)

@show_api.route('/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@show_api.route('/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
