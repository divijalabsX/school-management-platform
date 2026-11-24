import uuid

from app.utils.security import (
    create_access_token,
    verify_access_token
)


test_user_id = uuid.uuid4()

# Generate a token
token = create_access_token(test_user_id)

print("Token generated:", bool(token))

# Verify the token
payload = verify_access_token(token)

print("Token verified:", True)
print("User ID matches:", payload["sub"] == str(test_user_id))
print("Expiration exists:", "exp" in payload)