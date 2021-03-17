from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.forms import ModelForm, RadioSelect
from .models import *
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class ValidationDemoForm(forms.Form):
    name = forms.CharField(label='Enter Name', max_length=25, required=False)

    def clean_name(self):
        input_name = self.cleaned_data['name']
        if len(input_name.strip()) == 0:
            raise ValidationError("Please enter a name")
        return input_name

    gender_choices = (('male', 'Male'), ('female', 'FeMale'), ('others', 'Others'))
    gender = forms.ChoiceField(label='Select Gender', choices=gender_choices,
                               widget=forms.RadioSelect(), required=False)

    def clean_gender(self):
        input_gender = self.cleaned_data['gender']
        if len(input_gender.strip()) == "":
            raise ValidationError("Please select gender")
        return input_gender

    email = forms.EmailField(label='Enter Email Id')

    def clean_email(self):
        input_email = self.cleaned_data['email']
        validator = EmailValidator("Please enter a valid email address")
        validator(input_email)
        return input_email

    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput(), required=False)

    def clean_password(self):
        input_password = self.cleaned_data['password']
        if len(input_password) < 8:
            raise ValidationError('password must be 8 characters long')
        return input_password

    con_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), required=False)

    def clean_con_password(self):
        input_con_password = self.cleaned_data['con_password']
        input_password = self.data['password']
        if input_con_password == "":
            raise ValidationError('Please enter confirm password')
        elif input_con_password != input_password:
            raise ValidationError('Please enter same as password')
        return input_con_password

    address = forms.CharField(label='Enter Address', widget=forms.Textarea(attrs={'roes': 6, 'cols': 20}))

    def clean_address(self):
        input_address = self.cleaned_data['address']
        if len(input_address.strip()) == 0:
            raise ValidationError("Please enter a address")
        return input_address

    state_choices = (('', 'click here'), ('TS', 'Telangana'), ('AP', 'Andrapradesh'), ('WB', 'West Bengal'),
                     ('DL', 'Delhi'))
    state = forms.ChoiceField(label='Select State', choices=state_choices, required=False)

    def clean_state(self):
        input_state = self.cleaned_data['state']
        if input_state == "":
            raise ValidationError('Please select a state')
        return input_state

    percentage = forms.DecimalField(label='Enter Percentage', required=False)

    def clean_percentage(self):
        input_percentage = self.cleaned_data['percentage']
        if input_percentage is None:
            raise ValidationError("Please enter percentage")
        return input_percentage

    admission_date = forms.DateField(label='Enter DOJ',
                                     input_formats=['%d-%m-%Y'], help_text='format(dd-mm-yyyy)', required=False)

    def clean_date(self):
        input_date = self.cleaned_data['admission_date']
        if input_date is None:
            raise ValidationError("Please select date")
        return input_date

    agreetmc = forms.BooleanField(label='I Agree To Terms and Conditions', required=False)

    def clean_agreetmc(self):
        input_tnc = self.cleaned_data['agreetmc']
        # print(input_tnc)
        if input_tnc == False:
            raise ValidationError("Please agree terms and conditions")
        return input_tnc


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

        labels = {'state': _('Select State')}

    def clean_state(self):
        input_state = self.cleaned_data['state']
        if len(input_state.strip()) == 0:
            raise ValidationError('Please provide state name')
        return input_state


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

        labels = {
            'name': _('Enter a name'),
            'gender': _('select gender'),
            'package': _('enter package'),
            'address': _('enter address'),
            'location': _('enter location'),
            'photo': _('Upload a photo')
        }

        widget = {
            'gender': RadioSelect()
        }

        error_message = {
            'gender': {
                'required': _('Please select gender')
            }
        }

    def clean_name(self):
        # code to read name
        input_name = self.cleaned_data['name']
        if len(input_name.strip()) == 0:
            raise ValidationError("Please provide name")
        return input_name

    def clean_package(self):
        # code to read package
        input_package = self.cleaned_data['package']
        if input_package == None:
            raise ValidationError("Please enter package")
        return input_package

    def clean_address(self):
        # code to read address
        input_address = self.cleaned_data['address']
        if len(input_address.strip()) == 0:
            raise ValidationError("Please provide address")
        return input_address

    def clean_location(self):
        # code to read location
        input_location = self.cleaned_data['location']
        if input_location == None:
            raise ValidationError("Please select state")
        return input_location

    def clean_photo(self):
        photo = self.cleaned_data.get("photo", False)
        if type(photo) is str:
            # means no file uploaded so go for default file
            return photo
        if photo is False:
            # means no file uploaded so go for default file
            return 'no_photo.jpg'
        else:
            allowed_type = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in allowed_type:
                raise ValidationError("Please upload file with valid extension")
            if photo.size > 1024 * 50:
                raise ValidationError("Please upload file upto 50 KB")
        return photo


class RegistrationForm(ModelForm):
    re_password = forms.CharField(max_length=128, label="Re-enter password", widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.required = False

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 're_password']

        widgets = {
            'password': forms.PasswordInput()
        }

        help_text = {
            'email': _('this is your user name'),
            'password': _('password must be 8 characters at least')
        }

    def clean_first_name(self):
        input_first_name = self.cleaned_data['first_name']
        if len(input_first_name.strip()) == 0:
            raise ValidationError('Please provide your first name')
        return input_first_name

    def clean_last_name(self):
        input_last_name = self.cleaned_data['last_name']
        if len(input_last_name.strip()) == 0:
            raise ValidationError('Please provide your last name')
        return input_last_name

    def clean_email(self):
        input_email = self.cleaned_data['email']
        validator = EmailValidator('Please provide a valid email')
        validator(input_email)
        if User.objects.filter(email=input_email).exists():
            raise ValidationError('Email already exist')
        return input_email

    def clean_password(self):
        input_password = self.cleaned_data['password']
        if len(input_password) < 8:
            raise ValidationError('Password must be of at least 8 characters')
        return input_password

    def clean_re_password(self):
        input_re_password = self.cleaned_data['re_password']
        input_password = self.data['password']
        if input_re_password != input_password:
            raise ValidationError('Password and Re_password must match')
        return input_re_password

