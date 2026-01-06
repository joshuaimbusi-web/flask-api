from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Mentor(db.Model):
    __tablename__ = "mentors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    students = db.relationship("Student", backref="mentor", lazy=True)

    def __repr__(self):
        return f"<Mentor {self.name}>"


class Cohort(db.Model):
    __tablename__ = "cohorts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    students = db.relationship("Student", backref="cohort", lazy=True)

    def __repr__(self):
        return f"<Cohort {self.name}>"


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    mentor_id = db.Column(
        db.Integer,
        db.ForeignKey("mentors.id"),
        nullable=False
    )

    cohort_id = db.Column(
        db.Integer,
        db.ForeignKey("cohorts.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Student {self.name}>"
