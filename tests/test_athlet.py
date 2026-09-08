from src.athlet import Athlete


def test_training_status_for_low_volume():
    athlete = Athlete(name="Alex", sport="Running", weekly_hours=4)

    assert athlete.training_status() == "Build consistency"


def test_add_workout_and_summary():
    athlete = Athlete(
        name="Alex",
        sport="Running",
        weekly_hours=6,
        goal="Half marathon",
        workouts=["Warm-up run", "Tempo session"],
    )

    athlete.add_workout("Strength training")

    assert athlete.workouts == ["Warm-up run", "Tempo session", "Strength training"]
    assert "Half marathon" in athlete.weekly_summary()
    assert "6.0 hours" in athlete.weekly_summary()
