import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Olivia's 30th Birthday RSVP",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- CSS STYLING ----------

# st.markdown(
#     """
#     <style>
#     /* Force black text color on radio options and labels, including smaller descriptions */
#     div[role="radiogroup"] label,
#     .stRadio label,
#     .css-1o4mh9l, /* label inside radio groups */
#     .css-1nq57ik, /* possible radio description text */
#     .stTextInput label,
#     .stTextArea label {
#         color: black !important;
#     }

#     /* Also fix the smaller descriptive text under radio buttons */
#     div[role="radiogroup"] div[data-testid="stMarkdownContainer"] {
#         color: black !important;
#     }

#     /* Fix for text under radio buttons wrapped in spans or divs */
#     div[role="radiogroup"] span,
#     div[role="radiogroup"] div {
#         color: black !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <style>
#     body {
#         background-image: url("https://i.gifer.com/7CRL.gif");
#         background-size: cover;
#         background-attachment: fixed;
#         background-position: center;
#     }

#     .stApp {
#         background-color: rgba(255, 255, 255, 0.85);
#         padding: 1rem;
#         border-radius: 10px;
#         color: black !important;
#     }

#     html, body, .stApp, label, .css-1d391kg, .css-1n76uvr, .css-1v3fvcr, .st-bb, .stRadio label, .stTextInput label, .stTextArea label {
#         color: black !important;
#     }

#     /* Fix radio button options text color */
#     div[role="radiogroup"] label,
#     .stRadio label {
#         color: black !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# ---------- Load or Initialize Data ----------
try:
    rsvps = pd.read_csv("rsvp_data.csv")
except FileNotFoundError:
    rsvps = pd.DataFrame(columns=[
        "Name", "Attending", "Contribution", "Main Meal",
        "Dessert", "Allergies", "Notes", "Timestamp", "Paid"
    ])

# ---------- Session State ----------
if "show_payment" not in st.session_state:
    st.session_state.show_payment = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "full_name" not in st.session_state:
    st.session_state.full_name = ""
if "page" not in st.session_state:
    st.session_state.page = "🎉 RSVP"
if "admin_access" not in st.session_state:
    st.session_state.admin_access = False

# ---------- Navigation Sidebar ----------
page = st.sidebar.radio(
    "Navigate to:", 
    ["🎉 RSVP", "💳 Payment", "🔐 Host View"], 
    index=["🎉 RSVP", "💳 Payment", "🔐 Host View"].index(st.session_state.page) if st.session_state.page in ["🎉 RSVP", "💳 Payment", "🔐 Host View"] else 0
)
st.session_state.page = page

# ---------- PAGE 1: RSVP ----------
if st.session_state.page == "🎉 RSVP":
    st.markdown("<h3 style='text-align: center;'>✨ Olivia's 30th ✨</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>The Most Important Party of the Year.</h3>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center;'>Dinner and Ceilidh at Brinkburn Brewery</h6>", unsafe_allow_html=True)

    st.image("AIPIC.png", use_container_width=True)

    st.markdown("""
    <div style="padding:1rem; border-radius:0.75rem; border:1px solid var(--secondary-background); background-color:rgba(255,255,255,0.05)">
      <h3 style="text-align:center;">👑 You are invited! 👑</h3>
      <h5 style="text-align:center;">B THERE OR BE SQUARE</h5>
    </div>
    """, unsafe_allow_html=True)
      
    # 🎉 Countdown Timer
    event_date = datetime(2026, 1, 17, 17, 0, 0)  # 5:00pm
    now = datetime.now()
    countdown = event_date - now

    if countdown.total_seconds() > 0:
        days = countdown.days
        hours, remainder = divmod(countdown.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        st.markdown(f"""
        <div style="text-align: center; font-size: 1.5rem; padding: 1rem; background-color: #fffbe6; border-radius: 10px; margin-bottom: 1rem;">
            ⏳ <strong>Countdown to Party:</strong><br>
            <span style="font-size: 2rem;">{days}d {hours}h {minutes}m {seconds}s</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("🎉 The party has started!")

    st.markdown(
        """
        <h4 style="text-align:center;"><strong>Brinkburn Brewery</strong></h4>
        <p style="text-align:center">
          <a href="https://maps.app.goo.gl/m6KnHvk6p7oLzkUN9" target="_blank">📍 Ouseburn, Newcastle</a>
        </p>
        <h6>🗓️ <strong>Date:</strong> <span style="font-weight: normal;">Saturday, 17th January 2026</span></h6>
        <h6>🎭 <strong>Dress Code:</strong><br>
            <span style="font-weight: normal; padding-left: 1.5rem; display: block;">
                Lairds: <strong>kilts</strong> or suits
            </span>
            <span style="font-weight: normal; padding-left: 1.5rem; display: block;">
                Ladies: Dresses, fancy 👠💃 bring spare shoes if heels aren't the one for dancing
            </span>
        </h6>
        <h6>💰 <strong>Contribution:</strong> <span style="font-weight: normal;">£30 toward the meal and ceilidh, if you can ❤️ (Thank you, Rest will be covered by me)</span></h6>
        """, unsafe_allow_html=True
    )

    st.markdown("### 🕐 Timings:")
    st.markdown("""
    - Arrival/Bar opens: **5:00pm**  
    - Dinner begins: **6:00pm**  
    - Ceilidh: **8:00pm**  
    - Bar Close: **11:30pm** 
    - Kicking Out: **00:00am**  
    """)

    st.markdown("---")

    with st.form("rsvp_form"):
        first_name = st.text_input("First name")
        last_name = st.text_input("Last name")
        attending = st.radio("Will you attend?", ["Yes", "No", "Maybe"])
        contribution = st.radio("Can you contribute £30?", ["Yes", "No", "Not sure yet"])

        st.markdown("### 🍽️ Meal")
        st.markdown("""
        **TRIMMINGS INCLUDE:** Mashed potato, roast skin-on small potatoes, braised red cabbage,  
        pureed carrot and swede mash, Yorkshire pudding, seasonal vegetables, and gravy.
        """)

        course = st.radio(
            "Main Meal (choose one):",
            [
                "BEEF BRISKET: BRAISED IN OUR BYKER BROWN ALE",
                "LAMB SHOULDER: BRAISED IN OUR HOMAGE TO MESOPOTAMIA SHIRAZ AND HONEY PORTER",
                "PORK SHOULDER: BRAISED IN OUR GEORDIE PAGODA PALE ALE",
                "BEER-BRINED CHICKEN BREAST: BRINED IN OUR QUAYSIDE BLONDE CITRA ALE",
                "VEGETARIAN NUT ROAST (Vg): MATCH WITH OUR CUSHTY CUSHY",
                "VEGAN NUT ROAST (Vg): MATCH WITH OUR CUSHTY CUSHY"
            ]
        )

        dessert = st.radio("Dessert:", ["Non-Vegan Option", "Vegan Option"])
        allergies = st.text_area("Any allergies or intolerances?")
        notes = st.text_area("Other notes or special requests. e.g. Mobility issues, etc.")

        submitted = st.form_submit_button("Submit RSVP")

        if submitted:
            if not first_name.strip() or not last_name.strip():
                st.error("Please enter both your first and last name.")
            else:
                full_name = f"{first_name.strip()} {last_name.strip()}"
                st.session_state.full_name = full_name

                # Remove previous entry with the same name if exists
                rsvps = rsvps[~rsvps["Name"].str.strip().str.lower().eq(full_name.strip().lower())]

                new_entry = {
                    "Name": full_name,
                    "Attending": attending,
                    "Contribution": contribution,
                    "Main Meal": course,
                    "Dessert": dessert,
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

# ---------- PAGE 2: Payment ----------
elif st.session_state.page == "💳 Payment":
    if not st.session_state.show_payment:
        st.info("Please RSVP first before accessing the payment section.")
    elif st.session_state.payment_done:
        st.success("✅ Payment already confirmed. Thank you!")
    else:
        st.subheader("❤️ Thank You So Much! ❤️")
        monzo_user = "oliviapalombo"
        amount = 30
        message = st.session_state.full_name.replace(" ", "+")
        monzo_link = f"https://monzo.me/{monzo_user}/{amount}?d={message}"

        st.markdown(
            f'<div style="text-align: center; font-size: 1.25rem;">🎉 <a href="{monzo_link}" target="_blank">Pay £{amount} via Monzo.me</a> 🎉</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.write("After you've paid, let me know:")

        if st.button("✅ I’ve Paid", use_container_width=True, key="payment_confirm"):
            st.session_state.payment_done = True
            name_lower = st.session_state.full_name.strip().lower()
            rsvps.loc[rsvps["Name"].str.strip().str.lower() == name_lower, "Paid"] = "Yes"
            rsvps.to_csv("rsvp_data.csv", index=False)
            st.balloons()
            st.success("🎉 Thanks! Payment confirmed. 👑✨")

# ---------- PAGE 3: Host View ----------
elif st.session_state.page == "🔐 Host View":
    st.subheader("👑 Host RSVP Dashboard")

    if not st.session_state.admin_access:
        password = st.text_input("Enter host password:", type="password")
        if password == "abc123":
            st.session_state.admin_access = True
            st.success("Access granted.")
        elif password:
            st.warning("Incorrect password.")
    else:
        st.dataframe(rsvps)
        csv = rsvps.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", data=csv, file_name="rsvp_data.csv", mime="text/csv")






