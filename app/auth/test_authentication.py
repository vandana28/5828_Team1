from app.auth.authentication import verify_user, create_new_user
from werkzeug.security import generate_password_hash
from mock import patch, MagicMock
from bson import ObjectId

context = "app.auth.authentication"

pwd = "password"
pwd_hash = generate_password_hash(pwd)
oid = ObjectId()
valid_doc = {"_id": oid, "username": "user", "hash": pwd_hash}

def test_verify_user():
    with patch(context + ".database") as mock:
        mock.users.find_one.return_value = valid_doc
        result = verify_user("user", pwd)

        assert result.id == str(oid)
        assert result.username == "user"

        assert not verify_user("user", "wrong")

        mock.users.find_one.return_value = None
        assert not verify_user("user", pwd)

def test_create_new_user():
    with patch(context + ".database") as mock:
        mock.users.find_one.return_value = valid_doc

        assert not create_new_user("user", pwd)

        mock.users.find_one.return_value = None
        
        insert_ack = MagicMock()
        insert_ack.inserted_id = oid

        mock.users.insert_one.return_value = insert_ack

        result = create_new_user("user", pwd)
        assert result.username == "user"
        assert result.id == str(oid)
