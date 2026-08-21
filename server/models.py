from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    # An Exercise has many WorkoutExercises, and many Workouts through them
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Exercise must have a name.')
        return name

    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # A Workout has many WorkoutExercises, and many Exercises through them
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan'
    )
    exercises = db.relationship(
        'Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True
    )

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes is not None and duration_minutes <= 0:
            raise ValueError('Workout duration_minutes must be a positive integer.')
        return duration_minutes

    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes} min>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    __table_args__ = (
        CheckConstraint('reps > 0', name='check_reps_positive'),
        CheckConstraint('sets > 0', name='check_sets_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # A WorkoutExercise belongs to a Workout and an Exercise
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps <= 0:
            raise ValueError('reps must be a positive integer.')
        return reps

    @validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None and sets <= 0:
            raise ValueError('sets must be a positive integer.')
        return sets

    def __repr__(self):
        return f'<WorkoutExercise {self.id}, workout={self.workout_id}, exercise={self.exercise_id}, {self.sets}x{self.reps}>'