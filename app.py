import streamlit as st
import requests as re
import logging
import re as regex
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

# Keep your original local imports
from model_loader import ab_model, FEATURE_COLUMNS
import feature_extraction as fe

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Phishing Website Detection",
    page_icon="🔐",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background-color: #020617;
        color: #e5e7eb;
    }

    /* Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 1rem;
        background: #0f172a;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 2rem;
    }

    /* Hero Section */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    /* Input Box Styling */
    .stTextInput input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    /* Result Cards */
    .result-card {
        background: #111827;
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid #1e293b;
        margin-top: 1rem;
    }

    /* Project Overview Cards */
    .overview-card {
        background: #0f172a;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #1e293b;
        text-align: center;
        min-height: 150px;
    }

    .footer {
        text-align: center;
        padding: 3rem 0;
        color: #64748b;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- UTILITIES ---------------- #
def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ["http", "https"] and parsed.netloc != ""


def fetch_html(url):
    try:
        response = re.get(url, timeout=5, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        return response.text if response.status_code == 200 else None
    except:
        return None


def url_heuristic_score(url):
    parsed = urlparse(url)
    score, reasons = 0, []
    if regex.match(r"\d+\.\d+\.\d+\.\d+", parsed.netloc): score += 20; reasons.append("IP address used")
    if len(url) > 75: score += 10; reasons.append("Very long URL")
    if parsed.netloc.count(".") > 3: score += 10; reasons.append("Too many subdomains")
    if any(parsed.netloc.endswith(tld) for tld in [".xyz", ".top", ".click", ".zip"]): score += 15; reasons.append(
        "Suspicious TLD")
    if parsed.scheme != "https": score += 10; reasons.append("HTTPS not used")
    return min(score, 100), reasons


# ---------------- 1. NAVIGATION (From Sketch) ---------------- #
st.markdown("""
<div class="nav-bar">
    <div style="font-size: 1.5rem; font-weight: bold; color: #3b82f6;">🛡️ WEBSAFE</div>
    <div style="display: flex; gap: 30px; font-weight: 500;">
        <span style="color: white;">HOME</span>
        <span style="color: #94a3b8;">HOW IT WORKS</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- 2. HERO SECTION & 3. INPUT (From Sketch) ---------------- #
hero_col, img_col = st.columns([1.2, 1])


# ---------------- HERO SECTION & INPUT ---------------- #
# We use a container to apply vertical alignment to the columns
st.markdown("""
    <style>
    /* This target specifically ensures the columns are centered vertically */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

hero_col, img_col = st.columns([1.5, 1.5], gap="large")

with hero_col:
    # 1. System Status Badge
    st.markdown(
        '<span style="background-color: #1e293b; color: #3b82f6; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">● System Online</span>',
        unsafe_allow_html=True)

    # 2. Main Title
    st.markdown('<h1 class="hero-title" style="margin-top: 15px;">Phishing Website <br>Detection System</h1>',
                unsafe_allow_html=True)

    # 3. Description
    st.markdown("""
        <p style='color: #94a3b8; font-size: 1.15rem; line-height: 1.6; margin-bottom: 1.5rem;'>
            Protect your digital identity with real-time intelligence. Our advanced AI-driven 
            engine scans deep into URL structures and HTML source code to identify 
            deceptive websites.
        </p>
    """, unsafe_allow_html=True)

    # 4. Feature Badges
    st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 2rem;">
            <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); padding: 8px 12px; border-radius: 8px;">
                <span style="color: #3b82f6; font-weight: bold;">✓</span> <span style="font-size: 0.85rem; color: #cbd5e1;">Real-time Analysis</span>
            </div>
            <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); padding: 8px 12px; border-radius: 8px;">
                <span style="color: #3b82f6; font-weight: bold;">✓</span> <span style="font-size: 0.85rem; color: #cbd5e1;">AI-Powered</span>
            </div>
             <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); padding: 8px 12px; border-radius: 8px;">
                <span style="color: #3b82f6; font-weight: bold;">✓</span> <span style="font-size: 0.85rem; color: #cbd5e1;">Zero-Day Protection</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 5. URL Input & Button Area
    url_input = st.text_input("Enter URL to scan:", placeholder="https://example.com", label_visibility="collapsed")
    scan_btn = st.button("Check Security Status")

    result_container = st.empty()

with img_col:
    # Adding a small top margin to the image div to ensure it sits perfectly level
    st.markdown('<div style="margin-top: 50px;">', unsafe_allow_html=True)
    st.image("assest/img.jpg", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIC EXECUTION ---------------- #
if scan_btn:
    # We clear the reserved container and fill it with results
    with result_container.container():
        st.markdown("<br>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns([2, 1])

        with res_col1:
            if not is_valid_url(url_input):
                st.error("⚠️ Invalid URL Format. Please include http:// or https://")
            else:
                with st.spinner("Analyzing..."):
                    html = fetch_html(url_input)
                    if html:
                        try:
                            soup = BeautifulSoup(html, "html.parser")
                            features = fe.create_vector(soup)
                            prediction = ab_model.predict(pd.DataFrame([features], columns=FEATURE_COLUMNS))

                            if prediction[0] == 0:
                                st.success("✅ LEGITIMATE: This website appears safe to use.")
                            else:
                                st.error("🚨 PHISHING: This website shows signs of malicious intent.")
                        except Exception as e:
                            st.warning("Analysis failed due to site structure.")
                    else:
                        score, reasons = url_heuristic_score(url_input)
                        st.subheader("⚠️ URL Risk Analysis (Heuristic)")
                        st.progress(score / 100)
                        if reasons:
                            for r in reasons: st.info(f"• {r}")

        with res_col2:
            if is_valid_url(url_input):
                # Calculate risk label for metric
                risk_label = "Low"
                if 'prediction' in locals():
                    risk_label = "High" if prediction[0] != 0 else "Low"
                elif 'score' in locals():
                    risk_label = "High" if score > 50 else "Low"

                st.metric("Risk Level", risk_label)
                st.caption("Based on real-time metadata analysis.")



# ---------------- UPDATED CUSTOM CSS ---------------- #
st.markdown("""
<style>
    /* 1. Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* 2. Apply Font Globally */
    html, body, [class*="st-"], .main, .stMarkdown {
        font-family: 'Inter', sans-serif !important;
    }

    /* 3. Modernized Overview Cards with Fixed Height */
    .overview-card {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 2rem !important;
        border-radius: 24px !important;
        transition: all 0.3s ease;

        /* Ensures all boxes stay the same length */
        height: 480px !important; 
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        box-sizing: border-box;
    }

    /* 4. Interactive Hover Effect */
    .overview-card:hover {
        transform: translateY(-12px);
        border-color: #3b82f6 !important;
        background: rgba(30, 41, 59, 0.6) !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
    }

    /* 5. Typography for Card Content */
    .box-title {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
        display: block;
    }

    .box-description {
        font-size: 1.05rem !important;
        color: #cbd5e1 !important;
        line-height: 1.6 !important;
        text-align: left;
    }
    
    
    /* Custom Blue Small Button */
    div.stButton > button {
    background-color: #3b82f6 !important; /* Blue color */
    color: white !important;
    border: none !important;
    padding: 10px 25px !important; /* Smaller padding */
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    width: auto !important; /* Prevents stretching */
    transition: all 0.3s ease;
    display: block;
    margin: 0 auto; /* Centers the button if needed */
    }
    div.stButton > button:hover {
    background-color: #2563eb !important; /* Darker blue on hover */
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    transform: translateY(-2px);
    }

    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background-color: #020617;
        color: #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)



# ---------------- PROJECT OVERVIEW: STAGE 1 (Icon Row) ---------------- #
st.markdown("<br><br><h2 style='text-align: center; font-size: 2.5rem; font-weight: 800;'>How It Works</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 3rem;'>A technical breakdown of our multi-layered defense system.</p>", unsafe_allow_html=True)

ov_1, ov_2, ov_3, ov_4 = st.columns(4, gap="medium")

with ov_1:
    st.markdown('''
        <div class="overview-card">
            <h1 style="margin:0;">🧠</h1>
            <span class="box-title">Approach Used</span>
            <div class="box-description">
                <b>1. Content ML:</b> HTML is fetched and parsed via <b>BeautifulSoup</b> to detect malicious tag patterns.<br><br>
                <b>2. URL Heuristics:</b> A fallback system analyzing domain age, TLD, and structure when content is unreachable.
            </div>
        </div>
    ''', unsafe_allow_html=True)

with ov_2:
    st.markdown('''
        <div class="overview-card">
            <h1 style="margin:0;">📊</h1>
            <span class="box-title">Dataset Details</span>
            <div class="box-description">
                1. <b>Phishing:</b> Verified URLs from PhishTank sources.<br><br>
                2. <b>Legitimate:</b> Top-ranked domains from Tranco.<br><br>
                3. <b>Engineering:</b> 45+ unique features extracted and balanced.
            </div>
        </div>
    ''', unsafe_allow_html=True)

with ov_3:
    st.markdown('''
        <div class="overview-card">
            <h1 style="margin:0;">🤖</h1>
            <span class="box-title">Model Choice</span>
            <div class="box-description">
                <b>Winner: AdaBoost</b><br><br>
                Selected for its superior <b>Recall</b>. It effectively minimizes False Negatives compared to Random Forest and SVM models.
            </div>
        </div>
    ''', unsafe_allow_html=True)

with ov_4:
    st.markdown('''
        <div class="overview-card">
            <h1 style="margin:0;">📈</h1>
            <span class="box-title">Evaluation</span>
            <div class="box-description">
                The system prioritizes <b>Security First</b>. <br><br>
                Performance is measured across Accuracy and Precision, with a primary focus on <b>Phishing Recall</b> to ensure users stay protected.
            </div>
        </div>
    ''', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown(f"""
<div class="footer">
    <hr style="border-color: #1e293b;">
    MADE WITH ❤️ BY RAMESHWARI
</div>
""", unsafe_allow_html=True)