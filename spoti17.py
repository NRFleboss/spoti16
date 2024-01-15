import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Define your Spotify API credentials
SPOTIPY_CLIENT_ID = "d2289b4d890f4a39b027eb0d427c670d"
SPOTIPY_CLIENT_SECRET = "6eac9c07cf984a82a8f01f51011ff36f4"
SPOTIPY_REDIRECT_URI = "http://localhost:5000/callback"  # Change this to your redirect URI

def get_playlists(sp_oauth, query, market, offset=0, limit=20):
    try:
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        results = sp.search(q=query, type='playlist', market=market, offset=offset, limit=limit)
        playlists = results['playlists']['items']
        return playlists
    except Exception as e:
        st.error(f"Failed to retrieve playlists: {str(e)}")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("Spotify Playlist Search")

    selected_option = st.selectbox("Select an option", ["Single Market Search", "Multi-Country Search", "Excel Display", "Playlist Highlight"])

    if selected_option == "Single Market Search":
        # Original single market search functionality
        query = st.text_input("Query")
        market = st.text_input("Market")

        if st.button("Search"):
            if query and market:
                playlists = get_playlists(query, market)
                if playlists:
                    for i, playlist in enumerate(playlists, start=1):
                        with st.container():
                            st.markdown("---")  # Adds a horizontal line for separation
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.markdown(f"**{i}. {playlist['name']}** - *{playlist['owner']}*", unsafe_allow_html=True)

                            with col2:
                                if playlist['images']:
                                    st.markdown(f"<a href='{playlist['external_urls']['spotify']}' target='_blank'><img src='{playlist['images'][0]['url']}' width='80' height='80'></a>", unsafe_allow_html=True)
                else:
                    st.write("No playlists found or error in fetching playlists.")

    elif selected_option == "Multi-Country Search":
        # Multi-Country Search functionality
        st.subheader("Search Playlists Across Multiple Countries")
        multi_query = st.text_input("Enter your query for multi-country search", key="multi_query")

        if multi_query:
            display_playlists_for_countries(multi_query)

    elif selected_option == "Excel Display":
        st.subheader("Google Sheets Display")
        google_sheet_iframe = """
        <iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTe6Hks3FvRx1XNR_Ci9pNJUb0Q8nux1nC587p2ts4jDGI3UoIe9suOaf0QEJRT_pGbvlsGmNkuMx42/pubhtml?widget=true&amp;headers=false" width="100%" height="600"></iframe>
        """
        st.markdown(google_sheet_iframe, unsafe_allow_html=True)

    elif selected_option == "Playlist Highlight":
        st.subheader("Highlight Playlist from URL")
        playlist_url = st.text_input("Enter Spotify Playlist URL")
        word_query = st.text_input("Enter your search word")
        market = st.selectbox("Choose market", ['US', 'FR', 'DE', 'AU', 'CA', 'MX', 'ES', 'IT'])

        if st.button("Search and Highlight", key="highlight_search"):
            if word_query and market:
                playlists = get_playlists(word_query, market)
                if playlists:
                    highlighted_playlists = highlight_playlist(playlists, playlist_url)
                    display_playlist_with_highlight(highlighted_playlists)
                else:
                    st.write("No playlists found or error in fetching playlists.")

if __name__ == '__main__':
    main()
