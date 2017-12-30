import os
from urllib.parse import urljoin

from flask import Flask, render_template, session, redirect, url_for
from authlib.client.apps import twitter, github
from authlib.flask.client import OAuth

from ecssercise.models import User, Check

app = Flask(__name__, static_url_path='/static', instance_relative_config=True)
auth_module = {'twitter': twitter, 'github': github}


@app.route('/', methods=['get'])
def get_introduction():
    return render_template('introduction.html')


@app.route('/exercise/<int:exercise_number>', methods=['get'])
def get_exercises(exercise_number):
    template_path = os.path.join('exercises', f'exercise_{exercise_number}.html')
    return render_template(template_path, exercise_number=exercise_number)


@app.route('/oauth/<string:auth_type>', methods=['get'])
def get_oauth(auth_type):
    provider = auth_module.get(auth_type, None)
    if 'logged_in' in session or provider is None:
        return redirect(url_for('.get_introduction'))

    oauth = OAuth(app)
    provider.register_to(oauth)
    return provider.authorize_redirect(_generate_callback_url(auth_type))


@app.route('/callback/<string:auth_type>', methods=["get"])
def callback(auth_type):
    provider = auth_module[auth_type]
    token = provider.authorize_access_token()
    user_profile = provider.fetch_user()

    user = User.first_or_new(social_id=str(user_profile.id))
    user.set_token(token)
    user.set_user_data(user_profile)
    user.save()

    session['logged_in'] = user.social_id
    return redirect(url_for('.get_introduction'))


@app.route('/logout', methods=['get'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('.get_introduction'))


@app.route('/check/<int:exercise_number>', methods=['post'])
def post_check(exercise_number):
    user = User.find_by_social_id(session.get('logged_in', ''))
    if user is not None:
        check = Check.find_by_user_id_and_exercise_number(user.id, exercise_number)
        if check is None:
            check = Check()
            check.user_id = user.id
            check.exercise_number = exercise_number
            check.save()
        else:
            check.delete()

    return redirect(url_for('.get_exercises', exercise_number=exercise_number))


def _generate_callback_url(provider_name):
    return urljoin(app.config['OAUTH_CALLBACK_DOMAIN'], url_for('.callback', auth_type=provider_name))
