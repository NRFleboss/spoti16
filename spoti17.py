import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Define your Spotify API credentials
SPOTIPY_CLIENT_ID = "d2289b4d890f4a39b027eb0d427c670d"
SPOTIPY_CLIENT_SECRET = "6eac9c07cf984a82a8f01f51011ff36f4"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"  # Change this to your redirect URI

def main():
    st.set_page_config(layout="wide")
    st.title("Spotify Playlist Search")

    # Check if the user is authenticated with Spotify
    sp_oauth = SpotifyOAuth(
        SPOTIPY_CLIENT_ID,
        SPOTIPY_CLIENT_SECRET,
        SPOTIPY_REDIRECT_URI,
        scope="user-library-read",
    )

    token_info = sp_oauth.get_cached_token()
    if token_info is None or time.time() > token_info["expires_at"]:
        # Display a login button at the beginning
        st.warning("You are not logged in with Spotify.")
        auth_url = sp_oauth.get_authorize_url()
        if st.button("Login with Spotify"):
            st.markdown(f"Click [here]({auth_url}) to log in with your Spotify account.")
    else:
        st.success("You are logged in with Spotify.")

        tab1, tab2, tab3, tab4 = st.tabs(["Single Market Search", "Multi-Country Search", "Excel Display", "Playlist Highlight"])

        with tab1:
            # Original single market search functionality
            query = st.text_input("Query")
            market = st.text_input("Market")

            if st.button("Search"):
                if query and market:
                    playlists = get_playlists(sp_oauth, query, market)
                    if playlists:
                        for i, playlist in enumerate(playlists, start=1):
                            with st.container():
                                st.markdown("---")  # Adds a horizontal line for separation
                                col1, col2 = st.columns([3, 1])

                                with col1:
                                    st.markdown(f"**{i}. {playlist['name']}** - *{playlist['owner']['display_name']}*", unsafe_allow_html=True)

                                with col2:
                                    if playlist['images']:
                                        st.markdown(f"<a href='{playlist['external_urls']['spotify']}' target='_blank'><img src='{playlist['images'][0]['url']}' width='80' height='80'></a>", unsafe_allow_html=True)
                    else:
                        st.write("No playlists found or error in fetching playlists.")

    # Implement the rest of your tabs in a similar way

def get_playlists(sp_oauth, query, market, offset=0, limit=20):
    try:
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        results = sp.search(q=query, type='playlist', market=market, offset=offset, limit=limit)
        playlists = results['playlists']['items']
        return playlists
    except Exception as e:
        st.error(f"Failed to retrieve playlists: {str(e)}")
        return []

if __name__ == '__main__':
    main()
