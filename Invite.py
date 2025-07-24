import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Olivia's 30th RSVP", page_icon="🏰")

# Load existing responses
try:
    rsvps = pd.read_csv("rsvp_data.csv")
except FileNotFoundError:
    rsvps = pd.DataFrame(columns=[
        "Name", "Attending", "Contribution", "Diet", "Allergies", "Notes", "Timestamp"
    ])

tab1, tab2 = st.tabs(["🎟️ RSVP & Meal Preferences", "🔍 View RSVPs"])

# ---------- TAB 1: RSVP + Meal Preferences ----------
with tab1:
    st.markdown("<h1 style='text-align: center;'>✨ Olivia's 30th Birthday ✨</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Elibathian Banquet and Ceilidh at Lumley Castle</h3>", unsafe_allow_html=True)
    
    st.image(
        "https://eu-assets.simpleview-europe.com/durham2016/imageresizer/?image=%2Fdmsimgs%2F14_2094221340.jpg&action=Open_Graph_img" 
        )
        
    st.markdown("""
    <div style="background-color:#f9f4f1;padding:1.5rem;border-radius:1rem;border:1px solid #e0dede">

    <h2 style="text-align:center;color:#7a3e2e">👑 You are invited! 👑</h2>

    <p style="font-size:1.1rem;">
    Join me for a magical celebration of my <strong>30th birthday</strong> at the unforgettable
    <strong>Elibathian Banquet</strong> hosted at the magnificent:
    </p>

    <h3 style="text-align:center;color:#5e2b1c"><strong>🏰 Lumley Castle</strong></h3>
    <p style="text-align:center;margin-bottom:1rem;">
    <a href="https://www.google.com/maps/place/Lumley+Castle/@54.8533258,-1.5558391,17z/data=!4m9!3m8!1s0x487e7caad2d7ed1d:0x1d04593a95f1554b!5m2!4m1!1i2!8m2!3d54.8533258!4d-1.5532642!16zL20vMDRkcXBw?entry=ttu&g_ep=EgoyMDI1MDcyMi4wIKXMDSoASAFQAw%3D%3D" target="_blank">📍 Chester-le-Street, County Durham</a>
    </p>

    <hr style="margin-top:1.5rem; margin-bottom:1rem;">

    <h4 style="margin-bottom:0.3rem;">📅 <strong>Date:</strong></h4>
    <p style="font-size:1.1rem; margin-top:0;">Saturday, 17th January 2026</p>

    <h4 style="margin-bottom:0.3rem;">🎭 <strong>Dress Code:</strong></h4>
    <p style="font-size:1.1rem; margin-top:0;">Lords: <strong>Kilts</strong> if possible (or suit if not)
    <br>Ladies: Regal Attire</p>

    <h4 style="margin-bottom:0.3rem;">💰 <strong>Contribution:</strong></h4>
    <p style="font-size:1.1rem; margin-top:0;">
    If you're able to, a <strong>£32 contribution</strong> toward the food would be greatly appreciated ❤️  
    <br>I’ll gladly cover the rest.
    </p>

    </div>
    """, unsafe_allow_html=True)




    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🍷 Your evening includes:")
        st.markdown("""
        - Bagpipe arrival in the inner courtyard  
        - Entertainment by Lords & Ladies of the Court  
        - Five-course banquet  
        - A glass of red wine  
        - A glass of mead  
        - **Ceilidh dancing**   
        """)

    with col2:
        st.markdown("### 🕖 Evening Timings:")
        st.markdown("""
        - Bar opens: **6:00pm**  
        - Entertainment begins: **7:30pm**  
        - Entertainment ends: **~10:00pm**  
        - **Ceilidh starts:** **10:30pm**  
        - Bar closes: **12:30am**  
        - Ends: **1:00am**  
        """)

    st.markdown("---")

with st.form("rsvp_form"):
    # Collect existing names to allow selection
    existing_names = sorted(rsvps["Name"].dropna().unique())

    # Step 1: Session state init
    if "name_input" not in st.session_state:
        st.session_state.name_input = ""
    if "prev_selection" not in st.session_state:
        st.session_state.prev_selection = ""

    # Step 2: Selectbox for existing names
    name_selection = st.selectbox(
        "Select your name (or choose to enter a new one)",
        options=[""] + existing_names,
        index=0,
        key="name_selectbox"
    )

    # Step 4: Continue form if name entered
    if name_selection.strip():
    # Step 3: Sync text input with dropdown
        if name_selection and name_selection != st.session_state.prev_selection:
            st.session_state.name_input = name_selection
            st.session_state.prev_selection = name_selection

        name = st.text_input("Edit your name if needed", value=st.session_state.name_input, key="name_input_box")


        attending = st.radio("Will you attend?", ["Yes", "No", "Maybe"])
        contribution = st.radio(
            "Will you be able to contribute £32 toward your meal?",
            ["Yes", "No", "Not sure yet"]
        )
        diet = st.selectbox("Dietary preference", ["No preference", "Vegan", "Vegetarian", "Pescatarian"])
        allergies = st.text_area("Any allergies or intolerances?")
        notes = st.text_area("Other notes or special requests")

    submitted = st.form_submit_button("Fill In RSVP")

    if submitted:
        if not name.strip():
            st.error("Please enter your name before submitting.")
        else:
            # Step 5: Remove original name (if changed)
            if name_selection and name.strip().lower() != name_selection.strip().lower():
                rsvps = rsvps[rsvps["Name"].str.lower() != name_selection.strip().lower()]
            else:
                rsvps = rsvps[rsvps["Name"].str.lower() != name.strip().lower()]

            new_entry = {
                "Name": name.strip(),
                "Attending": attending,
                "Contribution": contribution,
                "Diet": diet,
                "Allergies": allergies,
                "Notes": notes,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            rsvps = pd.concat([rsvps, pd.DataFrame([new_entry])], ignore_index=True)
            rsvps.to_csv("rsvp_data.csv", index=False)
            st.success("Thank you! Your RSVP and preferences have been recorded.")

with tab2:
    st.header("🔍 RSVP List")
    st.dataframe(rsvps[['Name', 'Attending', 'Diet', 'Allergies', 'Notes']])