from client import supabase

response = (
    supabase
    .table("users")
    .select("*")
    .limit(1)
    .execute()
)

print("✅ Connected to Supabase!")
print("User data:")
print(response.data)