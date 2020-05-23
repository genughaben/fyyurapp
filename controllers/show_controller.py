from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
from models import db, Venue, Artist, Show, format_datetime
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
  shows = Show.query.order_by(Show.start_time.asc()).all()

  show_list = []
  show_entry = {}
  for show in shows:
      show_entry['venue_id'] = show.venue_id
      show_entry['venue_name'] = show.venue.name
      show_entry['artist_id'] = show.artist_id
      show_entry['artist_name'] = show.artist.name
      show_entry['artist_image_link'] = show.artist.image_link
      show_entry['start_time'] = show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
      show_list.append(show_entry)

  data = show_list
  return render_template('pages/shows.html', shows=data)

@show_api.route('/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@show_api.route('/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)
    try:
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )
        db.session.add(show)
        db.session.commit()
        flash('Success: Show was successfully listed!')
    except ValueError:
        flash('Error: show could not be listed.')
    return render_template('pages/home.html')
