import os, sys, re, argparse, requests, pandas as pd
from typing import Optional, Tuple, Dict, List
from flask import Flask, request, jsonify
import google.generativeai as genai

# Configuration & one‑time initialisation
LOCAL_DATA_PATH = "processed_local_data.csv"     # artist_name,artist_id

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    sys.exit("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=GOOGLE_API_KEY)

SPOTIFY_CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
if not (SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET):
    sys.exit("ßPlease export SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.")

AUTH_URL       = "https://accounts.spotify.com/api/token"
TOP_TRACKS_URL = "https://api.spotify.com/v1/artists/{artist_id}/top-tracks"

gemini_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config=genai.GenerationConfig(temperature=0.7),
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ],
)

# 1.  Load the CSV once → dict {artist_name_lower : artist_id}
def load_artist_map(csv_path: str) -> Dict[str, str]:
    if not os.path.exists(csv_path):
        print(f"⚠️  Artist CSV '{csv_path}' not found - music feature disabled.", file=sys.stderr)
        return {}
    df = pd.read_csv(csv_path)
    if not {"artist_name", "artist_id"}.issubset(df.columns):
        raise ValueError("CSV must have 'artist_name' and 'artist_id' headers.")
    
    # NEW – make *both* columns clean
    df["artist_name"] = df["artist_name"].str.strip().str.lower()
    df["artist_id"]   = df["artist_id"].str.strip()

    # build {lower_name : id}
    return dict(zip(df["artist_name"], df["artist_id"]))
ARTIST_MAP: Dict[str, str] = load_artist_map(LOCAL_DATA_PATH)

# 2.  Spotify helpers
def _get_spotify_token() -> str:
    resp = requests.post(
        AUTH_URL,
        data={"grant_type": "client_credentials"},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
        timeout=8,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

def fetch_top_tracks(artist_id: str, market: str = "US", n: int = 10) -> List[Dict]:
    token = _get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        TOP_TRACKS_URL.format(artist_id=artist_id),
        headers=headers,
        params={"market": market},
        timeout=8,
    )
    resp.raise_for_status()
    return resp.json().get("tracks", [])[:n]
def format_tracks(artist_name: str, tracks: List[Dict]) -> str:
    if not tracks:
        return f"I couldn't find any top songs for **{artist_name}**."
    lines = [f"**Most-streamed songs by {artist_name.title()}**"]
    for i, t in enumerate(tracks, 1):
        lines.append(f"{i:2}. {t['name']}  -  {t['album']['name']}")
    return "\n".join(lines)

# 3.  Tiny intent recogniser
MUSIC_PAT = re.compile(
    r"""
    (?P<prefix>top\s+(?:songs|tracks)\s+by\s+|                     # “top songs by …”
       best\s+(?:songs|tracks)\s+by\s+|
       what\s+are\s+(?:the\s+)?(?:most\s+)?popular\s+(?:songs|tracks)\s+by\s+)  # etc.
    (?P<artist>.+)$
    """,
    re.I | re.VERBOSE,
)

def detect_music_request(msg: str) -> Optional[str]:
    """Return artist string if this looks like a ‘top songs’ message, else None."""
    m = MUSIC_PAT.search(msg.strip())
    return m.group("artist").strip() if m else None

# 4.  Chatbot routing – decide music vs general chat
def get_response(user_msg: str) -> str:
    artist_raw = detect_music_request(user_msg)
    if artist_raw:
        artist_key = artist_raw.lower()
        artist_id = ARTIST_MAP.get(artist_key)
        if not artist_id:
            return (
                f"Sorry, I don’t have **{artist_raw}** in my local artist list yet. "
                "Try another artist or update the CSV."
            )
        try:
            tracks = fetch_top_tracks(artist_id)
            return format_tracks(artist_raw, tracks)
        except requests.HTTPError as e:
            return f"Spotify error: {e.response.status_code} – {e.response.text}"
        except Exception as e:
            return f"Unexpected error calling Spotify: {e}"

    try:
        gemini_reply = gemini_model.generate_content(user_msg)
        return "".join(p.text for p in gemini_reply.parts) if gemini_reply.parts else "(no response)"
    except Exception as e:
        return f"Gemini error: {e}"

# 5.  Flask app
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    json_in = request.get_json(silent=True)
    if not (json_in and isinstance(json_in.get("message"), str)):
        return jsonify({"error": "POST JSON with ‘message’: <string> required."}), 400
    reply = get_response(json_in["message"])
    return jsonify({"response": reply})

@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running."

# ------------------------------------------------------------
# 6.  CLI (run server or ETL)
# ------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify‑Gemini chatbot demo.")
    parser.add_argument("--run-etl", action="store_true", help="(placeholder) run ETL then exit")
    args = parser.parse_args()

    if args.run_etl:
        from your_module_name import run_etl_pipeline   # keep your existing ETL functions
        run_etl_pipeline()
    else:
        app.run(host="0.0.0.0", port=5001, debug=True)