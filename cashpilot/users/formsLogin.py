from django import forms

class loginForm(forms.Form):
    login = forms.CharField(label='login',max_length=50)
    senha = forms.CharField(label='senha',max_length=50,widget=forms.PasswordInput())
    
    def clean_login(self):
        login = self.cleaned_data['login']
        return login
        
