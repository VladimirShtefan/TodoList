import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import BoardParticipant


@pytest.mark.django_db
class TestBoardCreate:
    url = reverse('board_create')

    def test_board_create_successfully(self, login_user, current_user, faker):

        title = faker.text(max_nb_chars=255)
        response = login_user.post(self.url, data={'title': title})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('title') == title
        board_participant = BoardParticipant.objects.select_related('user').filter(user_id=current_user.id).first()
        assert board_participant.role == BoardParticipant.Role.owner

    def test_board_create_permission_denied(self, api_client, faker):
        title = faker.text(max_nb_chars=255)
        response = api_client.post(self.url, data={'title': title})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}


@pytest.mark.django_db
class TestBoardList:
    url = reverse('board_list')

    def test_get_board_list_successfully(self, current_user, board_factory, login_user):
        board_factory.create_batch(2, owner=current_user)
        response = login_user.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
