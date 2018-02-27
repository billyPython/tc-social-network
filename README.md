# social-network
Django REST API based social network

Endpoints:

    - signup:
        /sign-up/
        method POST
        payload_to_create={"username": username, "email": email, "password": password}
        respone serialized data

    - login:
        /login/
        method POST
        payload_to_create={"username": username, "password": password}
        respone user serialized data and auth cred

    - users:
        -/api/users/
            method GET,
        -/api/users/{id}/
            method GET

    - posts:
        /api/posts/
            methods (GET, POST, PATCH)
            payload_to_create={"title", title, "text": text}
            response serialized data

        /api/posts/{id}/like/
        methods GET
        response 201

        /api/posts/{id}/unlike/
        methods GET
        response 201

# 3rd party:

- username-generator
- pyhunter --> for email existence check
- clearbit --> enriching user data on sing up

# Bot usage:
- python manage.py bot --data json_file_path