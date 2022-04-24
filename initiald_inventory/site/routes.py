from flask import Blueprint, render_template
from flask_login.utils import login_required

"""
note that in the code below,
some arguments are specified when creating the Blueprint.
the frist arguemtn, "site", is the GBlueprint's name,
which is used by Flask's routing mechanism

the second arugment, __name__, is the Blueprint's import name,
which Flask uses to locate the Blueprints resources

"""

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')