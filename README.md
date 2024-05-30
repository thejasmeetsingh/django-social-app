# Django Social App

A small social networking application which allows user to:

1. Create an account.
2. Login into their account.
3. View other users on the system and search the users based on name or email address.
4. Send friend request to a user.
5. Accept/Reject a request received from a user.
6. View list of requests and filter them by request status.

## Security

1. Implements JWT authentication for users.
2. All APIs except `login` and `signup` will be called by authenticated users only.
3. `ScopedRateThrottle` is added so that users can not send more than 3 friend requests within a minute.
4. API permission is applied, which won't allow the sender or any other user to update the request user. It'll only be updated by the user whose request is intended to.

## Getting Started

**Prerequisite:** [Docker](https://www.docker.com/products/docker-desktop/) must be installed on your machine.

1. Clone the project repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run the project using `docker-compose up` command.
4. To stop the project, Run `docker-compose down`.

Once you run the project, Access the APIs at http://0.0.0.0:8000 address.

For get up and running quickly a fixtures file is added which contains mock data of 100 users. All the users have the same password: `1234`. This will allow anyone to test the APIs with good amount of records.

You can test the APIs on postman as well.

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/17396704-a24032fe-e59c-40a2-8019-b1df3d90e576?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D17396704-a24032fe-e59c-40a2-8019-b1df3d90e576%26entityType%3Dcollection%26workspaceId%3D392b781a-05ab-415b-9eb8-456aca6f3129)
