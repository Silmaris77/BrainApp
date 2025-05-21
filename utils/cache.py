import streamlit as st
from datetime import datetime, timedelta
import json

class Cache:
    @staticmethod
    def get(key, default=None, ttl_minutes=15):
        """Get value from cache"""
        if 'cache' not in st.session_state:
            st.session_state.cache = {}
        
        cache_data = st.session_state.cache.get(key)
        if cache_data is None:
            return default
        
        value, timestamp = cache_data
        if datetime.now() - timestamp > timedelta(minutes=ttl_minutes):
            del st.session_state.cache[key]
            return default
        
        return value

    @staticmethod
    def set(key, value, ttl_minutes=15):
        """Set value in cache"""
        if 'cache' not in st.session_state:
            st.session_state.cache = {}
        
        st.session_state.cache[key] = (value, datetime.now())

    @staticmethod
    def clear(key=None):
        """Clear cache for specific key or all cache"""
        if 'cache' not in st.session_state:
            return
        
        if key is None:
            st.session_state.cache = {}
        elif key in st.session_state.cache:
            del st.session_state.cache[key]

def cache_user_data(username):
    """Cache decorator for user data functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = f"user_data_{username}_{func.__name__}"
            cached_value = Cache.get(cache_key)
            
            if cached_value is not None:
                return cached_value
            
            result = func(*args, **kwargs)
            Cache.set(cache_key, result)
            return result
        return wrapper
    return decorator

def clear_user_cache(username):
    """Clear all cached data for a user"""
    if 'cache' in st.session_state:
        keys_to_clear = [
            key for key in st.session_state.cache.keys()
            if key.startswith(f"user_data_{username}_")
        ]
        for key in keys_to_clear:
            Cache.clear(key)