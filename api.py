from flask import Flask, render_template, request, jsonify
from flask import current_app as app
from models import db, User, Room, Booking
from services import UserService, RoomService, BookingService
from datetime import datetime

# app = Flask(__name__)

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize database
# db.init_app(app)

# # Create tables
# with app.app_context():
#     db.create_all()
# app = create_app()

# Error handler
def handle_error(error_message, status_code=400):
    return jsonify({'error': error_message}), status_code

# User endpoints
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        # Validate required fields
        # if not data or not all(k in data for k in ['name', 'email', 'department']):
        #     return handle_error("Missing required fields: name, email, department")
        
        user = UserService.create_user(
            name=data['name'],
        )
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except ValueError as e:
        return handle_error(str(e))
    except Exception as e:
        return handle_error(f"Internal server error {e}", 500)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify({'user': user.to_dict()})
        
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error("Internal server error", 500)

# Room endpoints
@app.route('/api/rooms', methods=['POST'])
def create_room():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['room_name', 'floor', 'capacity']):
            return handle_error("Missing required fields: room_name, floor, capacity")
        
        # Validate data types
        if not isinstance(data['floor'], int) or not isinstance(data['capacity'], int):
            return handle_error("Floor and capacity must be integers")
        
        room = RoomService.create_room(
            room_name=data['room_name'],
            floor=data['floor'],
            capacity=data['capacity']
        )
        
        return jsonify({
            'message': 'Room created successfully',
            'room': room.to_dict()
        }), 201
        
    except Exception as e:
        return handle_error("Internal server error", 500)

@app.route('/api/rooms', methods=['GET'])
def get_all_rooms():
    try:
        rooms = RoomService.get_all_rooms()
        return jsonify({
            'rooms': [room.to_dict() for room in rooms]
        })
        
    except Exception as e:
        return handle_error("Internal server error", 500)

# Booking endpoints
@app.route('/api/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['user_id', 'room_id', 'start_time', 'end_time']):
            return handle_error("Missing required fields: user_id, room_id, start_time, end_time")
        
        # Validate data types
        if not isinstance(data['user_id'], int) or not isinstance(data['room_id'], int):
            return handle_error("user_id and room_id must be integers")
        
        booking = BookingService.create_booking(
            user_id=data['user_id'],
            room_id=data['room_id'],
            start_time=data['start_time'],
            end_time=data['end_time']
        )
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
        
    except ValueError as e:
        return handle_error(str(e))
    except Exception as e:
        return handle_error("Internal server error", 500)

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    try:
        room_id = request.args.get('room_id')
        date = request.args.get('date')
        
        if not room_id and not date:
            bookings = BookingService.get_all_bookings()
            return jsonify({
            'bookings': [booking.to_dict() for booking in bookings]
        })

        if not room_id:
            return handle_error("room_id parameter is required")
        
        if not date:
            return handle_error("date parameter is required (format: YYYY-MM-DD)")
        
        # Validate room_id is integer
        try:
            room_id = int(room_id)
        except ValueError:
            return handle_error("room_id must be an integer")
        
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return handle_error("Invalid date format. Use YYYY-MM-DD")
        
        bookings = BookingService.get_bookings_by_room_and_date(room_id, date)
        
        return jsonify({
            'bookings': [booking.to_dict() for booking in bookings]
        })
        
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(f"Internal server error {e}", 500)

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    rooms = Room.query.all()
    bookings = Booking.query.all()
    return render_template('index.html', users=users, rooms=rooms, bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)