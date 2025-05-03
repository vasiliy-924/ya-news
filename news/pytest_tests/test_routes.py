# test_routes.py
import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args_fixture',
    [
        ('news:home', None),
        ('users:login', None),
        ('users:signup', None),
        ('news:detail', 'news_id'),
    ]
)
def test_pages_availability(client, name, args_fixture, request):
    args = request.getfixturevalue(args_fixture) if args_fixture else None
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_fixture, expected_status',
    [
        ('reader_client', HTTPStatus.NOT_FOUND),
        ('author_client', HTTPStatus.OK),
    ]
)
@pytest.mark.parametrize(
    'name',
    ['news:edit', 'news:delete']
)
def test_comment_edit_delete_availability(request, client_fixture, name, comment, expected_status):
    client = request.getfixturevalue(client_fixture)
    url = reverse(name, args=(comment.id,))
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ['news:edit', 'news:delete']
)
def test_redirect_for_anonymous(client, name, comment):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
