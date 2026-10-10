
import streamlit as st
import joblib
from pathlib import Path
from datetime import datetime
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(160deg, #08111f, #101d30);
    color: #f1f5f9;
}
.block-container {
    max-width: 800px;
    padding-top: 2rem;
}
.hero {
    padding: 24px;
    border-radius: 18px;
    background: linear-gradient(120deg, #123247, #172554);
    border: 1px solid #24516b;
    text-align: center;
}
.hero h1 { color: #67e8f9; }
.hero p { color: #dbeafe; }
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    min-height: 48px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).resolve().parent / "scam_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"Model loading failed: {type(e).__name__}: {e}")
    st.stop()

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>🛡️ CyberShield AI</h1>
    <p>AI-powered WhatsApp and SMS scam message checker</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.info(
    "Paste a suspicious message below. The AI will estimate whether "
    "it resembles a scam. Do not enter real passwords, OTPs, or private information."
)

# ---------------- MESSAGE SCANNER ----------------
st.subheader("🔎 Message Scanner")

message = st.text_area(
    "Message to check",
    height=160,
    placeholder="Paste your WhatsApp or SMS message here..."
)

if st.button("🔍 ANALYZE MESSAGE", type="primary"):
    if not message.strip():
        st.warning("Please paste a message first.")
    else:
        try:
            prediction = str(model.predict([message])[0]).lower()

            scam_score = None
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba([message])[0]
                classes = list(model.classes_)
                if "scam" in classes:
                    scam_score = float(probabilities[classes.index("scam")])

            st.divider()
            st.subheader("Analysis Result")

            if prediction == "scam":
                st.error("🚨 POSSIBLE SCAM DETECTED")
                st.write(
                    "Be careful. Avoid clicking suspicious links or sharing "
                    "OTPs, passwords, bank details, or personal information."
                )
            else:
                st.success("✅ NO SCAM DETECTED BY THE MODEL")
                st.write(
                    "The model classified this message as normal. "
                    "This does not guarantee that it is safe."
                )

            if scam_score is not None:
                st.metric("Estimated scam probability", f"{scam_score:.1%}")
                st.caption(
                    "This is a model score, not a verified real-world risk percentage."
                )

            # Simple indicators to help users review the message
            indicators = []
            lower_message = message.lower()

            if re.search(r"https?://|www\\.", lower_message):
                indicators.append("Contains a web link")

            if any(word in lower_message for word in [
                "urgent", "immediately", "act now", "blocked", "expire"
            ]):
                indicators.append("Uses urgent or pressure-based language")

            if any(word in lower_message for word in [
                "otp", "password", "bank details", "verify your account"
            ]):
                indicators.append("Mentions account verification or sensitive details")

            st.subheader("⚠️ Message Indicators")
            if indicators:
                for item in indicators:
                    st.write(f"• {item}")
            else:
                st.write("No basic warning indicators found by these simple checks.")

            st.caption(
                "Indicators are clues only. They do not prove a message is fraudulent."
            )

        except Exception:
            st.error("Analysis failed. Check that the model file and dependencies are valid.")

# ---------------- SHARE ----------------
st.divider()
st.subheader("📲 Share CyberShield AI")

st.write(
    "Once this app is deployed online, copy its public URL and send it "
    "to friends or classmates through WhatsApp."
)

st.code("Your public link will appear after deployment.")

st.markdown(
    "[Deploy for a public link with Streamlit Community Cloud](https://share.streamlit.io/)"
)

st.caption(
    "Student project prototype. Predictions may be incorrect. "
    "Do not rely on this app as your only scam protection."
)
