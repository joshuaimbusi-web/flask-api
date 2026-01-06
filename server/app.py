from flask import Flask, request, jsonify
from datetime import date
from models import db, Mentor, Student, Cohort
from sqlalchemy import func

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moringa.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.route("/mentors", methods=["POST"])
    def create_mentor():
        data = request.get_json()

        mentor = Mentor(
            name=data["name"],
            email=data["email"]
        )

        db.session.add(mentor)
        db.session.commit()

        return jsonify({
            "id": mentor.id,
            "name": mentor.name,
            "email": mentor.email
        }), 201

    @app.route("/cohorts", methods=["POST"])
    def create_cohort():
        data = request.get_json()

        cohort = Cohort(
            name=data["name"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"])
        )

        db.session.add(cohort)
        db.session.commit()

        return jsonify({
            "id": cohort.id,
            "name": cohort.name
        }), 201

    @app.route("/students", methods=["POST"])
    def enroll_student():
        data = request.get_json()

        student = Student(
            name=data["name"],
            mentor_id=data["mentor_id"],
            cohort_id=data["cohort_id"]
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({
            "id": student.id,
            "name": student.name,
            "mentor_id": student.mentor_id,
            "cohort_id": student.cohort_id
        }), 201

    @app.route("/students/<int:student_id>/defer", methods=["PATCH"])
    def defer_student(student_id):
        data = request.get_json()
        student = Student.query.get_or_404(student_id)

        student.cohort_id = data["new_cohort_id"]
        db.session.commit()

        return jsonify({
            "message": "Student deferred successfully",
            "student_id": student.id,
            "new_cohort_id": student.cohort_id
        })

    @app.route("/mentors/top-5", methods=["GET"])
    def top_5_mentors():
        results = (
            db.session.query(
                Mentor.id,
                Mentor.name,
                func.count(Student.id).label("total_students")
            )
            .join(Student)
            .group_by(Mentor.id)
            .order_by(func.count(Student.id).desc())
            .limit(5)
            .all()
        )

        return jsonify([
            {
                "mentor_id": r.id,
                "mentor_name": r.name,
                "total_students": r.total_students
            }
            for r in results
        ])

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(port=5555, debug=True)
