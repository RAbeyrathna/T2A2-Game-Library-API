# T2A2 - Game Library API - Rahal Abeyrathna

An API application designed and created for the Coder Academy T2A2 assignment.

[Github Repository](https://github.com/RAbeyrathna/T2A2-Game-Library-API)

[Trello Board](https://trello.com/b/5PyPfbK5/t2a2-game-library-api)

## Table of Contents

- [Installation of API](#installation-of-api)
- [R1: Problem Identification](#r1-problem-identification)
- [R2: Problem Significance](#r2-problem-significance)
- [R3: Database System Selection and Drawbacks](#r3-database-system-selection-and-drawbacks)
- [R4: ORM Functionalities and Benefits](#r4-orm-functionalities-and-benefits)
- [R5: API Endpoints Documentation](#r5-api-endpoints-documentation)
- [R6: Entity-Relationship Diagram (ERD)](#r6-entity-relationship-diagram-erd)
- [R7: Third-Party Services Integration](#r7-third-party-services-integration)
- [R8: Application Models and Relationships](#r8-application-models-and-relationships)
- [R9: Database Relations](#r9-database-relations)
- [R10: Task Allocation and Tracking](#r10-task-allocation-and-tracking)

## Installation of API

The steps below assume you are running on a MacOS or Linux based operating system.

1. Clone the API to your local machine from the GitHub repo above
2. Open the `'src'` folder in your terminal of choice
3. Run `python3 -m venv venv`
4. Run `source venv/bin/activate`
5. Run `flask db init` to intialise the database and create the tables
6. Run `flask db seed` to get the default seed data for the database
7. Run `flask run` to start the flask server on `http://localhost:8080`

## R1: Problem Identification

> Explain the problem that the application is designed to solve.

This API application gives gamers an effective management system to track their extensive game libraries. Current services such as Steam and Epic Games host and allow players to play several games, but do not offer an effective way to track the progress of the game, a personal rating of the game or the current status of a game. These games can also span across several services and platforms, scattering the library a gamer and making it difficult to manage.

This application streamlines the process and allows users to catalog their games and to assign statuses and scores of their own personal library, allowing them to get on top of their gaming habits and track it extensively.

A common frustration that gamers face is to be in the middle of a game, only to start a brand new game that has come out and to abandon their old one, forgetting it entirely. This tool can allow for gamers to now easily and effectively manage their libraries and to keep up to date of all the games they have played.

It also allows for gamers to track their gaming habits, tracking games by their genre and platform, letting gamers see their preferences and biases, which can inform their future gaming purchases.

## R2: Problem Significance

> Discuss why this is an important problem that needs solving.

As users purchase more and more games, spanning over all the different services and platforms, it can be difficult to remember what games have been played and what they thought of a game. This tool now allows them to catalog these games and easily pull up what their favourite games might be, what scores they've given and the status of a game to easily come back to.

A gamer can now put a game "On-hold", allowing them to start a new game without the fear of forgetting any other game they may have been playing as it is logged in the system and can be filtered by the status. This gives users control of their library, and allows for another way for gamers to hone in on their gaming habits and to track data that would otherwise be difficult to find.

As games can be found on different platforms, it can be easy to forget what games really caught your attention and you were intrigued in as games are constantly coming out and gamers are constantly overwhelmed by the options. Now gamers can keep everything in a single place and can come back to it whenever they want to see what games they are currently playing or what to play next.

## R3: Database System Selection and Drawbacks

> Justify the choice of database system and discuss potential drawbacks.

For this application, I opted to use PostgreSQL (also referred to as PSQL) as the database system.

### Benefits of Using PSQL

#### ACID Compliance

PSQL is known for the robustness and reliability that it offers. It complies with the ACID principles (Atomicity, Consistency, Isolation, Durability) which are important to establish secure and reliable database transactions.

A quick overview of ACID can be found below:

- Atomicity
  - If any part of the database transaction fails, the database is *rolled back* and ensures nothing is changed.
- Consistency
  - The database stays *consistent* and so any data written follows the set up data validation rules.
- Isolation
  - Multiple transactions in the database *do not conflict* with each other, as each transaction is completed in *isolation*
- Durability
  - Any data transaction that is completed, will be saved to the database, even in the event of a *power outage* or *other systematic failure*

This is important for many applications, let alone the one developed here as we want to ensure that when users interact with this application, that the data being worked with is stored in the database correctly and doesn't conflict with other entries, especially as many users would be working with the application at the same time.

#### Feature set and Community

PSQL has many features such as nested transactions, online/hot backups and asynchronous replication, but the community supporting the system have also developed extensions which further extend to this functionality.

This includes international character sets, storage of large binary objects such as videos and pictures, and supoprt for Most SQL data types.

The community supporting PSQL is vast and dedicated, which is also backed by the fact that PSQL is open-source, allowing for anyone to view and modify the source code as they wish to.

### Drawbacks of Using PSQL

While PSQL has many beenfits to it, there are a few drawbacks to take into consideration as well. PSQL is commonly criticized as being slower compared to other options such as MySQL and may not be as suitable for larger businesses to implement.

Postgres can also have a larger learning curve which can make it tougher to implement as the developers involved will need to learn and adjust to the database system. This can in turn, make migration more difficult as well after establishing use through PSQL.

Other DBMS such as, *MySQL* may be more simple and easier to learn and get familiar with, but does not offer the same amount of features and benefits that Postgres does. It was through this careful consideration that PSQL was chosen, as for this particular instance, it was easier to implement and provided more benefits than drawbacks in implementation.

## R4: ORM Functionalities and Benefits

> Detail the key functionalities and advantages of using an ORM in this application.

Utilising an ORM (Object-Relational Mapping) framework gave many functional benefits to the development of the application such as:

- Relational mapping of the database tables
- Generating schemas and managing the schemas
- Quickly and easily seeding data for the application
- Allowing for a simple and less complicated way to interact with the database, away from the terminal

In this case, SQLAlchemy was used as the ORM of choice, and so rather than working directly in PSQL can be complicated and confusing, SQLAlchemy provides us with abstraction and makes it easier for developers to write and code in a lanugage they are comfortable in, which greatly saved time and improved the quality of experience during the development of the application.

Rather than connecting into the database directly and creating each table by scratch, managing the relationships and adding the data manually, the ORM allows us to specify the tables, relationships and data all within Python. We can then easily create custom queries and commands, initalise and recreate the tables as needed, and get a more simplified but just as powerful overview and control over the entire application.

The ORM provides the developers a simpler and much more intuitive experience in developing the application, making small tasks which could otherwise be repetitive and complicated, seamless and simple. It also makes the process simpler to get accustomed, and as such reduces the amount of time wasted trying to learn new systems and to complete tasks which could otherwise be completed in a shorter amount of time.

The use of an ORM also promotes scalability and maintainability of the application as a whole, as developers are easily able to add tables, update the schemas, adding seed data etc. The models/tables are much easier to read and understand, and as such just as easy to modify and fine tune as needed.

To streamline your documentation and avoid repeating the sub-headings "Parameters/Response Body" and "Response" for each endpoint, while still maintaining clarity and readability, you can adopt a format that clearly separates each endpoint and its details without excessive repetition. Here's a revised structure that could work for you:

## R5: API Endpoints Documentation

> List and describe all the API endpoints included in the application.

### Authentication Routes

#### `POST - /auth/register` (User Registration)

This route allows users to register an account with the application which can then be used in the `/auth/login` route.

**Parameters/Response Body**:

- `username`: String - the username of the user
- `password`: String - the password of the user

Example request body:

```JSON
{
    "username": "Test User 1",
    "email": "user1@email.com",
    "password": "abcd123@"
}
```

**Response**:

Returns the created user account details including user_id, username, email, is_admin status, and a newly created user_library_id.

Example response:

```JSON
{
    "user_id": 2,
    "username": "Test User 1",
    "email": "user1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
        }
    ]
}
```

#### `POST - /auth/login` (User Login)

This route allows users to login with an account that has been previously registered.

**Parameters/Response Body**:

- `email`: String - the email of the user
- `password`: String - the password of the user

Example request body:

```JSON
{
    "email": "user1@email.com",
    "password": "abcd123@"
}
```

**Response**:

Returns the JWT token of the logged in user, along with email and is_admin status.

Example response:

```JSON
{
    "email": "user1@email.com",
    "token": "(TOKEN HERE)",
    "is_admin": false
}
```

---

### User Routes

#### `GET - /users/{user_id}` (Get One User record)

This route allows users to retrieve an individual user record from the database.

**Parameters/Response Body**:

No parameters needed in the response body. Only a `user_id` in the route.

**Response**:

Returns the user record with the corresponding ID.

Example response:

```JSON
{
    "user_id": 2,
    "username": "Test User 1",
    "email": "user1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
        }
    ]
}
```

---

#### `GET - /users/` (Get all User records)

This route allows users to retrieve all user record from the database.

**Parameters/Response Body**:

No parameters needed in the response body

**Response**:

Returns all user records currently registered in the database.

Example response:

```JSON
[
    {
        "user_id": 1,
        "username": "Admin Account",
        "email": "admin@email.com",
        "is_admin": true,
        "user_library": [
            {
                "user_library_id": 1
            }
        ]
    },
    {
        "user_id": 2,
        "username": "Test User 1",
        "email": "user1@email.com",
        "is_admin": false,
        "user_library": [
            {
                "user_library_id": 2
            }
        ]
    }
]
```

---

#### `DELETE - /users/{user_id}` (Delete a User record)

This route allows a user to delete an account from the database.
It requires the user to be logged in with an **admin** account or the owner of the account being deleted.

**Parameters/Response Body**:

- `user_id` of the account to be deleted is passed through the route

**Response**:

Example response:

```JSON
{
    "message": "User with ID '2' has been deleted successfully"
}
```

---

#### `UPDATE - /users/{user_id}` (Update a User record)

This route allows a user to modify an account from the database.
It requires the user to be logged in with an **admin** account or the owner of the account being edited.

**Parameters/Response Body**:

- `user_id` of the account to be modified is passed through the route
- The body contains the fields to be modified in the record

Example body-

```JSON
{
    "username": "User 1",
    "email": "username1@email.com"
}
```

**Response**:

Returns the user account with the updated fields.

Example response:

```JSON
{
    "user_id": 2,
    "username": "User 1",
    "email": "username1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
            }
    ]
}
```

---

### Genre Routes

#### `GET - /genres/{genre_id}` (Get One Genre record)

This route allows users to retrieve an individual user record from the database.

**Parameters/Response Body**:

No parameters needed in the response body. Only a `user_id` in the route.

**Response**:

Returns the user record with the corresponding ID.

Example response:

```JSON
{
    "user_id": 2,
    "username": "Test User 1",
    "email": "user1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
        }
    ]
}
```

---

#### `GET - /genres/` (Get all Genre records)

This route allows users to retrieve all genre record from the database.

**Parameters/Response Body**:

No parameters needed in the response body

**Response**:

Returns all genre records currently registered in the database.

Example response:

```JSON
[
    {
        "user_id": 1,
        "username": "Admin Account",
        "email": "admin@email.com",
        "is_admin": true,
        "user_library": [
            {
                "user_library_id": 1
            }
        ]
    },
    {
        "user_id": 2,
        "username": "Test User 1",
        "email": "user1@email.com",
        "is_admin": false,
        "user_library": [
            {
                "user_library_id": 2
            }
        ]
    }
]
```

---

#### `DELETE - /genres/{genre_id}` (Delete a Genre record)

This route allows a user to delete a genre from the database.
It requires the user to be logged in with an **admin** account.

**Parameters/Response Body**:

- `genre_id` of the account to be deleted is passed through the route

**Response**:

Example response:

```JSON
{
    "message": "User with ID '2' has been deleted successfully"
}
```

---

#### `UPDATE - /genres/{genre_id}` (Update a Genre record)

This route allows a user to modify a genre record from the database.
It requires the user to be logged in with an **admin** account.

**Parameters/Response Body**:

- `genre_id` of the account to be modified is passed through the route
- The body contains the fields to be modified in the record

Example body-

```JSON
{
    "username": "User 1",
    "email": "username1@email.com"
}
```

**Response**:

Returns the genre with the updated fields.

Example response:

```JSON
{
    "user_id": 2,
    "username": "User 1",
    "email": "username1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
            }
    ]
}
```

### Platform Routes

#### `GET - /platforms/{platform_id}` (Get One Platform record)

This route allows users to retrieve an individual platform record from the database.

**Parameters/Response Body**:

No parameters needed in the response body. Only a `platform_id` in the route.

**Response**:

Returns the platform record with the corresponding ID.

Example response:

```JSON
{
    "user_id": 2,
    "username": "Test User 1",
    "email": "user1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
        }
    ]
}
```

---

#### `GET - /platforms/` (Get all Platform records)

This route allows users to retrieve all platform record from the database.

**Parameters/Response Body**:

No parameters needed in the response body

**Response**:

Returns all platform records in the database.

Example response:

```JSON
[
    {
        "user_id": 1,
        "username": "Admin Account",
        "email": "admin@email.com",
        "is_admin": true,
        "user_library": [
            {
                "user_library_id": 1
            }
        ]
    },
    {
        "user_id": 2,
        "username": "Test User 1",
        "email": "user1@email.com",
        "is_admin": false,
        "user_library": [
            {
                "user_library_id": 2
            }
        ]
    }
]
```

---

#### `DELETE - /platforms/{platform_id}` (Delete a Platform record)

This route allows a user to delete a platform from the database.
It requires the user to be logged in with an **admin** account.

**Parameters/Response Body**:

- `platform_id` of the account to be deleted is passed through the route

**Response**:

Example response:

```JSON
{
    "message": "User with ID '2' has been deleted successfully"
}
```

---

#### `UPDATE - /platforms/{platform_id}` (Update a Platform record)

This route allows a user to modify a platform from the database.
It requires the user to be logged in with an **admin** account.

**Parameters/Response Body**:

- `platform_id` of the account to be modified is passed through the route
- The body contains the fields to be modified in the record

Example body-

```JSON
{
    "username": "User 1",
    "email": "username1@email.com"
}
```

**Response**:

Returns the platform with the updated fields.

Example response:

```JSON
{
    "user_id": 2,
    "username": "User 1",
    "email": "username1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
            }
    ]
}
```

### Game Routes

#### `GET - /games/{game_id}` (Get One Game record)

This route allows users to retrieve an individual game record from the database.

**Parameters/Response Body**:

No parameters needed in the response body. Only a `game_id` in the route.

**Response**:

Returns the game record with the corresponding ID.

Example response:

```JSON
{
    "user_id": 2,
    "username": "Test User 1",
    "email": "user1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
        }
    ]
}
```

---

#### `GET - /games/` (Get all Game records)

This route allows users to retrieve all game records from the database.

**Parameters/Response Body**:

No parameters needed in the response body

**Response**:

Returns all game records currently registered in the database.

Example response:

```JSON
[
    {
        "user_id": 1,
        "username": "Admin Account",
        "email": "admin@email.com",
        "is_admin": true,
        "user_library": [
            {
                "user_library_id": 1
            }
        ]
    },
    {
        "user_id": 2,
        "username": "Test User 1",
        "email": "user1@email.com",
        "is_admin": false,
        "user_library": [
            {
                "user_library_id": 2
            }
        ]
    }
]
```

---

#### `DELETE - /games/{game_id}` (Delete a Game record)

This route allows a user to delete an account from the database.
It requires the user to be logged in with an **admin** account.

**Parameters/Response Body**:

- `game_id` of the account to be deleted is passed through the route

**Response**:

Example response:

```JSON
{
    "message": "User with ID '2' has been deleted successfully"
}
```

---

#### `UPDATE - /games/{game_id}` (Update a Game record)

This route allows a user to modify a game record from the database.
It requires the user to be logged in with an **admin** account.

**Parameters/Response Body**:

- `game_id` of the account to be modified is passed through the route
- The body contains the fields to be modified in the record

Example body-

```JSON
{
    "username": "User 1",
    "email": "username1@email.com"
}
```

**Response**:

Returns the game with the updated fields.

Example response:

```JSON
{
    "user_id": 2,
    "username": "User 1",
    "email": "username1@email.com",
    "is_admin": false,
    "user_library": [
        {
            "user_library_id": 2
            }
    ]
}
```

### Library Routes

## R6: Entity-Relationship Diagram (ERD)

> Provide an ERD to visualize the database schema of the application.

![ERD Diagram](./docs/ERD_Diagram.png)

## R7: Third-Party Services Integration

> Describe any third-party services the application relies on and their purposes.

## R8: Application Models and Relationships

> Explain the models used in the project and the relationships between them.

## R9: Database Relations

> Discuss how database relations are implemented within the application.

## R10: Task Allocation and Tracking

> Outline how tasks are allocated and tracked during the project's development.

During the development of this project, I used Trello to track and manage the tasks I needed to complete. 

At the beginning of the project, I made a list of goals and deliverables I wanted to complete, and broke these down into subtasks and into cards where suitable. 

Each card then was given sub-tasks to break it down and work on individually.

I reviewed through the assignment rubric and ensured that there were cards tailored to ensuring I was on track and completing the assignment according to the rubric.

I would put all the tasks into the backlog initially, and would slowly move them into the `To Do` section once I was getting ready to work on them.

At the start of the day, I would review the Trello board, and move any tasks into the `Doing` section and focus on working those before looking back at the `To Do` and `Backlog` sections.

At some points, I would get carried away and work on parts or aspects of the application which would be apart of a card I wasn't focusing on, but I would simply tick of the relevant task on the card when this would happen.

I made sure to use due date to help keep me on track and to manage my workload so I could focus and prioritise tasks, and ensure I was staying within the time frame and completing the entire project on-time.

![Trello Board 1](./docs/trello-progress-1.png)
![Trello Board 2](./docs/trello-progress-2.png)
![Trello Board 3](./docs/trello-progress-3.png)
![Trello Board 4](./docs/trello-progress-4.png)