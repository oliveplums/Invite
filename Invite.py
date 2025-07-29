#
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Olivia's 30th Birthday RSVP",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load or initialize the RSVP data
try:
    rsvps = pd.read_csv("rsvp_data.csv")
except FileNotFoundError:
    rsvps = pd.DataFrame(columns=[
        "Name", "Attending", "Contribution", "Drink", "First Course", "Second Course", "Third Course", "Fourth Course",
        "Dessert", "Allergies", "Notes", "Timestamp", "Paid"
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

# Add a new page option
page = st.sidebar.radio("Navigate to:", ["🎉 RSVP", "💳 Payment", "🔐 Host View"], index=["🎉 RSVP", "💳 Payment", "🔐 Host View"].index(st.session_state.page) if st.session_state.page in ["🎉 RSVP", "💳 Payment", "🔐 Host View"] else 0)
st.session_state.page = page

# ---------- Page 1: RSVP ----------
if st.session_state.page == "🎉 RSVP":
    st.markdown("<h3 style='text-align: center;'>✨ Olivia's 30th Birthday ✨</h3>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center;'>Elibathian Banquet and Ceilidh at Lumley Castle</h6>", unsafe_allow_html=True)

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
        <a href="https://maps.app.goo.gl/KmAgLYoyM88FNqFR8" target="_blank">📍 Chester-le-Street, County Durham</a>
      </p>
      <h6>🗓️ <strong>Date:</strong> <span style="font-weight: normal;">Saturday, 17th January 2026</span></h6>
      <h6>🎭 <strong>Dress Code:</strong> <span style="font-weight: normal;">Lairds in </span><strong>kilts</strong><span style="font-weight: normal;"> or suits, Ladies in regal attire</span></h6>
      <h6>💰 <strong>Contribution:</strong> <span style="font-weight: normal;">£50 toward the feast, if you can ❤️ (Apologies The rest is covered by me – just asking for a little help with the food!)</span></h6>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🍷 What's included:")
    st.markdown("""
    - Bagpipe courtyard arrival  
    - Lairds & Ladies entertainment  
    - Five-course banquet  
    - A Goblet of Red wine & A Goblet of Mead  
    - **Ceilidh dancing**  
    """)

    st.markdown("### 🕐 Timings:")
    st.markdown("""
    - Arrival/Bar opens: **6:00pm**  
    - Entertainment begins: **7:00pm**  
    - Ceilidh: **10:30pm**  
    - Bar Close: **00:30pm** 
    - Carriages: **1:00am**  
    """)

    st.markdown("---")
    
    with st.form("rsvp_form"):
        first_name = st.text_input("First name")
        last_name = st.text_input("Last name")
    
        attending = st.radio("Will you attend?", ["Yes", "No", "Maybe"])
        contribution = st.radio("Can you contribute £50?", ["Yes", "No", "Not sure yet"])
    
        drink = st.radio(
            "Choose your drink option:",
            ["A Goblet of Red Wine & A Goblet of Mead", "Non-alcoholic Alternative"]
        )
    
        st.markdown("### 🍽️ Banquet Menu")
    
        # 1st course
        first_course = st.radio(
            "1st Course (choose one):",
            ["Homemade Vegetable Broth with Wholemeal Bread"]
        )
    
        # 2nd course
        second_course = st.radio(
            "2nd Course (choose one):",
            [
                "Fish Pie with Creamed Potato Topped with Cheese",
                "Butternut Squash Tart and Watercress",
                "Vegan option (TBC)"
            ]
        )
    
        # 3rd course
        third_course = st.radio(
            "3rd Course (choose one):",
            [
                "Ribs Cooked in Red Wine Sauce with Herbs",
                "Leek and Cheese Croquette with Mustard Mayonnaise",
                "Vegan option (TBC)"
            ]
        )
    
        # 4th course
        fourth_course = st.radio(
            "4th Course (choose one):",
            [
                "Chicken Cooked in Mead Sauce with Jacket Potato Salad and Basil Butter",
                "Wild Mushroom Wellington with Gratin Dauphinoise, Carrot and Green Bean Parcel with Vegetarian Gravy",
                "Vegan option (TBC)"
            ]
        )
    
        # Dessert
        dessert = st.radio(
            "Dessert:",
            [
                "Apple and Pear Crumble with Vanilla Ice Cream",
                "Vegan option (TBC)"
            ]
        )
    
        allergies = st.text_area("Any allergies or intolerances?")
        notes = st.text_area("Other notes or special requests. e.g Mobility Issues etc")
    
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
                    "Drink": drink,
                    "First Course": first_course,
                    "Second Course": second_course,
                    "Third Course": third_course,
                    "Fourth Course": fourth_course,
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

# ---------- Page 2: Payment ----------
elif st.session_state.page == "💳 Payment":
    if not st.session_state.show_payment:
        st.info("Please RSVP first before accessing the payment section.")
    elif st.session_state.payment_done:
        st.success("✅ Payment already confirmed. Thank you!")
    else:
        st.subheader("❤️Thank You So Much!❤️")
        st.write("If you’re able to contribute to your ticket the support means the world to me!")

        # Updated Monzo.me payment link
        monzo_user = "oliviapalombo"
        amount = 50
        message = st.session_state.full_name.replace(" ", "+")  # optional to add in message

        monzo_link = f"https://monzo.me/{monzo_user}/{amount}?d={message}"

        st.markdown(f"#### 🎉 [Pay £{amount} via Monzo.me]({monzo_link}) 🎉")
        st.markdown("---")
        st.write("After you've paid, let me know:")

        if st.button("✅ I’ve Paid", use_container_width=True, key="payment_confirm"):
            st.session_state.payment_done = True
            name_lower = st.session_state.full_name.strip().lower()
            rsvps.loc[rsvps["Name"].str.strip().str.lower() == name_lower, "Paid"] = "Yes"
            rsvps.to_csv("rsvp_data.csv", index=False)
            st.balloons()
            st.success("🎉 Thanks! Payment confirmed. 👑✨")



# Add "Admin" page for viewing RSVPs
if "admin_access" not in st.session_state:
    st.session_state.admin_access = False


# ---------- Page 3: Host View ----------
if st.session_state.page == "🔐 Host View":
    st.header("👑 Host RSVP Dashboard")

    if not st.session_state.admin_access:
        password = st.text_input("Enter host password:", type="password")
        if password == "abc123":
            st.session_state.admin_access = True
            st.success("Access granted.")
        else:
            st.warning("Enter the correct password to access the dashboard.")
    else:
        st.dataframe(rsvps)
        csv = rsvps.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", data=csv, file_name="rsvp_data.csv", mime="text/csv")

