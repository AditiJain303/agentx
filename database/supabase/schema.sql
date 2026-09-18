CREATE TABLE public.users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    monthly_income NUMERIC(12,2) NOT NULL,
    current_balance NUMERIC(12,2) NOT NULL,
    risk_profile TEXT,
    monthly_savings_target NUMERIC(12,2),
    financial_goal TEXT,
    CONSTRAINT users_income_positive CHECK (monthly_income >= 0),
    CONSTRAINT users_balance_valid CHECK (current_balance >= 0)
);

CREATE TABLE public.expenses (
    expense_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    category TEXT NOT NULL,
    merchant TEXT NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    payment_method TEXT,
    CONSTRAINT expenses_amount_positive CHECK (amount > 0),
    CONSTRAINT expenses_user_fk FOREIGN KEY (user_id)
        REFERENCES public.users(user_id) ON DELETE CASCADE
);

CREATE TABLE public.budgets (
    budget_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    category TEXT NOT NULL,
    monthly_limit NUMERIC(12,2) NOT NULL,
    month TEXT NOT NULL,
    CONSTRAINT budgets_limit_positive CHECK (monthly_limit > 0),
    CONSTRAINT budgets_user_fk FOREIGN KEY (user_id)
        REFERENCES public.users(user_id) ON DELETE CASCADE,
    CONSTRAINT budgets_unique_category_month
        UNIQUE (user_id, category, month)
);

CREATE TABLE public.subscriptions (
    subscription_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    service TEXT NOT NULL,
    category TEXT,
    monthly_cost NUMERIC(12,2) NOT NULL,
    start_date DATE,
    last_used DATE,
    active BOOLEAN DEFAULT TRUE,
    CONSTRAINT subscriptions_cost_positive CHECK (monthly_cost > 0),
    CONSTRAINT subscriptions_user_fk FOREIGN KEY (user_id)
        REFERENCES public.users(user_id) ON DELETE CASCADE
);

CREATE TABLE public.savings_goals (
    goal_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    goal_name TEXT NOT NULL,
    target_amount NUMERIC(12,2) NOT NULL,
    current_saved NUMERIC(12,2) NOT NULL DEFAULT 0,
    target_date DATE,
    priority TEXT,
    CONSTRAINT goals_target_positive CHECK (target_amount > 0),
    CONSTRAINT goals_saved_valid
        CHECK (current_saved >= 0 AND current_saved <= target_amount),
    CONSTRAINT goals_user_fk FOREIGN KEY (user_id)
        REFERENCES public.users(user_id) ON DELETE CASCADE
);

CREATE TABLE public.financial_decisions (
    decision_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    question TEXT NOT NULL,
    decision TEXT,
    amount NUMERIC(12,2),
    reason TEXT,
    outcome TEXT,
    CONSTRAINT decisions_amount_valid
        CHECK (amount IS NULL OR amount >= 0),
    CONSTRAINT decisions_user_fk FOREIGN KEY (user_id)
        REFERENCES public.users(user_id) ON DELETE CASCADE
);

CREATE TABLE public.agent_actions (
    action_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    action_type TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT,
    CONSTRAINT actions_user_fk FOREIGN KEY (user_id)
        REFERENCES public.users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_expenses_user_id
    ON public.expenses(user_id);

CREATE INDEX idx_expenses_date
    ON public.expenses(date);

CREATE INDEX idx_expenses_user_date
    ON public.expenses(user_id, date);

CREATE INDEX idx_expenses_category
    ON public.expenses(category);

CREATE INDEX idx_budgets_user_id
    ON public.budgets(user_id);

CREATE INDEX idx_subscriptions_user_id
    ON public.subscriptions(user_id);

CREATE INDEX idx_savings_goals_user_id
    ON public.savings_goals(user_id);

CREATE INDEX idx_financial_decisions_user_id
    ON public.financial_decisions(user_id);

CREATE INDEX idx_agent_actions_user_id
    ON public.agent_actions(user_id);