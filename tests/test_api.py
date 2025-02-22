import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from blogs.models import Post, Author, Comment
from django.contrib.auth import get_user_model
import datetime


User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def author(db, user):
    return Author.objects.create(name="Test Author", email="author@example.com", user=user)

@pytest.fixture
def active_post(db, author):
    return Post.objects.create(
        title="Active Post",
        content="This is an active post.",
        published_date=timezone.now(),
        author=author,
        status="published",
        active=True
    )

@pytest.fixture
def inactive_post(db, author):
    return Post.objects.create(
        title="Inactive Post",
        content="This is an inactive post.",
        published_date=timezone.now(),
        author=author,
        status="draft",
        active=False
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_post_list_shows_only_active_posts(api_client, active_post, inactive_post):
    url = reverse('api-post-list')  
    response = api_client.get(url, format='json')
    
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    returned_post = data[0]
    assert returned_post['title'] == active_post.title
    assert returned_post['author_name'] == active_post.author.name


#test2

# @pytest.fixture
# def user(db):
#     return User.objects.create_user(username="testuser", password="password123")

# @pytest.fixture
# def author(db, user):
#     return Author.objects.create(name="Test Author", email="author@example.com", user=user)

# @pytest.fixture
# def api_client():
#     return APIClient()

@pytest.fixture
def posts(db, author):
    """
    Create three posts with different published_dates:
      - One before the date range.
      - One inside the date range.
      - One after the date range.
    """
    now = timezone.now()
    post_before = Post.objects.create(
        title="Post Before",
        content="Content before the range.",
        published_date=now - datetime.timedelta(days=10),
        author=author,
        status="published",
        active=True
    )
    post_in_range = Post.objects.create(
        title="Post In Range",
        content="Content in range.",
        published_date=now - datetime.timedelta(days=5),
        author=author,
        status="published",
        active=True
    )
    post_after = Post.objects.create(
        title="Post After",
        content="Content after the range.",
        published_date=now - datetime.timedelta(days=1),
        author=author,
        status="published",
        active=True
    )
    return (post_before, post_in_range, post_after)

@pytest.mark.django_db
def test_post_list_filter_by_date_range(api_client, posts):
    """
    Test that the PostListAPIView returns only posts with published_date within the range.
    """
    # Calculate our date range: we want posts published between 7 days ago and 3 days ago.
    now = timezone.now().date()
    start_date = now - datetime.timedelta(days=7)
    end_date = now - datetime.timedelta(days=3)
    
    url = reverse('api-post-list')  # Make sure this matches your URL config.
    response = api_client.get(url, {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }, format='json')
    
    # Assert HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    # Only the post with published_date between start_date and end_date should be returned.
    # According to our fixture, that should be "Post In Range".
    assert isinstance(data, list)
    assert len(data) == 1
    
    returned_post = data[0]
    assert returned_post['title'] == "Post In Range"
    # You can also assert on other fields if needed:
    # assert returned_post['content'] == "Content in range."


#task3

@pytest.mark.django_db
def test_create_post_as_author(api_client, user, author):
    # Log in the user to simulate an authenticated request.
    api_client.login(username='testuser', password='password123')
    
    url = reverse('api-post-create')  # Ensure this matches the URL name in your urls configuration.
    
    # Create a valid payload.
    data = {
        "title": "Unique Post Title",
        "content": "This is some valid content for the post. It is long enough.",
        "published_date": timezone.now().isoformat()
    }
    
    response = api_client.post(url, data, format='json')
    
    # Assert the response status is 201 Created.
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check that the response includes the expected success message.
    response_data = response.json()
    assert response_data.get("message") == "Post created successfully!"
    
    # Verify that the post exists in the database and is associated with the correct author.
    created_post = Post.objects.get(title=data["title"])
    assert created_post.content == data["content"]
    assert created_post.author == author
    assert created_post.active is True


#task4
@pytest.mark.django_db
def test_edit_post_as_author(api_client, user, author, active_post):
    # Log in the user
    api_client.login(username='testuser', password='password123')
    
    # Build URL for editing the post (ensure the URL name matches your configuration)
    url = reverse('api-post-edit', kwargs={'pk': active_post.pk})
    
    # Data for editing the post
    updated_data = {
        "title": "Updated Title",
        "content": "This is the updated content for the post. It is now longer.",
        "active": False
    }
    
    # Send the PUT request to update the post
    response = api_client.put(url, updated_data, format='json')
    
    # Assert that the update was successful
    assert response.status_code == status.HTTP_200_OK
    
    # Refresh the post instance from the database and verify changes
    active_post.refresh_from_db()
    assert active_post.title == updated_data["title"]
    assert active_post.content == updated_data["content"]
    assert active_post.active == updated_data["active"]

#task5
@pytest.fixture
def post_to_delete(db, author):
    return Post.objects.create(
        title="Post to Delete",
        content="This post will be deleted by its author.",
        published_date=timezone.now(),
        author=author,
        status="published",
        active=True
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_delete_post_as_author(api_client, user, author, post_to_delete):
    # Log in as the user
    api_client.login(username='testuser', password='password123')
    
    # Construct the URL for deleting the post
    url = reverse('api-post-delete', kwargs={'pk': post_to_delete.pk})
    
    # Send a DELETE request
    response = api_client.delete(url)
    
    # Assert that the response status code is 204 No Content
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify that the post has been deleted from the database
    with pytest.raises(Post.DoesNotExist):
        Post.objects.get(pk=post_to_delete.pk)




#task6

@pytest.fixture
def active_post(db, author):
    # Create an active post
    return Post.objects.create(
        title="Active Post",
        content="Content of the active post.",
        published_date=timezone.now(),
        author=author,
        status="published",
        active=True
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_create_comment_as_logged_in_user(api_client, user, active_post):
    # Log in the user to simulate an authenticated request
    api_client.login(username='testuser', password='password123')
    
    # URL for creating a comment on the specific post (ensure URL name matches your configuration)
    url = reverse('api-comment-create', kwargs={'post_pk': active_post.pk})
    
    # Define the payload for the comment
    data = {
        "content": "This is a valid comment."
    }
    
    # Send POST request to create a comment
    response = api_client.post(url, data, format='json')
    
    # Assert that the response status is HTTP 201 Created
    assert response.status_code == status.HTTP_201_CREATED
    
    # Retrieve the created comment from the database
    comment = Comment.objects.get(post=active_post, content=data["content"])
    
    # Assert that the comment is associated with the correct post and user
    assert comment.post == active_post
    assert comment.user == user


#task7
@pytest.fixture
def active_post(db, author):
    return Post.objects.create(
        title="Active Post",
        content="Content of the active post.",
        published_date=timezone.now(),
        author=author,
        status="published",
        active=True
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_create_comment_as_non_logged_in_user(api_client, active_post):
    # Note: Do not log in any user.
    
    # Build the URL for comment creation. Make sure the URL name matches your configuration.
    url = reverse('api-comment-create', kwargs={'post_pk': active_post.pk})
    
    # Define the payload for the comment.
    data = {
        "content": "This is a comment from a non-logged-in user."
    }
    
    # Send the POST request to create a comment.
    response = api_client.post(url, data, format='json')
    
    # Assert that the response status is HTTP 201 Created.
    assert response.status_code == status.HTTP_201_CREATED
    
    # Retrieve the created comment from the database.
    comment = Comment.objects.get(post=active_post, content=data["content"])
    
    # Assert that the comment is associated with the correct post and that no user is associated.
    assert comment.post == active_post
    assert comment.user is None