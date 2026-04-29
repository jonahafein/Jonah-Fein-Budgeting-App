-- USERS
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_email TEXT UNIQUE,
    birthdate DATE
);

-- DASHBOARD
CREATE TABLE dashboard (
    user_id INT PRIMARY KEY,
    margin_on_debt_monthly INT,
    trad_401k_contributions INT,
    trad_401k_match_annual INT,
    roth_ira_monthly INT,
    roth_401k_contributions_monthly INT,
    roth_401k_match_monthly INT,
    years_from_retirement INT,
    brokerage_contributions_monthly INT,
    years_from_brokerage INT,
    future_savings_view INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- DEBT
CREATE TABLE debt (
    debt_id SERIAL PRIMARY KEY,
    user_id INT,
    debt_item TEXT,
    debt_balance NUMERIC(12,2),
    debt_interest NUMERIC(5,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- EXPENSES
CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    user_id INT,
    category TEXT,
    amount NUMERIC(12,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- GOALS
CREATE TABLE goals (
    goal_id SERIAL PRIMARY KEY,
    user_id INT,
    goal_name TEXT,
    target_amount NUMERIC(12,2),
    timeline_years INT,
    priority TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- HOME
CREATE TABLE home (
    user_id INT PRIMARY KEY,
    paid_off BOOLEAN,
    home_value NUMERIC(12,2),
    years NUMERIC(5,2),
    balance NUMERIC(12,2),
    interest NUMERIC(5,2),
    fees NUMERIC(12,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- INCOME
CREATE TABLE income (
    user_id INT PRIMARY KEY,
    annual_income NUMERIC(12,2),
    annual_bonus NUMERIC(12,2),
    state_tax_perc NUMERIC(12,2),
    local_tax_perc NUMERIC(12,2),
    marriage_status TEXT,
    employer_match NUMERIC(12,2),
    months_worked INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- NON-HOME ASSETS
CREATE TABLE non_home_assets (
    user_id INT PRIMARY KEY,
    savings NUMERIC(12,2),
    apy NUMERIC(5,2),
    brokerage NUMERIC(12,2),
    brokerage_returns NUMERIC(5,2),
    retirement NUMERIC(12,2),
    retirement_returns NUMERIC(5,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);