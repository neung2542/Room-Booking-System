import requests
from datetime import datetime, timedelta

# Base URL
BASE_URL = "http://localhost:5000/api"

def test_api():
    print("=== Testing Meeting Room API ===\n")
    
    # 1. Create users
    print("1. Creating users...")
    users_data = [
        {"name": "สมชาย ใจดี", "email": "somchai@company.com", "department": "IT"},
        {"name": "สมหญิง รักงาน", "email": "somying@company.com", "department": "HR"},
        {"name": "วิชาญ เก่งเก่า", "email": "wichan@company.com", "department": "Finance"}
    ]
    
    created_users = []
    for user_data in users_data:
        response = requests.post(f"{BASE_URL}/users", json=user_data)
        if response.status_code == 201:
            user = response.json()["user"]
            created_users.append(user)
            print(f"✓ Created user: {user['name']} (ID: {user['id']})")
        else:
            print(f"✗ Failed to create user: {response.json()}")
    
    # 2. Create rooms
    print("\n2. Creating rooms...")
    rooms_data = [
        {"room_name": "ห้องประชุมใหญ่", "floor": 5, "capacity": 20},
        {"room_name": "ห้องประชุมเล็ก", "floor": 3, "capacity": 8},
        {"room_name": "ห้องประชุมบอร์ด", "floor": 10, "capacity": 12}
    ]
    
    created_rooms = []
    for room_data in rooms_data:
        response = requests.post(f"{BASE_URL}/rooms", json=room_data)
        if response.status_code == 201:
            room = response.json()["room"]
            created_rooms.append(room)
            print(f"✓ Created room: {room['room_name']} (ID: {room['id']})")
        else:
            print(f"✗ Failed to create room: {response.json()}")
    
    # 3. Get all rooms
    print("\n3. Getting all rooms...")
    response = requests.get(f"{BASE_URL}/rooms")
    if response.status_code == 200:
        rooms = response.json()["rooms"]
        print(f"✓ Found {len(rooms)} rooms")
        for room in rooms:
            print(f"  - {room['room_name']} (Floor: {room['floor']}, Capacity: {room['capacity']})")
    else:
        print(f"✗ Failed to get rooms: {response.json()}")
    
    # 4. Create bookings
    print("\n4. Creating bookings...")
    
    # Calculate future dates
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
    
    bookings_data = [
        {
            "user_id": created_users[0]["id"],
            "room_id": created_rooms[0]["id"],
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        },
        {
            "user_id": created_users[1]["id"],
            "room_id": created_rooms[1]["id"],
            "start_time": (start_time + timedelta(hours=2)).isoformat(),
            "end_time": (end_time + timedelta(hours=2)).isoformat()
        }
    ]
    
    created_bookings = []
    for booking_data in bookings_data:
        response = requests.post(f"{BASE_URL}/bookings", json=booking_data)
        if response.status_code == 201:
            booking = response.json()["booking"]
            created_bookings.append(booking)
            print(f"✓ Created booking: {booking['user']['name']} -> {booking['room']['room_name']}")
        else:
            print(f"✗ Failed to create booking: {response.json()}")
    
    # 5. Test duplicate booking (should fail)
    print("\n5. Testing duplicate booking (should fail)...")
    duplicate_booking = {
        "user_id": created_users[2]["id"],
        "room_id": created_rooms[0]["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/bookings", json=duplicate_booking)
    if response.status_code == 400:
        print(f"✓ Correctly rejected duplicate booking: {response.json()['error']}")
    else:
        print(f"✗ Should have rejected duplicate booking: {response.json()}")
    
    # 6. Test past booking (should fail)
    print("\n6. Testing past booking (should fail)...")
    past_booking = {
        "user_id": created_users[0]["id"],
        "room_id": created_rooms[1]["id"],
        "start_time": "2023-01-01T09:00:00",
        "end_time": "2023-01-01T10:00:00"
    }
    
    response = requests.post(f"{BASE_URL}/bookings", json=past_booking)
    if response.status_code == 400:
        print(f"✓ Correctly rejected past booking: {response.json()['error']}")
    else:
        print(f"✗ Should have rejected past booking: {response.json()}")
    
    # 7. Get bookings by room and date
    print("\n7. Getting bookings by room and date...")
    target_date = start_time.strftime('%Y-%m-%d')
    
    response = requests.get(f"{BASE_URL}/bookings", params={
        "room_id": created_rooms[0]["id"],
        "date": target_date
    })
    
    if response.status_code == 200:
        bookings = response.json()["bookings"]
        print(f"✓ Found {len(bookings)} bookings for {created_rooms[0]['room_name']} on {target_date}")
        for booking in bookings:
            print(f"  - {booking['user']['name']}: {booking['start_time']} - {booking['end_time']}")
    else:
        print(f"✗ Failed to get bookings: {response.json()}")
    
    # 8. Get user info
    print("\n8. Getting user info...")
    if created_users:
        user_id = created_users[0]["id"]
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            user = response.json()["user"]
            print(f"✓ User info: {user['name']} ({user['email']}) - {user['department']}")
        else:
            print(f"✗ Failed to get user info: {response.json()}")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")