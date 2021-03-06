import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import utc
from myblog.models import Post, Category


class PostTestCase(TestCase):
    fixtures = ['myblog_test_fixture.json', ]

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def test_unicode(self):
        expected = u"This is a title"
        p1 = Post(title=expected)
        actual = unicode(p1)
        self.assertEqual(expected, actual)

    def test_author_names(self):
        names = [("Bob", "Marley", "Bob Marley"),
                 ("Name", "Two", "Name Two"),
                 ("Sting", "", "Sting ")]

        author = User()
        p1 = Post(author=author)

        for first_name, last_name, expected in names:
            author.first_name = first_name
            author.last_name = last_name
            actual = p1.author_name()
            self.assertEqual(expected, actual)

    def test_author_name(self):
        expected = u"Mr. Administrator"
        p1 = Post(author=self.user)
        actual = p1.author_name()
        self.assertEqual(expected, actual)


class CategoryTestCase(TestCase):

<<<<<<< HEAD
    def test_unicode(self):
=======
    def test_string(self):
>>>>>>> 9dbe86e8adf3bd25afa6bffc104b04c9cdd80f2a
        expected = 'A String'
        c1 = Category(name=expected)
        actual = str(c1.name)
        self.assertEqual(expected, actual)


class FrontEndTestCase(TestCase):
    """test views provided in the front-end"""
    fixtures = ['myblog_test_fixture.json', ]

    def setUp(self):
        self.now = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.timedelta = datetime.timedelta(15)
        author = User.objects.get(pk=1)
        category = Category()
        category.name = "Test Category"
        category.save()
        category.post = []
        category.save()

        for count in range(1, 11):
            post = Post(title="Post %d Title" % count,
                        text="foo",
                        author=author)
            if count < 6:
                # publish the first five posts
                pubdate = self.now - self.timedelta * count
                post.published_date = pubdate
            post.save()
            if count % 2:
                category.posts.add(post)
                category.save()

    def test_list_only_published(self):
        resp = self.client.get('/')
        self.assertTrue("Recent Posts" in resp.content)
        for count in range(1, 11):
            title = "Post %d Title" % count
            if count < 6:
                self.assertContains(resp, title, count=1)
            else:
                self.assertNotContains(resp, title)

    def test_details_only_published(self):
        for count in range(1, 11):
            title = "Post %d Title" % count
            post = Post.objects.get(title=title)
            resp = self.client.get('/posts/%d/' % post.pk)
            if count < 6:
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, title)
            else:
                self.assertEqual(resp.status_code, 404)

    def test_category(self):
        resp = self.client.get('/categories/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp, "Category: Test Category")
        self.assertEqual(resp, "Post 1 Title")
        self.assertEqual(resp, "Post 3 Title")
        self.assertEqual(resp, "Post 5 Title")
