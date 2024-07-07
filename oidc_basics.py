import base64
import json
import datetime

def generate_openid_token(issuer, subject, audience):
    # Define token claims
    claims = {
        "iss": issuer,
        "sub": subject,
        "aud": audience,
        "exp": (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).timestamp(),
        "iat": datetime.datetime.utcnow().timestamp(),
    }

    # Encode claims as JSON
    encoded_claims = json.dumps(claims)

    # Base64 encode the JSON claims
    encoded_token = base64.urlsafe_b64encode(encoded_claims.encode('utf-8')).decode('utf-8')

    return encoded_token

def authenticate():
    username = input("Enter username: ")
    password = input("Enter password: ") 

    if username == "jchow" and password == "Hello123!!":
        return True
    else:
        return False

if __name__ == "__main__":

    if authenticate():

        issuer = "https://jchowlabs.com"
        subject = "jchow@jchowlabs.com"
        audience = "https://service.jchowlabs.com"

        openid_token = generate_openid_token(issuer, subject, audience)

        print()
        print("OpenID Connect Token:")
        print(openid_token)

    else:
        print("Invalid username or password. Authentication failed.")
