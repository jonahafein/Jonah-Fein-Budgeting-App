import streamlit as st 
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db import Database

# making user enter email to log in first
if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()

# getting their user_id  
db = Database()
user = db.get_user(st.session_state.email)
if not user:
    st.error("User not found")
    st.stop()

user_id = user["user_id"]

settings = db.get_settings(user_id)
debt_aggression = settings["debt_aggression"] if settings else "extremely"
emergency_importance = settings["emergency_importance"] if settings else "extremely"
ai_permission = settings["ai_permission"] if settings else "no"
investing_aggression = settings["investing_aggression"] if settings else "balanced"
bonus_strategy = settings["bonus_strategy"] if settings else "save"

st.session_state.debt_aggression = debt_aggression if debt_aggression else "extremely"
st.session_state.emergency_importance = emergency_importance if emergency_importance else "extremely"
st.session_state.ai_permission = ai_permission if ai_permission else "no"
st.session_state.investing_aggression = investing_aggression if investing_aggression else "balanced"
st.session_state.bonus_strategy = bonus_strategy if bonus_strategy else "save"


st.title("Settings:")
st.write("The goal of this page is to help you set your preferences for us to best customize your experience.")

st.subheader("Debt Agression")
if st.session_state.email:
    email = st.session_state.email
    debt_aggression = st.selectbox("How aggressive are you willing to be with paying off your debt? (ignore if you don't have any debt)", ["extremely", "moderately", "minimally"], value = st.session_state.debt_aggression)
    st.session_state.debt_aggression = debt_aggression
    ai_permission = st.selectbox("Allow the AI assistant to access your financial data for more personalized help?",options=["no", "yes"], value = st.session_state.ai_permission)
    st.caption(
        "If you choose 'yes', the assistant will use your inputs (income, expenses, assets, etc.) to give better recommendations. "
        "Your data is only used within this app and is not shared externally. "
        "You can still use the assistant without sharing your data."
    )
    st.session_state.ai_permission = ai_permission
    emergency_importance = st.selectbox("How important is saving at least 3 months of expenses to you? (ignore if you've already saved 3+ months of expenses)", ["extremely", "moderately", "minimally"], value = st.session_state.emergency_importance)
    st.session_state.emergency_importance = emergency_importance
    investing_aggression = st.selectbox("How aggressively do you want to invest?",options = ["conservative", "balanced", "aggressive"], value = st.session_state.investing_aggression)
    st.session_state.investing_aggression = investing_aggression
    bonus_strategy = st.selectbox("How do you want to use your bonus?", options = ["save", "invest", "split"], value = st.session_state.bonus_strategy)
    st.session_state.bonus_strategy = bonus_strategy
    if st.button("Save Settings"):
        db = Database()
        user_id = db.get_user(email)["user_id"]
        db.update_settings(user_id, debt_aggression, ai_permission, emergency_importance, investing_aggression, bonus_strategy)
        st.success("Settings Saved!")