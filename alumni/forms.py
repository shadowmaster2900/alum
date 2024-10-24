# alumni/forms.py

from django import forms
from .models import School, Alumni, TrackRecord, AlumniCollection, AlumniGroup, UserProfile, JobOpening


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['title', 'description', 'company', 'location']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['show_name', 'show_graduate_year', 'show_birthday', 'show_socials', 'show_location', 'show_education', 'show_current_job', 'show_email', 'show_military', 'show_marital']
        # Add fields for other columns as needed


class AlumniFilterForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all(), empty_label="All Schools", required=False)
    graduate_year = forms.IntegerField(min_value=1900, max_value=2050, required=False)
    name = forms.CharField(max_length=100, required=False)

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']

class TrackRecordForm(forms.ModelForm):
    class Meta:
        model = TrackRecord
        fields = ['record', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AlumniAdminForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = '__all__'

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['alumni_collection', 'name', 'birthday', 'graduate_year', 'school', 'class_number', 'major', 'city', 'location', 'education_info', 'current_job', 'GBT', 'interaction_status', 'description', 'military_status', 'marital_status']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'name': {'required': ''},
            'email': {'required': ''},
            'birthday': {'required': ''},
        }
    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)

        # Filter the queryset for 'alumni_collection' based on the school of the alumni
        self.fields['alumni_collection'].queryset = AlumniCollection.objects.filter(school=school)


        
class AlumniCollectionForm(forms.ModelForm):
    class Meta:
        model = AlumniCollection
        fields = ['year']

class AlumniGroupForm(forms.ModelForm):
    class Meta:
        model = AlumniGroup
        fields = ['name']