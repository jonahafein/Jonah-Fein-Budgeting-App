# Jonah-Fein-Budgeting-App
This will be a manual budgeting app inspired by the Every Dollar app.

Eventually it will (hopefully) not be manual.

TODO/Ideas:
- Need methods for users to update data √
- Fix home data bug for entering and saving √
- Income and expenses (make necessary methods in db) √
- Balance and interest rate not saving for house √
- Apy (and likely returns not accepting decimals) √
- Ask for state and local taxes (should be done but need to test) √
- Ask for age (FIX: allow further back inputs) √
- Ask single or married (need to update income table + db methods) - should be done but need to test √
- IMPORTANT: ability for user to edit debt_df (change values or delete items) - same thing for expenses √(Need to test for debt) √
- IMPORTANT: edge case of user starts job mid year so annual income (for tax sake) doesn't align with monthly income for margin sake
- util methods for dashboard √
- Could have a taxes page showing how much to pay each month and avoid big refund or owing tons
- Give time estimates to goals in dashboard
- Need to account for interest rate on debt (we'll just do avalanche method)
- Ask for employer match + if they have access to roth, traditional, both or neither 401k in income
- include 401k match in calculations
- Sometimes more 401k leads to more margin post 401k - Let's see if we can't calculate and optimize this as a rec (or just an fyi)
- After each slider, update monthly margin, let user know, and then set limits to everything
- Save the session state in dashboard in case user goes to other pages
- dashboard (make it update assets and goals as time goes on)
- Check if I ever even use the insert methods or just update
- Add buckets savings (for specific things)
- Add a free LLM for recs + insights
- For recs, find areas to cut costs maybe? - ai insights?
- Make it track month by month (could do beginning or end of the month or both)
- Make the UI look nicer (use st.form for debt_df and expense_df later) - also go and change lots of st.write to be f"{}" format
- Write out sql_table_creation.sql
- maybe add a questions and answers/useful tools or explanations / help page. - also sources and reccomendation logic. 



