from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post
# Create your tests here.

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )
        
        cls.post = Post.objects.create(
            title="Test Title",
            body="Test Body",
            author=cls.user
        )
        
    def test_post_model(self):
        self.assertEqual(self.post.title, "Test Title")
        self.assertEqual(self.post.body, "Test Body")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "Test Title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")
        
    def test_urls_exist_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        
    def test_url_names(self):
        # TEST HOME
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Body")
        self.assertTemplateUsed(response, "home.html")
        # TEST POST_DETAIL
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/100000/") # FALSE TEST CEHCKS CONVICTION
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Test Title")
        self.assertTemplateUsed(response, "post_detail.html")
        
        