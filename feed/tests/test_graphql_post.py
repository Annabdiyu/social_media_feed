import pytest
from graphene.test import Client
from backend.schema import schema
from django.test import RequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_post():
    user = User.objects.create_user(
        email="abdiyuanna@gmail.com",
        username="annaabdiyu",
        name="annaabdiyu",
        password="AASTUSOT1"
    )

    client = Client(schema)
    request = RequestFactory().post("/graphql/")
    res = client.execute(
        '''
        mutation {
            tokenAuth(email:"abdiyuanna@gmail.com", password:"AASTUSOT1") {
                token
            }
        }
        ''',
        context_value=request 
    )

    # Helpful assertions to catch future issues
    assert "errors" not in res, f"GraphQL errors: {res.get('errors')}"
    token_data = res.get("data", {}).get("tokenAuth")
    assert token_data and token_data.get("token"), f"tokenAuth failed: {res}"
