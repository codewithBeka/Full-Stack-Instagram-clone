
from django.urls import path
from post.views import home,NewPost,PostDetails,tags,like,favorite,homeLikes,explore,savePost,comment_post,update_post,deletePost,reels,like_post,unlike_post


urlpatterns = [
   	path('', home, name='home'),
   	path('explore/', explore, name='explore'),
   	path('reels/', reels, name='reels'),
   	path('newpost/', NewPost, name='newpost'),
   	path('<uuid:post_id>/update', update_post, name='update_post'),
   	path('<uuid:post_id>/delete', deletePost, name='deletePost'),
   	path('homeLikes/', homeLikes, name='homelikes'),
   	path('<uuid:post_id>', PostDetails, name='postdetails'),
   	path('<uuid:post_id>/like', like, name='postlike'),
   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
   	path('<uuid:post_id>/savePost', savePost, name='savePost'),
   	path('tag/<slug:tag_slug>', tags, name='tags'),
    path('post/<uuid:post_id>/comment/', comment_post, name='comment_post'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('unlike/<int:post_id>/', unlike_post, name='unlike_post'),
    ]