from django import forms
from post.models import Post


class NewPostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ('picture', 'caption', 'tags')
		def __init__(self, *args, **kwargs):
			super(NewPostForm, self).__init__(*args, **kwargs)
			self.fields['caption'].widget.attrs['placeholder'] = 'Add a Title'
			self.fields['tags'].widget.attrs['placeholder'] = 'Tell everyone what your pin is about..'
			
			for visible in self.visible_fields():
				if visible.name == 'description':
					visible.field.widget.attrs['class'] = 'description-input border form-control'
				elif visible.name == 'board':
					visible.field.widget.attrs['class'] = 'board-input border form-control'
				else:
					visible.field.widget.attrs['class'] = 'form-control border rounded-pill'



class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('picture', 'caption', 'tags')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        self.fields['caption'].widget.attrs['placeholder'] = 'Add a Title'
        self.fields['tags'].widget.attrs['placeholder'] = 'Tell everyone what your post is about..'

        for visible in self.visible_fields():
            if visible.name == 'description':
                visible.field.widget.attrs['class'] = 'description-input border form-control'
            elif visible.name == 'board':
                visible.field.widget.attrs['class'] = 'board-input border form-control'
            else:
                visible.field.widget.attrs['class'] = 'form-control border rounded-pill'
"""

class NewPostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('picture', 'caption', 'tags')
		def __init__(self, *args, **kwargs):
			super(NewPostForm, self).__init__(*args, **kwargs)
			self.fields['caption'].widget.attrs['placeholder'] = 'Add a Title'
			self.fields['tags'].widget.attrs['placeholder'] = 'Tell everyone what your pin is about..'
			
			for visible in self.visible_fields():
				if visible.name == 'description':
					visible.field.widget.attrs['class'] = 'description-input border form-control'
				elif visible.name == 'board':
					visible.field.widget.attrs['class'] = 'board-input border form-control'
				else:
					visible.field.widget.attrs['class'] = 'form-control border rounded-pill'

"""