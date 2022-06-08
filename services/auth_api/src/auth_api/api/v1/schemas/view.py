from auth_api.extensions import ma


class ExpiringSubscriptionSchema(ma.Schema):
    user_uuid = ma.String(required=True, example='768b49ca-02d9-4524-9f13-3ac70f0cd7eb')
    role_uuid = ma.String(required=True, example='768b49ca-02d9-4524-9f13-3ac70f0cd7eb')
