import streamlit as st

try:
    from supabase import create_client, Client
    try:
        supabase: Client = create_client(
            st.secrets.get("SUPABASE_URL"),
            st.secrets.get("SUPABASE_KEY")
        )
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        supabase = None
except Exception:
    print("Supabase package not installed; database features disabled.")
    supabase = None