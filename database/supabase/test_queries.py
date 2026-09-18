from database.supabase.queries import (
    get_user_profile,
    get_recent_expenses,
    get_subscriptions,
    get_savings_goals,
    get_previous_decisions,
    get_agent_actions,
    get_financial_context,
)

USER_ID = "U001"

print("\n========== USER PROFILE ==========")
print(get_user_profile(USER_ID))

print("\n========== RECENT EXPENSES ==========")
print(get_recent_expenses(USER_ID, limit=5))

print("\n========== SUBSCRIPTIONS ==========")
print(get_subscriptions(USER_ID))

print("\n========== SAVINGS GOALS ==========")
print(get_savings_goals(USER_ID))

print("\n========== PREVIOUS DECISIONS ==========")
print(get_previous_decisions(USER_ID))

print("\n========== AGENT ACTIONS ==========")
print(get_agent_actions(USER_ID))

print("\n========== COMPLETE FINANCIAL CONTEXT ==========")
context = get_financial_context(USER_ID)

print("Context sections:", list(context.keys()))