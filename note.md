## 1. django 프로젝트 시작
#### (1) 데이터 베이스 생성
```
python manage.py migrate
```
ls 해주면 db.sqlit3 파일이 생성된 것을 보임

#### (2) 관리자 계정 생성
```
python manage.py createsuperuser
```
username, email, password 입력
```
python manage.py runserver
```
admin 페이지에 들어가서 로그인 하면 완료

#### (3) 앱 만들기
```
python manage.py startapp 앱명
```

####(4) Django 프로젝트에 등록하기
main 프로젝트 - settings.py - INSTALLED_APPS 에 만들었던 앱을 추가해 주기
ex) 'blog'

## 2. Model 만들기
**(1) app / models.py 모델 생성**
```py
class Post(models.Model):
    title=models.CharField(max_length=30)
    content=models.TextField()
```
####(2) app / admin.py 모델 등록
```py
from .models import Post  #Post가 선언 된 파일을 가져오기
admin.site.register(Post)  #Post 모델을 선언해주어야 admin 사이트에 Post 모델이 등록됨
```
#### (3) migrate 해주기 
```commandline
python manage.py makemigrations
python manage.py migrate
```
#### (4) 시간 설정하기
app/models.py
```py
class Post(models.Model):
    created_at=models.DateTimeField(auto_now_add=True) #시간 자동 부여
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):  #Model안의 내용을 화면에 출력하는 기능
        return f'[{self.pk}]{self.title}:{self.created_at}'  
        #게시글을 만들 때 마다 고유의 키를 부여함 -> pk(primary key)
```
main/settings.py
```py
TIME_ZONE = 'Asia/Seoul'
USE_TZ = False
```

## 3. 웹페이지 만들기
### (1) FBV
#### a. 블로그 리스트 페이지

- main/urls.py
```python
from django.urls import path, include 
urlpatterns=[
    path('blog/', include('blog.urls'))
]
```
- blog/urls.py 만들기
```python
from django.urls import path
from . import views
urlpatterns=[
    path('', views.index)  #views.함수이름
]
```

- blog/views.py
```python
from .models import Post

def index(request):
    posts1=Post.objects.all().order_by('-pk') # .order_by('-pk') : 역순으로 
    #Post 모델에 있는 모든 것들을 posts1에 넣음 -> 템플릿에서 사용된 데이터를 views에서 준비
    return render(request, 'blog/index.html', {'posts':posts1})
    #posts 인자는 template 폴더에서 찾음  #오른쪽 posts1가 위에서 선언한 posts1
```

- blog/templates/blog/index.html 만들기
```html
{% for p in posts %}
    <h2>{{p.title}}</h2>
    <h3>{{p.created_at}}</h3>
    <p>{{p.content}}</p>
{% endfor %}
```

---
#### b.블로그 상세 페이지
- blog/urls.py 만들기
```python
path('<int:pk>/', views.single_post_page) #pk인수가 들어왔을 때 single_post_page 함수 호출
```

- blog/views.py
```python
def single_post_page(request,pk):  #pk에 따라 불러오는 글이 달라지니 views 쪽에 pk도 전달해야 함
     post2=Post.objects.get(pk=pk)  #get : 특정한 거만 가져오기  #Post가 가지고 있는 필드 이름=위에서 받은 인자
     return render(request,'blog/single_post_page.html',{'post':post2})
```

- blog/templates/blog/single_post_page.html 만들기
```python
<h1>{{post.title}}</h1>
<h3>{{post.created_at}}</h3>
<p>{{post.content}}</p>
<hr />
<h4>여기에 댓글 작성</h4>
```


---
### (2) CBV
클래스 안에 있는 메서드를 호출하는 형태로 view 만들어주기

ListView, DetailView를 제공해줌

ListView : 포스트 목록 페이지, 모델명_list.html을 인식함, as_view() 메서드(ListView에서 제공)를 부름
DetailView : 모델명_detail.html을 인식함
- main/urls.py
```python
from django.urls import path, include 
urlpatterns=[
    path('admin/', admin.site.urls),  #IP주소/admin
    path('blog/', include('blog.urls')), #blog 폴더에 있는 urls를 불러오기  #IP주소/blog
]
```
- blog/urls.py 만들기
```python
#urlpatterns에 작성해둔 코드들 삭제 
from django.urls import path
from . import views

urlpatterns=[
    path('',views.PostList.as_view()),  #views.모델명List.as_view()을 호출하기
    path('<int:pk>/',views.PostDetail.as_view())  #views.모델명Detail.as_view()을 호출하기
]
```
- blog/views.py
```python
from .models import Post
from django.views.generic import ListView, DetailView
class PostList(ListView):  #ListView를 상속받음
    model=Post #사용할 모델명인 Post를 정의해주기
    ordering='-pk' #최신순으로 보여주기
    #템플릿을 통해 전달되는데 자동으로 모델명_list.html과 연결됨  -> post_list.html
    #자동으로 전달되는 파라미터 : 모델명_list -> post_list

class PostDetail(DetailView):
    model=Post
    #템플릿은 자동으로 모델명_detail.html과 연결됨 -> post_detail.html
    #자동으로 전달되는 파라미터 : 모델명 -> post
```
- blog/templates/blog/post_list.html 만들기
```python
{% for p in post_list %}
    <h2>{{p.title}}</h2>
    <h3>{{p.created_at}}</h3>
    <p>{{p.content}}</p>
{% endfor %}
```
- blog/templates/blog/post_detail.html 만들기
```python
<head>
    <title>Blog Post - {{post.title}}</title>
</head>
<h1>{{post.title}}</h1>
<h3>{{post.created_at}}</h3>
<p>{{post.content}}</p>
<hr />
<h4>여기에 댓글 작성</h4>
```

### (3) 링크를 통해 블로그 페이지 이동하기
- blog/models.py
```python
def get_absolute_url(self):
    return f'/blog/{self.pk}/' #fstring 문자열을 리턴해주기
```
- blog/templates/blog/post_list.html
```python
<h2><a href="{{p.get_absolute_url}}">{{p.title}}</a></h2> 
#이렇게 수정해주면 포스트 제목을 누르면 디테일 페이지로 이동
```










### (4) 대문페이지 , 자기소개 페이지만들기
- main/urls.py
```python
path('',include('single_pages.urls')) #ip주소/
```
- single_pages/urls.py 만들기
```python
from django.urls import path
from . import views

urlpatterns=[ #ip주소/
    path('',views.landing), #ip주소/
    path('about_me/',views.about_me) #ip주소/about_me/
]

- single_pages/views.py
```python
def landing(request):
    return render(request, 'single_pages/landing.html')

def about_me(request):
    return render(request,'single_pages/about_me.html')
```
- single_pages/templates/single_pages/landing.html 만들기
```python
<nav>
    <a href="/blog/">Blog</a>
    <a href="/about_me/">About Me</a>
</nav>
```
- single_pages/templates/single_pages/about_me.html 만들기
```python
<nav>
    <a href="/blog/">Blog</a>
    <a href="/about_me/">About Me</a>
</nav>
```