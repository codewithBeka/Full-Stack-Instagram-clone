To implement the functionality to display only videos and enable infinite scroll on the "reels.html" page, you can make the following changes:

1. **Update the view to fetch only video posts:**
In your `views.py`, update the `ReelsView` to fetch only the posts that are of type 'video':

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ReelsView(ListView):
    model = Post
    template_name = 'reels.html'
    context_object_name = 'posts'
    paginate_by = 10  # Number of posts to display per page

    def get_queryset(self):
        return Post.objects.filter(get_type='video').order_by('-posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['posts'], self.paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context
```

2. **Update the `reels.html` template:**
In your `reels.html` template, update the code to display the video posts and implement the infinite scroll functionality:

```html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container">
    <div class="row" id="posts-container">
        {% for post in posts %}
        {% if post.get_type == 'video' %}
        <div class="col-md-4 mb-4">
            <div class="card">
                <video class="card-img-top" controls>
                    <source src="{{ post.picture.url }}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <div class="card-body">
                    <p class="card-text">{{ post.caption }}</p>
                </div>
            </div>
        </div>
        {% endif %}
        {% endfor %}
    </div>
    {% if posts.has_next %}
    <div class="d-flex justify-content-center">
        <button class="btn btn-primary btn-load-more">Load More</button>
    </div>
    {% endif %}
</div>

<script>
    let page = 2;
    let isLoading = false;

    $('.btn-load-more').click(function() {
        if (!isLoading) {
            isLoading = true;
            $.ajax({
                url: '?page=' + page,
                type: 'GET',
                success: function(data) {
                    let posts = $(data).find('#posts-container').html();
                    $('#posts-container').append(posts);
                    page++;
                    isLoading = false;
                    if (!$(data).find('.btn-load-more').length) {
                        $('.btn-load-more').hide();
                    }
                }
            });
        }
    });

    $(window).scroll(function() {
        if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10 && !isLoading) {
            $('.btn-load-more').click();
        }
    });
</script>
{% endblock %}
```

In this updated code:

- The `ReelsView` now fetches only the posts with `get_type` as 'video'.
- The `reels.html` template displays the video posts in a grid layout.
- The template includes a "Load More" button that triggers an AJAX request to fetch the next page of video posts.
- The template also includes a scroll event listener that automatically triggers the "Load More" button when the user scrolls to the bottom of the page.

With these changes, the "reels.html" page will display only video posts and enable infinite scroll functionality, where the next set of video posts will be loaded as the user scrolls down the page.