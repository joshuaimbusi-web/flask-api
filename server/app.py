from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Mentor


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moringa.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)

    # ---------- Resources ----------

    class MentorListResource(Resource):
        def get(self):
            mentors = Mentor.query.all()
            return [
                {
                    "id": m.id,
                    "name": m.name,
                    "email": m.email
                }
                for m in mentors
            ], 200

        def post(self):
            data = request.get_json()

            mentor = Mentor(
                name=data["name"],
                email=data["email"]
            )

            db.session.add(mentor)
            db.session.commit()

            return {
                "id": mentor.id,
                "name": mentor.name,
                "email": mentor.email
            }, 201

    class MentorResource(Resource):
        def get(self, mentor_id):
            mentor = Mentor.query.get_or_404(mentor_id)
            return {
                "id": mentor.id,
                "name": mentor.name,
                "email": mentor.email
            }, 200

        def patch(self, mentor_id):
            mentor = Mentor.query.get_or_404(mentor_id)
            data = request.get_json()

            if "name" in data:
                mentor.name = data["name"]
            if "email" in data:
                mentor.email = data["email"]

            db.session.commit()

            return {
                "message": "Mentor updated successfully",
                "id": mentor.id,
                "name": mentor.name,
                "email": mentor.email
            }, 200

        def delete(self, mentor_id):
            mentor = Mentor.query.get_or_404(mentor_id)

            db.session.delete(mentor)
            db.session.commit()

            return {
                "message": "Mentor deleted successfully"
            }, 204

    # ---------- Routes ----------

    api.add_resource(MentorListResource, "/mentors")
    api.add_resource(MentorResource, "/mentors/<int:mentor_id>")

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(port=5555, debug=True)
