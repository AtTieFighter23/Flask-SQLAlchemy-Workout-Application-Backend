#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():

    # reset data and add new example data, committing to db
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    push_up = Exercise(name="Push Up", category="Strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="Strength", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="Strength", equipment_needed=True)
    plank = Exercise(name="Plank", category="Core", equipment_needed=False)
    running = Exercise(name="Running", category="Cardio", equipment_needed=False)

    db.session.add_all([push_up, squat, bench_press, plank, running])
    db.session.commit()

    workout1 = Workout(date=date(2026, 8, 17), duration_minutes=45, notes="Upper body focus")
    workout2 = Workout(date=date(2026, 8, 19), duration_minutes=30, notes="Quick core and cardio")

    db.session.add_all([workout1, workout2])
    db.session.commit()

    workout_exercises = [
        WorkoutExercise(workout=workout1, exercise=push_up, reps=15, sets=3, duration_seconds=None),
        WorkoutExercise(workout=workout1, exercise=bench_press, reps=10, sets=4, duration_seconds=None),
        WorkoutExercise(workout=workout2, exercise=plank, reps=1, sets=3, duration_seconds=60),
        WorkoutExercise(workout=workout2, exercise=running, reps=1, sets=1, duration_seconds=900),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("🌱 Database seeded successfully!")