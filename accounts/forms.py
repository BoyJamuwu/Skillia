from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "nombre@ejemplo.com"}),
    )


class EmailUserCreationForm(UserCreationForm):
    full_name = forms.CharField(label="Nombre Completo")
    email = forms.EmailField(label="Correo Electrónico")

    class Meta:
        model = User
        fields = ("full_name", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
        return user