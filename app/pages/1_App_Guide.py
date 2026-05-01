import streamlit as st 

st.markdown("""
## Overview

This app is designed to help users optimize their finances in a simple and intuitive way. All inputs are currently manual, with plans to automate them in the future.

The app is best used at the beginning of each month to organize your budget and decide how to allocate your available margin. However, you can use it as frequently or infrequently as you’d like.

**NOTE**: I am not a financial or tax expert. I've done a bit of personal finance research, and the logic and recommendations used in this app are based on what I am choosing to do with my personal finances. 

If at any point you are stuck or need anything clarified, the help page has an ai chatbot to assist you!

---

## Getting Started

At the beginning of each month (or as a first-time user), start by updating the **Assets and Goals** page. Values do not update automatically, so be sure to manually input any changes and click **Save** at the bottom.

Next, update **Settings and/or Income and Expenses** if:
- You are a first-time user, or  
- Your preferences and/or financial situation has changed  

Again, be sure to click **Save** after making any updates.

---

## Using the Dashboard

The **Dashboard** provides:
- A snapshot of your financial position  
- Personalized recommendations  
- Financial planning with tools to explore saving and investing strategies

Adjust the sliders to test different allocation strategies and decide how to best use your monthly margin. Once finished, click **Save** at the bottom to preserve your selections and projections.

---

## Keeping Everything Updated

If you apply any recommendations from the dashboard that change your financial inputs (income, expenses, assets, settings, etc.), make sure to update those changes on the appropriate pages and save them.

After updating, return to the dashboard to see:
- An updated financial snapshot  
- Revised recommendations  
- New projections  
            
**NOTE:** If you reload the app at any point, you will have to log back in. There is no need to reload after saving values. 
            
--- 
## Coming Soon
- A place in the app to download and upload bank statements to see how your spending compared to your chosen budget
- Excel Sheet export of your financial plan
 
""")
