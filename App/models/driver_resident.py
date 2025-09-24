from werkzeug.security import check_password_hash, generate_password_hash  
from App.database import db


class Driver(db.Model):
    __tablename__ = "drivers"

    driver_id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="offline")   # offline | scheduled | 
    location_id = db.Column(db.Integer, nullable=False, default=0)

    
    routes = db.relationship(
        "Route",
        back_populates="driver",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __init__(self, driver_name, status="offline", location_id=0):
        self.driver_name = driver_name
        self.status = status
        self.location_id = location_id

    def schedule_drive(self, street_id: str, *, location_id: int):
        
        from .route import Route  

        route = Route(
            driver_id=self.driver_id,
            location_id=location_id,
            route_status="scheduled",
        )
        db.session.add(route)

        
        self.status = "scheduled"
        self.location_id = location_id
        return route

    def get_json(self):
        return {
            "driver_id": self.driver_id,
            "driver_name": self.driver_name,
            "status": self.status,
            "location_id": self.location_id,
            "routes": [r.route_id for r in self.routes],
        }


class Resident(db.Model):
    __tablename__ = "residents"

    resident_id = db.Column(db.Integer, primary_key=True)
    resident_name = db.Column(db.String(80), nullable=False)
    location_id = db.Column(db.Integer, nullable=False)

    def __init__(self, resident_name, location_id):
        self.resident_name = resident_name
        self.location_id = location_id

    def view_routes(self, location_id: int):
        
        from .route import Route
        return (
            Route.query.filter_by(location_id=location_id)
            .order_by(Route.route_id)
            .all()
        )

    def send_request(self, driver_id: int, location_id: int):
        
        from .route import Route

        route = (
            Route.query.filter_by(driver_id=driver_id)
            .order_by(Route.route_id.desc())
            .first()
        )
        if not route:
            return f"No active route found for driver {driver_id}."
        return route.receive_request(self.resident_id, location_id)

    def track_driver(self, driver_id: int):
        
        driver = Driver.query.get(driver_id)
        return driver.location_id if driver else None

    def get_json(self):
        return {
            "resident_id": self.resident_id,
            "resident_name": self.resident_name,
            "location_id": self.location_id,
        }
