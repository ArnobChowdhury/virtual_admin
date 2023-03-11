## Guide to this project

#### Install the dependencies

```
pip install -r requirements.txt
```

#### Migrate the db

```
python3 manage.py migrate
```

#### Run the project in development mode

```
python3 manage.py runserver
```

#### Create an user

Send a POST request to http://127.0.0.1:8000/accounts/register/. Example JSON body

```
{
  "username":"foo1",
  "password": "awesomePassword123",
  "first_name": "Foo1",
  "last_name": "Bar1"
}
```

#### Login

This project handles authorization with SimpleJWT. Collect an access token and a refresh token from http://127.0.0.1:8000/api/token/

```
{
  "username": "foo1",
  "password": "awesomePassword123"
}
```

#### Create a company

An user can create a company. This gives them a row in `Company` table and a row in `Employee` table. This also makes them an admin to this company. Send a POST request to http://127.0.0.1:8000/accounts/create-company/ . This endpoint expects company information and the employment information of the person creating the company.

Authorization header example:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4NTA1NzI4LCJpYXQiOjE2Nzg0MTkzMjgsImp0aSI6IjE1MDkzNzcwMWViODQ1MTRiYzZlNWU1MTQ5NTY1ZWE5IiwidXNlcl9pZCI6NX0.ZwnEEwmMROSaCvFUgC7fsnkAyLU7i2wQ0tx0b3rJtEA
```

JSON Body example:

```
{
  "company": {
    "name": "NRB15 Bank Ltd."
  },
  "admin": {
    "department": "Administration",
    "designation": "General Manager"
  }
}
```

#### Add an employee to the company

Only an admin can add another user as an employee of the company. Please note, a new user account is to be created before adding the user as employee. Send a POST request to http://127.0.0.1:8000/accounts/add-employee/ . Authorization header like previous example is needed.
JSON body example:

```
{
  "user_id": 5,
  "department": "Marketing",
  "designation": "Manager",
  "is_admin": false
}
```

#### Create a device

We have a model called `Device`. An admin can add new devices, which then can be borrowed by other employees. Right now 3 types of devices can be created, Phone - `PH`, Laptop - `LT` and Tab - `TAB`. Send a POST request to http://127.0.0.1:8000/requisition/devices/. Authorization header is needed.
JSON body example:

```
{
  "type": "PH",
  "name": "Samsung A53"
}
```

#### Get a device

Any employee can get information about any device in their company. Authorization headers are needed. Send a GET request to http://127.0.0.1:8000/requisition/devices/

#### Requisition

Any employee can apply for a requisition to get a device for particular time, stating their reason. Send POST request to http://127.0.0.1:8000/requisition/applications/ . JSON Body example:

```
{
  "device_id": 1,
  "requested_checkout_date": "2023-03-10T10:00:00.175Z",
  "requested_return_date": "2023-03-14T17:00:00.175Z",
  "reason": "For app testing"
}
```

#### Check status of requisition/s

Any employee can check the status of any requisitions of their company. Authorization header is needed. Send GET a request to http://127.0.0.1:8000/requisition/applications/ for all the requisitions. And for a single requisition, Send a GET request like this with the id of the requisition - http://127.0.0.1:8000/requisition/applications/4 . Replace `4` with the requisition `id`.

#### Approve a requistion application

Only an admin can approve a requisition request. Send a POST request to http://127.0.0.1:8000/requisition/applications/4/approve/ with an admin Authorization header. Replace `4` with the requisition `id`.

#### Reject a requisition application

Only an admin can reject a requisition request. Send a POST request to http://127.0.0.1:8000/requisition/applications/4/reject/ with Authorization header of an admin. Replace `4` with the requisition `id`.

#### Device checkout

Employees can checkout a device when an admin has approved the requisition request. Send a POST request like this http://127.0.0.1:8000/requisition/applications/4/device_checkout/ , where `4` is the id of the requistion application row. Authorization header is needed.

#### Device return

Employees can return a device they have checked out. Send a POST request to http://127.0.0.1:8000/requisition/applications/4/device_return/ . Authorization headers are needed. They need to send the condition of the device they are returning.

```
{
  "condition": "OK"
}
```
