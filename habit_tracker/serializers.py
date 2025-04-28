from rest_framework import serializers
from habit_tracker.models import Habit
from habit_tracker.validators import (
    RelatedAndAwardValidator,
    HabitTimeToCompleteValidator,
    HabitRelatedHabitIsPleasantValidator,
    HabitPleasantValidator,
    HabitFrequencyValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки"""

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedAndAwardValidator(),
            HabitTimeToCompleteValidator(),
            HabitRelatedHabitIsPleasantValidator(),
            HabitPleasantValidator(),
            HabitFrequencyValidator(),
        ]
