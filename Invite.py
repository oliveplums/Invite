#
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Olivia's 30th RSVP",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load or initialize the RSVP data
try:
    rsvps = pd.read_csv("rsvp_data.csv")
except FileNotFoundError:
    rsvps = pd.DataFrame(columns=[
        "Name", "Attending", "Contribution", "Diet", "Allergies", "Notes", "Timestamp", "Paid"
    ])

# Session state defaults
if "show_payment" not in st.session_state:
    st.session_state.show_payment = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "full_name" not in st.session_state:
    st.session_state.full_name = ""
if "page" not in st.session_state:
    st.session_state.page = "🎉 RSVP"

# Replace sidebar with top navigation (mobile friendly)
page = st.sidebar.radio("Navigate to:", ["🎉 RSVP", "💳 Payment"],
                    index=["🎉 RSVP", "💳 Payment"].index(st.session_state.page))
st.session_state.page = page

# ---------- Page 1: RSVP ----------
if st.session_state.page == "🎉 RSVP":
    st.markdown("<h2 style='text-align: center;'>✨ Olivia's 30th Birthday ✨</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Elibathian Banquet and Ceilidh at Lumley Castle</h4>", unsafe_allow_html=True)

    st.image(
        "https://eu-assets.simpleview-europe.com/durham2016/imageresizer/?image=%2Fdmsimgs%2F14_2094221340.jpg&action=Open_Graph_img",
        use_container_width=True
    )

    st.markdown("""
    <div style="
        padding:1rem;
        border-radius:0.75rem;
        border:1px solid var(--secondary-background);
        background-color:rgba(255,255,255,0.05)
    ">
    <h3 style="text-align:center;">👑 You are invited! 👑</h3>
    <h4 style="text-align:center;"><strong>🏰 Lumley Castle</strong></h4>
    <p style="text-align:center">
    <a href="https://www.lumleycastle.com/" target="_blank">📍 Chester-le-Street, County Durham</a>
    </p>
    <h5>🗓️ <strong>Date:</strong> Saturday, 17th January 2026</h5>
    <h5>🎭 <strong>Dress Code:</strong> Lords in <strong>kilts</strong> or suits, Ladies in regal attire</h5>
    <h5>💰 <strong>Contribution:</strong> £35 toward the feast, if you can ❤️</h5>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🍷 What's included:")
    st.markdown("""
    - Bagpipe courtyard arrival  
    - Lords & Ladies entertainment  
    - Five-course banquet  
    - Red wine & mead  
    - **Ceilidh dancing**  
    """)

    st.markdown("### 🕐 Timings:")
    st.markdown("""
    - Bar opens: **6:00pm**  
    - Show begins: **7:30pm**  
    - Ceilidh: **10:30pm**  
    - Carriages: **1:00am**  
    """)

    st.markdown("---")

    with st.form("rsvp_form"):
        first_name = st.text_input("First name")
        last_name = st.text_input("Last name")

        attending = st.radio("Will you attend?", ["Yes", "No", "Maybe"])
        contribution = st.radio("Can you contribute £32?", ["Yes", "No", "Not sure yet"])
        diet = st.selectbox("Dietary preference", ["No preference", "Vegan", "Vegetarian", "Pescatarian"])
        allergies = st.text_area("Any allergies or intolerances?")
        notes = st.text_area("Other notes or special requests")

        submitted = st.form_submit_button("Submit RSVP")

        if submitted:
            if not first_name.strip() or not last_name.strip():
                st.error("Please enter both your first and last name.")
            else:
                full_name = f"{first_name.strip()} {last_name.strip()}"
                st.session_state.full_name = full_name

                rsvps = rsvps[~rsvps["Name"].str.strip().str.lower().eq(full_name.strip().lower())]

                new_entry = {
                    "Name": full_name,
                    "Attending": attending,
                    "Contribution": contribution,
                    "Diet": diet,
                    "Allergies": allergies,
                    "Notes": notes,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Paid": "No"
                }
                rsvps = pd.concat([rsvps, pd.DataFrame([new_entry])], ignore_index=True)
                rsvps.to_csv("rsvp_data.csv", index=False)

                if attending == "Yes" and contribution == "Yes":
                    st.success("Thanks! You're being redirected to the payment page...")
                    st.session_state.show_payment = True
                    st.session_state.payment_done = False
                    st.session_state.page = "💳 Payment"
                    st.rerun()
                else:
                    st.success("Thanks! Your RSVP has been recorded.")

# ---------- Page 2: Payment ----------
elif st.session_state.page == "💳 Payment":
    if not st.session_state.show_payment:
        st.info("Please RSVP first before accessing the payment section.")
    elif st.session_state.payment_done:
        st.success("✅ Payment already confirmed. Thank you!")
    else:
        st.header("❤️Thank You So Much!❤️")
        st.write("💳 Please pop your NAME in the payment notes!")

        st.markdown("### 🎉 [Pay £35 via Link](https://revolut.me/olivia3tw?amount=32&currency=GBP) 🎉")
        st.markdown("---")
        st.write("After you've paid, let me know:")

        if st.button("✅ I’ve Paid", use_container_width=True, key="payment_confirm"):
            st.session_state.payment_done = True
            name_lower = st.session_state.full_name.strip().lower()
            rsvps.loc[rsvps["Name"].str.strip().str.lower() == name_lower, "Paid"] = "Yes"
            rsvps.to_csv("rsvp_data.csv", index=False)
            st.balloons()
            st.success("🎉 Thanks! Payment confirmed. 👑✨")
