from src.athlet import Athlete


def main():
    name = input("Enter athlete name: ").strip() or "Unknown athlete"
    sport = input("Enter sport: ").strip() or "General fitness"
    goal = input("Enter training goal: ").strip() or "General fitness"

    try:
        weekly_hours = float(input("Enter weekly training hours: ").strip() or "0")
    except ValueError:
        weekly_hours = 0.0

    workouts = []
    workout_count = int(input("How many workouts would you like to add? ").strip() or "0")

    for i in range(workout_count):
        workout_name = input(f"Workout {i + 1}: ").strip()
        if workout_name:
            workouts.append(workout_name)

    athlete = Athlete(
        name=name,
        sport=sport,
        weekly_hours=weekly_hours,
        goal=goal,
        workouts=workouts,
    )

    print(f"\nWelcome to Athlet, {athlete.name}!")
    print(athlete.weekly_summary())


if __name__ == "__main__":
    main()
