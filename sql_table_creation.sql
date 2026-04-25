-- Run the following in your Azure SQL Database to create necessary tables:
CREATE TABLE [dbo].[users]
(
	  [user_id] INT NOT NULL IDENTITY(1,1)
	, [user_email] VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
	, [birthdate] DATE NULL
	, CONSTRAINT [PK__users__B9BE370F56A07DBD] PRIMARY KEY ([user_id] ASC)
)

CREATE UNIQUE NONCLUSTERED INDEX [UQ__users__B0FBA2129CBCF8AD] ON [dbo].[users] ([user_email] ASC)

CREATE TABLE [dbo].[dashboard]
(
	  [user_id] INT NOT NULL
	, [trad_401k_contributions] INT NULL
	, [trad_401k_match_annual] INT NULL
	, [roth_ira_monthly] INT NULL
	, [roth_401k_contributions_monthly] INT NULL
	, [roth_401k_match_monthly] INT NULL
	, [years_from_retirement] INT NULL
	, [brokerage_contributions_monthly] INT NULL
	, [years_from_brokerage] INT NULL
	, [future_savings_view] INT NULL
	, CONSTRAINT [PK__dashboar__B9BE370F7D3DF9F5] PRIMARY KEY ([user_id] ASC)
)

ALTER TABLE [dbo].[dashboard] WITH CHECK ADD CONSTRAINT [FK__dashboard__user___29221CFB] FOREIGN KEY([user_id]) REFERENCES [dbo].[users] ([user_id])
ALTER TABLE [dbo].[dashboard] CHECK CONSTRAINT [FK__dashboard__user___29221CFB]

CREATE TABLE [dbo].[debt]
(
	  [debt_id] INT NOT NULL IDENTITY(1,1)
	, [user_id] INT NULL
	, [debt_item] VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
	, [debt_balance] DECIMAL(12,2) NULL
	, [debt_interest] DECIMAL(5,2) NULL
	, CONSTRAINT [PK__debt__A7DCE7F98F8B058D] PRIMARY KEY ([debt_id] ASC)
)

ALTER TABLE [dbo].[debt] WITH CHECK ADD CONSTRAINT [FK__debt__user_id__05D8E0BE] FOREIGN KEY([user_id]) REFERENCES [dbo].[users] ([user_id]) ON DELETE CASCADE
ALTER TABLE [dbo].[debt] CHECK CONSTRAINT [FK__debt__user_id__05D8E0BE]

CREATE TABLE [dbo].[expenses]
(
	  [expense_id] INT NOT NULL IDENTITY(1,1)
	, [user_id] INT NULL
	, [category] VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
	, [amount] DECIMAL(12,2) NULL
	, CONSTRAINT [PK__expenses__404B6A6BA56EDEDF] PRIMARY KEY ([expense_id] ASC)
)

ALTER TABLE [dbo].[expenses] WITH CHECK ADD CONSTRAINT [FK__expenses__user_i__18EBB532] FOREIGN KEY([user_id]) REFERENCES [dbo].[users] ([user_id]) ON DELETE CASCADE
ALTER TABLE [dbo].[expenses] CHECK CONSTRAINT [FK__expenses__user_i__18EBB532]

CREATE TABLE [dbo].[goals]
(
	  [goal_id] INT NOT NULL IDENTITY(1,1)
	, [user_id] INT NULL
	, [goal] VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
	, CONSTRAINT [PK__goals__76679A24044F83CA] PRIMARY KEY ([goal_id] ASC)
)

ALTER TABLE [dbo].[goals] WITH CHECK ADD CONSTRAINT [FK__goals__user_id__02FC7413] FOREIGN KEY([user_id]) REFERENCES [dbo].[users] ([user_id]) ON DELETE CASCADE
ALTER TABLE [dbo].[goals] CHECK CONSTRAINT [FK__goals__user_id__02FC7413]

CREATE UNIQUE NONCLUSTERED INDEX [UQ__goals__1DE1FE8BF1BF7353] ON [dbo].[goals] ([user_id] ASC, [goal] ASC)

CREATE TABLE [dbo].[home]
(
	  [user_id] INT NOT NULL
	, [paid_off] BIT NULL
	, [home_value] DECIMAL(12,2) NULL
	, [years] DECIMAL(5,2) NULL
	, [balance] DECIMAL(12,2) NULL
	, [interest] DECIMAL(5,2) NULL
	, [fees] DECIMAL(12,2) NULL
	, CONSTRAINT [PK__home__B9BE370F426EEC37] PRIMARY KEY ([user_id] ASC)
)

ALTER TABLE [dbo].[home] WITH CHECK ADD CONSTRAINT [FK__home__user_id__7F2BE32F] FOREIGN KEY([user_id]) REFERENCES [dbo].[users] ([user_id]) ON DELETE CASCADE
ALTER TABLE [dbo].[home] CHECK CONSTRAINT [FK__home__user_id__7F2BE32F]

CREATE TABLE [dbo].[income]
(
	  [user_id] INT NOT NULL
	, [annual_income] DECIMAL(12,2) NULL
	, [annual_bonus] DECIMAL(12,2) NULL
	, [state_tax_perc] DECIMAL(12,2) NULL
	, [local_tax_perc] DECIMAL(12,2) NULL
	, [marriage_status] VARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
	, [employer_match] DECIMAL(12,2) NULL
	, [months_worked] INT NULL
	, CONSTRAINT [PK__income__B9BE370F9AC23DA9] PRIMARY KEY ([user_id] ASC)
)

ALTER TABLE [dbo].[income] WITH CHECK ADD CONSTRAINT [FK__income__user_id__160F4887] FOREIGN KEY([user_id]) REFERENCES [dbo].[users] ([user_id]) ON DELETE CASCADE
ALTER TABLE [dbo].[income] CHECK CONSTRAINT [FK__income__user_id__160F4887]

CREATE TABLE [dbo].[non_home_assets]
(
	  [user_id] INT NOT NULL
	, [savings] DECIMAL(12,2) NULL
	, [apy] DECIMAL(5,2) NULL
	, [brokerage] DECIMAL(12,2) NULL
	, [brokerage_returns] DECIMAL(5,2) NULL
	, [retirement] DECIMAL(12,2) NULL
	, [retirement_returns] DECIMAL(5,2) NULL
	, CONSTRAINT [PK__non_home__B9BE370F1371B572] PRIMARY KEY ([user_id] ASC)
)

ALTER TABLE [dbo].[non_home_assets] WITH CHECK ADD CONSTRAINT [FK__non_home___user___7C4F7684] FOREIGN KEY([user_id]) REFERENCES [dbo].[users] ([user_id]) ON DELETE CASCADE
ALTER TABLE [dbo].[non_home_assets] CHECK CONSTRAINT [FK__non_home___user___7C4F7684]

