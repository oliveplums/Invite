import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------- CONFIGURATION ----------
st.set_page_config(
    page_title="Olivia's 30th Birthday RSVP",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- EMAIL FUNCTION ----------
def send_email_notification(new_entry):
    sender_email = "oliviapalombo314@gmail.com"  # ← replace with your Gmail
    receiver_email = "oliviapalombo314@gmail.com"
    app_password = "Rooster6!!!"     # ← replace with your Gmail App Password

    subject = f"New RSVP from {new_entry['Name']}"
    body = "\n".join([f"{k}: {v}" for k, v in new_entry.items()])

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")

# ---------- BACKGROUND STYLING ----------
st.markdown(
    """
    <style>
    body {
        background-image: url("https://i.gifer.com/7CRL.gif");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- LOAD OR INITIALIZE RSVP DATA ----------
try:
    rsvps = pd.read_csv("rsvp_data.csv")
except FileNotFoundError:
    rsvps = pd.DataFrame(columns=[
        "Name", "Attending", "Contribution","Accommodation", "Main Meal",
        "Dessert", "Allergies", "Notes", "Timestamp", "Paid", "Wine"
    ])

# ---------- SESSION STATE ----------
for key, val in {
    "show_payment": False,
    "payment_done": False,
    "full_name": "",
    "page": "🎉 RSVP",
    "admin_access": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------- NAVIGATION ----------
page = st.sidebar.radio(
    "Navigate to:", 
    ["🎉 RSVP", "💳 Payment", "🔐 Host View"], 
    index=["🎉 RSVP", "💳 Payment", "🔐 Host View"].index(st.session_state.page)
)
st.session_state.page = page

# ---------- RSVP PAGE ----------
if page == "🎉 RSVP":
    with st.form("rsvp_form"):
        first_name = st.text_input("First name")
        last_name = st.text_input("Last name")
        attending = st.radio("Will you attend?", ["Yes", "No", "Maybe"])
        contribution = st.radio("Can you contribute £30?", ["Yes", "No", "Not sure yet"])
        
        # Accommodation Option
        st.markdown("### 🏨 Accommodation")
        st.markdown(
            "I'll be arranging a nearby hotel for everyone so we can stay together, "
            "and I'll try to get a group discount. Tick if you need accommodation."
        )
        accommodation = st.multiselect(
            "Which nights would you like accommodation for?",
            ["Friday night", "Saturday night"],
            help="You can select one or both nights, or leave blank if you don't need it."
        )
    
        st.markdown("### 🍽️ Meal")
        st.markdown("**TRIMMINGS INCLUDE:** Mashed potato, Yorkshire pudding, seasonal veg, gravy, and more.")
    
        meal_options = [
            "BEEF BRISKET: braised in our Byker Brown Ale",
            "LAMB SHOULDER: braised in our Homage to Mesopotamia Shiraz and Honey Porter",
            "PORK SHOULDER: braised in our Geordie Pagoda Pale Ale",
            "BEER-BRINED CHICKEN BREAST: brined in our Quayside Blonde Citra Ale",
            "VEGETARIAN NUT ROAST: match with our Cushty Cushy",
            "VEGAN NUT ROAST: match with our Cushty Cushy"
        ]
        styled_options = [f"**{opt.split(':')[0]}**  \n{opt.split(':')[1].strip()}" for opt in meal_options]
        course = st.radio("Main Meal (choose one):", styled_options)
        dessert = st.radio("Dessert:", ["Non-Vegan Option", "Vegan Option"])
        Wine = st.radio("Glass of Wine:", ["Red", "White"])
        allergies = st.text_area("Any allergies or intolerances?")
        notes = st.text_area("Other notes or special requests. e.g. Mobility issues, etc.")
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
                    "Accommodation": ", ".join(accommodation) if accommodation else "None",
                    "Main Meal": course,
                    "Dessert": dessert,
                    "Wine": Wine,
                    "Allergies": allergies,
                    "Notes": notes,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Paid": "No"
                }
                rsvps = pd.concat([rsvps, pd.DataFrame([new_entry])], ignore_index=True)
                rsvps.to_csv("rsvp_data.csv", index=False)
    
                send_email_notification(new_entry)
    
                if attending == "Yes" and contribution == "Yes":
                    st.success("Thanks! You're being redirected to the payment page...")
                    st.session_state.show_payment = True
                    st.session_state.page = "💳 Payment"
                    st.rerun()
                else:
                    st.success("Thanks! Your RSVP has been recorded.")


# ---------- PAYMENT PAGE ----------
elif page == "💳 Payment":
    if not st.session_state.show_payment:
        st.info("Please RSVP first before accessing the payment section.")
    elif st.session_state.payment_done:
        st.success("✅ Payment already confirmed. Thank you!")
    else:
        st.subheader("❤️ Thank You So Much! ❤️")
        st.write("Now you don't have to cry thinking you can't be with me on my birthday!")
        monzo_link = f"https://monzo.me/oliviapalombo/30?d={st.session_state.full_name.replace(' ', '+')}"
        st.markdown(f'<div style="text-align: center;"><a href="{monzo_link}" target="_blank">💳 Pay £30 via Monzo.me</a></div>', unsafe_allow_html=True)
        st.markdown("---")
        if st.button("✅ I’ve Paid", use_container_width=True):
            st.session_state.payment_done = True
            rsvps.loc[rsvps["Name"].str.lower().str.strip() == st.session_state.full_name.lower().strip(), "Paid"] = "Yes"
            rsvps.to_csv("rsvp_data.csv", index=False)
            st.balloons()
            st.success("🎉 Thanks! Payment confirmed.")

# ---------- HOST VIEW ----------
elif page == "🔐 Host View":
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















