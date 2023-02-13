import pytest

from django.urls import reverse
from rest_framework import status

from core.serializers import UserLoginSerializer, UserProfileSerializer


@pytest.mark.django_db
class TestLogin:
    url = reverse('user-login')

    def test_login_successfully(self, api_client, user_factory, faker):
        password = faker.password()
        user = user_factory.create(password=password)
        response = api_client.post(self.url, data={'username': user.username,
                                                   'password': password
                                                   })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == UserLoginSerializer(user).data

    def test_login_failure(self, api_client, user_factory):
        user = user_factory.build()
        response = api_client.post(self.url, data={'username': user.username,
                                                   'password': user.password
                                                   })
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Не верный логин или пароль'}


@pytest.mark.django_db
class TestSignUp:
    url = reverse('user-signup')

    def test_signup_successfully(self, api_client, faker):
        username = faker.user_name()
        password = faker.password()
        user = {
            'username': username,
            'password': password,
            'password_repeat': password
        }
        response = api_client.post(self.url, data=user)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('username') == username

    def test_signup_failure(self, api_client, faker):
        username = faker.user_name()
        password = faker.password()
        password_repeat = faker.password()
        user = {
            'username': username,
            'password': password,
            'password_repeat': password_repeat,
        }
        response = api_client.post(self.url, data=user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'password_repeat': ['Пароли должны совпадать']}

    def test_password_validation(self, api_client, faker):
        username = faker.user_name()
        password = faker.password(length=4)
        user = {
            'username': username,
            'password': password,
            'password_repeat': password
        }
        response = api_client.post(self.url, data=user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'password': ['Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.']
        }

        password = '12345678'
        user = {
            'username': username,
            'password': password,
            'password_repeat': password
        }
        response = api_client.post(self.url, data=user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'password': ['Введённый пароль слишком широко распространён.',
                                                'Введённый пароль состоит только из цифр.']}


@pytest.mark.django_db
class TestUserProfile:
    url = reverse('user-profile')

    def test_get_profile_successfully(self, api_client, login_user, current_user):
        response = login_user.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserProfileSerializer(current_user).data

    def test_get_profile_failure(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_edit_profile_successfully(self, login_user, current_user, faker):
        username = current_user.username
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        response = login_user.put(self.url, data={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': current_user.id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }

    def test_partial_edit_profile_successfully(self, login_user, current_user, faker):
        last_name = faker.last_name()
        response = login_user.patch(self.url, data={
            'last_name': last_name,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': current_user.id,
            'username': current_user.username,
            'first_name': current_user.first_name,
            'last_name': last_name,
            'email': current_user.email,
        }

    def test_delete_profile_successfully(self, login_user, current_user):
        response = login_user.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUpdatePassword:
    url = reverse('user-update-password')

    def test_update_user_password_successfully(self, api_client, faker, user_factory):
        password = faker.password()
        new_password = faker.password()
        user = user_factory.create(password=password)
        api_client.force_login(user)
        response = api_client.put(self.url, data={
            'old_password': password,
            'new_password': new_password,
        })
        assert response.status_code == status.HTTP_200_OK

    def test_update_user_password_failure(self, api_client, faker, user_factory):
        password = faker.password()
        new_password = faker.password(length=4)
        user = user_factory.create(password=password)
        api_client.force_login(user)
        response = api_client.put(self.url, data={
            'old_password': password,
            'new_password': new_password,
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'new_password': ['Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.']
        }
