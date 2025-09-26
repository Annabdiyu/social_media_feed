

---

# 📘 Social Media Feed API Documentation

Welcome to the **Social Media Feed API**.
This API powers a social-media platform built with **Django, GraphQL (Graphene), and PostgreSQL**.

---

## 🔑 Authentication

All mutations and queries requiring user context use **JWT (JSON Web Token)**.

### Obtain a Token

```graphql
mutation {
  tokenAuth(email: "user@example.com", password: "yourPassword") {
    token
  }
}
```

Include the token in the `Authorization` header of subsequent requests:

```
Authorization: JWT <token>
```

### Verify / Refresh

```graphql
mutation { verifyToken(token: "<token>") { payload } }
mutation { refreshToken(token: "<token>") { token } }
```

---

## 📂 Queries

### 1️⃣ **Get Current User**

```graphql
query {
  me {
    id
    username
    name
    email
    avatar
    bio
    postsCount
  }
}
```

### 2️⃣ **Fetch a Single Post**

```graphql
query {
  post(id: "POST_ID") {
    id
    content
    createdAt
    likesCount
    commentsCount
    sharesCount
    author {
      id
      username
    }
  }
}
```

### 3️⃣ **Fetch Recent Posts**

```graphql
query {
  posts(first: 10) {
    id
    content
    createdAt
    likesCount
    commentsCount
  }
}
```

---

## ✍️ Mutations

### 1️⃣ **Create Post**

```graphql
mutation {
  createPost(content: "Hello World!") {
    post {
      id
      content
      createdAt
    }
  }
}
```

### 2️⃣ **Update Post**

```graphql
mutation {
  updatePost(postId: "POST_ID", content: "Edited text!") {
    post {
      id
      content
    }
  }
}
```

### 3️⃣ **Delete Post**

```graphql
mutation {
  deletePost(postId: "POST_ID") {
    ok
  }
}
```

### 4️⃣ **Like / Unlike Post**

```graphql
mutation {
  likePost(postId: "POST_ID") {
    ok
    likesCount
  }
}
mutation {
  unlikePost(postId: "POST_ID") {
    ok
  }
}
```

### 5️⃣ **Create Comment**

```graphql
mutation {
  createComment(postId: "POST_ID", content: "Nice post!") {
    comment {
      id
      content
      author {
        username
      }
    }
  }
}
```

---

## 🗂 Data Model

| Model        | Key Fields                                                             |
| ------------ | ---------------------------------------------------------------------- |
| **User**     | id, username, name, email, avatar, bio, postsCount                     |
| **Post**     | id, content, author, createdAt, likesCount, commentsCount, sharesCount |
| **Comment**  | id, post, author, content, createdAt                                   |
| **PostLike** | id, post, user                                                         |

---

## ⚙️ Error Handling

Errors follow standard GraphQL error responses:

```json
{
  "errors": [
    { "message": "Authentication required", "locations": [...], "path": [...] }
  ]
}
```

Always check the `"errors"` array before using `"data"`.

---

## 🌐 Base URLs

* **Local Development:** `http://localhost:8000/graphql/`
* **Production (if deployed):** `https://<your-domain>/graphql/`

---

## 🧩 Tips

* Use [GraphQL Playground](https://github.com/graphql/graphql-playground) or Postman for testing.
* Use the `first` argument in `posts` query for pagination.

---

**Maintainers:** Babi 
Built with ❤️ using **Django • Graphene • PostgreSQL**

---


