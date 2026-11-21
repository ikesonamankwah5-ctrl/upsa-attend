from django import forms
from .models import PracticeSession


class PracticeSessionForm(forms.ModelForm):

    class Meta:
        model = PracticeSession

        fields = [
            'course_name',
            'difficulty',
            'question_format',
            'mode',
            'number_of_questions',
            'time_limit_minutes',
        ]

        widgets = {
            'course_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Organisational Behaviour'
            }),

            'difficulty': forms.Select(),

            'question_format': forms.Select(),

            'mode': forms.Select(),

            'number_of_questions': forms.NumberInput(attrs={
                'min': 1,
                'max': 100,
            }),

            'time_limit_minutes': forms.NumberInput(attrs={
                'min': 1,
                'max': 180,
            }),
        }