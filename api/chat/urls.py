from django.urls import path, include

urlpatterns = [
    path('comments/', include('api.chat.comment.urls')),
    path('comment-participants/', include('api.chat.comment_participant.urls'))
]