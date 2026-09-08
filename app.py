import calendar
import hashlib
import hmac
import math
import secrets
import sqlite3
from datetime import datetime
from statistics import mean

import pandas as pd
import streamlit as st

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
        .auth-page {
            max-width: 1120px;
            margin: 0 auto;
        }
        .auth-hero {
            min-height: 360px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 34px;
            border-radius: 24px;
            overflow: hidden;
            background: linear-gradient(90deg, rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0.55)),
                url("https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1600&q=85") center/cover;
            box-shadow: 0 20px 45px rgba(3, 12, 24, 0.4);
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
        .auth-kicker {
            color: #000000;
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }
        .auth-title {
            max-width: 620px;
            margin: 8px 0;
            color: #000000;
            font-size: clamp(2.2rem, 5vw, 4.6rem);
            line-height: 0.98;
            font-weight: 850;
        }
        .auth-copy {
            max-width: 520px;
            margin: 0;
            color: #000000;
            font-size: 1.05rem;
        }
        .auth-choice {
            padding: 20px 22px 8px;
            text-align: center;
        }
        .auth-choice h3 {
            margin-bottom: 4px;
            color: #000000;
        }
        .auth-choice p {
            color: #000000;
            margin-bottom: 0;
        }
        @media (max-width: 700px) {
            .auth-hero {
                min-height: 410px;
                padding: 24px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

DEFAULT_PROFILES = {
    "demo": {
        "username": "demo",
        "password": "demo123",
        "name": "Maria",
        "sport": "Swimming",
        "goal": "Open Water Race",
        "weekly_target": 12.5,
    }
}

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
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                sport TEXT NOT NULL,
                goal TEXT NOT NULL,
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
        demo = DEFAULT_PROFILES["demo"]
        connection.execute(
            """
            INSERT OR IGNORE INTO profiles
                (username, password_hash, name, sport, goal, weekly_target)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                demo["username"],
                hash_password(demo["password"]),
                demo["name"],
                demo["sport"],
                demo["goal"],
                demo["weekly_target"],
            ),
        )


def get_profile(username: str):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT username, name, sport, goal, weekly_target FROM profiles WHERE username = ?",
            (username,),
        ).fetchone()
    return dict(row) if row else None


def authenticate(username: str, password: str) -> bool:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT password_hash FROM profiles WHERE username = ?",
            (username.strip(),),
        ).fetchone()
    return bool(row and password_matches(password, row["password_hash"]))


def create_account(username: str, password: str, name: str, sport: str, goal: str, weekly_target: float):
    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO profiles
                    (username, password_hash, name, sport, goal, weekly_target)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    username.strip(),
                    hash_password(password),
                    name,
                    sport,
                    goal,
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
            SET name = ?, sport = ?, goal = ?, weekly_target = ?
            WHERE username = ?
            """,
            (profile["name"], profile["sport"], profile["goal"], profile["weekly_target"], username),
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


st.set_page_config(page_title="Athlet Dashboard", page_icon="🏃", layout="wide")

initialize_database()

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = None
if "show_success_flash" not in st.session_state:
    st.session_state.show_success_flash = False

if st.session_state.current_user is None:
    st.markdown('<div class="auth-page">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="auth-hero">
            <div class="auth-kicker">BioAthletic performance club</div>
            <div class="auth-title">Run your strongest season.</div>
            <p class="auth-copy">Track the work, protect your recovery, and turn every session into forward motion.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.auth_mode is None:
        st.markdown(
            """
            <div class="auth-choice">
                <h3>Welcome to your training space</h3>
                <p>Choose how you want to continue.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        login_col, signup_col = st.columns(2)
        with login_col:
            st.markdown(
                '<div class="auth-choice"><h3>Already training with us?</h3><p>Pick up where you left off.</p></div>',
                unsafe_allow_html=True,
            )
            if st.button("Log in", type="primary", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
        with signup_col:
            st.markdown(
                '<div class="auth-choice"><h3>Starting your journey?</h3><p>Build your athlete profile.</p></div>',
                unsafe_allow_html=True,
            )
            if st.button("Create profile", type="primary", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()
    elif st.session_state.auth_mode == "login":
        if st.button("← Back to welcome", key="login_back", type="secondary"):
            st.session_state.auth_mode = None
            st.rerun()
        st.subheader("Log in to your training space")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in", type="secondary", use_container_width=True)
            if submitted:
                if authenticate(username, password):
                    st.session_state.current_user = username.strip()
                    st.session_state.show_success_flash = True
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    else:
        if st.button("← Back to welcome", key="signup_back", type="secondary"):
            st.session_state.auth_mode = None
            st.rerun()
        st.subheader("Create your athlete profile")
        with st.form("signup_form"):
            new_username = st.text_input("New username")
            new_password = st.text_input("New password", type="password")
            new_name = st.text_input("Full name")
            new_sport = st.text_input("Sport")
            new_goal = st.text_input("Goal")
            new_target = st.number_input("Weekly target (hours)", min_value=0.0, step=0.5, value=5.0)
            signup_submitted = st.form_submit_button("Create", type="secondary", use_container_width=True)
            if signup_submitted:
                if not new_username or not new_password:
                    st.warning("Username and password are required.")
                elif create_account(
                    new_username,
                    new_password,
                    new_name or new_username,
                    new_sport or "General fitness",
                    new_goal or "General fitness",
                    float(new_target),
                ) is False:
                    st.warning("That username already exists.")
                else:
                    st.session_state.current_user = new_username.strip()
                    st.session_state.show_success_flash = True
                    st.success("Profile created successfully.")
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

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
        updated_sport = st.text_input("Sport", value=profile["sport"])
        updated_goal = st.text_input("Goal", value=profile["goal"])
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
                </div>
            </div>
        </div>
        """.format(profile_photo, profile["name"], profile["sport"], profile["goal"]),
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

col1, col2, col3 = st.columns(3)
col1.metric("Athlete", profile["name"])
col2.metric("Sport", profile["sport"])
col3.metric("Goal", profile["goal"])

col4, col5, col6 = st.columns(3)
col4.metric("Total sessions", summary["total_sessions"])
col5.metric("This month", f"{summary['monthly_hours']} h")
col6.metric("Weekly target", f"{profile['weekly_target']} h")

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

physics_tab, chemistry_tab, biology_tab, math_tab, food_tab = st.tabs(
    ["⚡ Physics", "💧 Chemistry", "🫀 Biology", "📐 Math", "🍽️ Makanan"]
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
    st.caption("Estimate your baseline energy needs before planning training fuel.")
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

with math_tab:
    st.markdown("### Pace and performance")
    st.caption("Use distance and time to evaluate training pace.")
    distance_km = st.number_input("Distance (km)", min_value=0.1, value=5.0, key="math_distance")
    time_min = st.number_input("Time (min)", min_value=1.0, value=30.0, key="math_time")
    speed_kmh = distance_km / (time_min / 60)
    st.metric("Speed", f"{speed_kmh:.2f} km/h")
    st.caption("Formula: speed = distance / time")
    st.caption("Use pace trends to guide endurance and tempo work.")
    if speed_kmh < 6:
        render_assessment(
            "Low pace efficiency",
            "Your pace is below the training target. Focus on endurance pacing, cadence work, and progressive tempo sessions.",
        )
    else:
        render_assessment(
            "Solid pace output",
            "Your speed is in a good performance range. Keep increasing volume with controlled intensity.",
            good=True,
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
