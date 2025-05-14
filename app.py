import streamlit as st
#from flight_search import search_flights
#from chatbot import ask_gpt
import pandas as pd
import openai



def search_flights(from_city, to_city, depart_date, trip_type="One way", return_date=None):
    df = pd.read_excel("flights.xlsx")
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    depart_flights = df[
        (df['From'].str.lower() == from_city.lower()) &
        (df['To'].str.lower() == to_city.lower()) &
        (df['Date'] == depart_date)
    ]

    if trip_type == "Return" and return_date:
        return_flights = df[
            (df['From'].str.lower() == to_city.lower()) &
            (df['To'].str.lower() == from_city.lower()) &
            (df['Date'] == return_date)
        ]
        return depart_flights, return_flights

    return depart_flights, pd.DataFrame()  # Empty df if not a return trip



def ask_gpt(query):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-4o
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content.strip()


st.set_page_config(page_title="Qatar AI Airways", layout="wide")

# Custom CSS for header & button
st.markdown("""
<style>
.hero-section {
    position: relative;
    width: 100%;
    height: 400px;
    background-image: url('https://www.qatarairways.com/content/dam/images/renditions/horizontal-1/miscellaneous/payment/h1-card-laptop-hn.jpg');
    background-size: cover;
    background-position: center;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    margin-bottom: 3rem;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom right, rgba(0, 0, 0, 0.4), rgba(0,0,0,0.7));
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 2rem 3rem;
    color: white;
}

.hero-overlay h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-overlay p {
    font-size: 1.2rem;
}

.qatar-logo {
    width: 180px;
    margin-bottom: 2rem;
}
</style>

<div class="hero-section">
  <div class="hero-overlay">
    <img src="https://www.usqbc.org/public/frontend/images/our_members/Qatar_Airways_Logo.png" class="qatar-logo" />
    <h1>Fly the World with Qatar Airways</h1>
    <p>Discover luxury, comfort, and award-winning service on every journey.</p>
  </div>
</div>
""", unsafe_allow_html=True)


# HERO section
st.markdown("""
<div class="hero">
    <h1>Book now, Pay using EMI</h1>
    <p>Pay online in easy monthly installment of up to 12 months</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["🛫 Book a Flight", "🧠 Travel Assistant (AI)"])

with tab1:
    st.markdown("<div class='search-section'>", unsafe_allow_html=True)
    st.subheader("Search Flights")

    col1, col2, col3 = st.columns(3)
    with col1:
        trip_type = st.radio("Trip Type", ["Return", "One way", "Multi-city"], horizontal=True)
    with col2:
        from_city = st.text_input("From", "Doha")
        to_city = st.text_input("To", "Dubai")
    with col3:
        passengers = st.selectbox("Passengers / Class", ["1 Passenger Economy", "2 Business Class"])

    col4, col5 = st.columns(2)
    with col4:
        depart_date = st.date_input("Departure", value=pd.to_datetime("2025-05-14"))
    with col5:
        return_date = st.date_input("Return", value=pd.to_datetime("2025-05-21"))

    if st.button("🔍 Search Flights", type="primary"):
        outbound_flights, return_flights = search_flights(
            from_city, to_city, depart_date, trip_type, return_date
        )

        if not outbound_flights.empty:
            st.success(f"{len(outbound_flights)} outbound flights found.")
            st.subheader("Outbound Flights")
            st.dataframe(outbound_flights)
        else:
            st.warning("No outbound flights found.")

        if trip_type == "Return":
            if not return_flights.empty:
                st.success(f"{len(return_flights)} return flights found.")
                st.subheader("Return Flights")
                st.dataframe(return_flights)
            else:
                st.warning("No return flights found.")



    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("Ask our AI anything about your travel")
    question = st.text_area("E.g. What documents do I need for Germany?")
    if st.button("Ask AI ✈️"):
        if question:
            with st.spinner("Thinking..."):
                st.markdown(ask_gpt(question))
        else:
            st.warning("Please enter a question.")

# Fancy Offers Section
st.markdown("""
<style>
.card-container {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 3rem;
}
.card {
    flex: 1 1 220px;
    max-width: 260px;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    background: #fff;
    transition: 0.3s ease;
}
.card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
}
.card h4 {
    margin: 0.5rem;
}
.card p {
    margin: 0.5rem;
    font-size: 0.9rem;
    color: #555;
}
.card a {
    display: block;
    margin: 0.5rem;
    font-weight: bold;
    color: #8c154d;
    text-decoration: none;
}
</style>

<h2>Start planning your next trip</h2>
<p>Thinking of travelling somewhere soon? Here are some options to help you get started.</p>

<div class="card-container">
    <div class="card">
        <img src="https://www.qatarairways.com/content/dam/images/renditions/horizontal-3/brand/aircraft/codeshare-partners/h3-qr-indigo.jpg" />
        <h4>Discover the world with IndiGo</h4>
        <a href="#">Book now →</a>
    </div>
    <div class="card">
        <img src="https://www.qatarairways.com/content/dam/us/h3/h3-visit-qatar-mia-family-dhow-qta.jpg" />
        <h4>Stopover in Qatar from $14</h4>
        <a href="#">Find out more →</a>
    </div>
    <div class="card">
        <img src="https://www.qatarairways.com/content/dam/images/renditions/horizontal-3/brand/aircraft/a350/h3-a350-aircraft-flight1.jpg" />
        <h4>Save up to 15% with HDFC</h4>
        <a href="#">Book now →</a>
    </div>
    <div class="card">
        <img src="https://www.qatarairways.com/content/dam/images/renditions/horizontal-3/campaigns/global/destinations-promo/h3-toronto-tower.jpg" />
        <h4>Enjoy 5x weekly flights to Toronto</h4>
        <a href="#">Discover more →</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<hr style="margin-top:3rem; margin-bottom:1rem;">
<h3>Find great fares</h3>
""", unsafe_allow_html=True)

fare_city = st.text_input("From", "Mumbai BOM")
trending_fares = pd.DataFrame({
    "To": ["Doha", "Dubai", "New York", "London"],
    "Price (USD)": [150, 220, 650, 580],
    "Airline": ["Qatar Airways"]*4,
    "Class": ["Economy", "Economy", "Business", "Economy"]
})
st.dataframe(trending_fares, use_container_width=True)
