from App.database import db


class Stop(db.Model):
    __tablename__ = "stops"

    stop_id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(
        db.Integer, db.ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False
    )
    location_id = db.Column(db.Integer, nullable=False)
    stop_status = db.Column(db.String(20), nullable=False, default="pending")  # pending | arrived | completed

    route = db.relationship("Route", back_populates="stops")

    def __init__(self, route_id, location_id, stop_status="pending"):
        self.route_id = route_id
        self.location_id = location_id
        self.stop_status = stop_status

    def get_json(self):
        return {
            "stop_id": self.stop_id,
            "route_id": self.route_id,
            "location_id": self.location_id,
            "stop_status": self.stop_status,
        }
