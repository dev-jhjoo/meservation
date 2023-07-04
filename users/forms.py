from django import forms

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
