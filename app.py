import calendar
import hashlib
import hmac
import math
import re
import secrets
import sqlite3
from datetime import datetime
from statistics import mean

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Athlet Dashboard", page_icon="🏃", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background: #f5f7fa;
            color: #000000;
        }
        .stApp p,
        .stApp label,
        .stApp [data-testid="stMarkdownContainer"] {
            color: #000000;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3, h4 {
            color: #000000;
        }
        .main-header {
            background: #ffffff;
            border: 1px solid #e3e8ef;
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 18px;
            box-shadow: 0 8px 24px rgba(23, 32, 51, 0.06);
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            color: #000000;
        }
        .brand-mark {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 48px;
            height: 48px;
            border-radius: 14px;
            background: #d9f5e8;
            color: #16724d;
            font-size: 1.5rem;
            box-shadow: none;
        }
        .stMetric, [data-testid="stMetricValue"] {
            background: #ffffff;
            border: 1px solid #e3e8ef;
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: 0 6px 18px rgba(23, 32, 51, 0.05);
        }
        .stMetric [data-testid="stMetricLabel"] {
            color: #000000;
            font-weight: 600;
        }
        .stMetric [data-testid="stMetricValue"] {
            color: #16724d;
            font-weight: 800;
        }
        .stDataFrame {
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #e3e8ef;
        }
        div[data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid #e3e8ef;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 6px 18px rgba(23, 32, 51, 0.05);
        }
        .stProgress > div > div {
            background: #2fa66f;
        }
        .stAlert {
            background: #ffffff;
            border: 1px solid #e3e8ef;
        }
        .stTabs [role="tablist"] {
            gap: 8px;
            background: #ffffff;
            border: 1px solid #e3e8ef;
            border-radius: 12px;
            padding: 8px;
        }
        .stTabs [role="tab"] {
            min-height: 54px;
            border-radius: 8px;
            color: #000000;
            font-weight: 700;
        }
        .stTabs [role="tab"]:hover {
            background: #edf8f2;
            color: #16724d;
        }
        .stTabs [aria-selected="true"] {
            background: #d9f5e8;
            color: #16724d;
        }
        .sidebar-content {
            background: #ffffff;
        }
        section[data-testid="stSidebar"] button {
            background: #ffffff;
            color: #000000;
            border: 1px solid #cbd5e1;
        }
        section[data-testid="stSidebar"] button:hover {
            background: #f1f5f9;
            color: #000000;
            border-color: #94a3b8;
        }
        section[data-testid="stSidebar"] .st-key-logout_container button {
            background: #dc2626;
            color: #000000;
            border-color: #b91c1c;
        }
        section[data-testid="stSidebar"] .st-key-logout_container button:hover {
            background: #b91c1c;
            color: #000000;
        }
        div[data-testid="stForm"] button[kind="primary"],
        .stButton button[kind="primary"] {
            background: #dc2626;
            color: #000000;
            border-color: #b91c1c;
        }
        div[data-testid="stForm"] button[kind="primary"]:hover,
        .stButton button[kind="primary"]:hover {
            background: #b91c1c;
            color: #000000;
        }
        div[data-testid="stForm"] button[kind="secondary"] {
            background: #ffffff;
            color: #000000;
            border-color: #cbd5e1;
        }
        div[data-testid="stForm"] button[kind="secondary"]:hover {
            background: #f1f5f9;
            color: #000000;
            border-color: #94a3b8;
        }
        .login-success-flash {
            position: fixed;
            inset: 0;
            z-index: 9999;
            pointer-events: none;
            background: url("https://images.unsplash.com/photo-1530549387789-4c1017266635?auto=format&fit=crop&w=1800&q=90") center/cover;
            animation: champion-flash 3s ease-out forwards;
        }
        @keyframes champion-flash {
            0% { opacity: 0; }
            12% { opacity: 1; }
            82% { opacity: 1; }
            100% { opacity: 0; }
        }
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        .stApp {
            --auth-ink: #1d2927;
            --auth-muted: #78827d;
            --auth-line: #dce3dc;
            --auth-cream: #f6f8f3;
            --auth-white: #ffffff;
            --auth-leaf: #3b7558;
            --auth-leaf-dark: #2f513f;
            --auth-lime: #d4ec9c;
            --auth-orange: #ee9062;
            background: var(--auth-cream);
            font-family: "DM Sans", sans-serif;
        }
        .auth-reference-grid {
            min-height: calc(100vh - 3rem);
        }
        .auth-reference-visual {
            position: relative;
            min-height: 700px;
            overflow: hidden;
            padding: 42px 8.2vw 35px 5vw;
            color: #f3f6ed;
            background: linear-gradient(135deg, rgba(25, 60, 43, .82), rgba(25, 60, 43, .2)),
                url("https://images.unsplash.com/photo-1538805060514-97d9cc17730c?auto=format&fit=crop&w=1400&q=85") center/cover;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .auth-reference-visual::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(13, 42, 30, .2), rgba(13, 42, 30, .18) 52%, rgba(13, 42, 30, .75));
            pointer-events: none;
        }
        .auth-reference-visual > * {
            position: relative;
            z-index: 1;
        }
        .auth-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #ffffff;
            font-family: "Space Grotesk", sans-serif;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -.04em;
        }
        .auth-brand span:last-child span {
            color: var(--auth-lime);
        }
        .auth-brand-mark {
            display: inline-flex;
            align-items: end;
            gap: 3px;
            width: 25px;
            height: 22px;
            transform: skew(-18deg);
        }
        .auth-brand-mark span {
            display: block;
            width: 5px;
            border-radius: 4px 4px 1px 1px;
            background: var(--auth-lime);
        }
        .auth-brand-mark span:nth-child(1) { height: 12px; opacity: .65; }
        .auth-brand-mark span:nth-child(2) { height: 19px; }
        .auth-brand-mark span:nth-child(3) { height: 15px; opacity: .8; }
        .auth-visual-copy {
            max-width: 420px;
            margin: auto 0 13vh;
        }
        .auth-eyebrow {
            margin: 0 0 17px;
            color: var(--auth-lime);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .16em;
            text-transform: uppercase;
        }
        .auth-visual-copy h1,
        .auth-form-copy h2 {
            margin: 0;
            font-family: "Space Grotesk", sans-serif;
            letter-spacing: -.075em;
            line-height: .96;
        }
        .auth-visual-copy h1 {
            color: #f3f6ed;
            font-size: clamp(48px, 5.5vw, 78px);
            font-weight: 600;
        }
        .auth-visual-copy h1 em {
            color: var(--auth-lime);
            font-weight: 500;
        }
        .auth-visual-description {
            max-width: 305px;
            margin: 28px 0 0;
            color: rgba(243, 246, 237, .78);
            font-size: 14px;
            line-height: 1.65;
        }
        .auth-visual-footer {
            display: flex;
            align-items: center;
            gap: 17px;
            color: rgba(243, 246, 237, .66);
            font-size: 10px;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .auth-progress-track {
            width: 70px;
            height: 2px;
            background: rgba(255,255,255,.35);
        }
        .auth-progress-track span {
            display: block;
            width: 34%;
            height: 100%;
            background: var(--auth-lime);
        }
        div[data-testid="column"]:has(.auth-form-panel) {
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 50px 8vw 30px;
            background: var(--auth-cream);
        }
        .auth-form-wrap {
            width: min(100%, 390px);
            margin: auto;
        }
        .auth-form-copy h2 {
            color: var(--auth-ink);
            font-size: clamp(38px, 4vw, 52px);
            font-weight: 600;
        }
        .auth-form-copy > p:last-child {
            margin: 17px 0 38px;
            color: var(--auth-muted);
            font-size: 14px;
        }
        .auth-form-panel div[data-testid="stForm"] {
            padding: 0;
            border: 0;
            background: transparent;
            box-shadow: none;
        }
        .auth-form-panel div[data-testid="stTextInput"] label {
            display: block;
            margin: 0 0 9px;
            color: #4e5a54;
            font-size: 12px;
            font-weight: 700;
        }
        .auth-form-panel div[data-testid="stTextInput"] input {
            min-height: 48px;
            border: 1px solid var(--auth-line);
            border-radius: 4px;
            color: var(--auth-ink);
            background: var(--auth-white);
            font-size: 13px;
        }
        .auth-form-panel div[data-testid="stTextInput"] input:focus {
            border-color: var(--auth-leaf);
            box-shadow: 0 0 0 3px rgba(59,117,88,.1);
        }
        .auth-form-panel div[data-testid="stFormSubmitButton"] button {
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 50px;
            margin-top: 23px;
            padding: 16px 18px;
            border: 0;
            border-radius: 3px;
            color: #ffffff;
            background: var(--auth-leaf-dark);
            font-size: 12px;
            font-weight: 700;
        }
        .auth-form-panel div[data-testid="stFormSubmitButton"] button:hover {
            color: #ffffff;
            background: var(--auth-leaf);
        }
        .auth-form-panel > div[data-testid="stButton"] button {
            margin-top: 23px;
            padding: 0;
            border: 0;
            color: var(--auth-muted);
            background: transparent;
            font-size: 11px;
            font-weight: 700;
        }
        .auth-form-panel > div[data-testid="stButton"] button:hover {
            color: var(--auth-leaf-dark);
            text-decoration: underline;
        }
        @media (max-width: 850px) {
            .auth-reference-grid { min-height: auto; }
            .auth-reference-visual { min-height: 365px; padding: 28px 8vw 23px; }
            div[data-testid="column"]:has(.auth-form-panel) { min-height: 600px; padding: 42px 8vw 26px; }
        }
        @media (max-width: 520px) {
            .auth-reference-visual { min-height: 310px; }
            .auth-visual-copy { margin-top: 60px; margin-bottom: 0; }
            .auth-visual-description { display: none; }
            div[data-testid="column"]:has(.auth-form-panel) { min-height: 0; padding: 29px 24px 22px; }
        }
        @media (max-width: 600px) {
            .block-container {
                width: 100%;
                max-width: 100%;
                padding: 0 12px 24px;
            }
            div[data-testid="stHorizontalBlock"] {
                gap: 0.75rem;
            }
            .auth-reference-visual {
                min-height: 330px;
                padding: 25px 22px 22px;
                border-radius: 0 0 14px 14px;
            }
            .auth-brand {
                font-size: 16px;
            }
            .auth-visual-copy h1 {
                font-size: clamp(42px, 14vw, 62px);
            }
            div[data-testid="column"]:has(.auth-form-panel) {
                padding: 30px 22px 26px;
                border-radius: 14px;
            }
            .auth-form-copy h2 {
                font-size: 42px;
            }
            .auth-form-panel input,
            .auth-form-panel button {
                min-height: 50px;
            }
            div[data-testid="stFormSubmitButton"] button {
                min-height: 52px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

DEFAULT_PROFILES = {
    "demo": {
        "username": "demo@example.com",
        "email": "demo@example.com",
        "password": "demo123",
        "name": "Maria",
        "sport": "Swimming",
        "goal": "Open Water Race",
        "height": 165.0,
        "weekly_target": 12.5,
    }
}

SPORT_OPTIONS = [
    "Volly",
    "Run",
    "Bycling",
    "Basketball",
    "swimming",
    "football",
    "badminton",
    "weight lifting",
    "hocky",
    "yoga",
    "pilates",
]

DATABASE_PATH = "bioathletic.db"

FOOD_PRESETS = {
    "Junk food": {
        "Burger (1 porsi)": 310,
        "Pizza (1 slice)": 298,
        "Mie instan (1 bungkus)": 435,
        "Kentang goreng (1 porsi)": 275,
        "Nugget ayam (6 pc)": 250,
        "Donat (1 buah)": 200,
        "Hot dog (1 buah)": 270,
        "Keripik kentang (1 bungkus kecil)": 175,
        "Ayam goreng tepung (1 potong)": 350,
        "Sosis goreng (1 buah)": 150,
    },
    "Makanan Indonesia": {
        "Nasi putih (1 porsi)": 180,
        "Nasi goreng (1 porsi)": 350,
        "Mie goreng (1 porsi)": 400,
        "Sate ayam (10 tusuk)": 450,
        "Rendang (1 porsi)": 350,
        "Gado-gado (1 porsi)": 325,
        "Ketoprak (1 porsi)": 275,
        "Bakso (1 mangkok)": 300,
        "Soto ayam (1 mangkok)": 250,
        "Rawon (1 mangkok)": 300,
        "Pecel lele (1 porsi)": 450,
        "Ayam penyet (1 porsi)": 600,
        "Martabak telor (1 porsi)": 525,
        "Martabak manis (1 potong)": 350,
        "Pisang goreng (3 buah)": 225,
        "Risol (1 buah)": 175,
        "Pastel (1 buah)": 175,
        "Lemper (1 buah)": 165,
        "Onde-onde (1 buah)": 150,
        "Klepon (1 buah)": 90,
    },
    "Real food": {
        "Nasi merah (1 porsi)": 150,
        "Oatmeal (1 porsi)": 150,
        "Dada ayam bakar (100g)": 165,
        "Ikan salmon panggang (100g)": 200,
        "Ikan tuna (100g)": 130,
        "Telur rebus (1 butir)": 78,
        "Telur dadar (1 butir)": 100,
        "Tempe goreng (100g)": 200,
        "Tahu goreng (100g)": 150,
        "Brokoli rebus (100g)": 35,
        "Bayam rebus (100g)": 23,
        "Wortel mentah (100g)": 41,
        "Kentang rebus (1 buah)": 80,
        "Ubi jalar panggang (1 buah)": 125,
        "Alpukat (1/2 buah)": 160,
        "Pisang (1 buah)": 100,
        "Apel (1 buah)": 80,
        "Jeruk (1 buah)": 60,
        "Semangka (100g)": 30,
        "Yoghurt plain (1 cup)": 125,
        "Susu rendah lemak (1 gelas)": 120,
        "Kacang almond (20 gr)": 115,
        "Edamame rebus (100g)": 120,
        "Salad sayur (tanpa dressing)": 75,
        "Quinoa matang (1 porsi)": 222,
        "Greek yoghurt plain (1 cup)": 130,
        "Blueberries (1 cup)": 84,
        "Whole-grain toast (1 slice)": 100,
        "Peanut butter (1 tbsp)": 95,
        "Hummus (2 tbsp)": 70,
        "Chickpeas matang (100g)": 164,
        "Lentils matang (100g)": 116,
        "Tofu panggang (100g)": 144,
        "Shrimp panggang (100g)": 99,
        "Turkey breast (100g)": 135,
        "Olive oil (1 tbsp)": 119,
        "Mixed berries (1 cup)": 70,
    },
    "Sports fuel": {
        "Energy gel (1 sachet)": 100,
        "Sports drink (500 ml)": 120,
        "Protein shake (1 serving)": 180,
        "Granola (50g)": 230,
        "Peanut butter sandwich (1)": 350,
        "Banana and yoghurt bowl (1)": 240,
        "Chocolate milk (300 ml)": 220,
        "Trail mix (30g)": 150,
    },
    "Minuman": {
        "Air putih": 0,
        "Teh tawar": 3,
        "Kopi hitam": 4,
        "Jus jeruk (1 gelas)": 110,
        "Jus apel (1 gelas)": 120,
        "Susu murni (1 gelas)": 150,
        "Soda (1 kaleng)": 150,
        "Bubble tea (1 gelas)": 400,
        "Frappuccino (1 gelas)": 500,
    },
}


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return f"{salt}${digest.hex()}"


def password_matches(password: str, stored_hash: str) -> bool:
    try:
        salt, expected_digest = stored_hash.split("$", 1)
    except ValueError:
        return False
    actual_digest = hash_password(password, salt).split("$", 1)[1]
    return hmac.compare_digest(actual_digest, expected_digest)


def initialize_database():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                username TEXT PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                sport TEXT NOT NULL,
                goal TEXT NOT NULL,
                height REAL NOT NULL DEFAULT 0,
                weekly_target REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                date TEXT NOT NULL,
                name TEXT NOT NULL,
                sport TEXT NOT NULL,
                duration INTEGER NOT NULL,
                type TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES profiles(username)
            );
            CREATE TABLE IF NOT EXISTS food_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                date TEXT NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                servings REAL NOT NULL,
                calories INTEGER NOT NULL,
                FOREIGN KEY (username) REFERENCES profiles(username)
            );
            """
        )
        profile_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(profiles)").fetchall()
        }
        if "email" not in profile_columns:
            connection.execute("ALTER TABLE profiles ADD COLUMN email TEXT")
            connection.execute("UPDATE profiles SET email = username WHERE email IS NULL OR email = ''")
        if "height" not in profile_columns:
            connection.execute("ALTER TABLE profiles ADD COLUMN height REAL NOT NULL DEFAULT 0")
        demo = DEFAULT_PROFILES["demo"]
        connection.execute(
            """
            INSERT OR IGNORE INTO profiles
                (username, email, password_hash, name, sport, goal, height, weekly_target)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                demo["username"],
                demo["email"],
                hash_password(demo["password"]),
                demo["name"],
                demo["sport"],
                demo["goal"],
                demo["height"],
                demo["weekly_target"],
            ),
        )


def get_profile(username: str):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT username, name, sport, goal, height, weekly_target FROM profiles WHERE username = ?",
            (username,),
        ).fetchone()
    return dict(row) if row else None


def authenticate(username: str, password: str) -> str | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT username, password_hash FROM profiles WHERE email = ?",
            (username.strip(),),
        ).fetchone()
    if row and password_matches(password, row["password_hash"]):
        return row["username"]
    return None


def is_valid_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()))


def create_account(
    username: str,
    email: str,
    password: str,
    name: str,
    sport: str,
    goal: str,
    height: float,
    weekly_target: float,
):
    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO profiles
                    (username, email, password_hash, name, sport, goal, height, weekly_target)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    username.strip(),
                    email.strip(),
                    hash_password(password),
                    name,
                    sport,
                    goal,
                    height,
                    weekly_target,
                ),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def save_profile(username: str, profile: dict):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE profiles
            SET name = ?, sport = ?, goal = ?, height = ?, weekly_target = ?
            WHERE username = ?
            """,
            (
                profile["name"],
                profile["sport"],
                profile["goal"],
                profile["height"],
                profile["weekly_target"],
                username,
            ),
        )


def get_workouts(username: str):
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT date, name, sport, duration, type FROM workouts WHERE username = ? ORDER BY date",
            (username,),
        ).fetchall()
    return [dict(row) for row in rows]


def save_workout(username: str, workout: dict):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO workouts (username, date, name, sport, duration, type)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                workout["date"],
                workout["name"],
                workout["sport"],
                workout["duration"],
                workout["type"],
            ),
        )


def save_food_entry(username: str, entry: dict):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO food_entries (username, date, name, category, servings, calories)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                entry["date"],
                entry["name"],
                entry["category"],
                entry["servings"],
                entry["calories"],
            ),
        )


def get_food_entries(username: str):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT date, name, category, servings, calories
            FROM food_entries
            WHERE username = ?
            ORDER BY date DESC, id DESC
            """,
            (username,),
        ).fetchall()
    return [dict(row) for row in rows]


def render_assessment(status: str, detail: str, good: bool = False):
    if good:
        bg = "rgba(61, 217, 178, 0.12)"
        border = "rgba(61, 217, 178, 0.45)"
        text = "#d8fff1"
        label = "✅ Good"
    else:
        bg = "rgba(255, 104, 104, 0.12)"
        border = "rgba(255, 104, 104, 0.5)"
        text = "#ffdede"
        label = "⚠️ Needs attention"

    st.markdown(
        f"""
        <div style="margin-top: 12px; padding: 12px 14px; border-radius: 12px; border: 1px solid {border}; background: {bg}; color: {text};">
            <div style="font-weight: 700; margin-bottom: 6px;">{label} - {status}</div>
            <div>{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def weekly_progress_data(workouts):
    if not workouts:
        return pd.DataFrame({"week": [], "minutes": [], "target": []})

    df = pd.DataFrame(workouts)
    df["date"] = pd.to_datetime(df["date"])
    df["week_start"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit="D")
    weekly = df.groupby("week_start")["duration"].sum().reset_index()
    weekly["week"] = weekly["week_start"].dt.strftime("%Y-%m-%d")
    weekly = weekly[["week", "duration"]].rename(columns={"duration": "minutes"})
    weekly["target"] = 0
    return weekly.sort_values("week").reset_index(drop=True)


def default_workouts():
    now = datetime.now()
    year = now.year
    month = now.month
    return [
        {
            "date": f"{year}-{month:02d}-02",
            "name": "Tempo run",
            "sport": "Running",
            "duration": 45,
            "type": "Endurance",
        },
        {
            "date": f"{year}-{month:02d}-05",
            "name": "Strength session",
            "sport": "Running",
            "duration": 35,
            "type": "Strength",
        },
        {
            "date": f"{year}-{month:02d}-09",
            "name": "Recovery swim",
            "sport": "Swimming",
            "duration": 30,
            "type": "Recovery",
        },
        {
            "date": f"{year}-{month:02d}-14",
            "name": "Interval training",
            "sport": "Running",
            "duration": 50,
            "type": "Speed",
        },
        {
            "date": f"{year}-{month:02d}-18",
            "name": "Mobility",
            "sport": "General",
            "duration": 20,
            "type": "Mobility",
        },
    ]


def total_minutes_for_month(workouts, month, year):
    return sum(
        item["duration"]
        for item in workouts
        if datetime.strptime(item["date"], "%Y-%m-%d").month == month
        and datetime.strptime(item["date"], "%Y-%m-%d").year == year
    )


def render_calendar(year: int, month: int, workouts):
    month_calendar = calendar.monthcalendar(year, month)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    month_workouts = {}
    for workout in workouts:
        date = datetime.strptime(workout["date"], "%Y-%m-%d")
        if date.year == year and date.month == month:
            month_workouts.setdefault(date.day, []).append(workout)

    st.subheader(f"{calendar.month_name[month]} {year} training calendar")
    for name in day_names:
        st.write(f"**{name}**")

    columns = st.columns(7)
    for week in month_calendar:
        for i, day in enumerate(week):
            with columns[i]:
                if day == 0:
                    st.write("")
                    st.write("")
                    continue

                items = month_workouts.get(day, [])
                total = sum(item["duration"] for item in items)
                if items:
                    st.markdown(
                        f"<div style='border:1px solid #ddd; border-radius:10px; padding:8px; background:#eef7ff; min-height:110px;'>"
                        f"<b>{day}</b><br>"
                        f"{len(items)} session(s)<br>"
                        f"{total} min</div>",
                        unsafe_allow_html=True,
                    )
                    for item in items:
                        st.caption(f"• {item['name']} ({item['duration']} min)")
                else:
                    st.markdown(
                        f"<div style='border:1px solid #ddd; border-radius:10px; padding:8px; min-height:110px;'><b>{day}</b></div>",
                        unsafe_allow_html=True,
                    )


initialize_database()

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "auth_mode" not in st.session_state or st.session_state.auth_mode in (None, "welcome"):
    st.session_state.auth_mode = "login"
if "show_success_flash" not in st.session_state:
    st.session_state.show_success_flash = False

if st.session_state.current_user is None:
    if st.session_state.auth_mode == "login":
        visual_col, form_col = st.columns([47, 53], gap="small")
        with visual_col:
            st.markdown(
                """
                <section class="auth-reference-visual">
                    <header class="auth-brand">
                        <span class="auth-brand-mark" aria-hidden="true"><span></span><span></span><span></span></span>
                        <span>Bio<span>Athletic</span></span>
                    </header>
                    <div class="auth-visual-copy">
                        <p class="auth-eyebrow">Intelligence in motion</p>
                        <h1>Train your<br><em>whole</em> self.</h1>
                        <p class="auth-visual-description">A more considered approach to performance, recovery, and the everyday rituals that move you forward.</p>
                    </div>
                    <div class="auth-visual-footer">
                        <span>01 / 03</span>
                        <div class="auth-progress-track"><span></span></div>
                        <span>bioathletic.co</span>
                    </div>
                </section>
                """,
                unsafe_allow_html=True,
            )
        with form_col:
            st.markdown(
                """
                <section class="auth-form-panel">
                    <div class="auth-form-wrap">
                        <div class="auth-form-copy">
                            <p class="auth-eyebrow" style="color:#3b7558;">Member portal</p>
                            <h2>Welcome back.</h2>
                            <p>Sign in to continue your practice.</p>
                        </div>
                """,
                unsafe_allow_html=True,
            )
            with st.form("login_form"):
                email = st.text_input("Email address", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Enter member space  →", type="secondary", use_container_width=True)
                if submitted:
                    authenticated_username = authenticate(email, password)
                    if authenticated_username:
                        st.session_state.current_user = authenticated_username
                        st.session_state.show_success_flash = True
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
            st.markdown(
                """
                        <p class="auth-signup-copy">New to BioAthletic?</p>
                    </div>
                </section>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Create an account", key="login_create_account", type="secondary"):
                st.session_state.auth_mode = "signup"
                st.rerun()
            if st.button("← Return to sign in", key="login_back", type="secondary"):
                st.session_state.auth_mode = "login"
                st.rerun()
    else:
        if st.button("← Back to welcome", key="signup_back", type="secondary"):
            st.session_state.auth_mode = "login"
            st.rerun()
        st.subheader("Create your athlete profile")
        with st.form("signup_form"):
            new_username = st.text_input("Username", placeholder="Choose a username")
            new_email = st.text_input("Email address", placeholder="you@example.com")
            new_password = st.text_input("New password", type="password")
            new_goal = st.text_input("Goal", placeholder="e.g. Complete a 10K")
            new_height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=1.0)
            new_sport = st.selectbox("Sport", SPORT_OPTIONS)
            signup_submitted = st.form_submit_button("Create account", type="secondary", use_container_width=True)
            if signup_submitted:
                if not new_username or not new_email or not new_password:
                    st.warning("Username, email address, and password are required.")
                elif not is_valid_email(new_email):
                    st.warning("Enter a valid email address.")
                elif create_account(
                    new_username,
                    new_email,
                    new_password,
                    new_username,
                    new_sport,
                    new_goal or "General fitness",
                    float(new_height),
                    5.0,
                ) is False:
                    st.warning("That email address is already registered.")
                else:
                    st.session_state.current_user = new_email.strip()
                    st.session_state.show_success_flash = True
                    st.success("Profile created successfully.")
                    st.rerun()

    st.stop()


username = st.session_state.current_user
profile = get_profile(username)
workouts = get_workouts(username)
food_entries = get_food_entries(username)

if st.session_state.show_success_flash:
    st.markdown('<div class="login-success-flash" aria-hidden="true"></div>', unsafe_allow_html=True)
    st.session_state.show_success_flash = False

st.markdown(
    """
    <div class="main-header">
        <div class="brand">
            <span class="brand-mark">🏅</span>
            <span>BioAthletic</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Training intelligence for performance, recovery, and progress")

with st.sidebar:
    st.header("Profile management")
    with st.form("athlete_form"):
        updated_name = st.text_input("Name", value=profile["name"])
        sport_options = SPORT_OPTIONS if profile["sport"] in SPORT_OPTIONS else [profile["sport"], *SPORT_OPTIONS]
        updated_sport = st.selectbox("Sport", sport_options, index=sport_options.index(profile["sport"]))
        updated_goal = st.text_input("Goal", value=profile["goal"])
        updated_height = st.number_input(
            "Height (cm)", min_value=50.0, max_value=250.0, step=1.0, value=float(profile["height"] or 170.0)
        )
        updated_target = st.number_input(
            "Weekly target (hours)", min_value=0.0, step=0.5, value=float(profile["weekly_target"])
        )
        profile_submitted = st.form_submit_button("Save profile")
        if profile_submitted:
            profile.update(
                {
                    "name": updated_name,
                    "sport": updated_sport,
                    "goal": updated_goal,
                    "height": float(updated_height),
                    "weekly_target": float(updated_target),
                }
            )
            save_profile(username, profile)
            st.success("Profile saved.")

    st.header("Add workout")
    with st.form("workout_form"):
        workout_name = st.text_input("Workout name", "Tempo run")
        workout_date = st.date_input("Date")
        duration = st.number_input("Duration (minutes)", min_value=10, step=5, value=45)
        workout_type = st.selectbox("Type", ["Endurance", "Strength", "Speed", "Recovery", "Mobility"])
        submitted = st.form_submit_button("Add workout")
        if submitted:
            workouts.append(
                {
                    "date": workout_date.isoformat(),
                    "name": workout_name,
                    "sport": profile["sport"],
                    "duration": int(duration),
                    "type": workout_type,
                }
            )
            save_workout(username, workouts[-1])
            st.success("Workout added.")

    with st.container(key="logout_container"):
        if st.button("Logout", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()


current_month = datetime.now().month
current_year = datetime.now().year
summary = {
    "total_sessions": len(workouts),
    "monthly_minutes": total_minutes_for_month(workouts, current_month, current_year),
    "monthly_hours": round(total_minutes_for_month(workouts, current_month, current_year) / 60, 1),
    "weekly_target_minutes": profile["weekly_target"] * 60,
}
today_iso = datetime.now().date().isoformat()
today_food_entries = [entry for entry in food_entries if entry["date"] == today_iso]
today_calories = sum(entry["calories"] for entry in today_food_entries)

profile_photo = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=400&q=80"
profile_col, leaderboard_col = st.columns([1.4, 1.2])

with profile_col:
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.09); border-radius: 18px; padding: 18px; box-shadow: 0 10px 24px rgba(0,0,0,0.18);">
            <div style="display: flex; align-items: center; gap: 16px;">
                <img src="{}" style="width: 90px; height: 90px; object-fit: cover; border-radius: 50%; border: 3px solid #7ce5c7;" />
                <div>
                    <div style="font-size: 1.2rem; font-weight: 700;">{}</div>
                    <div style="color: #000000;">{}</div>
                    <div style="color: #16724d; font-weight: 600; margin-top: 6px;">Goal: {}</div>
                    <div style="color: #52605a; margin-top: 4px;">Height: {} cm</div>
                </div>
            </div>
        </div>
        """.format(profile_photo, profile["name"], profile["sport"], profile["goal"], profile["height"]),
        unsafe_allow_html=True,
    )

with leaderboard_col:
    team_df = pd.DataFrame(
        [
            {"Rank": 1, "Athlete": "Maria", "Minutes": 342},
            {"Rank": 2, "Athlete": "Omar", "Minutes": 298},
            {"Rank": 3, "Athlete": "Nia", "Minutes": 271},
            {"Rank": 4, "Athlete": "You", "Minutes": int(sum(item["duration"] for item in workouts))},
        ]
    )
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.09); border-radius: 18px; padding: 18px; box-shadow: 0 10px 24px rgba(0,0,0,0.18);">
            <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 10px;">🏆 Team leaderboard</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(team_df, hide_index=True, use_container_width=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Athlete", profile["name"])
col2.metric("Sport", profile["sport"])
col3.metric("Goal", profile["goal"])
col4.metric("Height", f"{profile['height']} cm")

col5, col6, col7 = st.columns(3)
col5.metric("Total sessions", summary["total_sessions"])
col6.metric("This month", f"{summary['monthly_hours']} h")
col7.metric("Weekly target", f"{profile['weekly_target']} h")

food_metric_col, food_note_col = st.columns([1, 2])
food_metric_col.metric("Today's calories", f"{today_calories:,} kcal")
food_note_col.caption(
    "Open the Makanan tab beside Math to set your commitment, add meals, and calculate your daily intake."
)

progress = min(summary["monthly_hours"] / max(profile["weekly_target"], 1), 1.0)
st.subheader("Progress toward goal")
st.progress(
    progress,
    text=f"Monthly progress: {summary['monthly_hours']} / {profile['weekly_target']} hours ({progress:.0%})",
)

weekly_chart_df = weekly_progress_data(workouts)
if weekly_chart_df.empty:
    st.info("Add workouts to see your weekly progress chart.")
else:
    weekly_chart_df["target"] = profile["weekly_target"] * 60
    st.subheader("Weekly target vs actual training")
    st.caption("Actual minutes per week compared with your planned target")
    st.line_chart(
        weekly_chart_df.set_index("week")[["minutes", "target"]].rename(
            columns={"minutes": "Actual minutes", "target": "Target minutes"}
        )
    )

render_calendar(current_year, current_month, workouts)

st.markdown("### Plan a workout")
st.caption("Choose a date and training focus. Your session will appear on the calendar and in your progress charts.")
with st.form("calendar_workout_form"):
    calendar_col1, calendar_col2, calendar_col3, calendar_col4 = st.columns([1.2, 1.2, 1.4, 0.8])
    with calendar_col1:
        planned_date = st.date_input("Training date", value=datetime.now().date(), key="calendar_date")
    with calendar_col2:
        planned_type = st.selectbox(
            "Training focus",
            ["Endurance", "Speed", "Strength", "Recovery", "Mobility", "Technique", "Other"],
            key="calendar_type",
        )
    with calendar_col3:
        planned_name = st.text_input("Workout name", value="Training session", key="calendar_name")
    with calendar_col4:
        planned_duration = st.number_input(
            "Minutes", min_value=10, max_value=600, step=5, value=45, key="calendar_duration"
        )
    calendar_submitted = st.form_submit_button("＋ Add to calendar", use_container_width=True)
    if calendar_submitted:
        if not planned_name.strip():
            st.warning("Add a workout name before saving.")
        else:
            save_workout(
                username,
                {
                    "date": planned_date.isoformat(),
                    "name": planned_name.strip(),
                    "sport": profile["sport"],
                    "duration": int(planned_duration),
                    "type": planned_type,
                },
            )
            st.success(f"{planned_type} workout added for {planned_date.strftime('%d %b %Y')}.")
            st.rerun()

st.subheader("Science & Performance Hub")

physics_tab, chemistry_tab, biology_tab, math_tab, performance_tab, food_tab = st.tabs(
    ["⚡ Physics", "💧 Chemistry", "🫀 Biology", "📐 Math", "🏅 Performance", "🍽️ Makanan"]
)

with physics_tab:
    st.markdown("### Power and movement")
    st.caption("Enter your movement data to evaluate power output.")
    mass_kg = st.number_input("Mass (kg)", min_value=1.0, value=70.0, key="physics_mass")
    velocity_m_s = st.number_input("Velocity (m/s)", min_value=0.0, value=8.0, key="physics_velocity")
    kinetic_energy = 0.5 * mass_kg * velocity_m_s ** 2
    st.metric("Kinetic Energy", f"{kinetic_energy:.2f} J")
    st.caption("Formula: Ek = 1/2 mv²")
    st.caption("Movement energy rises with both speed and mass.")
    if velocity_m_s < 5:
        render_assessment(
            "Low speed / power output",
            "Your movement output is below a strong training range. Prioritize sprint mechanics, acceleration work, and explosive strength sessions.",
        )
    else:
        render_assessment(
            "Good power output",
            "Speed is in a strong range for performance work. Maintain this with regular sprint and power sessions.",
            good=True,
        )

with chemistry_tab:
    st.markdown("### Hydration and heat")
    st.caption("Enter body and training conditions to estimate fluid needs.")
    body_weight = st.number_input("Body weight (kg)", min_value=20.0, value=70.0, key="chem_weight")
    sweat_loss = st.number_input("Sweat loss (L)", min_value=0.0, value=1.5, key="chem_sweat")
    heat = st.number_input("Temperature (°C)", min_value=10.0, value=28.0, key="chem_temp")
    hydration = body_weight * 0.033 + sweat_loss + max(0, heat - 25) * 0.1
    st.metric("Hydration Need", f"{hydration:.2f} L")
    st.caption("Formula: H = 0.033W + sweat loss + heat bonus")
    st.caption("Fluid replacement supports electrolyte balance and performance.")
    if hydration < 1.5:
        render_assessment(
            "Dehydration risk",
            "Your fluid target is low for training. Drink more water, add electrolytes, and hydrate before, during, and after training.",
        )
    elif hydration < 2.0:
        render_assessment(
            "Hydration is borderline",
            "Increase water intake and consider a sodium/electrolyte drink during hot or long sessions.",
        )
    else:
        render_assessment(
            "Good hydration plan",
            "Hydration support is solid. Maintain your fluid timing around training and long sessions.",
            good=True,
        )

with biology_tab:
    st.markdown("### Energy and recovery")
    st.caption("Use body data, heart rate, and weekly training to guide recovery and fueling.")
    age = st.number_input("Age", min_value=10, value=28, key="bio_age")
    weight_kg = st.number_input("Weight (kg)", min_value=20.0, value=70.0, key="bio_weight")
    height_cm = st.number_input("Height (cm)", min_value=100.0, value=175.0, key="bio_height")
    sex = st.selectbox("Sex", ["Male", "Female"], key="bio_sex")
    if sex == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    st.metric("BMR", f"{bmr:.0f} kcal/day")
    st.caption("Formula: BMR = 10W + 6.25H - 5A ± 5")
    st.caption("BMR estimates baseline calories at rest.")
    if bmr < 1400:
        render_assessment(
            "Low resting energy need",
            "Your baseline energy need is low for high training demands. Improve nutrition quality and total calorie intake to support recovery.",
        )
    elif bmr > 2200:
        render_assessment(
            "High baseline energy need",
            "Prioritize recovery with enough carbohydrates, protein, and calories around training.",
        )
    else:
        render_assessment(
            "Balanced energy profile",
            "Resting energy demand is supportive of sustained training. Keep consistent fueling and recovery habits.",
            good=True,
        )

    bmi = weight_kg / (height_cm / 100) ** 2
    st.metric("BMI", f"{bmi:.1f}")
    st.caption("Formula: BMI = weight / height². Use this as a screening estimate, not a diagnosis.")

    heart_rate_max = 208 - 0.7 * age
    zone_col1, zone_col2 = st.columns(2)
    with zone_col1:
        resting_hr = st.number_input("Resting heart rate (bpm)", min_value=30, max_value=120, value=60, key="bio_resting_hr")
    with zone_col2:
        training_zone = st.selectbox("Training zone", [1, 2, 3, 4, 5], index=1, key="bio_training_zone")
    heart_rate_low = resting_hr + (heart_rate_max - resting_hr) * (0.50 + (training_zone - 1) * 0.10)
    heart_rate_high = resting_hr + (heart_rate_max - resting_hr) * (0.60 + (training_zone - 1) * 0.10)
    st.metric("Recommended heart-rate range", f"{heart_rate_low:.0f}-{heart_rate_high:.0f} bpm")

    bio_col1, bio_col2 = st.columns(2)
    with bio_col1:
        weekly_minutes = st.number_input("Weekly training minutes", min_value=0, max_value=3000, value=180, key="bio_weekly_minutes")
    with bio_col2:
        session_rpe = st.slider("Session effort (RPE 1-10)", min_value=1, max_value=10, value=6, key="bio_session_rpe")
    training_load = weekly_minutes * session_rpe
    estimated_calories = max(0, training_load * 0.08 + (bmr * 0.15))
    st.metric("Weekly training load", f"{training_load:,} AU")
    st.metric("Estimated exercise calories", f"{estimated_calories:,.0f} kcal")
    st.caption("Training load = weekly minutes × perceived effort. Increase gradually and watch sudden spikes.")

with math_tab:
    st.markdown("### Sport performance calculator")
    st.caption("Choose a sport to calculate a useful performance metric.")
    sport_metric = st.selectbox("Sport metric", ["Running", "Football", "Basketball", "Fencing", "Swimming"], key="math_sport_metric")
    if sport_metric == "Football":
        passes_attempted = st.number_input("Passes attempted", min_value=1, value=40, key="math_passes_attempted")
        passes_completed = st.number_input("Passes completed", min_value=0, max_value=int(passes_attempted), value=min(34, int(passes_attempted)), key="math_passes_completed")
        distance_km = st.number_input("Distance covered (km)", min_value=0.0, value=8.0, key="math_football_distance")
        st.metric("Pass accuracy", f"{passes_completed / passes_attempted * 100:.1f}%")
        st.metric("Distance covered", f"{distance_km:.1f} km")
    elif sport_metric == "Basketball":
        field_goals_made = st.number_input("Field goals made", min_value=0, value=8, key="math_fg_made")
        field_goals_attempted = st.number_input("Field goals attempted", min_value=1, value=16, key="math_fg_attempted")
        points = st.number_input("Points scored", min_value=0, value=20, key="math_points")
        minutes_played = st.number_input("Minutes played", min_value=1.0, value=32.0, key="math_basketball_minutes")
        st.metric("Field-goal percentage", f"{field_goals_made / field_goals_attempted * 100:.1f}%")
        st.metric("Points per minute", f"{points / minutes_played:.2f}")
    elif sport_metric == "Fencing":
        attacks = st.number_input("Successful attacks", min_value=0, value=12, key="math_attacks")
        attempts = st.number_input("Attack attempts", min_value=1, value=20, key="math_attack_attempts")
        reaction_ms = st.number_input("Average reaction time (ms)", min_value=1, value=240, key="math_reaction")
        st.metric("Attack success rate", f"{attacks / attempts * 100:.1f}%")
        st.metric("Reaction time", f"{reaction_ms:.0f} ms")
    elif sport_metric == "Swimming":
        swim_distance = st.number_input("Distance (m)", min_value=25.0, value=100.0, key="math_swim_distance")
        swim_time = st.number_input("Time (seconds)", min_value=1.0, value=90.0, key="math_swim_time")
        strokes = st.number_input("Strokes", min_value=1, value=40, key="math_swim_strokes")
        st.metric("Pace per 100 m", f"{swim_time / swim_distance * 100:.1f} sec")
        st.metric("SWOLF", f"{swim_time / swim_distance * 100 + strokes:.0f}")
    else:
        distance_km = st.number_input("Distance (km)", min_value=0.1, value=5.0, key="math_distance")
        time_min = st.number_input("Time (min)", min_value=1.0, value=30.0, key="math_time")
        speed_kmh = distance_km / (time_min / 60)
        st.metric("Speed", f"{speed_kmh:.2f} km/h")
        st.metric("Pace", f"{time_min / distance_km:.2f} min/km")
        st.caption("Formula: speed = distance / time")
        if speed_kmh < 6:
            render_assessment("Low pace efficiency", "Focus on endurance pacing, cadence work, and progressive tempo sessions.")
        else:
            render_assessment("Solid pace output", "Keep increasing volume with controlled intensity.", good=True)

with performance_tab:
    st.markdown("### Performance math calculator")
    st.caption("Use recent results to estimate pace, target times, and training progression.")
    performance_col1, performance_col2 = st.columns(2)
    with performance_col1:
        recent_distance = st.number_input("Recent distance (km)", min_value=0.4, value=5.0, key="performance_distance")
        recent_time = st.number_input("Recent time (minutes)", min_value=1.0, value=30.0, key="performance_time")
        target_distance = st.number_input("Target distance (km)", min_value=0.4, value=10.0, key="performance_target_distance")
    with performance_col2:
        weekly_load_now = st.number_input("Current weekly load (minutes)", min_value=0, value=180, key="performance_load_now")
        weekly_load_previous = st.number_input("Previous weekly load (minutes)", min_value=0, value=160, key="performance_load_previous")
        goal_time = st.number_input("Goal time (minutes)", min_value=1.0, value=55.0, key="performance_goal_time")

    recent_pace = recent_time / recent_distance
    riegel_time = recent_time * (target_distance / recent_distance) ** 1.06
    pace_gap = max(0.0, riegel_time - goal_time)
    load_change = 0.0 if weekly_load_previous == 0 else (weekly_load_now - weekly_load_previous) / weekly_load_previous * 100
    st.metric("Current pace", f"{recent_pace:.2f} min/km")
    st.metric("Estimated target time", f"{riegel_time:.1f} min")
    st.metric("Goal pace gap", f"{pace_gap:.1f} min")
    st.metric("Weekly load change", f"{load_change:+.1f}%")
    st.caption("Target estimate uses the Riegel prediction: new time = recent time × (new distance / recent distance)^1.06.")
    if load_change > 20:
        render_assessment(
            "Training-load spike",
            "Your weekly load increased by more than 20%. Consider adding recovery before increasing intensity again.",
        )
    elif pace_gap <= 0:
        render_assessment(
            "Goal pace is within reach",
            "Your estimated target time meets or beats the goal. Keep building consistency and protect recovery.",
            good=True,
        )
    else:
        render_assessment(
            "Progressive target",
            f"You are approximately {pace_gap:.1f} minutes from the goal at this distance. Use controlled tempo sessions to close the gap.",
        )

with food_tab:
    st.markdown("### Daily nutrition planner")
    st.caption("Set your commitment first, then add meals one by one before calculating your daily intake.")
    commitment_key = f"food_commitment_{username}"

    if not st.session_state.get(commitment_key):
        st.info(f"Your current performance goal is: {profile['goal']}")
        with st.form("food_commitment_form"):
            commitment = st.text_area(
                "Your nutrition commitment",
                value=f"I will choose food that supports my goal: {profile['goal']}",
                height=90,
            )
            commitment_submitted = st.form_submit_button("Save commitment and open food list")
            if commitment_submitted:
                if commitment.strip():
                    st.session_state[commitment_key] = commitment.strip()
                    st.rerun()
                st.warning("Write a commitment before opening the food calculator.")
    else:
        st.success(f"Commitment: {st.session_state[commitment_key]}")
        food_date = st.date_input("Food log date", value=datetime.now().date(), key="food_log_date")
        selected_date = food_date.isoformat()
        selected_entries = [entry for entry in food_entries if entry["date"] == selected_date]

        input_mode = st.radio(
            "Calorie input",
            ["Choose from food list", "Input calories myself"],
            horizontal=True,
            key="food_input_mode",
        )
        with st.form("food_item_form"):
            if input_mode == "Input calories myself":
                food_category = st.selectbox(
                    "Category",
                    list(FOOD_PRESETS) + ["Others"],
                    key="manual_food_category",
                )
                food_name = st.text_input("Food and drink name", key="custom_food_name")
                custom_category = food_category
                calories_per_serving = st.number_input(
                    "Calories for this food or drink (kcal)",
                    min_value=0,
                    max_value=3000,
                    step=5,
                    value=200,
                    key="custom_food_calories",
                )
                st.caption("Manual mode: type the food name and calorie number yourself. No preset food list is used.")
            else:
                food_category = st.selectbox("Category", list(FOOD_PRESETS), key="preset_food_category")
                food_name = st.selectbox("Food or drink", list(FOOD_PRESETS[food_category]), key="preset_food_name")
                custom_category = food_category
                calories_per_serving = FOOD_PRESETS[food_category][food_name]
                st.caption(f"Preset estimate: {calories_per_serving} kcal per serving")
            servings = st.number_input("Servings", min_value=0.25, max_value=20.0, step=0.25, value=1.0, key="food_servings")
            item_calories = round(calories_per_serving * servings)
            st.metric("Item calories", f"{item_calories} kcal")
            add_food_item = st.form_submit_button("＋ Add food item")
            if add_food_item:
                if not food_name.strip():
                    st.warning("Enter a food or drink name.")
                else:
                    save_food_entry(
                        username,
                        {
                            "date": selected_date,
                            "name": food_name.strip(),
                            "category": custom_category,
                            "servings": float(servings),
                            "calories": item_calories,
                        },
                    )
                    st.rerun()

        if selected_entries:
            st.markdown("#### Today's food list")
            for index, entry in enumerate(selected_entries, start=1):
                st.write(f"{index}. **{entry['name']}** ({entry['calories']} kcal) · {entry['category']}")
            calculate_food = st.button("Calculate daily calories", type="primary", use_container_width=True)
            if calculate_food:
                calculated_calories = sum(entry["calories"] for entry in selected_entries)
                junk_categories = {"Junk food", "Soda"}
                junk_items = [entry["name"] for entry in selected_entries if entry["category"] in junk_categories]
                st.metric(f"Total calories for {food_date.strftime('%d %b %Y')}", f"{calculated_calories:,} kcal")
                if junk_items:
                    st.error(
                        f"Nutrition reminder: {', '.join(junk_items)} may not support your goal '{profile['goal']}'. Choose water, real food, or a balanced meal next."
                    )
                elif calculated_calories > 3000:
                    st.warning(
                        "Your logged intake is high for this day. Review portion sizes and balance energy-dense foods with training demand."
                    )
                else:
                    st.success(f"Your food choices are currently aligned with your goal: {profile['goal']}.")
        else:
            st.info("No food items for this date yet. Add your first item above.")

st.subheader("Recent workouts")
workout_df = pd.DataFrame(workouts)
if not workout_df.empty:
    workout_df = workout_df.sort_values("date", ascending=False)
    workout_df["date"] = pd.to_datetime(workout_df["date"]).dt.strftime("%Y-%m-%d")
    st.dataframe(workout_df[["date", "name", "type", "duration", "sport"]], use_container_width=True)
else:
    st.info("No workouts logged yet.")

st.subheader("Recent food")
food_df = pd.DataFrame(food_entries)
if not food_df.empty:
    food_df = food_df.rename(
        columns={"date": "Date", "name": "Food / drink", "category": "Category", "servings": "Servings", "calories": "Calories (kcal)"}
    )
    st.dataframe(
        food_df[["Date", "Food / drink", "Category", "Servings", "Calories (kcal)"]],
        hide_index=True,
        use_container_width=True,
    )
else:
    st.info("No food entries yet. Add your first meal from the Makanan panel.")
