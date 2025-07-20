from models import db, User, Room, Booking
from datetime import datetime, date
from sqlalchemy import and_, or_

class UserService:
    @staticmethod
    def create_user(name):
        existing_user = User.query.filter_by(name=name).first()
        if existing_user:
            raise ValueError("Name already exists")
        
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user

class RoomService:
    @staticmethod
    def create_room(room_name, floor, capacity):
        room = Room(room_name=room_name, floor=floor, capacity=capacity)
        db.session.add(room)
        db.session.commit()
        return room
    
    @staticmethod
    def get_all_rooms():
        return Room.query.all()
    
    @staticmethod
    def get_room_by_id(room_id):
        room = Room.query.get(room_id)
        if not room:
            raise ValueError("Room not found")
        return room

class BookingService:
    @staticmethod
    def create_booking(user_id, room_id, start_time, end_time):
        # Validate user exists
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Validate room exists
        room = Room.query.get(room_id)
        if not room:
            raise ValueError("Room not found")
        
        # Parse datetime strings if they are strings
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        # Validate booking time logic
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")
        
        if start_time < datetime.now():
            raise ValueError("Cannot book room in the past")
        
        # Check for overlapping bookings
        overlapping_booking = Booking.query.filter(
            and_(
                Booking.room_id == room_id,
                or_(
                    # New booking starts during existing booking
                    and_(Booking.start_time <= start_time, Booking.end_time > start_time),
                    # New booking ends during existing booking
                    and_(Booking.start_time < end_time, Booking.end_time >= end_time),
                    # New booking completely contains existing booking
                    and_(Booking.start_time >= start_time, Booking.end_time <= end_time)
                )
            )
        ).first()
        
        if overlapping_booking:
            raise ValueError("Room is already booked for this time period")
        
        # Create booking
        booking = Booking(
            user_id=user_id,
            room_id=room_id,
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(booking)
        db.session.commit()
        return booking
    
    @staticmethod
    def get_bookings_by_room_and_date(room_id, target_date):
        # Validate room exists
        room = Room.query.get(room_id)
        if not room:
            raise ValueError("Room not found")
        
        # Parse date string if it's a string
        if isinstance(target_date, str):
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        
        # Get bookings for the specified date
        bookings = Booking.query.filter(
            and_(
                Booking.room_id == room_id,
                db.func.date(Booking.start_time) == target_date
            )
        ).order_by(Booking.start_time).all()
        
        return bookings
    
    @staticmethod
    def get_all_bookings():
        return Booking.query.all()