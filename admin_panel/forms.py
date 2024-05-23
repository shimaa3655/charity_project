from django import forms
from django.contrib.auth.models import User
from project.models import *
from django.core.validators import RegexValidator

egyptian_phone_validator = RegexValidator(
    regex=r'^01[0-9]{9}$',
    message='Please enter a valid Egyptian mobile phone number.'
)

class UserProfileForm(forms.ModelForm):
    mobile_phone = forms.CharField(max_length=11, validators=[egyptian_phone_validator])

    class Meta:
        model = UserProfile
        fields = ['mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters.")
        return last_name

class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters.")
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
            raise forms.ValidationError(
                "Password and confirm password do not match"
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AddUserProfileForm(forms.ModelForm):
    mobile_phone = forms.CharField(max_length=11, validators=[egyptian_phone_validator])

    class Meta:
        model = UserProfile
        fields = ['mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country']

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class FeaturedProjectForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=None, label='Project')

    class Meta:
        model = FeaturedProject
        fields = ['project', 'is_featured']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'project', 'text']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'user', 'project']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['user', 'comment', 'text']

class TagSelectionForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'projects']

    projects = forms.ModelMultipleChoiceField(queryset=Project.objects.all(),  required=True, widget=forms.SelectMultiple(attrs={'class': 'select2'}))

class RateProjectForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='User')
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label='Project')
    rating = forms.IntegerField(label='Rating', min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['user', 'project', 'rating']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['user', 'project', 'comment', 'reason']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time', 'creator', 'is_cancelled', 'country']
        widgets = {
            'start_time': forms.DateInput(attrs={'type': 'date'}),
            'end_time': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not any(char.isalpha() for char in title):
            raise forms.ValidationError('Title must contain at least one letter.')
        return title

    def clean_details(self):
        details = self.cleaned_data['details']
        if not any(char.isalpha() for char in details):
            raise forms.ValidationError('Details must contain at least one letter.')
        return details

    def clean_country(self):
        country = self.cleaned_data['country']
        if not all(char.isalpha() or char.isspace() for char in country):
            raise forms.ValidationError('Country must contain only letters and spaces.')
        return country

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time', 'creator', 'is_cancelled', 'country']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ProjectCancellationForm(forms.ModelForm):
    class Meta:
        model = ProjectCancellation
        fields = ['project', 'cancellation_reason']

class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectPicture
        fields = ['project', 'image']
