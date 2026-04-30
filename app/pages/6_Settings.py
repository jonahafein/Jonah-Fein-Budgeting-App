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
months_emergency_desire = settings["months_emergency_desire"] if settings else 3
emergency_importance = settings["emergency_importance"] if settings else "extremely"
investing_aggression = settings["investing_aggression"] if settings else "balanced"
bonus_strategy = settings["bonus_strategy"] if settings else "save"

st.session_state.debt_aggression = debt_aggression if debt_aggression else "extremely"
st.session_state.months_emergency_desire = months_emergency_desire if months_emergency_desire else 3
st.session_state.emergency_importance = emergency_importance if emergency_importance else "extremely"
st.session_state.investing_aggression = investing_aggression if investing_aggression else "balanced"
st.session_state.bonus_strategy = bonus_strategy if bonus_strategy else "save"


st.title("Settings")
st.write("The goal of this page is to help you set your preferences for us to best customize your experience.")

if st.session_state.email:
    email = st.session_state.email
    debt_and_emergency = ("extremely", "moderately", "minimally")
    idx_debt_agg = debt_and_emergency.index(st.session_state.debt_aggression)
    idx_emergency = debt_and_emergency.index(st.session_state.emergency_importance)
    debt_aggression = st.selectbox("How aggressive are you willing to be with paying off your debt? (ignore if you don't have any debt)", options = ("extremely", "moderately", "minimally"), index = idx_debt_agg)
    st.session_state.debt_aggression = debt_aggression
    months_emergency_desire = st.slider("Ideally, how many months of expenses would you consider to be suffient savings for your emergency fund?", value = st.session_state.months_emergency_desire, max_value = 36)
    emergency_importance = st.selectbox("How important is having a sufficient emergency fund to you?", options = ("extremely", "moderately", "minimally"), index = idx_emergency)
    st.session_state.emergency_importance = emergency_importance
    investing_choice = ("conservative", "balanced", "aggressive")
    idx_investing = investing_choice.index(st.session_state.investing_aggression)
    investing_aggression = st.selectbox("How aggressively do you want to invest?", options = ("conservative", "balanced", "aggressive"), index = idx_investing)
    st.session_state.investing_aggression = investing_aggression
    bonus_choice = ("save", "invest", "split")
    idx_bonus = bonus_choice.index(st.session_state.bonus_strategy)
    bonus_strategy = st.selectbox("How do you want to use your bonus?", options = ("save", "invest", "split"), index = idx_bonus)
    st.session_state.bonus_strategy = bonus_strategy
    if st.button("Save Settings"):
        db = Database()
        user_id = db.get_user(email)["user_id"]
        db.update_settings(user_id, debt_aggression, months_emergency_desire, emergency_importance, investing_aggression, bonus_strategy)
        st.success("Settings Saved!")