import calendar
from html import escape
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
        .nutrition-commitment-card {
            margin: 12px 0 20px;
            padding: 18px 20px;
            border: 1px solid #b8dcbc;
            border-left: 5px solid #77b982;
            border-radius: 10px;
            background: #e4f4e3;
            color: #23452d;
            box-shadow: 0 6px 18px rgba(59, 117, 88, 0.1);
        }
        div[data-testid="stTextArea"] textarea {
            background: #f0faef;
            border-color: #b8dcbc;
            color: #23452d;
        }
        .nutrition-commitment-label {
            margin-bottom: 7px;
            color: #356342 !important;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .nutrition-commitment-text {
            color: #23452d !important;
            font-size: 1.05rem;
            font-weight: 600;
            line-height: 1.55;
        }
        .stApp .nutrition-commitment-card,
        .stApp .nutrition-commitment-card p,
        .stApp .nutrition-commitment-card [data-testid="stMarkdownContainer"] {
            color: #23452d !important;
        }
        .food-entry-panel {
            margin: 16px 0 8px;
            padding: 18px;
            border: 1px solid #eadfca;
            border-radius: 14px;
            background: linear-gradient(135deg, #fffaf0, #fffdf8);
            box-shadow: 0 8px 20px rgba(116, 82, 36, 0.08);
        }
        .food-entry-kicker {
            margin-bottom: 4px;
            color: #9a5b2b;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .food-entry-title {
            margin-bottom: 14px;
            color: #3b3024;
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
        }
        .food-input-card {
            padding: 12px 14px 4px;
            border: 1px solid #f0dfc3;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.78);
        }
        .food-input-card label {
            color: #594534 !important;
        }
        .nutrition-dashboard-card {
            margin: 22px 0 18px;
            padding: 24px 26px;
            border: 1px solid #c8e3c9;
            border-radius: 16px;
            background: #e8f5e9;
            color: #244b32;
            box-shadow: 0 8px 22px rgba(76, 120, 79, 0.1);
        }
        .nutrition-dashboard-card h3 {
            margin: 0 0 6px;
            color: #244b32;
        }
        .nutrition-dashboard-card p {
            margin: 0;
            color: #466a4f !important;
        }
        .nutrition-summary-card {
            min-height: 118px;
            padding: 16px;
            border: 1px solid #e1e8df;
            border-radius: 12px;
            background: #ffffff;
        }
        .nutrition-summary-label {
            color: #66736a;
            font-size: 0.82rem;
            font-weight: 700;
        }
        .nutrition-summary-value {
            margin: 7px 0;
            color: #244b32;
            font-size: 1.35rem;
            font-weight: 800;
        }
        .nutrition-summary-card .stProgress > div > div {
            background: #77b982;
        }
        .nutrition-action-card {
            padding: 16px;
            border: 1px solid #eadfca;
            border-radius: 12px;
            background: #fffaf0;
        }
        .stApp .st-key-food_item_form label,
        .stApp .st-key-food_item_form [data-testid="stWidgetLabel"],
        .stApp .st-key-food_item_form [data-testid="stMarkdownContainer"],
        .stApp .st-key-food_item_form [data-testid="stMarkdownContainer"] p,
        .stApp .st-key-food_item_form [role="radiogroup"] label,
        .stApp .st-key-food_item_form [data-baseweb="select"] {
            color: #594534 !important;
        }
        .stApp .st-key-food_item_form [role="option"] {
            color: #594534 !important;
            background: #fffdf8;
        }
        .stApp .st-key-food_item_form [role="option"][aria-selected="true"] {
            color: #ffffff !important;
            background: #9a5b2b;
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

SPORT_PHOTOS = {
    "volly": "https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?auto=format&fit=crop&w=600&q=85",
    "run": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&w=600&q=85",
    "bycling": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=600&q=85",
    "basketball": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=600&q=85",
    "swimming": "https://images.unsplash.com/photo-1530549387789-4c1017266635?auto=format&fit=crop&w=600&q=85",
    "football": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=600&q=85",
    "badminton": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=600&q=85",
    "weight lifting": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=600&q=85",
    "hocky": "https://images.unsplash.com/photo-1515703407324-5f753afd8be8?auto=format&fit=crop&w=600&q=85",
    "yoga": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=600&q=85",
    "pilates": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=600&q=85",
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

DRINK_PRESETS = {
    "Water and hydration": {
        "Water": 0,
        "Mineral water": 0,
        "Coconut water (250 ml)": 45,
        "Electrolyte tablet drink (500 ml)": 10,
        "Low-sugar electrolyte drink (500 ml)": 40,
    },
    "Tea and coffee": {
        "Unsweetened tea": 3,
        "Black coffee": 4,
        "Green tea": 2,
        "Milk tea (250 ml)": 120,
    },
    "Milk and recovery": {
        "Whole milk (250 ml)": 150,
        "Low-fat milk (250 ml)": 120,
        "Kefir (250 ml)": 140,
        "Protein shake (1 serving)": 180,
        "Chocolate milk (300 ml)": 220,
    },
    "Juice and occasional drinks": {
        "Orange juice (250 ml)": 110,
        "Apple juice (250 ml)": 120,
        "Soda (1 can)": 150,
        "Bubble tea (1 cup)": 400,
        "Frappuccino (1 cup)": 500,
    },
    "Previous drink list": {
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

FOOD_PRESETS.update(
    {
        "High-protein foods": {
            "Chicken breast (100 g)": 165,
            "Lean beef (100 g)": 190,
            "Salmon (100 g)": 200,
            "Tuna (100 g)": 130,
            "Greek yogurt (1 cup)": 130,
            "Cottage cheese (1 cup)": 210,
            "Egg whites (3)": 51,
            "Lentils (100 g cooked)": 116,
            "Chickpeas (100 g cooked)": 164,
            "Seitan (100 g)": 141,
        },
        "Carbohydrate foods": {
            "White rice (1 cup)": 205,
            "Brown rice (1 cup)": 215,
            "Pasta (1 cup cooked)": 220,
            "Sweet potato (1 medium)": 112,
            "Bagel (1)": 280,
            "Rice cakes (2)": 70,
            "Dates (3)": 200,
            "Corn tortilla (2)": 104,
        },
        "Healthy fats": {
            "Avocado (1/2)": 160,
            "Almonds (20 g)": 115,
            "Walnuts (20 g)": 131,
            "Chia seeds (1 tbsp)": 60,
            "Flax seeds (1 tbsp)": 37,
            "Tahini (1 tbsp)": 89,
            "Olive oil (1 tbsp)": 119,
        },
        "Vegetables and fruit": {
            "Broccoli (100 g)": 35,
            "Spinach (100 g)": 23,
            "Carrot (100 g)": 41,
            "Bell pepper (100 g)": 31,
            "Tomato (1 medium)": 22,
            "Apple (1)": 80,
            "Banana (1)": 100,
            "Mango (1 cup)": 99,
            "Berries (1 cup)": 84,
        },
    }
)

FOOD_CATEGORY_GROUPS = {
    "Vegetables": {
        "Broccoli (100 g)": 34,
        "Spinach (100 g)": 23,
        "Cauliflower (100 g)": 25,
        "Carrot (100 g)": 41,
        "Bell pepper (100 g)": 31,
        "Cucumber (100 g)": 15,
        "Tomato (100 g)": 18,
        "Mushrooms (100 g)": 22,
        "Zucchini (100 g)": 17,
    },
    "Healthy fats": FOOD_PRESETS["Healthy fats"].copy(),
    "Fruit": {
        "Apple (100 g)": 52,
        "Banana (100 g)": 89,
        "Orange (100 g)": 47,
        "Mango (100 g)": 60,
        "Pineapple (100 g)": 50,
        "Watermelon (100 g)": 30,
        "Grapes (100 g)": 69,
        "Strawberries (100 g)": 32,
        "Blueberries (100 g)": 57,
        "Papaya (100 g)": 43,
        "Dates (100 g)": 282,
    },
    "Carbohydrate & grains": FOOD_PRESETS["Carbohydrate foods"].copy(),
    "Plant protein": {
        "Tofu (100 g)": 76,
        "Tempeh (100 g)": 195,
        "Edamame (100 g)": 121,
        "Lentils, cooked (100 g)": 116,
        "Chickpeas, cooked (100 g)": 164,
        "Black beans, cooked (100 g)": 132,
        "Green peas (100 g)": 84,
        "Seitan (100 g)": 141,
    },
    "Eggs & dairy": {
        "Whole egg (1 large)": 72,
        "Egg white (100 g)": 52,
        "Greek yogurt (100 g)": 59,
        "Skyr (100 g)": 63,
        "Cottage cheese (100 g)": 98,
        "Whole milk (250 ml)": 153,
        "Low-fat milk (250 ml)": 105,
        "Cheddar (100 g)": 403,
        "Mozzarella (100 g)": 280,
    },
    "Protein": FOOD_PRESETS["High-protein foods"].copy(),
    "Seafood & meat": {
        "Chicken breast (100 g)": 165,
        "Turkey breast (100 g)": 135,
        "Lean beef (100 g)": 200,
        "Pork tenderloin (100 g)": 143,
        "Lamb (100 g)": 250,
        "Salmon (100 g)": 208,
        "Tuna (100 g)": 132,
        "Cod (100 g)": 82,
        "Shrimp (100 g)": 99,
        "Crab (100 g)": 97,
    },
    "Food limit": FOOD_PRESETS["Junk food"].copy(),
    "Other": FOOD_PRESETS["Makanan Indonesia"].copy(),
}

NUTRITION_FOODS = {
    "Chicken breast": {"category": "Protein", "serving": 100, "unit": "g", "calories": 165, "protein": 31.0, "carbs": 0.0, "fat": 3.6},
    "White rice": {"category": "Carbohydrate & grains", "serving": 100, "unit": "g", "calories": 130, "protein": 2.7, "carbs": 28.0, "fat": 0.3},
    "Broccoli": {"category": "Vegetables", "serving": 100, "unit": "g", "calories": 34, "protein": 2.8, "carbs": 6.6, "fat": 0.4},
    "Avocado": {"category": "Healthy fats", "serving": 100, "unit": "g", "calories": 160, "protein": 2.0, "carbs": 8.5, "fat": 14.7},
    "Greek yogurt": {"category": "Eggs & dairy", "serving": 100, "unit": "g", "calories": 59, "protein": 10.0, "carbs": 3.6, "fat": 0.4},
    "Salmon": {"category": "Seafood & meat", "serving": 100, "unit": "g", "calories": 208, "protein": 20.4, "carbs": 0.0, "fat": 13.4},
    "Tofu": {"category": "Plant protein", "serving": 100, "unit": "g", "calories": 76, "protein": 8.0, "carbs": 1.9, "fat": 4.8},
    "Banana": {"category": "Fruit", "serving": 100, "unit": "g", "calories": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3},
}

SPORT_FOOD_ADDITIONS = {
    "volly": {
        "Volleyball fuel": {"Banana": 100, "Rice bowl with chicken": 520, "Yogurt and granola": 240},
    },
    "run": {
        "Running fuel": {"Bagel": 280, "Dates (3)": 200, "Oatmeal with banana": 250},
    },
    "bycling": {
        "Cycling fuel": {"Rice cakes (2)": 180, "Peanut butter sandwich": 350, "Energy bar": 220},
    },
    "basketball": {
        "Basketball fuel": {"Turkey sandwich": 360, "Chicken and rice": 520, "Banana": 100},
    },
    "swimming": {
        "Swimming fuel": {"Oatmeal with berries": 280, "Egg and toast": 240, "Chicken pasta": 560},
    },
    "football": {
        "Football fuel": {"Beef and rice": 600, "Potato and eggs": 330, "Turkey wrap": 390},
    },
    "badminton": {
        "Badminton fuel": {"Fruit and yogurt": 210, "Rice and tofu": 430, "Trail mix (30 g)": 150},
    },
    "weight lifting": {
        "Strength fuel": {"Greek yogurt and berries": 220, "Chicken and sweet potato": 520, "Cottage cheese and fruit": 230},
    },
    "hocky": {
        "Hockey fuel": {"Salmon and potatoes": 540, "Turkey pasta": 560, "Oatmeal with milk": 300},
    },
    "yoga": {
        "Yoga fuel": {"Apple and almonds": 195, "Lentil bowl": 380, "Greek yogurt": 130},
    },
    "pilates": {
        "Pilates fuel": {"Eggs and avocado toast": 330, "Quinoa salad": 300, "Cottage cheese and fruit": 230},
    },
}


def food_presets_for_sport(sport: str) -> dict:
    presets = {category: items.copy() for category, items in FOOD_CATEGORY_GROUPS.items()}
    for category, items in SPORT_FOOD_ADDITIONS.get(sport.strip().lower(), {}).items():
        presets.setdefault("Other", {}).update(items)
    return presets


MACRO_RATIOS = {
    "Protein": (0.55, 0.05, 0.40),
    "Seafood & meat": (0.45, 0.05, 0.50),
    "Plant protein": (0.30, 0.30, 0.40),
    "Eggs & dairy": (0.30, 0.20, 0.50),
    "Carbohydrate & grains": (0.10, 0.80, 0.10),
    "Fruit": (0.05, 0.90, 0.05),
    "Vegetables": (0.15, 0.75, 0.10),
    "Healthy fats": (0.05, 0.10, 0.85),
    "Food limit": (0.10, 0.45, 0.45),
    "Other": (0.15, 0.55, 0.30),
}


def nutrition_totals(entries: list[dict]) -> dict:
    totals = {"calories": 0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for entry in entries:
        calories = float(entry["calories"])
        protein_ratio, carbs_ratio, fat_ratio = MACRO_RATIOS.get(entry["category"], MACRO_RATIOS["Other"])
        totals["calories"] += calories
        totals["protein"] += calories * protein_ratio / 4
        totals["carbs"] += calories * carbs_ratio / 4
        totals["fat"] += calories * fat_ratio / 9
    return totals


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
                weekly_target REAL NOT NULL,
                nutrition_commitment TEXT NOT NULL DEFAULT ''
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
        def ensure_profile_column(column_name: str, column_definition: str) -> bool:
            profile_columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(profiles)").fetchall()
            }
            if column_name in profile_columns:
                return False
            try:
                connection.execute(
                    f"ALTER TABLE profiles ADD COLUMN {column_name} {column_definition}"
                )
            except sqlite3.OperationalError:
                refreshed_columns = {
                    row["name"] for row in connection.execute("PRAGMA table_info(profiles)").fetchall()
                }
                if column_name not in refreshed_columns:
                    raise
                return False
            return True

        if ensure_profile_column("email", "TEXT"):
            connection.execute("UPDATE profiles SET email = username WHERE email IS NULL OR email = ''")
        ensure_profile_column("height", "REAL NOT NULL DEFAULT 0")
        ensure_profile_column("nutrition_commitment", "TEXT NOT NULL DEFAULT ''")
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
            "SELECT username, name, sport, goal, height, weekly_target, nutrition_commitment FROM profiles WHERE username = ?",
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


def save_nutrition_commitment(username: str, commitment: str):
    with get_connection() as connection:
        connection.execute(
            "UPDATE profiles SET nutrition_commitment = ? WHERE username = ?",
            (commitment.strip(), username),
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
        label = "✅ Good"
    else:
        bg = "rgba(255, 104, 104, 0.12)"
        border = "rgba(255, 104, 104, 0.5)"
        label = "⚠️ Needs attention"

    st.markdown(
        f"""
        <div style="margin-top: 12px; padding: 12px 14px; border-radius: 12px; border: 1px solid {border}; background: {bg}; color: #000000;">
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
                    st.session_state.current_user = new_username.strip()
                    st.session_state.show_success_flash = True
                    st.success("Profile created successfully.")
                    st.rerun()

    st.stop()


username = st.session_state.current_user
profile = get_profile(username)
if profile is None:
    st.session_state.current_user = None
    st.session_state.auth_mode = "login"
    st.error("We could not load your profile. Please sign in again.")
    st.stop()
workouts = get_workouts(username)
food_entries = get_food_entries(username)
profile_photo = SPORT_PHOTOS.get(
    profile["sport"].strip().lower(),
    "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=400&q=80",
)

if st.session_state.show_success_flash:
    st.markdown(
        f'<div class="login-success-flash" style="background-image: url(\'{profile_photo}\');" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )
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
    "Open Nutrition to set your commitment, add meals, and calculate your daily intake."
)

st.markdown(
    """
    <div class="nutrition-dashboard-card">
        <h3>🥗 Commitment Nutrition</h3>
        <p>Build healthier eating habits and fuel your performance.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
if st.button("Explore Nutrition →", key="explore_nutrition", type="secondary"):
    st.session_state["nutrition_view"] = "Daily Nutrition"
    st.rerun()

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

food_tab, physics_tab, chemistry_tab, biology_tab, math_tab, performance_tab = st.tabs(
    ["🥗 Nutrition", "⚡ Physics", "💧 Chemistry", "🫀 Biology", "📐 Math", "🏅 Performance"]
)

sport_name = profile["sport"]
sport_key = sport_name.strip().lower()

with physics_tab:
    st.markdown(f"### {sport_name} physics")
    st.caption("This calculator is selected automatically from your registered sport.")
    mass_kg = st.number_input("Body mass (kg)", min_value=1.0, value=70.0, key="physics_mass")
    if sport_key == "volly":
        jump_height = st.number_input("Vertical jump height (m)", min_value=0.01, value=0.45, key="physics_jump_height")
        push_time = st.number_input("Take-off time (s)", min_value=0.05, value=0.35, key="physics_jump_time")
        power = mass_kg * 9.81 * jump_height / push_time
        st.metric("Jump power", f"{power:.0f} W")
        st.caption("Formula: P = mgh / t")
    elif sport_key in {"run", "bycling"}:
        speed = st.number_input("Speed (m/s)", min_value=0.0, value=8.0 if sport_key == "run" else 7.0, key="physics_speed")
        grade = st.number_input("Incline (%)", min_value=0.0, max_value=30.0, value=1.0, key="physics_grade")
        power = mass_kg * 9.81 * speed * (grade / 100)
        st.metric("Hill power", f"{power:.0f} W")
        st.caption("Formula: P = mgv × grade")
    elif sport_key in {"weight lifting", "basketball", "football", "hocky", "badminton"}:
        load = st.number_input("Moved load (kg)", min_value=1.0, value=mass_kg, key="physics_load")
        movement_speed = st.number_input("Movement speed (m/s)", min_value=0.01, value=1.5, key="physics_movement_speed")
        movement_time = st.number_input("Movement time (s)", min_value=0.05, value=0.5, key="physics_movement_time")
        power = 0.5 * load * movement_speed**2 / movement_time
        st.metric("Explosive power", f"{power:.0f} W")
        st.caption("Formula: P = 1/2 mv² / t")
    else:
        movement_speed = st.number_input("Movement speed (m/s)", min_value=0.0, value=2.0, key="physics_movement_speed")
        movement_time = st.number_input("Movement time (s)", min_value=0.05, value=1.0, key="physics_movement_time")
        power = 0.5 * mass_kg * movement_speed**2 / movement_time
        st.metric("Movement power", f"{power:.0f} W")
        st.caption("Formula: P = 1/2 mv² / t")
    render_assessment(
        "Power calculation ready",
        f"Use this {sport_name} result to compare sessions under similar conditions.",
        good=True,
    )

with chemistry_tab:
    st.markdown(f"### {sport_name} chemistry")
    st.caption("Measure your own sweat loss instead of guessing it.")
    st.info(
        "How to measure: weigh yourself before and after training in similar clothing, record every drink, "
        "and record urine during the session. A 1 kg body-mass change is approximately 1 L of fluid."
    )
    body_weight = st.number_input("Body weight before (kg)", min_value=20.0, value=70.0, key="chem_weight_before")
    post_weight = st.number_input("Body weight after (kg)", min_value=20.0, value=69.0, key="chem_weight_after")
    session_minutes = st.number_input("Session duration (minutes)", min_value=1.0, value=60.0, key="chem_duration")
    fluid_intake = st.number_input("Fluid consumed (L)", min_value=0.0, value=0.5, key="chem_fluid_intake")
    urine_loss = st.number_input("Urine passed during session (L)", min_value=0.0, value=0.0, key="chem_urine_loss")
    body_mass_loss = max(0.0, body_weight - post_weight)
    sweat_loss = body_mass_loss + fluid_intake - urine_loss
    sweat_rate = sweat_loss / (session_minutes / 60)
    fluid_need = sweat_loss * 1.25
    sodium_need = sweat_loss * 800
    st.metric("Estimated sweat loss", f"{sweat_loss:.2f} L")
    st.metric("Sweat rate", f"{sweat_rate:.2f} L/hour")
    st.metric("Fluid replacement", f"{fluid_need:.2f} L")
    st.metric("Estimated sodium replacement", f"{sodium_need:.0f} mg")
    st.caption("Formula: sweat loss = pre-weight − post-weight + fluid consumed − urine; replacement target = 125% of loss.")
    render_assessment("Session chemistry ready", f"Plan fluids and electrolytes around your {sport_name} session.", good=True)

with biology_tab:
    st.markdown(f"### {sport_name} biology")
    st.caption("Estimate sport-session energy use and heart-rate training zones.")
    age = st.number_input("Age", min_value=10, value=28, key="bio_age")
    weight_kg = st.number_input("Weight (kg)", min_value=20.0, value=70.0, key="bio_weight")
    sport_met = {"volly": 8.0, "run": 9.8, "bycling": 8.0, "basketball": 8.0, "swimming": 8.3, "football": 10.0, "badminton": 7.0, "weight lifting": 6.0, "hocky": 8.0, "yoga": 2.5, "pilates": 3.0}.get(sport_key, 6.0)
    minutes = st.number_input("Session duration (minutes)", min_value=1.0, value=60.0, key="bio_session_minutes")
    calories = sport_met * 3.5 * weight_kg / 200 * minutes
    st.metric(f"Estimated {sport_name} calories", f"{calories:,.0f} kcal")
    st.caption(f"Formula: kcal = MET × 3.5 × body mass × minutes / 200; selected MET = {sport_met:.1f}.")
    heart_rate_max = 208 - 0.7 * age
    resting_hr = st.number_input("Resting heart rate (bpm)", min_value=30, max_value=120, value=60, key="bio_resting_hr")
    training_zone = st.selectbox("Training zone", [1, 2, 3, 4, 5], index=1, key="bio_training_zone")
    heart_rate_low = resting_hr + (heart_rate_max - resting_hr) * (0.50 + (training_zone - 1) * 0.10)
    heart_rate_high = resting_hr + (heart_rate_max - resting_hr) * (0.60 + (training_zone - 1) * 0.10)
    st.metric("Recommended heart-rate range", f"{heart_rate_low:.0f}-{heart_rate_high:.0f} bpm")
    st.caption("Formula: Karvonen-style reserve zone using estimated max HR = 208 - 0.7 × age.")
    render_assessment("Sport energy estimate ready", f"Use the {sport_name} estimate with your actual session duration and effort.", good=True)

with math_tab:
    st.markdown(f"### {sport_name} math")
    st.caption("Your registered sport selects the performance calculation automatically.")
    if sport_key == "football":
        passes_attempted = st.number_input("Passes attempted", min_value=1, value=40, key="math_passes_attempted")
        passes_completed = st.number_input("Passes completed", min_value=0, max_value=int(passes_attempted), value=min(34, int(passes_attempted)), key="math_passes_completed")
        distance_km = st.number_input("Distance covered (km)", min_value=0.0, value=8.0, key="math_football_distance")
        st.metric("Pass accuracy", f"{passes_completed / passes_attempted * 100:.1f}%")
        st.metric("Distance covered", f"{distance_km:.1f} km")
    elif sport_key == "basketball":
        field_goals_made = st.number_input("Field goals made", min_value=0, value=8, key="math_fg_made")
        field_goals_attempted = st.number_input("Field goals attempted", min_value=1, value=16, key="math_fg_attempted")
        points = st.number_input("Points scored", min_value=0, value=20, key="math_points")
        minutes_played = st.number_input("Minutes played", min_value=1.0, value=32.0, key="math_basketball_minutes")
        st.metric("Field-goal percentage", f"{field_goals_made / field_goals_attempted * 100:.1f}%")
        st.metric("Points per minute", f"{points / minutes_played:.2f}")
    elif sport_key == "swimming":
        swim_distance = st.number_input("Distance (m)", min_value=25.0, value=100.0, key="math_swim_distance")
        swim_time = st.number_input("Time (seconds)", min_value=1.0, value=90.0, key="math_swim_time")
        strokes = st.number_input("Strokes", min_value=1, value=40, key="math_swim_strokes")
        st.metric("Pace per 100 m", f"{swim_time / swim_distance * 100:.1f} sec")
        st.metric("SWOLF", f"{swim_time / swim_distance * 100 + strokes:.0f}")
    elif sport_key == "run":
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
    elif sport_key == "bycling":
        distance_km = st.number_input("Distance (km)", min_value=0.1, value=20.0, key="math_cycle_distance")
        time_min = st.number_input("Ride time (min)", min_value=1.0, value=60.0, key="math_cycle_time")
        elevation = st.number_input("Elevation gain (m)", min_value=0.0, value=200.0, key="math_cycle_elevation")
        st.metric("Average speed", f"{distance_km / (time_min / 60):.2f} km/h")
        st.metric("Climbing rate", f"{elevation / (time_min / 60):.0f} m/h")
    elif sport_key == "volly":
        successful = st.number_input("Successful attacks", min_value=0, value=12, key="math_volly_success")
        attempts = st.number_input("Attack attempts", min_value=1, value=20, key="math_volly_attempts")
        jumps = st.number_input("Jumps", min_value=1, value=30, key="math_volly_jumps")
        st.metric("Attack success rate", f"{successful / attempts * 100:.1f}%")
        st.metric("Jump rate", f"{jumps:.0f} jumps/session")
    elif sport_key in {"badminton", "hocky"}:
        shots = st.number_input("Successful shots", min_value=0, value=20, key="math_shots_success")
        attempts = st.number_input("Shot attempts", min_value=1, value=35, key="math_shot_attempts")
        match_minutes = st.number_input("Match time (min)", min_value=1.0, value=60.0, key="math_match_minutes")
        st.metric("Shot success rate", f"{shots / attempts * 100:.1f}%")
        st.metric("Shot rate", f"{attempts / match_minutes:.2f}/min")
    elif sport_key == "weight lifting":
        load = st.number_input("Weight lifted (kg)", min_value=1.0, value=60.0, key="math_lift_load")
        reps = st.number_input("Repetitions", min_value=1, value=8, key="math_lift_reps")
        sets = st.number_input("Sets", min_value=1, value=3, key="math_lift_sets")
        st.metric("Training volume", f"{load * reps * sets:.0f} kg")
        st.metric("Estimated 1RM", f"{load * (1 + reps / 30):.1f} kg")
    else:
        minutes = st.number_input("Practice time (minutes)", min_value=1.0, value=45.0, key="math_practice_minutes")
        sessions = st.number_input("Sessions per week", min_value=1, value=3, key="math_practice_sessions")
        st.metric("Weekly practice time", f"{minutes * sessions:.0f} min")
        st.metric("Average session", f"{minutes:.0f} min")

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
    nutrition_view = st.radio(
        "Nutrition workspace",
        ["Daily Nutrition", "Food Database", "Meal Builder", "Nutrition Calculator", "My Nutrition Progress"],
        horizontal=True,
        key="nutrition_view",
    )
    nutrition_totals_today = nutrition_totals(today_food_entries)
    nutrition_goal = profile["goal"] or "General fitness"
    calorie_target = 2600 if "muscle" in nutrition_goal.lower() else 2400
    macro_targets = {"protein": 160, "carbs": 300, "fat": 70}

    st.markdown("## 🥗 Nutrition")
    st.caption("Fuel your body based on your sport, training, and goals.")
    context_col1, context_col2, context_col3 = st.columns(3)
    context_col1.metric("Your sport", profile["sport"])
    context_col2.metric("Your goal", profile["goal"])
    context_col3.metric("Today's nutrition", f"{nutrition_totals_today['calories']:,.0f} / {calorie_target:,} kcal")

    st.markdown("### Nutrition summary")
    summary_cards = st.columns(4)
    summary_values = [
        ("🔥 Calories", f"{nutrition_totals_today['calories']:,.0f} / {calorie_target:,} kcal", nutrition_totals_today["calories"] / calorie_target),
        ("💪 Protein", f"{nutrition_totals_today['protein']:.0f} / {macro_targets['protein']} g", nutrition_totals_today["protein"] / macro_targets["protein"]),
        ("⚡ Carbs", f"{nutrition_totals_today['carbs']:.0f} / {macro_targets['carbs']} g", nutrition_totals_today["carbs"] / macro_targets["carbs"]),
        ("🥑 Fat", f"{nutrition_totals_today['fat']:.0f} / {macro_targets['fat']} g", nutrition_totals_today["fat"] / macro_targets["fat"]),
    ]
    for summary_card, (label, value, completion) in zip(summary_cards, summary_values):
        with summary_card:
            st.markdown(
                f'<div class="nutrition-summary-card"><div class="nutrition-summary-label">{label}</div><div class="nutrition-summary-value">{value}</div></div>',
                unsafe_allow_html=True,
            )
            st.progress(min(completion, 1.0))
    st.caption("Protein, carbohydrate, and fat values are approximate estimates based on each logged food category.")

    st.markdown("### What would you like to do?")
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    action_col1.button("🍎 Find Food", key="nutrition_find_food", on_click=lambda: st.session_state.update(nutrition_view="Food Database"))
    action_col2.button("🍱 Build a Meal", key="nutrition_build_meal", on_click=lambda: st.session_state.update(nutrition_view="Meal Builder"))
    action_col3.button("🧮 Calculate Nutrition", key="nutrition_calculate", on_click=lambda: st.session_state.update(nutrition_view="Nutrition Calculator"))
    action_col4.button("📊 View Progress", key="nutrition_progress", on_click=lambda: st.session_state.update(nutrition_view="My Nutrition Progress"))

    if nutrition_view == "Food Database":
        st.markdown("### Food Database")
        food_search = st.text_input("Search food", placeholder="Search chicken, rice, fruit...", key="nutrition_food_search")
        food_category = st.selectbox("Category", ["All", *sorted({food["category"] for food in NUTRITION_FOODS.values()})], key="nutrition_database_category")
        matching_foods = {
            name: food
            for name, food in NUTRITION_FOODS.items()
            if (not food_search or food_search.lower() in name.lower())
            and (food_category == "All" or food["category"] == food_category)
        }
        if matching_foods:
            selected_food_name = st.selectbox("Choose a food", list(matching_foods), key="nutrition_selected_food")
            selected_food = matching_foods[selected_food_name]
            serving_amount = st.number_input(
                f"Serving ({selected_food['unit']})",
                min_value=1.0,
                value=float(selected_food["serving"]),
                step=10.0,
                key="nutrition_serving_amount",
            )
            serving_multiplier = serving_amount / selected_food["serving"]
            food_detail_cols = st.columns(4)
            food_detail_cols[0].metric("Calories", f"{selected_food['calories'] * serving_multiplier:.0f} kcal")
            food_detail_cols[1].metric("Protein", f"{selected_food['protein'] * serving_multiplier:.1f} g")
            food_detail_cols[2].metric("Carbohydrates", f"{selected_food['carbs'] * serving_multiplier:.1f} g")
            food_detail_cols[3].metric("Fat", f"{selected_food['fat'] * serving_multiplier:.1f} g")
            st.caption(f"{selected_food_name} · {selected_food['category']} · values are approximate")
        else:
            st.info("No foods match that search and category.")

    elif nutrition_view == "Meal Builder":
        st.markdown("### 🍱 Build Your Meal")
        st.caption("Choose foods and change the quantities to recalculate the meal automatically.")
        meal_rows = []
        for meal_index in range(3):
            meal_columns = st.columns([2, 1])
            with meal_columns[0]:
                meal_food_name = st.selectbox("Food", ["No food", *NUTRITION_FOODS], key=f"meal_food_{meal_index}")
            with meal_columns[1]:
                meal_amount = st.number_input("Amount (g)", min_value=1.0, value=100.0, step=25.0, key=f"meal_amount_{meal_index}")
            if meal_food_name != "No food":
                meal_rows.append((NUTRITION_FOODS[meal_food_name], meal_amount))
        meal_totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
        for meal_food, meal_amount in meal_rows:
            meal_multiplier = meal_amount / meal_food["serving"]
            for nutrient in meal_totals:
                meal_totals[nutrient] += meal_food[nutrient] * meal_multiplier
        meal_metrics = st.columns(4)
        meal_metrics[0].metric("Total calories", f"{meal_totals['calories']:.0f} kcal")
        meal_metrics[1].metric("Protein", f"{meal_totals['protein']:.1f} g")
        meal_metrics[2].metric("Carbs", f"{meal_totals['carbs']:.1f} g")
        meal_metrics[3].metric("Fat", f"{meal_totals['fat']:.1f} g")
        if st.button("Save Meal", key="save_nutrition_meal"):
            st.session_state["saved_nutrition_meal"] = meal_totals
            st.success("Meal saved for this session.")

    elif nutrition_view == "Nutrition Calculator":
        st.markdown("### 🧮 Nutrition Calculator")
        calculator_col1, calculator_col2 = st.columns(2)
        with calculator_col1:
            calculator_weight = st.number_input("Body weight (kg)", min_value=20.0, value=70.0, key="nutrition_calc_weight")
            calculator_duration = st.number_input("Workout duration (minutes)", min_value=1.0, value=60.0, key="nutrition_calc_duration")
        with calculator_col2:
            calculator_intensity = st.selectbox("Workout intensity", ["Low", "Moderate", "High"], index=1, key="nutrition_calc_intensity")
            intensity_factor = {"Low": 5.0, "Moderate": 7.0, "High": 9.0}[calculator_intensity]
        estimated_energy = intensity_factor * 3.5 * calculator_weight / 200 * calculator_duration
        calculator_results = st.columns(3)
        calculator_results[0].metric("Estimated energy expenditure", f"{estimated_energy:,.0f} kcal")
        calculator_results[1].metric("Suggested hydration", f"{calculator_duration / 60 * 0.5:.1f} L")
        calculator_results[2].metric("Suggested protein range", f"{calculator_weight * 1.4:.0f}-{calculator_weight * 2:.0f} g")
        st.caption("These are estimates for planning, not medical advice. Actual needs vary with training, climate, and individual health.")

    elif nutrition_view == "My Nutrition Progress":
        st.markdown("### 📊 My Nutrition Progress")
        progress_by_date = {}
        for entry in food_entries:
            progress_by_date[entry["date"]] = progress_by_date.get(entry["date"], 0) + entry["calories"]
        if progress_by_date:
            progress_df = pd.DataFrame(
                [{"date": date, "calories": calories} for date, calories in sorted(progress_by_date.items())]
            ).tail(14).set_index("date")
            st.line_chart(progress_df, y="calories")
            st.caption(f"Showing the latest {len(progress_df)} logged day(s) against an estimated target of {calorie_target:,} kcal.")
        else:
            st.info("Add food entries to see your nutrition progress here.")

    st.divider()
    st.markdown("### Daily nutrition planner")
    st.caption("Choose a sport-specific food or drink, or type any item and calorie value you want to track.")
    default_commitment = profile.get("nutrition_commitment") or f"I will choose food that supports my goal: {profile['goal']}"
    commitment_state_key = f"nutrition_commitment_input_{username}"
    if commitment_state_key not in st.session_state:
        st.session_state[commitment_state_key] = default_commitment
    commitment = st.text_area(
        "Nutrition commitment (editable)",
        height=90,
        key=commitment_state_key,
    )
    if st.button("Save nutrition commitment", key=f"save_commitment_{username}"):
        if commitment.strip():
            save_nutrition_commitment(username, commitment)
            profile["nutrition_commitment"] = commitment.strip()
            st.session_state[commitment_state_key] = commitment.strip()
            st.success("Nutrition commitment updated.")
        else:
            st.warning("Write a commitment before saving.")

    commitment_text = escape(profile.get("nutrition_commitment") or default_commitment)
    st.markdown(
        f"""
        <div class="nutrition-commitment-card">
            <div class="nutrition-commitment-label">Nutrition commitment</div>
            <div class="nutrition-commitment-text">{commitment_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if commitment_text:
        food_date = st.date_input("Food log date", value=datetime.now().date(), key="food_log_date")
        selected_date = food_date.isoformat()
        selected_entries = [entry for entry in food_entries if entry["date"] == selected_date]

        sport_food_presets = food_presets_for_sport(profile["sport"])

        input_mode = st.radio(
            "Calorie input",
            ["Choose from food list", "Input calories myself"],
            horizontal=True,
            key=f"food_input_mode_{username}",
        )
        with st.form("food_item_form"):
            st.markdown(
                '<div class="food-entry-panel"><div class="food-entry-kicker">Build your plate</div><div class="food-entry-title">What are you adding today?</div>',
                unsafe_allow_html=True,
            )
            if input_mode == "Input calories myself":
                food_column, drink_column = st.columns(2)
                with food_column:
                    st.markdown('<div class="food-input-card">', unsafe_allow_html=True)
                    food_name = st.text_input("Food name", placeholder="e.g. Chicken and rice", key=f"custom_food_name_{username}")
                    food_calories = st.number_input("Food calories (kcal)", min_value=0, max_value=3000, step=5, value=200, key=f"custom_food_calories_{username}")
                    st.markdown('</div>', unsafe_allow_html=True)
                with drink_column:
                    st.markdown('<div class="food-input-card">', unsafe_allow_html=True)
                    drink_name = st.text_input("Drink name (optional)", placeholder="e.g. Coconut water", key=f"custom_drink_name_{username}")
                    drink_calories = st.number_input("Drink calories (kcal)", min_value=0, max_value=3000, step=5, value=0, key=f"custom_drink_calories_{username}")
                    st.markdown('</div>', unsafe_allow_html=True)
                custom_category = st.selectbox(
                    "Category",
                    ["Other", "Vegetables", "Healthy fats", "Fruit", "Carbohydrate & grains", "Plant protein", "Eggs & dairy", "Protein", "Seafood & meat", "Food limit"],
                    key=f"custom_food_category_{username}",
                )
                food_name = food_name or drink_name
                calories_per_serving = food_calories if food_name == st.session_state.get(f"custom_food_name_{username}", "") else drink_calories
                st.caption("Type a food or drink in its own column. Add one item per submission.")
            else:
                selected_item = st.radio(
                    "Choose food or drink",
                    ["Food", "Drink"],
                    horizontal=True,
                    key=f"preset_item_type_{username}",
                )
                if selected_item == "Food":
                    food_category = st.selectbox(
                        "Food category",
                        list(sport_food_presets),
                        key=f"preset_food_category_{username}",
                    )
                    food_name = st.selectbox(
                        "Food",
                        list(sport_food_presets[food_category]),
                        key=f"preset_food_name_{username}_{food_category}",
                    )
                    calories_per_serving = sport_food_presets[food_category][food_name]
                else:
                    drink_category = st.selectbox(
                        "Drink category",
                        ["Drink"],
                        key=f"preset_drink_category_{username}",
                    )
                    drink_options = {
                        item: calories
                        for drink_group in DRINK_PRESETS.values()
                        for item, calories in drink_group.items()
                    }
                    drink_name = st.selectbox(
                        "Drink",
                        list(drink_options),
                        key=f"preset_drink_name_{username}",
                    )
                    calories_per_serving = drink_options[drink_name]
                if selected_item == "Food":
                    custom_category = food_category
                else:
                    food_name = drink_name
                    custom_category = drink_category
                st.caption(f"{selected_item} estimate: {calories_per_serving} kcal per serving for {profile['sport']}")
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
                    st.markdown('</div>', unsafe_allow_html=True)

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
