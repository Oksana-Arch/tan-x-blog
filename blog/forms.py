from django import forms
from .models import Post, Tag, Category, Comment
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'comment', 'body', 'tags', 'categories', 'author', 'status', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()
            if new_slug == 'create':
                raise ValidationError('Slug may not be "Create"')
            return new_slug

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()
            if new_slug == 'create':
                raise ValidationError('Slug my not be "Create"')
            return new_slug

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_slug(self):
            new_slag = self.cleaned_data['slug'].lower()
            if new_slag == 'create':
                raise ValidationError('Slug my not be "Create"')
            return new_slag

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('email', 'content')

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'office.phir@gma|'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write here'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'type': 'search'}))

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea())
    copy = forms.BooleanField(required=False, label='Send a copy to me')
