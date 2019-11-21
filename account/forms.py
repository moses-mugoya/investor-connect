from django import forms
from .models import Profile, User, Chat, Verification, BusinessManagement
from django_countries import Countries


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


class UserRegistrationForm(forms.ModelForm):
    CHOICES = [
        ('Innovator', 'Innovator'),
        ('Investor', 'Investor'),
        ('Entrepreneur', 'Entrepreneur'),
        ('Partner', 'Partner'),
        ('Service Provider', 'Service Provider')
    ]
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'repeat password'}))
    usertype = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label_suffix="",label='Register as', required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
                               label_suffix="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
                             label_suffix="")

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=13, min_length=13, widget=forms.TextInput(attrs={'placeholder': '00 3241 xxx xxxx'}))
    country = forms.ChoiceField(choices=Countries)

    class Meta:
        model = Profile
        fields = ('address', 'profile_image', 'profession', 'zip_code', 'street', 'town', 'phone_number', 'country', 'bio')


class ChatForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your message here...'}),
                               label_suffix="")

    class Meta:
        model = Chat
        fields = ('message',)


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type the username to search'}),
        label_suffix="")


class VerificationForm(forms.ModelForm):
    CHOICES = [
        ('Passport', 'Passport'),
        ('Driver Licence', 'Driver Licence'),
        ('Voter Card', 'Voter Card'),
        ('National ID', 'National ID')
    ]
    document_type = forms.ChoiceField(choices=CHOICES, label='Please choose the document type to upload')
    document = forms.FileField(label='Please choose your document')

    class Meta:
        model = Verification
        fields = ('document_type', 'document')


class BusinessManagementForm(forms.ModelForm):
    class Meta:
        model = BusinessManagement
        fields = ('first_name', 'last_name', 'email', 'message')




