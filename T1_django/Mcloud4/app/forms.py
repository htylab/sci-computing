"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class BootstrapCurveFittingForm(forms.Form):
    """Fitting form for T1, T2  which uses boostrap CSS."""
    t_value = forms.CharField(label='t_value', max_length=254,widget=forms.TextInput(attrs={'size':'100'}))
    y_value = forms.CharField(label='y_value',max_length=254,widget=forms.TextInput(attrs={'size':'100'}))

    crim_value = forms.CharField(label='crim_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':'per capita crime rate by town'}))
    zn_value = forms.CharField(label='zn_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':'0%~100%'}))
    indus_value = forms.CharField(label='indus_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':'%'}))

    CHOICES=[('1','1 (if tract bounds river)'),('0','0 (otherwise)')]
    chas_value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    #chas_value = forms.CharField(label='chas_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':' '}))

    nox_value = forms.CharField(label='nox_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':'nitric oxides concentration'}))
    rm_value = forms.CharField(label='rm_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':'average number of rooms per dwelling'}))
    age_value = forms.CharField(label='age_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':'%'}))
    dis_value = forms.CharField(label='dis_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':' '}))
    rad_value = forms.CharField(label='rad_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':' '}))
    tax_value = forms.CharField(label='tax_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':' '}))
    ptratio_value = forms.CharField(label='ptratio_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':' '}))
    b_value = forms.CharField(label='b_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':' '}))
    lstat_value = forms.CharField(label='lstat_value',max_length=254,widget=forms.TextInput(attrs={'size':'100','placeholder':' '}))
