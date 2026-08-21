from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise, ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


# Define Routes here

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        all_workouts = Workout.query.all()
        return make_response(workouts_schema.dump(all_workouts), 200)

    if request.method == 'POST':
        data = request.get_json()
        try:
            validated = workout_schema.load(data, partial=True)
            new_workout = Workout(
                date=validated.get('date'),
                duration_minutes=validated.get('duration_minutes'),
                notes=validated.get('notes'),
            )
            db.session.add(new_workout)
            db.session.commit()
            return make_response(workout_schema.dump(new_workout), 201)
        except (ValidationError, ValueError) as e:
            db.session.rollback()
            return make_response({'errors': str(e)}, 400)


@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def workout_by_id(id):
    workout = Workout.query.filter_by(id=id).first()

    if workout is None:
        return make_response({'error': 'Workout not found'}, 404)

    if request.method == 'GET':
        return make_response(workout_schema.dump(workout), 200)

    if request.method == 'DELETE':
        db.session.delete(workout)
        db.session.commit()
        return make_response({}, 204)


@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        all_exercises = Exercise.query.all()
        return make_response(exercises_schema.dump(all_exercises), 200)

    if request.method == 'POST':
        data = request.get_json()
        try:
            validated = exercise_schema.load(data, partial=True)
            new_exercise = Exercise(
                name=validated.get('name'),
                category=validated.get('category'),
                equipment_needed=validated.get('equipment_needed'),
            )
            db.session.add(new_exercise)
            db.session.commit()
            return make_response(exercise_schema.dump(new_exercise), 201)
        except (ValidationError, ValueError) as e:
            db.session.rollback()
            return make_response({'errors': str(e)}, 400)


@app.route('/exercises/<int:id>', methods=['GET', 'DELETE'])
def exercise_by_id(id):
    exercise = Exercise.query.filter_by(id=id).first()

    if exercise is None:
        return make_response({'error': 'Exercise not found'}, 404)

    if request.method == 'GET':
        return make_response(exercise_schema.dump(exercise), 200)

    if request.method == 'DELETE':
        db.session.delete(exercise)
        db.session.commit()
        return make_response({}, 204)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    if workout is None:
        return make_response({'error': 'Workout not found'}, 404)
    if exercise is None:
        return make_response({'error': 'Exercise not found'}, 404)

    data = request.get_json()
    try:
        validated = workout_exercise_schema.load(data, partial=True)
        new_workout_exercise = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            reps=validated.get('reps'),
            sets=validated.get('sets'),
            duration_seconds=validated.get('duration_seconds'),
        )
        db.session.add(new_workout_exercise)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_workout_exercise), 201)
    except (ValidationError, ValueError) as e:
        db.session.rollback()
        return make_response({'errors': str(e)}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)