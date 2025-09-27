from App.database import db


class Route(db.Model):
    __tablename__ = "routes"

    route_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(
        db.Integer, db.ForeignKey("drivers.driver_id", ondelete="CASCADE"), nullable=False
    )
    location_name = db.Column(db.String(80), nullable=False)
    resident_id = db.Column(db.Integer, nullable=True)
    route_status = db.Column(
        db.String(20), nullable=False, default="idle"
    )  

    driver = db.relationship("Driver", back_populates="routes")

    stops = db.relationship(
        "Stop",
        back_populates="route",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def add_stop(self, *, location_name: str):
        
        from .stop import Stop

        stop = Stop(
            route_id=self.route_id,
            location_name=location_name,
            stop_status="pending",
        )
        db.session.add(stop)
        return stop

    def receive_request(self, resident_id: int, location_name: str) -> str:
    
        self.location_name = location_name
        self.route_status = "assigned"
        return (
            f"Request from resident {resident_id} received; "
            f"driver assigned to location {location_name}."
        )

    def get_json(self):
        return {
            "route_id": self.route_id,
            "driver_id": self.driver_id,
            "location_name": self.location_name,
            "route_status": self.route_status,
        }
