# Get User By Id

Fetches user details based on user id

**URL** : `/user/:user_id`

**URL Parameters** : `user_id=[string]` where `user_id` is the ID of the User in the database.

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "email": "alex@some.com",
    "user_id": "e16666ff-c559-4aab-96eb-f0a5c2c77b18",
    "username": "Alex",
    "enrolled": 0
}
```