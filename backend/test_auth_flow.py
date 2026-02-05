import requests
import uuid

BASE_URL = "http://localhost:8000/api"

def test_auth_flow():
    # 1. Signup
    email = f"test_{uuid.uuid4()}@example.com"
    password = "password123"
    name = "Test User"

    print(f"Testing Signup with {email}...")
    signup_payload = {
        "email": email,
        "password": password,
        "name": name
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_payload)
        if response.status_code == 200:
            print("Signup Successful")
            data = response.json()
            # print(data)
        else:
            print(f"Signup Failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"Signup Exception: {e}")
        return

    # 2. Signin
    print("\nTesting Signin...")
    signin_payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signin", json=signin_payload)
        if response.status_code == 200:
            print("Signin Successful")
            data = response.json()
            if "token" in data:
                print("Token received")
            else:
                print("Token missing in response")
        else:
            print(f"Signin Failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"Signin Exception: {e}")
        return

    # 3. Invalid Signin
    print("\nTesting Invalid Signin...")
    invalid_payload = {
        "email": email,
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signin", json=invalid_payload)
        if response.status_code == 401:
            print("Invalid Signin Correctly Rejected (401)")
        else:
            print(f"Invalid Signin returned unexpected status: {response.status_code}")
    except Exception as e:
        print(f"Invalid Signin Exception: {e}")

if __name__ == "__main__":
    test_auth_flow()
