from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from post.models import Follow

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Story(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_user')
	content = models.FileField(upload_to=user_directory_path)
	caption = models.TextField(max_length=50)
	expired = models.BooleanField(default=False)
	posted = models.DateTimeField(auto_now_add=True)
    
    
	def __str__(self):
		return self.user.username

class StoryStream(models.Model):
	following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_following')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	story = models.ManyToManyField(Story, related_name='storiess')
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.following.username + ' - ' + str(self.date)

	def add_post(sender, instance, *args, **kwargs):
		new_story = instance
		user = new_story.user
		followers = Follow.objects.all().filter(following=user)

		for follower in followers:
			try:
				s = StoryStream.objects.get(user=follower.follower, following=user)
			except StoryStream.DoesNotExist:
				s = StoryStream.objects.create(user=follower.follower, date=new_story.posted, following=user)
			s.story.add(new_story)
			s.save()

# Create your models here.

class StoryComment(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE,related_name='story')
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='storyuser')
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	
# Story Stream
post_save.connect(StoryStream.add_post, sender=Story)

#see on some second if comment is false
"""
from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_user')
    content = models.FileField(upload_to='user_{0}/{1}'.format)
    caption = models.TextField(max_length=50)
    expired = models.BooleanField(default=False)
    posted = models.DateTimeField(auto_now_add=True)
    seen_by = models.ManyToManyField(User, related_name='seen_stories', blank=True)

    def __str__(self):
        return self.user.username

class StoryStream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ManyToManyField(Story, related_name='storiess')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.following.username + ' - ' + str(self.date)

    @classmethod
    def add_post(cls, sender, instance, *args, **kwargs):
        new_story = instance
        user = new_story.user
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            try:
                s = cls.objects.get(user=follower.follower, following=user)
            except cls.DoesNotExist:
                s = cls.objects.create(user=follower.follower, date=new_story.posted, following=user)
            s.story.add(new_story)
            s.save()


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime, timedelta

from stories.models import Story, StoryStream
from stories.forms import NewStoryForm

@login_required
def NewStory(request):
    user = request.user
    if request.method == "POST":
        form = NewStoryForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('content')
            caption = form.cleaned_data.get('caption')
            story = Story(user=user, content=file, caption=caption)
            story.save()
            StoryStream.add_post(sender=Story, instance=story)
            return redirect('index')
    else:
        form = NewStoryForm()
    context = {'form': form}
    return render(request, 'newstory.html', context)

@login_required
def ShowMedia(request, stream_id):
    stories = StoryStream.objects.get(id=stream_id)
    media_st = stories.story.all().exclude(seen_by=request.user).values()
    stories_list = list(media_st)
    return JsonResponse(stories_list, safe=False)

@login_required
def MarkStoryAsSeen(request, story_id):
    story = Story.objects.get(id=story_id)
    story.seen_by.add(request.user)
    story.save()
    return JsonResponse({'success': True})

	
	
	function markStoryAsSeen(story_id) {
    $.ajax({
        url: '/stories/mark-as-seen/' + story_id,
        type: 'POST',
        success: function(response) {
            // Update the UI to reflect that the story has been seen
            // For example, you could hide the story or change its appearance
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}
"""

"""
class StoryStream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ManyToManyField(Story, related_name='storiess')
    date = models.DateTimeField(auto_now_add=True)
    seen_by = models.ManyToManyField(User, related_name='seen_stories', blank=True)

    def __str__(self):
        return self.following.username + ' - ' + str(self.date)

    def add_post(sender, instance, *args, **kwargs):
        new_story = instance
        user = new_story.user
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            try:
                s = StoryStream.objects.get(user=follower.follower, following=user)
            except StoryStream.DoesNotExist:
                s = StoryStream.objects.create(user=follower.follower, date=new_story.posted, following=user)
            s.story.add(new_story)
            s.seen_by.add(follower.follower)
            s.save()


			@login_required
def MarkStoryAsSeen(request, story_id):
    try:
        story_stream = StoryStream.objects.get(story__id=story_id, user=request.user)
        story_stream.seen_by.add(request.user)
        story_stream.save()
        return JsonResponse({'success': True})
    except StoryStream.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Story not found'})


		// Assuming you have a way to get the story_id
$.ajax({
    url: '/stories/mark-as-seen/' + story_id,
    type: 'POST',
    success: function(response) {
        if (response.success) {
            // Story has been marked as seen
        } else {
            console.error(response.error);
        }
    },
    error: function(xhr, status, error) {
        console.error(error);
    }
});




germini ai 

from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from post.models import Follow

# Create your models here.

def user_directory_path(instance, filename):
    # ... (same as before)

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_user')
    content = models.FileField(upload_to=user_directory_path)
    caption = models.TextField(max_length=50)
    expired = models.BooleanField(default=False)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class StoryView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

class StoryStream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ManyToManyField(Story, related_name='storiess')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.following.username + ' - ' + str(self.date)

    def add_post(sender, instance, *args, **kwargs):
        new_story = instance
        user = new_story.user
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            try:
                s = StoryStream.objects.get(user=follower.follower, following=user)
            except StoryStream.DoesNotExist:
                s = StoryStream.objects.create(user=follower.follower, date=new_story.posted, following=user)
            s.story.add(new_story)
            s.save()

# Story Stream & View Tracking
post_save.connect(StoryStream.add_post, sender=Story)
post_save.connect(StoryView.objects.create, sender=Story, weak=False)


def ShowMedia(request, stream_id):
    user = request.user
    stories = StoryStream.objects.get(id=stream_id).story.filter(storyview__user=user)
    # ... (rest of the logic)

{% for story in stories %}
    {% if not story.storyview_set.filter(user=user).exists %}
        {% endif %}
{% endfor %}

"""