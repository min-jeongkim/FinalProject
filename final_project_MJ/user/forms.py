from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        error_messages={"required": "입력이 잘못되었습니다."}, max_length=64, label="email"
    )
    username = forms.CharField(
        error_messages={"required": "입력이 잘못되었습니다."},
        label="ID",
    )
    password1 = forms.CharField(
        error_messages={"required": "입력이 잘못되었습니다."},
        widget=forms.PasswordInput,
        label="PW",
    )
    password2 = forms.CharField(
        error_messages={"required": "입력이 잘못되었습니다."},
        widget=forms.PasswordInput,
        label="PW check",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {"username", "password"}
        widgets = {
            "username": forms.TextInput(attrs={"style": "width:270px;"}),
            "password": forms.PasswordInput(attrs={"style": "width:270px;"}),
        }

    def clean__Username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
            return username
        except models.User.DoesNotExist:
            self.add_error("username", forms.ValidationError("ID 또는 PW를 잘못 입력했습니다."))

    def clean(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")
        print("5", password, username)
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("ID 또는 PW를 잘못 입력했습니다."))
        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError("ID 또는 PW를 잘못 입력했습니다."))

        return super().clean()
