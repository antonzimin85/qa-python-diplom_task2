class UserData:

    USERS_WITHOUT_MANDATORY_FIELD = [
        {"email": "fake_email@test.com", "password": "test_password"},
        {"email": "fake_email@test.com", "name": "test_name"},
        {"password": "test_password", "name": "test_name"}
    ]
    NOT_EXISTING_USER_CREDENTIALS = {"email": "not_existing_email@test.com", "password": "test_password"}
    EMPTY_USER_CREDENTIALS = {"Authorization": ""}
    UPDATE_USER_DATA = [
        ({"name": "updated_name"}, "name"),
        ({"email": "updated_new_email@japan.com"}, "email"),
    ]
