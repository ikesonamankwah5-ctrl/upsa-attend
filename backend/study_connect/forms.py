from django import forms
from django.utils import timezone

from .models import StudyGroup, StudySession


class StudyGroupForm(forms.ModelForm):

    class Meta:
        model = StudyGroup

        fields = [
            'title',
            'description',
            'course',
            'programme',
            'academic_level',
            'visibility',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Financial Reporting Study Group'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'What is this study group about?'
            }),

            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Financial Reporting'
            }),

            'programme': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Business Administration'
            }),

            'academic_level': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Level 300'
            }),

            'visibility': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class StudySessionForm(forms.ModelForm):

    class Meta:
        model = StudySession

        fields = [
            'title',
            'description',
            'session_type',
            'meeting_location',
            'meeting_link',
            'scheduled_at',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Financial Reporting Revision'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe what the session will cover.'
            }),

            'session_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'meeting_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the physical meeting location'
            }),

            'meeting_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your virtual meeting link'
            }),

            'scheduled_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def clean_scheduled_at(self):
        scheduled_at = self.cleaned_data['scheduled_at']

        if timezone.is_naive(scheduled_at):
            scheduled_at = timezone.make_aware(scheduled_at)

        if scheduled_at <= timezone.now():
            raise forms.ValidationError(
                'Please select a future date and time.'
            )

        return scheduled_at

    def clean(self):
        cleaned_data = super().clean()

        session_type = cleaned_data.get('session_type')
        meeting_location = cleaned_data.get('meeting_location')
        meeting_link = cleaned_data.get('meeting_link')

        if session_type == 'VIRTUAL' and not meeting_link:
            self.add_error(
                'meeting_link',
                'A meeting link is required for virtual sessions.'
            )

        if session_type == 'PHYSICAL' and not meeting_location:
            self.add_error(
                'meeting_location',
                'A meeting location is required for physical sessions.'
            )

        return cleaned_data
class GroupMessageForm(forms.ModelForm):

    class Meta:
        from .models import GroupMessage

        model = GroupMessage
        fields = ['message']

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a message to your study group...',
            }),
        }