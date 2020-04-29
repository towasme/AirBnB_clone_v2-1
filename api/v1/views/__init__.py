#!/usr/bin/python3
""" initializes the app """

from flask import Blueprint
import api.v1.views.index


app_views = Blueprint('/api/v1')
