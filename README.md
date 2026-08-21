# Flask-SQLAlchemy Workout Application Backend

## Description

A backend API for a workout tracking application used by personal trainers. The API allows trainers to create, view, and delete workouts and exercises, and to associate exercises with workouts — including reps, sets, and duration for each exercise performed. Built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.

## Installation

1. Clone the repository:
```bash
   git clone git@github.com:AtTieFighter23/Flask-SQLAlchemy-Workout-Application-Backend.git
   cd Flask-SQLAlchemy-Workout-Application-Backend
```

2. Install dependencies and enter the virtual environment:
```bash
   pipenv install
   pipenv shell
```

3. Navigate into the `server/` directory and set environment variables:
```bash
   cd server
   export FLASK_APP=app.py
   export FLASK_RUN_PORT=5555
```

4. Initialize the database and run migrations:
```bash
   flask db upgrade head
```

5. Seed the database with example data:
```bash
   python seed.py
```

## Running the Application

From the `server/` directory:

```bash
flask run
```

The API will be available at `http://127.0.0.1:5555`.

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get a single workout, including its associated exercises with reps/sets/duration |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout and its associated workout-exercise records |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise, including its associated workouts |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated workout-exercise records |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout, including reps, sets, and duration |

## Data Validation

- **Table constraints**: `Exercise.name` is unique and required; `WorkoutExercise.reps` and `sets` must be positive (database-level `CHECK` constraints).
- **Model validations**: `Exercise.name` must be non-empty; `Workout.duration_minutes` must be a positive integer; `WorkoutExercise.reps`/`sets` must be positive integers.
- **Schema validations**: `Exercise.name` must be at least 1 character; `Workout.duration_minutes` must be at least 1; `WorkoutExercise.reps`/`sets` must be at least 1.

## Screenshot

TODO: add a screenshot of a working endpoint response.

## Dependencies

See `Pipfile` for the full list, including Flask, Flask-Migrate, Flask-SQLAlchemy, and Marshmallow.