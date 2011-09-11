from django.test import TestCase

__test__ = {
"doctest1": """
>>> from blog.models import Post
>>> from django.contrib.auth.models import User
>>> import datetime
>>> user = User.objects.get_or_create(username="test")[0]
>>> post1 = Post.objects.get_or_create(title="Test One", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 50, 18))[0]
>>> post2 = Post.objects.get_or_create(title="Test Two", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 51, 18))[0]
>>> post3 = Post.objects.get_or_create(title="Test Three", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 52, 18))[0]
>>> post4 = Post.objects.get_or_create(title="Test Four", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 53, 18))[0]
>>> post5 = Post.objects.get_or_create(title="Test Five", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 54, 18))[0]
>>> post6 = Post.objects.get_or_create(title="Test Six", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 55, 18))[0]
>>> post7 = Post.objects.get_or_create(title="Test Seven", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 56, 18))[0]
>>> paginator = Post.objects.get_paginated_posts(user)
>>> post = paginator.page(4).object_list[0]
>>> post.get_page(user)
4
""",
}

#"doctest2": 
"""
>>> from blog.models import Post
>>> from django.contrib.auth.models import User
>>> import datetime
>>> user = User.objects.get_or_create(username="test2", is_superuser=True)[0]
>>> post1 = Post.objects.get_or_create(title="Test2 One", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 57, 18))[0]
>>> post2 = Post.objects.get_or_create(title="Test2 Two", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 58, 18))[0]
>>> post3 = Post.objects.get_or_create(title="Test2 Three", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 58, 20))[0]
>>> post4 = Post.objects.get_or_create(title="Test2 Four", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 12, 58, 25))[0]
>>> post5 = Post.objects.get_or_create(title="Test2 Five", content = "Some Content", user = user, publish = False, time = datetime.datetime(2010, 12, 14, 12, 59, 10))[0]
>>> post6 = Post.objects.get_or_create(title="Test2 Six", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 59, 30))[0]
>>> post7 = Post.objects.get_or_create(title="Test2 Seven", content = "Some Content", user = user, publish = True, time = datetime.datetime(2010, 12, 14, 11, 59, 50))[0]
>>> paginator = Post.objects.get_paginated_posts(user)
>>> post = paginator.page(4).object_list[0]
>>> post.get_page(user)
4
"""