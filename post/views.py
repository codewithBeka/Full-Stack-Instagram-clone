from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from post.models import Stream, Post, Tag,Likes,Follow
from post.forms import NewPostForm,PostUpdateForm
from notifications .models import Notification
from django.contrib.auth.decorators import login_required
from django.template import loader
from authy.models import Profile
from stories.models import Story, StoryStream
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView
import json
from django.http import JsonResponse

# Create your views here.
from django.db.models import Q

@login_required
def home(request):
	user = request.user
	profile = Profile.objects.get(user=user)

	# Get all the posts
	all_posts = Post.objects.order_by('-posted')

	# Get all the posts the user is following
	following_posts = Stream.objects.filter(user=user).values_list('post_id', flat=True)

	# Filter the posts to only include the ones the user is following and the ones the user owns
	post_items = all_posts.filter(Q(id__in=following_posts) | Q(user=user)).distinct()

	# Get all the users the user is not following
	users_not_following = User.objects.exclude(id__in=Follow.objects.filter(follower=user).values_list('following_id', flat=True))[:5]

	stories = StoryStream.objects.filter(user=user)

	# Get the user's notifications
	notifications = Notification.objects.filter(user=user).order_by('-date')
	Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
	# Get the number of comments for each post
	post_comments = {}
	for post in post_items:
		post_comments[post.id] = Comment.objects.filter(post=post).count()
		
	count_notifications = 0
	count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

	#for current userlike 
	for post in post_items:
			post.is_liked = Likes.objects.filter(post=post, user=user).exists()


	# Handle search functionality
	search_query = request.GET.get('search')
	if search_query:
		users = User.objects.filter(
			Q(first_name__icontains=search_query) |
			Q(last_name__icontains=search_query) |
			Q(username__icontains=search_query)
		)
	else:
		users = []
	comments = Comment.objects.all()

	

	context = {
		'post_items': post_items,
		'stories': stories,
		'profile': profile,
		'all_users': users_not_following,
		'notifications': notifications,
		'searched_users': users,
		'comments': comments,
        'count_notifications':count_notifications,
		'post_comments': post_comments
	}

	return render(request, 'home.html', context)

@login_required
def reels(request):
	videos= Post.objects.all()
	comments = Comment.objects.all()

	context ={
		"videos":videos,
		"comments":comments
	}

	return render(request,"reels.html",context)

# @login_required
# def home(request):
#     user = request.user
#     profile = Profile.objects.get(user=user)

#     # Get all the posts
#     all_posts = Post.objects.order_by('-posted')

#     # Get all the posts the user is following
#     following_posts = Stream.objects.filter(user=user).values_list('post_id', flat=True)

#     # Filter the posts to only include the ones the user is following and the ones the user owns
#     post_items = all_posts.filter(Q(id__in=following_posts) | Q(user=user)).distinct()

#     # Get all the users the user is not following
#     users_not_following = User.objects.exclude(id__in=Follow.objects.filter(follower=user).values_list('following_id', flat=True))[:5]

#     stories = StoryStream.objects.filter(user=user)

#     # Get the user's notifications
#     notifications = Notification.objects.filter(user=user).order_by('-date')
#     Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
#     print(stories)



#     context = {
#         'post_items': post_items,
#         'stories': stories,
#         'profile': profile,
#         'all_users': users_not_following,
#         'notifications': notifications,
#     }

#     return render(request, 'home.html', context)

@login_required
def homeLikes(request):
	user = request.user
	post_id = request.GET.get('post_id')

	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(post_id=post_id, user=user).count()
	

	if not liked:
				like = Likes.objects.create(user=user, post_id=post_id)
				like.save()
				current_likes = current_likes + 1
				post.likes = current_likes
				post.userlike =True
				post.save()
				return redirect('/')

	else:
			Likes.objects.filter(user=user,post_id=post_id).delete()
			current_likes = current_likes - 1
			post.likes = current_likes
			post.userlike =False
			post.save()
			return redirect('/')
	# user = request.user

	# post_id = request.GET.get('post_id')

	# profile = Profile.objects.get(user=user)
	# post = get_object_or_404(Post, id=post_id)




	# #for comments 

	# #comment
	# comments = Comment.objects.filter(post=post).order_by('date')
	
	# if request.user.is_authenticated:
	# 	#profile = Profile.objects.get(user=user)
	# 	#For the color of the favorite button

	# 	if profile.favorites.filter(id=post_id).exists():
	# 		favorited = True

	# #Comments Form
	# if request.method == 'POST':
	# 	form = CommentForm(request.POST)
	# 	if form.is_valid():
	# 		comment = form.save(commit=False)
	# 		comment.post = post
	# 		comment.user = user
	# 		comment.save()
	# 		return HttpResponseRedirect(reverse('home', args=[post_id]))
	# else:
	# 	form = CommentForm()


	# context = {
	# 	'profile':profile,
	# 	'favorited':favorited,
	# 	'profile':profile,
	# 	'form':form,
	# 	'comments':comments,

	# }

	# return HttpResponse(loader.get_template('home.html').render(context, request))


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if not Likes.objects.filter(post=post, user=user).exists():
        like = Likes.objects.create(post=post, user=user)
        like.save()
        post.likes += 1
        post.userlike = True
        post.save()

        # Create a notification for the post owner
        notify = Notification.objects.create(
            post=post, sender=user, user=post.user, notification_type=1
        )
        notify.save()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unlike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if Likes.objects.filter(post=post, user=user).exists():
        like = Likes.objects.get(post=post, user=user)
        like.delete()
        post.likes -= 1
        post.userlike = False
        post.save()

        # Delete the notification for the post owner
        notify = Notification.objects.filter(
            post=post, sender=user, notification_type=1
        ).first()
        if notify:
            notify.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

class ExploreView(ListView):
    model = Post
    template_name = 'explore.html'
    context_object_name = 'posts'
    ordering = ['-posted']
    paginate_by = 24

    def get_queryset(self):
        return Post.objects.all()
	
@login_required
def explore(request):
	all_posts= Post.objects.all()
	context ={"posts":all_posts}
	return render(request,"explore.html",context)




@login_required
def NewPost(request):
	user = request.user
	tags=Tag.objects.all()
	tags_objs = []

	if request.method == 'POST':
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			picture = form.cleaned_data.get('picture')
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tags')
			for tag in tags_form:
				t, created = Tag.objects.get_or_create(title=tag.title)
				tags_objs.append(t)

			# Create the Post object only once
			p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
			p.tags.set(tags_objs)
			p.save()
			return redirect('home')
	else:
		form = NewPostForm()

	context = {
		'form': form,
		"tags":tags
	}

	return render(request, 'newpost.html', context)




@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance=post, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostUpdateForm(instance=post, user=request.user)

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'updatepost.html', context)

@login_required(login_url='login')
def deletePost(request, post_id):
	post = Post.objects.get(id=post_id)

	if request.user != post.user:
		return HttpResponse('Your are not allowed here!!')

	if request.method == 'POST':
		post.delete()
		return redirect('home')
	return render(request, 'delete.html', {'obj': post})



def PostDetails(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	user = request.user
	profile = Profile.objects.get(user=user)
	favorited = False

	#comment
	comments = Comment.objects.filter(post=post).order_by('date')
	
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=user)
		#For the color of the favorite button

		if profile.favorites.filter(id=post_id).exists():
			favorited = True

	#Comments Form
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = user
			comment.save()
			return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	else:
		form = CommentForm()


	template = loader.get_template('post_detail.html')

	context = {
		'post':post,
		'favorited':favorited,
		'profile':profile,
		'form':form,
		'comments':comments,
	}

	return HttpResponse(template.render(context, request))


def tags(request, tag_slug):

	
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-posted')

	template = loader.get_template('tags.html')

	context = {
		'posts':posts,
		'tag':tag,
	}

	return HttpResponse(template.render(context, request))

@login_required
def like(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(post_id=post_id, user=user).count()

	if not liked:
				like = Likes.objects.create(user=user, post_id=post_id)
				like.save()
				current_likes = current_likes + 1
				post.likes = current_likes
				post.userlike =True
				post.save()

	else:
			Likes.objects.filter(user=user,post_id=post_id).delete()
			current_likes = current_likes - 1
			post.likes = current_likes
			post.userlike =False
			post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))




@login_required
def favorite(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)
		post.postsaved = False
	else:
		profile.favorites.add(post)
		post.postsaved = True

	profile.save()
	post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))



@login_required
def savePost(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
        post.postsaved = False
    else:
        profile.favorites.add(post)
        post.postsaved = True

    profile.save()
    post.save()

    return redirect("home")
@login_required
def comment_post(request, post_id):
	if request.method == 'POST':
		post = Post.objects.get(id=post_id)
		comment_body = request.POST.get('comment_body')
		Comment.objects.create(post=post, user=request.user, body=comment_body)
	return redirect('home')


# @login_required
# def homeLikes(request):
#     user = request.user
#     post_id = request.GET.get('post_id')

#     post = Post.objects.get(id=post_id)
#     current_likes = post.likes
#     liked = Likes.objects.filter(post_id=post_id, user=user).count()

#     if not liked:
#         like = Likes.objects.create(user=user, post_id=post_id)
#         like.save()
#         current_likes = current_likes + 1
#         post.likes = current_likes
#         post.userlike = True
#         post.save()
#         return JsonResponse({'success': True, 'likes': current_likes, 'liked': True})
#     else:
#         Likes.objects.filter(user=user, post_id=post_id).delete()
#         current_likes = current_likes - 1
#         post.likes = current_likes
#         post.userlike = False
#         post.save()
#         return JsonResponse({'success': True, 'likes': current_likes, 'liked': False})

# @login_required
# def savePost(request, post_id):
#     user = request.user
#     post = Post.objects.get(id=post_id)
#     profile = Profile.objects.get(user=user)

#     if profile.favorites.filter(id=post_id).exists():
#         profile.favorites.remove(post)
#         post.postsaved = False
#     else:
#         profile.favorites.add(post)
#         post.postsaved = True

#     profile.save()
#     post.save()

#     return JsonResponse({'success': True, 'saved': post.postsaved})

# @login_required
# def comment_post(request, post_id):
#     if request.method == 'POST':
#         post = Post.objects.get(id=post_id)
#         comment_body = request.POST.get('comment_body')
#         comment = Comment.objects.create(post=post, user=request.user, body=comment_body)
#         return JsonResponse({
#             'success': True,
#             'comment_id': comment.id,
#             'comment_body': comment.body,
#             'comment_user': comment.user.username,
#             'comment_date': comment.created.strftime('%b %d, %Y')
#         })
#     return JsonResponse({'success': False})