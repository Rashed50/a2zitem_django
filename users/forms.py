from django import forms
from django.forms import (
    ModelForm, TextInput, Select, CheckboxInput, NumberInput, FileInput, SelectMultiple, Textarea,
    PasswordInput, EmailInput
)

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreationForm(forms.ModelForm):
    input_style = 'width:100%;padding:10px 12px;font-size:14px;border:1px solid #d1d5db;border-radius:4px;background-color:#fff;box-sizing:border-box;'
    checkbox_style = 'width:16px;height:16px;cursor:pointer;'

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password'
        }),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'image', 'gender', 'dob',
            'is_admin', 'is_active', 'is_email_verified', 'is_phone_verified',
        ]
        
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Write email', 'required': True}),
            'first_name': TextInput(attrs={'placeholder': 'Write first name', 'required': True}),
            'last_name': TextInput(attrs={'placeholder': 'Write last name', 'required': True}),
            'phone': TextInput(attrs={'placeholder': 'Write phone number', 'required': True}),
            'dob': forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': 'Select a date', 'type': 'date'}),
            'image': FileInput(attrs={'accept': 'image/jpeg,image/png,image/jpg'}),
            'gender': Select(),
            'is_email_verified': CheckboxInput(),
            'is_phone_verified': CheckboxInput(),
            'is_active': CheckboxInput(),
        }
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")
        if password1 and len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        return password2
    

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)

        # print("--------------------")
        # print("User = ", self.cleaned_data["name"])
        # print("--------------------")

        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Password fields style
        self.fields['password'].widget.attrs['style'] = self.input_style
        self.fields['password2'].widget.attrs['style'] = self.input_style

        # Other fields style
        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['style'] = self.checkbox_style
            elif 'style' not in field.widget.attrs:
                field.widget.attrs['style'] = self.input_style


## For Django Admin Panel
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'image', 'is_email_verified', 'is_phone_verified', 'is_admin']

    def clean_password(self):
        return self.initial['password']
    




class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'image', 'dob', 'gender',
        ]

        widgets = {
            'email' : EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Write email',
                'required': True
            }),

            'first_name' : TextInput( attrs={
                'class': 'form-control',  
                'placeholder': 'Write first name',
                'required': True,
            }),

            'last_name' : TextInput( attrs={
                'class': 'form-control', 
                'id': 'name',  
                'placeholder': 'Write last name',
                'required': True,
            }),

            'phone' : TextInput( attrs={
                'class': 'form-control', 
                'placeholder': 'Write phone number',
                'required': True
            }),

            'dob' : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
            }),

            'image' : FileInput( attrs={
                # 'class': 'form-control show-img', 
                'class': 'form-control', 
                'accept' : 'image/jpeg image/png image/jpg',
                # 'style': 'border-style: dotted;',
            }),

            'gender': forms.Select(attrs={
                'class': 'form-control js-choice', 
                'id': "gender", 
            }),

            # 'is_superuser': CheckboxInput(attrs={'class': 'form-check-input' }),
            # 'is_admin'    : CheckboxInput(attrs={'class': 'form-check-input' }),
            # 'is_verified' : CheckboxInput(attrs={'class': 'form-check-input' }),
            # 'is_active'   : CheckboxInput(attrs={'class': 'form-check-input' }),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')

        if not image:
            instance = self.instance
            cleaned_data['image'] = instance.image

        return cleaned_data
    
