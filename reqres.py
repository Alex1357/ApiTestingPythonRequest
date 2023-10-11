import requests
import pytest
from hamcrest import assert_that, not_none, equal_to, has_key, has_entries, is_, not_, empty, contains_string


@pytest.fixture(scope="session")
def session():
    session = requests.Session()
    yield session
    session.close()


class TestReqRes:
    @pytest.mark.description("Request: GET - get list of user with info about them. "
                             "Respond body: json file with information about user."
                             "Status code: 200, success ")
    def test_get_user_list(self, session):
        params = {"page": 2}

        respond = session.get('https://reqres.in/api/users', params=params)

        assert_that(respond.status_code, equal_to(200))
        assert_that(respond.json(), has_entries(
            {"data": not_(empty())}))

    @pytest.mark.description('Request: POST - create new user in the system'
                             'Respond body: all entered information about user'
                             'Status code: 201')
    def test_post_create_user(self, session):
        body_data = {"name": "Alex",
                     "job": "None"}

        respond = session.post('https://reqres.in/api/users', json=body_data)
        respond_json = respond.json()

        assert_that(respond.status_code, equal_to(201))
        assert_that(respond_json, has_entries(
            {**body_data,
             'id': (not_(empty()) and is_(str)),
             'createdAt': (not_(empty()) and is_(str))
             }))

    @pytest.mark.description('Request: PUT - update info about user'
                             'Respond body: name, job and  updatedAt'
                             'Status code: 200')
    def test_put_update_user(self, session):
        body_data = {'name': 'Alex',
                     'job': 'QA'}

        respond = session.put('https://reqres.in/api/users/2', json=body_data)
        respond_json = respond.json()

        assert_that(respond.status_code, equal_to(200))
        assert_that(respond_json, has_entries(
            {**body_data,
             "updatedAt": (is_(str) and not_(empty()))
             }))

    @pytest.mark.description('Request: DELETE - remove user from the system'
                             'Respond body: updatedAt'
                             'Status code: 200')
    def test_delete_user(self, session):
        respond = session.put('https://reqres.in/api/users/2')
        respond_json = respond.json()

        assert_that(respond.status_code, equal_to(200))
        assert_that(respond_json, has_entries(
            {'updatedAt': (is_(str) and not_(empty()))}
        ))
