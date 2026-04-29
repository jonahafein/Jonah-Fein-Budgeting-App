# Jonah-Fein-Budgeting-App
This will be a manual budgeting app inspired by the Every Dollar app.

Eventually it will (hopefully) not be manual.

TODO/Ideas:
- Lots of dashboard will need to be redone or updated with settings + goals + 12 mo plan
- switch 401k to monthly everywhere
- will need to redefine goals table in supabase
- margin_on_debt_monthly to session state and database
- Generate excel as 12 month plan / outlook (would need to ask when bonus comes)
- Update App Guide for settings + goals 
- Could have 3rd column to expenses to classify needs versus wants - useful in recs
- Secondary income question
- Have mortgage load as an expense automatically possibly
- Tax deduction for kids + other deductions
- Could do percentile of net worth for age or percentile of everything for age
- Add buckets savings (for specific things)
- Savings buckets/goals
- Projections could include time frame for getting out of debt for those in debt, also time frame for savings goals/buckets (in the sheet)
- have some check for negative monthly margin with warning user must fix (income up expenses down)
- Make it track month by month (could do beginning or end of the month or both)
- Make the UI look nicer (use st.form for debt_df and expense_df later) - also go and change lots of st.write to be f"{}" format
- Eventually could have a progress over time page or add on to dashboard - would require selecting date and adding to supabase
- maybe give an "other" for assets and let user value it 


