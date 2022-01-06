from flask import Blueprint, request, redirect, jsonify, make_response
from datetime import timedelta, date


net = Blueprint('net', __name__)


@net.route('/signup', methods=['POST'])
def signup():
    return make_response("OK", 200)
