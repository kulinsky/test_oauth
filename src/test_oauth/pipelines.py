from urllib3.exceptions import ReadTimeoutError
import vk


def save_profile(backend, user, response, *args, **kwargs):
    """ get user photo and friend list"""
    if backend.name == 'vk-oauth2':

        profile = user.userprofile

        if profile is None:
            raise ValueError('profile not found')

        if not profile.friends:
            token = response.get('access_token')
            session = vk.Session(token)
            api = vk.API(session, v='5.80', lang='ru')

            try:
                friends = api.friends.get(
                    count=6,
                    fields='first_name, last_name, photo_200_orig'
                )['items']
            except ReadTimeoutError('frieends timeout error'):
                print('frieends timeout error')
                friends = []

            try:
                photo = api.users.get(fields='photo_max_orig')[0]['photo_max_orig']
            except ReadTimeoutError('photo timeout error'):
                print('photo timeout error')
                photo = response.get('photo')
            finally:
                photo = photo.replace('?ava=1','')

            profile.friends = friends
            profile.photo = photo
            profile.save()