from dataclasses import dataclass, field


@dataclass
class Athlete:
    name: str
    sport: str
    weekly_hours: float = 0.0
    goal: str = "General fitness"
    workouts: list[str] = field(default_factory=list)

    def training_status(self) -> str:
        if self.weekly_hours >= 10:
            return "Strong training load"
        if self.weekly_hours >= 5:
            return "Steady progress"
        return "Build consistency"

    def add_workout(self, workout: str) -> None:
        self.workouts.append(workout)

    def weekly_summary(self) -> str:
        return (
            f"Athlete: {self.name}\n"
            f"Sport: {self.sport}\n"
            f"Goal: {self.goal}\n"
            f"Weekly training: {float(self.weekly_hours):.1f} hours\n"
            f"Status: {self.training_status()}\n"
            f"Workouts: {', '.join(self.workouts) if self.workouts else 'No workouts logged yet'}"
        )
