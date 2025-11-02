import streamlit as st
import pandas as pd
import openai

# ============ BACKEND SETUP ============
# Set your OpenAI API key (replace with your own key)
openai.api_key = "YOUR_OPENAI_API_KEY"

# Load EV dataset
ev_data = pd.read_csv("ev_data.csv")

# Function to search EV info
def get_ev_info(model_name):
    model_name = model_name.lower()
    for _, row in ev_data.iterrows():
        if model_name in row['Model'].lower():
            return f"""
*Model:* {row['Model']}
- Battery Capacity: {row['Battery_kWh']} kWh  
- Range: {row['Range_km']} km  
- Charging Time: {row['Charging_Time_hr']} hrs  
- Price: ₹{row['Price_Lakh']} lakh
"""
    return "Sorry, I couldn’t find that EV model in my database."

# Function to generate AI response
def generate_response(user_query):
    # Add EV data lookup
    for model in ev_data["Model"]:
        if model.lower() in user_query.lower():
            return get_ev_info(model)

    # Otherwise, use Generative AI
    prompt = f"""
You are an AI chatbot that gives information about Electric Vehicles (EVs).
Answer the following user query clearly and briefly:
{user_query}
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "⚠ Error generating response. Check your API key or internet connection."

# ============ FRONTEND (STREAMLIT UI) ============
st.set_page_config(page_title="EV Performance Chatbot", page_icon="⚡", layout="centered")

st.title("⚡ EV Performance Chatbot using Generative AI")
st.write("Ask me anything about Electric Vehicles — models, range, charging time, or comparisons!")

# Text input
user_query = st.text_input("Enter your question here:")

if st.button("Ask"):
    if user_query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = generate_response(user_query)
        st.markdown("### 💬 Chatbot Response:")
        st.write(answer)

st.markdown("---")
st.caption("Developed by Abhilasha J. Rathi — TE Computer Engineering Project 2025")