Flask Social Network REST API. 

The project uses JWT for authentication.

<h4>POST /login</h4>

endpoint for user login

Request body:

Data required for user login

Example request:

<code>{
    "email": "artem@example.com",
    "password": "password"
}</code>

Responses:

<code>201 Created</code> response contains JWT token

Example response (201 Created):

<code>{
    "token": "<jwt_token>"
}</code>

<code><jwt_token></code> - generated JWT token

<code>401 Unauthorized</code> if data in the request body is incorrect or user doesn't exist

<code>403 Forbidden</code> if password isn`t correct

<h4>POST /sign_up</h4>

endpoint for user sign up

Request body:

Data required for user sign up

Example request:

<code>{
    "name": "Artem",
    "email": "artem@example.com",
    "password": "password"
}</code>

Responses:

<code>201 Created</code> response contains JWT token

Example response (201 Created):

<code>{
    "token": "<jwt_token>"
}</code>

<code><jwt_token></code> - generated JWT token

<h4>POST /post/create</h4>

post creation endpoint

Request body:

The post to create

<h5>Request parameters:</h5>

JWT token for personal access to the API

<code>x-access-tokens</code> required in header

Example request:

<code>{
    "title": "title of the post",
    "description": "description of the post",
    "user_id": 5
}</code>

<code>user_id</code> current user id

Responses:

<code>201 Created</code> Post successfully created

<code>403 Forbidden</code> User id isn`t valid

<h4>POST /post/like</h4>

endpoint for like the post

Request body:

The like to create

<h5>Request parameters:</h5>

JWT token for personal access to the API

<code>x-access-tokens</code> required in header

Example request:

<code>{
    "user_id": 1,
    "post_id": 1
}</code>

<code>user_id</code> current user id

Responses:

<code>201 Created</code> You liked this post!

<code>202 Accepted</code> Like is already present

<code>403 Forbidden</code> User id isn`t valid

<code>404 Not found</code> Post doesn't exist

<h4>POST /post/unlike</h4>

endpoint for unlike the post

Request body:

Like to be removed

<h5>Request parameters:</h5>

JWT token for personal access to the API

<code>x-access-tokens</code> required in header

Example request:

<code>{
    "user_id": 2,
    "post_id": 1
}</code>

<code>user_id</code> current user id

Responses:

<code>200 OK</code> You removed like

<code>403 Forbidden</code> User id isn`t valid

<code>404 Not found</code> Like isn`t present

<h4>GET /analytics</h4>

analytics about how many likes was made between two dates

<code>analytics?date_from=2022-01-06&date_to=2022-01-09</code> Example URL

API returns analytics aggregated by day

<h5>Request parameters:</h5>

JWT token for personal access to the API

<code>x-access-tokens</code> required in header

Responses:

<code> 200 OK </code>

Response Example (200 OK):

{
    "2022-01-07": 5,
    "2022-01-08": 16,
    "2022-01-09": 8
}

<h4>GET /analytics/<user_id></h4>

endpoint that shows when user was login last time and when he
made a last request to the service

authorized user can get analytics on any user registered on the network

<code><user_id></code> id of user for which you need to get analytics

<h5>Request parameters:</h5>

JWT token for personal access to the API

<code>x-access-tokens</code> required in header

Responses:

<code> 200 OK </code>

Response Example (200 OK):

<code>
{
    "last user activity": "Fri, 07 Jan 2022 23:12:11 GMT",  <br>"last user login": "Fri, 07 Jan 2022 23:09:06 GMT"}</code>

Testing was carried out using Postman.

To run the application, you need to create a virtual environment:

<code>pip install virtualenv</code>

<code>virtualenv env</code>

<code>env\Scripts\activate.ps1</code>

Use <code>flask run</code> for run the app in social_network folder.

For run project please provide the .env file with settings:

<code>DATABASE_URL</code>

<code>ADMIN_PASSWORD</code>

<code>ADMIN_USERNAME</code>

<code>SECRET_KEY</code>

and .flaskenv file with settings:

<code>FLASK_APP</code>

<code>FLASK_ENV</code>