from fastapi import FastAPI
from pydantic import BaseModel
import hashlib
import os
import time

# Initialize FastAPI app
app = FastAPI()

# RockYou wordlist path
ROCKYOU_PATH = "rockyou.txt"

def load_rockyou():
    if not os.path.exists(ROCKYOU_PATH):
        print("RockYou wordlist not found! Make sure rockyou.txt is in the same directory.")
        return set()
    
    with open(ROCKYOU_PATH, "r", encoding="latin-1") as f:
        return set(line.strip() for line in f)

def is_in_rockyou(password, rockyou_set):
    return password in rockyou_set

def estimate_brute_force_time(password):
    char_sets = {
        "lowercase": "abcdefghijklmnopqrstuvwxyz",
        "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "digits": "0123456789",
        "symbols": "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~"
    }

    char_space = 0
    for key, value in char_sets.items():
        if any(c in value for c in password):
            char_space += len(value)

    password_length = len(password)
    total_combinations = char_space ** password_length

    hash_rate = 10**10  # Assuming hash rate (hashes per second)
    estimated_seconds = total_combinations / hash_rate

    return estimated_seconds

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} days"
    else:
        return f"{seconds / 31536000:.2f} years"

# Pydantic model to handle request body
class PasswordRequest(BaseModel):
    password: str

# API endpoint to check password
@app.post("/check-password/")
async def check_password(request: PasswordRequest):
    password = request.password
    rockyou_set = load_rockyou()

    if is_in_rockyou(password, rockyou_set):
        return {"message": "Password found in RockYou wordlist (instant crack)."}
    else:
        estimated_time = estimate_brute_force_time(password)
        return {"estimated_time": format_time(estimated_time)}

