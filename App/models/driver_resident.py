from werkzeug.security import check_password_hash, generate_password_hash  
from App.database import db


class Driver(db.Model):
    __tablename__ = "drivers"

    driver_id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="offline")   # offline | scheduled | 
    location_name = db.Column(db.String(80), nullable=False)

    
    routes = db.relationship(
        "Route",
        back_populates="driver",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __init__(self, driver_name, status="offline", location_name="HQ"):
        self.driver_name = driver_name
        self.status = status
        self.location_name = location_name

    def schedule_drive(self, *, location_name: str, resident_id: int = None):
        
        from .route import Route  

        route = Route(
            driver_id=self.driver_id,
            location_name=location_name,
            resident_id=resident_id,
            route_status="scheduled",
        )
        db.session.add(route)

        
        self.status = "scheduled"
        self.location_name = location_name
        return route

    def get_json(self):
        return {
            "driver_id": self.driver_id,
            "driver_name": self.driver_name,
            "status": self.status,
            "location_name": self.location_name,
            "routes": [route.route_id for route in self.routes],
        }


class Resident(db.Model):
    __tablename__ = "residents"

    resident_id = db.Column(db.Integer, primary_key=True)
    resident_name = db.Column(db.String(80), nullable=False)
    location_name = db.Column(db.String(80), nullable=False)

    def __init__(self, resident_name, location_name):
        self.resident_name = resident_name
        self.location_name = location_name

    def view_routes(self, location_name: str):
        
        from .route import Route
        return (
            Route.query.filter_by(location_name=location_name)
            .order_by(Route.route_id)
            .all()
        )

    def send_request(self, driver_id: int, location_name: str):
        from .route import Route

        route = (
            Route.query.filter_by(driver_id=driver_id)
            .order_by(Route.route_id.desc())
            .first()
        )
        if not route:
            return f"No active route found for driver {driver_id}."
        
        return route.receive_request(self.resident_id, location_name)




    def track_driver(self, driver_id: int):
        
        driver = Driver.query.get(driver_id)
        return driver.location_name if driver else None

    def get_json(self):
        return {
            "resident_id": self.resident_id,
            "resident_name": self.resident_name,
            "location_name": self.location_name,
        }
