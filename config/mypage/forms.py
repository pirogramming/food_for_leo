from django import forms

from mypage.models import Profile, Pet, Diary


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'kind', 'petInfo']


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content', 'img']
