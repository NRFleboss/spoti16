from flask import Flask, redirect, request
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Spotify OAuth settings
SPOTIPY_CLIENT_ID = 'd2289b4d890f4a39b027eb0d427c670d'
SPOTIPY_CLIENT_SECRET = '6eac9c07cf984a82a8f01f51011ff36f4'
SPOTIPY_REDIRECT_URI = 'https://spoti16.streamlit.app/callback'  # Local Flask app callback URL

sp_oauth = SpotifyOAuth(
    SPOTIPY_CLIENT_ID, 
    SPOTIPY_CLIENT_SECRET, 
    SPOTIPY_REDIRECT_URI,
    scope='user-library-read'
)

@app.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']
    # Redirect back to the Streamlit app with the token
    return redirect(f'https://spoti16.streamlit.app/?token={access_token}')

if __name__ == '__main__':
    app.run(debug=True)
