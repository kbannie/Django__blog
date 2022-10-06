from django.urls import path
from . import views

urlpatterns=[
    path('',views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),

    # path('',views.index),  #IP주소/blog  #views 연결하기  #.index : 함수명
    # path('<int:pk>/', views.single_post_page)
]