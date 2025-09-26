# Social Backend API Documentation

This document provides detailed usage instructions for the GraphQL API of the **Social Backend** project.

## Base URL
```
http://<your-domain-or-localhost>/graphql/
```

## Authentication
- Obtain a JWT token via `tokenAuth` mutation.
- Pass the token in the `Authorization` header: `Authorization: JWT <token>`.

## Queries

### 1. Fetch Current User
```graphql
query {
  me {
    id
    username
    email
    postsCount
  }
}
```

### 2. Fetch All Posts
```graphql
query {
  posts(first: 10) {
    id
    content
    author { username }
    createdAt
    likesCount
    commentsCount
    sharesCount
  }
}
```

### 3. Fetch Single Post
```graphql
query {
  post(id: "<post_id>") {
    id
    content
    author { username }
    createdAt
  }
}
```

## Mutations

### 1. Create Post
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

### 2. Update Post
```graphql
mutation {
  updatePost(postId: "<post_id>", content: "Updated content") {
    post { id content }
  }
}
```

### 3. Delete Post
```graphql
mutation {
  deletePost(postId: "<post_id>") {
    ok
  }
}
```

### 4. Like/Unlike Post
```graphql
mutation {
  likePost(postId: "<post_id>") {
    ok
    likesCount
  }
}

mutation {
  unlikePost(postId: "<post_id>") {
    ok
  }
}
```

### 5. Create Comment
```graphql
mutation {
  createComment(postId: "<post_id>", content: "Nice!") {
    comment {
      id
      content
      author { username }
    }
  }
}
```

## Notes
- All mutations except `tokenAuth` require a valid JWT token.
- Pagination is supported in `posts(first, after)` for scalable querying.

---
© 2025 Social Media Feed Backend Project