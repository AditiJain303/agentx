from .client import supabase


def get_user_profile(user_id):
    response = (
        supabase
        .table("users")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    return response.data


def get_recent_expenses(user_id, limit=20):
    response = (
        supabase
        .table("expenses")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


def get_subscriptions(user_id):
    response = (
        supabase
        .table("subscriptions")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return response.data


def get_savings_goals(user_id):
    response = (
        supabase
        .table("savings_goals")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return response.data


def get_previous_decisions(user_id):
    response = (
        supabase
        .table("financial_decisions")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
        .execute()
    )

    return response.data


def get_agent_actions(user_id, limit=20):
    response = (
        supabase
        .table("agent_actions")
        .select("*")
        .eq("user_id", user_id)
        .order("timestamp", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data


def get_financial_context(user_id):
    return {
        "profile": get_user_profile(user_id),
        "recent_expenses": get_recent_expenses(user_id),
        "subscriptions": get_subscriptions(user_id),
        "savings_goals": get_savings_goals(user_id),
        "previous_decisions": get_previous_decisions(user_id),
        "agent_actions": get_agent_actions(user_id),
    }