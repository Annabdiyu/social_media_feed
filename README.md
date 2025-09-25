# 🚀 Social Media Feed Backend

> **Django + PostgreSQL + GraphQL backend** powering a real-time social media feed.  
>
> Scalable, secure, and built for lightning-fast queries.
>
> A modern social-media style application where users can **create posts, like/unlike, comment, update, and delete posts**—all powered by a secure **GraphQL API** and backed by **PostgreSQL**.

---

## 🌟 Features at a Glance
- **Flexible GraphQL API** – Fetch exactly the data you need
- **Rich Interactions** – Users can create posts, like/unlike, comment, and share
- **Authentication** – JWT-based login & token verification
- **Scalable Design** – Optimized database schema for high traffic
- **Production Ready** – Follows Django best practices and includes test coverage

---

## 🏗️ Tech Stack
| Layer         | Technology |
|-------------- |-----------|
| Backend       | **Django 5** |
| Database      | **PostgreSQL 14+** |
| API Protocol  | **GraphQL (Graphene-Django)** |
| Auth          | **graphql-jwt** |
| Deployment    | Any WSGI/ASGI host (e.g. Render, Railway, Heroku) |

---

```
Django (backend)
│
├── Graphene-Django (GraphQL layer)
│    └── JWT Auth (graphql-jwt)
│
└── PostgreSQL (data storage)
```



- **Models:** `User`, `Post`, `Comment`, `PostLike`
- **Schema:** Query & Mutation types for posts, comments, likes
- **Security:** Environment-based secrets, login required decorators

---

## 🚦 Quick Start

### 1️⃣ Prerequisites
- Python **3.12+**
- PostgreSQL **14+**
- Node.js (optional, only if you plan to use a frontend client)
- Git

### 2️⃣ Clone & Enter
```bash
git clone https://github.com/Annabdiyu/social_media_feed.git
cd social-nexus
```


### 3️⃣ Create & Activate Virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 5️⃣ Database Setup

Create a PostgreSQL database and user:

```sql
CREATE DATABASE social_nexus;
CREATE USER social_user WITH PASSWORD 'strong_password';
ALTER ROLE social_user SET client_encoding TO 'utf8';
ALTER ROLE social_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE social_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_nexus TO social_user;
```

### 6️⃣ Environment Variables

Create a file named **`.env`** in the project root:

```
DEBUG=True
SECRET_KEY=replace_me_with_a_long_secret
DATABASE_URL=postgres://social_user:strong_password@127.0.0.1:5432/social_nexus
REDIS_URL=redis://127.0.0.1:6379/0
```

### 7️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8️⃣ Create a Superuser

```bash
python manage.py createsuperuser
```

### 9️⃣ Start Development Server

```bash
python manage.py runserver
```

Visit **[http://127.0.0.1:8000/graphql/](http://127.0.0.1:8000/graphql/)** for the GraphiQL playground.

---

## 🧪 Running Tests

```bash
pytest
```

This runs the suite in `feed/tests/` including GraphQL mutation tests.

---

## 🔑 Example GraphQL Mutations

Create a post:

```graphql
mutation {
  createPost(content: "Hello World!") {
    post { id content createdAt }
  }
}
```

Like a post:

```graphql
mutation {
  likePost(postId: "1") {
    ok
    likesCount
  }
}
```

Update a post:

```graphql
mutation {
  updatePost(postId: "1", content: "Updated!") {
    post { id content }
  }
}
```

---

## 🌍 Deployment (Heroku/Render/Railway)

1. Push code to GitHub.
2. Provision a PostgreSQL add-on or managed DB.
3. Set environment variables (`DATABASE_URL`, `SECRET_KEY`, `REDIS_URL`, `DEBUG=False`) on the hosting platform.
4. Run:

   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

---

## 🏅 Project Structure

```
social-backend/
│
├── backend/           # Django project settings
├── feed/              # App with models, schema, tests
├── manage.py
└── README.md
```

---

## 📜 License

MIT License – free to use and modify.

---

## 🙌 Acknowledgements

Built with ❤️ using:

* [Django](https://www.djangoproject.com/)
* [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/)
* [PostgreSQL](https://www.postgresql.org/)
* [graphql-jwt](https://github.com/flavors/django-graphql-jwt)

---

## 🧭 Author

**Anna Abdiyu (Anish)**
📧 [abdiyuanna@gmail.com](mailto:abdiyuanna@gmail.com)
💻 [GitHub](https://github.com/Annabdiyu)







