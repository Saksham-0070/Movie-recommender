import logging
import os
import pickle
import gdown

import pandas as pd
import requests
import streamlit as st
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
try:
    API_KEY = st.secrets["TMDB_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = os.getenv("TMDB_API_KEY")

PLACEHOLDER_IMG = "https://placehold.co/500x750/1a1a2e/ffffff?text=No+Image"
TMDB_BASE_URL   = "https://api.themoviedb.org/3/movie"
TMDB_IMG_BASE   = "https://image.tmdb.org/t/p/w500/"


# ─────────────────────────────────────────────
# Custom CSS — Dark Cinematic UI
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Space+Mono:wght@400;700&display=swap');

    /* ── Global Reset ── */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    .stApp {
        background: #07070f;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,60,255,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,180,255,0.08) 0%, transparent 60%);
    }

    /* hide default streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2.5rem !important; padding-bottom: 3rem !important; max-width: 960px; }

    /* ── Hero Title ── */
    .hero-wrap {
        text-align: center;
        padding: 2.5rem 0 1.2rem;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 5.5rem !important;
        font-weight: 900;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 40%, #38bdf8 75%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.1;
    }
    .hero-sub {
        color: rgba(255,255,255,0.38);
        font-size: 0.95rem;
        font-weight: 300;
        margin-top: 0.5rem;
        letter-spacing: 0.5px;
    }

    /* ── Selectbox label ── */
    .stSelectbox label p {
        color: rgba(255,255,255,0.55) !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.6px;
        text-transform: uppercase;
    }

    /* ── Selectbox wrapper — glowing border ── */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 14px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 0.25rem 0.5rem !important;
        box-shadow:
            0 0 0 1px rgba(99,60,255,0.0),
            inset 0 1px 0 rgba(255,255,255,0.06);
        transition: box-shadow 0.3s ease, border-color 0.3s ease;
        position: relative;
    }
    .stSelectbox > div > div:focus-within,
    .stSelectbox > div > div:hover {
        border-color: rgba(167,139,250,0.5) !important;
        box-shadow:
            0 0 0 3px rgba(99,60,255,0.15),
            0 0 30px rgba(99,60,255,0.12),
            inset 0 1px 0 rgba(255,255,255,0.08) !important;
    }

    /* rainbow glow bar under selectbox */
    .glow-bar {
        height: 2px;
        width: 100%;
        border-radius: 2px;
        background: linear-gradient(90deg,
            #ff4e50, #fc913a, #f9d423,
            #36d1dc, #5b86e5, #a855f7, #ff4e50);
        background-size: 200% 100%;
        animation: rainbowSlide 3s linear infinite;
        margin-top: -2px;
        opacity: 0.85;
        border-radius: 0 0 14px 14px;
    }
    @keyframes rainbowSlide {
        0%   { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    /* ── Recommend Button ── */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 2rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        color: #ffffff !important;
        background: linear-gradient(135deg, #6d28d9, #2563eb) !important;
        border: none !important;
        border-radius: 12px !important;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(99,60,255,0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(99,60,255,0.55) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── Movie Cards ── */
    .movie-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        overflow: hidden;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        cursor: pointer;
    }
    .movie-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 40px rgba(99,60,255,0.3), 0 0 0 1px rgba(167,139,250,0.3);
        border-color: rgba(167,139,250,0.35);
    }
    .movie-card img {
        width: 100%;
        display: block;
        border-radius: 14px 14px 0 0;
    }
    .movie-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        color: rgba(255,255,255,0.75);
        text-align: center;
        padding: 0.6rem 0.5rem 0.7rem;
        line-height: 1.3;
        letter-spacing: 0.2px;
    }

    /* ── Results heading ── */
    .results-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: rgba(255,255,255,0.25);
        letter-spacing: 2px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 1.2rem;
        margin-top: 0.5rem;
    }

    /* ── Divider ── */
    .fancy-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(167,139,250,0.3), rgba(56,189,248,0.3), transparent);
        margin: 1.5rem 0;
        border: none;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #a78bfa !important; }

    /* ── Streamlit image override ── */
    .stImage > img {
        border-radius: 14px 14px 0 0 !important;
    }

    /* scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #07070f; }
    ::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.3); border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HTTP Session with Retry Logic
# ─────────────────────────────────────────────
def create_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

SESSION = create_session()


# ─────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1Q77qkoyf_FLM2pHyO8WwEz_e9VTK44PA"
    gdown.download(url, "similarity.pkl", quiet=False)

    with open("movies_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

    return pd.DataFrame(movies_dict), similarity


# ─────────────────────────────────────────────
# Poster Fetching
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_poster(movie_id):
    if not API_KEY:
        logger.warning("TMDB API key not set.")
        return PLACEHOLDER_IMG
    try:
        response = SESSION.get(
            f"{TMDB_BASE_URL}/{movie_id}",
            params={"api_key": API_KEY, "language": "en-US"},
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        return TMDB_IMG_BASE + poster_path if poster_path else PLACEHOLDER_IMG
    except requests.exceptions.Timeout:
        logger.warning("Timeout for movie ID %s.", movie_id)
    except requests.exceptions.HTTPError as e:
        logger.warning("HTTP error for movie ID %s: %s", movie_id, e)
    except requests.exceptions.ConnectionError as e:
        logger.warning("Connection error for movie ID %s: %s", movie_id, e)
    except requests.exceptions.RequestException as e:
        logger.warning("Network error for movie ID %s: %s", movie_id, e)
    except (KeyError, ValueError) as e:
        logger.warning("Parse error for movie ID %s: %s", movie_id, e)
    return PLACEHOLDER_IMG


# ─────────────────────────────────────────────
# Recommendation Logic
# ─────────────────────────────────────────────
def recommend(movie, movies_df, similarity_matrix, top_n=5):
    matches = movies_df[movies_df["title"] == movie]
    if matches.empty:
        st.error(f"Movie '{movie}' not found in the dataset.")
        return [], []
    movie_index = matches.index[0]
    distances   = similarity_matrix[movie_index]
    top_indices = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1: top_n + 1]
    titles, posters = [], []
    for idx, _ in top_indices:
        row = movies_df.iloc[idx]
        titles.append(row["title"])
        posters.append(fetch_poster(row["movie_id"]))
    return titles, posters


# ─────────────────────────────────────────────
# App UI
# ─────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="CineMatch — Movie Recommender",
        page_icon="🎬",
        layout="centered",
    )

    inject_css()

    # ── Hero ──
    st.markdown("""
        <div class="hero-wrap">
            <p class="hero-title">🎬 CineMatch</p>
            <p class="hero-sub">Discover movies tailored to your taste</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    movies, similarity = load_data()

    # ── Search area ──
    selected_movie = st.selectbox(
        "CHOOSE A MOVIE",
        movies["title"].values,
        label_visibility="visible",
    )

    # rainbow glow bar
    st.markdown('<div class="glow-bar"></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Button ──
    if st.button("✦ Find Recommendations"):
        with st.spinner("Finding your next favourite movies..."):
            names, posters = recommend(selected_movie, movies, similarity)

        if names:
            st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
            st.markdown('<p class="results-label">✦ recommended for you</p>', unsafe_allow_html=True)

            cols = st.columns(len(names), gap="small")
            for col, name, poster in zip(cols, names, posters):
                with col:
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{poster}" alt="{name}"/>
                            <div class="movie-title">{name}</div>
                        </div>
                    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()