from app import app
from models import db, Mentor, Cohort, Student
from datetime import date

with app.app_context():
    print("Seeding database...")

    # Clear existing data
    Student.query.delete()
    Mentor.query.delete()
    Cohort.query.delete()

    # Create mentors
    mentors = [
        Mentor(name="Steve Jobs", email="Tomashi@moringa.com"),
        Mentor(name="Brian Otieno", email="brian@moringa.com"),
        Mentor(name="Sam Tomashi", email="tomashi@moringa.com"),
        Mentor(name="David Kimani", email="david@moringa.com"),
        Mentor(name="Esther Njeri", email="esther@moringa.com"),
        Mentor(name="Frank Ouma", email="frank@moringa.com"),
    ]

    db.session.add_all(mentors)
    db.session.commit()

    # Create cohorts
    cohorts = [
        Cohort(
            name="Software Engineering FT-01",
            start_date=date(2025, 3, 8),
            end_date=date(2026, 3, 8)
        ),
        Cohort(
            name="Software Engineering FT-02",
            start_date=date(2025, 7, 10),
            end_date=date(2026, 2, 10)
        ),
    ]

    db.session.add_all(cohorts)
    db.session.commit()

    # Create students
    students = [
        Student(name="Joshua Biboko", mentor_id=mentors[0].id, cohort_id=cohorts[0].id),
        Student(name="Roy Cheruiyot", mentor_id=mentors[0].id, cohort_id=cohorts[0].id),
        Student(name="Nathan Kuira", mentor_id=mentors[1].id, cohort_id=cohorts[0].id),
        Student(name="Mercy Mwangi", mentor_id=mentors[2].id, cohort_id=cohorts[1].id),
        Student(name="Kibet Chumo", mentor_id=mentors[2].id, cohort_id=cohorts[1].id),
        Student(name="Ann Wambui", mentor_id=mentors[2].id, cohort_id=cohorts[1].id),
        Student(name="Peter Kamau", mentor_id=mentors[3].id, cohort_id=cohorts[1].id),
    ]

    db.session.add_all(students)
    db.session.commit()

    print("Database seeded successfully!")
