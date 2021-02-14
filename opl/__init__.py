from . import oplmain
from flask import redirect, make_response, request, url_for
import json
from simplexml import dumps
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import requests
from flask import render_template

# main object created here:
oplMain = oplmain.OplMain()
oplAPIApp = oplMain.get_app()
oplApi = oplMain.get_api()
oplLoginManager = oplMain.get_login_manager()
oplOAuth2Client = oplMain.get_oauth2_client()
# setup all controller here
oplMain.setup_controllers()

from opl.oplapi.dataaccess.UserDA import UserDataAccess
from opl.oplapi.model.user import User
userDA = UserDataAccess(oplAPIApp.config['DATABASE_OPL'])

# Flask-Login helper to retrieve a user from our db
@oplLoginManager.user_loader
def load_user(id):
    return userDA.selectById(id)

@oplAPIApp.route("/opl/home")
def hello():
    message = "Hello, World"
    return render_template('index.html', message=message)


# homepage: /index
@oplAPIApp.route("/opl/index")
def index():
    print("index(): current_user.is_authenticated: {}".format(current_user.is_authenticated))
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'
            '<br/><br/><a class="button" href="/logout">Google Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a><br/><br/><a class="button" href="/logout">Google Logout</a>'

# login: /login
def get_google_provider_cfg():
    return requests.get(oplAPIApp.config['GOOGLE_DISCOVERY_URL']).json()

@oplAPIApp.route("/opl/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = oplOAuth2Client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    print("login(): current_user.is_authenticated: {}".format(current_user.is_authenticated))
    return redirect(request_uri)

# login callback: /login/callback

@oplAPIApp.route("/opl/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = oplOAuth2Client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(oplAPIApp.config['OPL_GOOGLE_CLIENT_ID'], oplAPIApp.config['OPL_GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens!
    oplOAuth2Client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = oplOAuth2Client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google

    # Doesn't exist? Add it to the database.
    user = userDA.selectByGoogleId(unique_id)
    if user is None:
        user = userDA.selectByEmail(users_email)
        if user is not None:
            userDA.update_google_info(user)
        else:
            user = User(id = -1,
                        email = users_email,
                        name = users_name,
                        display_name = users_name,
                        google_id = unique_id,
                        profile_pic = picture,
                        user_type_id = 3)  # regalar user
            userDA.insert(user)
    # Begin user session by logging the user in
    login_user(user)
    # Send user back to homepage
    print("callback(): current_user.is_authenticated: {}".format(current_user.is_authenticated))
    return redirect(oplAPIApp.config['GOOGLE_CALLBACK_URL'])
    # return redirect(url_for("index"))

@oplAPIApp.route("/opl/logout")
@login_required
def logout():
    logout_user()
    return redirect(oplAPIApp.config['GOOGLE_CALLBACK_URL'])
    # return redirect(url_for("index"))

# redirect the root to swagger documentation
@oplAPIApp.route('/opl')
def home():
    return redirect('/opl/doc/', code=302)

@oplApi.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

@oplApi.representation('application/xml')
def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp

# run app if this is starting point
if __name__ == '__main__':
    oplMain.run()
