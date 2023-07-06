from django import forms
from users.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=16,
        widget=forms.TextInput(
            attrs={"placeholder": "사용자 이름을 입력하세요."},
        )
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호를 입력하세요."},
        )
    )

class SignupForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=16,
        widget=forms.TextInput(
            attrs={"placeholder": "사용자 이름을 입력하세요."},
        )
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호를 입력하세요."},
        )
    )
    password_check = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호를 다시 입력하세요."},
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "이메일을 입력하세요."},
        )
    )
    first_name = forms.CharField(
        max_length=16,
        widget=forms.TextInput(
            attrs={"placeholder": "이름을 입력하세요."},
        )
    )
    last_name = forms.CharField(
        max_length=16,
        widget=forms.TextInput(
            attrs={"placeholder": "성을 입력하세요."},
        )
    )
    description = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "자기소개를 입력하세요."},
        )
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        # email = self.cleaned_data["email"].
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"입력한 사용자명({username})은 이미 사용 중입니다.")
        # if User.objects.filter(email=email).exists():
        #     raise forms.ValidationError("이미 사용중인 이메일입니다.")
        return username
    
    def clean(self):
        password = self.cleaned_data["password"]
        password_check = self.cleaned_data["password_check"]
        if password != password_check:
            self.add_error("password2", "비밀번호와 비밀번호 확인란의 값이 다릅니다.")
        
    def save(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        email = self.cleaned_data["email"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        description = self.cleaned_data["description"]
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            description=description,
        )
        return user
    