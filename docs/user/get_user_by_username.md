# Get User By Username

Fetches user details based on username

**URL** : `/user/by-username/:username`

**URL Parameters** : `username=[string]` where `username` is the username of the User in the database.

**Query Parameters** : `?create_user=[boolean]` where `create_user` specifies to create the user if one is not found

**Method** : `GET`

**Data**: `{}`

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "email": "alex@some.com",
    "user_id": "e16666ff-c559-4aab-96eb-f0a5c2c77b18",
    "username": "Alex"
}
```