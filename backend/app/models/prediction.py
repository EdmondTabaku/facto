from app import db


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news = db.Column(db.String(5000), nullable=False)
    prediction = db.Column(db.Integer, nullable=False)
    confidence = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Prediction {self.id}>"
