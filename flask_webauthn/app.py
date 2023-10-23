import os
import secrets
from dataclasses import dataclass, field
from flask import Flask, abort, jsonify, render_template, request, session
from typing import List, Optional

from fido2 import cbor
from fido2.server import Fido2Server
from fido2.webauthn import (AttestationObject, AttestedCredentialData, AuthenticatorAttachment, AuthenticatorData, 
                            CollectedClientData, PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity, 
                            UserVerificationRequirement)

# Initialized Flask app with random session token
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Sets RP_NAME and RP_HOST from environment variables
RP_NAME = os.environ.get("RP_NAME", "WebAuthN Demo")
RP_HOST = os.environ.get("RP_HOST", "localhost")
relying_party = PublicKeyCredentialRpEntity(name=RP_NAME, id=RP_HOST)
fido_server = Fido2Server(relying_party)

# Dataclass for user profile information
@dataclass
class UserProfile:

    user_id: str
    username: str
    display_name: str
    credentials: List[AttestedCredentialData] = field(default_factory=list)

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "display_name": self.display_name,
        }

# Stores user profile data in database
@dataclass
class UserDatabase:

    users: List[UserProfile] = field(default_factory=list)

    def find(self, user_id) -> Optional[UserProfile]:
        for user in self.users:
            if user.user_id == user_id:
                return user

    def add(self, user: UserProfile):
        if len(self.users) == 20:
            self.users.pop(0)
        self.users.append(user)

# Initializes UserDatabase instance to store user data
user_database_instance = UserDatabase()

# Routes for index, user list, registration, and authentication
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def api_register():

    data = request.json or {}
    user_id = data["userId"]
    username = data["userName"]
    display_name = data["displayName"]

    # if the user is not already known, create them and add them to the list then
    # continue with the security key registration process.
    if not (user := user_database_instance.find(user_id)):
        user = UserProfile(user_id, username, display_name)
        user_database_instance.add(user)

    pk_user_entity = PublicKeyCredentialUserEntity(
        username, str.encode(user_id), display_name
    )

    # this will handle the case where the key has already been registered.
    data, state = fido_server.register_begin(
        pk_user_entity,
        user.credentials,
        user_verification=UserVerificationRequirement.DISCOURAGED,
        authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
    )

    # saves the public key credentials for this user in memory
    session[f"state-{user_id}"] = state

    return cbor.encode(data)


@app.route("/register/complete", methods=["POST"])
def register_complete():
    
    data = cbor.decode(request.get_data())
    user_id = data["userId"]  
    client_data = CollectedClientData(data["clientDataJSON"])  
    att_obj = AttestationObject(data["attestationObject"])  

    if not (user := user_database_instance.find(user_id)):
        return abort(404)

    auth_data = fido_server.register_complete(
        session[f"state-{user_id}"], client_data, att_obj
    )
    if auth_data.credential_data:
        user.credentials.append(auth_data.credential_data)

    return cbor.encode({"status": "ok"})


@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json or {}
    user_id = data["userId"]  

    if not (user := user_database_instance.find(user_id)):
        return abort(404)

    auth_data, state = fido_server.authenticate_begin(user.credentials)
    session[f"state-{user_id}"] = state
    return cbor.encode(auth_data)


@app.route("/authenticate/complete", methods=["POST"])
def authenticate_complete():

    data = cbor.decode(request.get_data())
    user_id = data["userId"]  

    if not (user := user_database_instance.find(user_id)):
        return abort(404)

    credential_id = data["credentialId"]  
    client_data = CollectedClientData(data["clientDataJSON"])  
    auth_data = AuthenticatorData(data["authenticatorData"])  
    signature = data["signature"]  

    fido_server.authenticate_complete(
        session.pop(f"state-{user_id}"),
        user.credentials,
        credential_id,  
        client_data,
        auth_data,
        signature,  
    )

    return cbor.encode({"status": "OK"})

def main():
    app.run(ssl_context="adhoc")

if __name__ == "__main__":
    main()
