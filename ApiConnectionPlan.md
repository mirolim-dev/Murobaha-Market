# Murobaha Market API Connection Plan

This document provides a comprehensive guide for integrating various clients (Web, Mobile, Telegram Bot) with the Murobaha Market Django REST API.

---

## Base URL & General Info
- **Local Development**: `http://localhost:8000/api`
- **Production**: `https://api.yourdomain.com/api`
- **Format**: All requests and responses use `application/json`.
- **Date Format**: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).

---

## 1. Authentication (JWT)

The API uses **JSON Web Tokens (JWT)**. Protected endpoints require the `Authorization` header.

### Obtain Token
- **Endpoint**: `POST /token/`
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJhbG...",
    "refresh": "eyJhbG..."
  }
  ```

### Refresh Token
- **Endpoint**: `POST /token/refresh/`
- **Request Body**: `{"refresh": "REFRESH_TOKEN"}`
- **Response**: `{"access": "NEW_ACCESS_TOKEN"}`

### Header Requirement
```http
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 2. User & Account Management

### Retrieve Profile
- **Endpoint**: `GET /v1/account/profile/` (**Protected**)
- **Response**:
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Enthusiastic buyer",
    "location": "Tashkent",
    "birth_date": "1990-01-01",
    "phone_number": "+998901234567"
  }
  ```

### Update Profile
- **Endpoint**: `PATCH /v1/account/profile/` (**Protected**)
- **Request Body**: (Any field listed in GET, except `id` and `email`)
  ```json
  {
    "first_name": "Jonathan",
    "bio": "Updated bio"
  }
  ```
- **Response**: Same as GET (updated).

---

## 3. Products & Catalog

### List Products
- **Endpoint**: `GET /v1/product/`
- **Query Params**:
  - `search`: Filter by name or description (e.g., `?search=iphone`)
  - `category`: Filter by category ID (e.g., `?category=1`)
  - `ordering`: Sort by `price`, `name`, or `created_at` (prefix with `-` for descending, e.g., `?ordering=-price`)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Iphone 15 Pro",
      "price": "999.00",
      "category": 1,
      "category_name": "Electronics",
      "main_image": "https://api.domain.com/media/iphone15.jpg"
    }
  ]
  ```

### List Categories
- **Endpoint**: `GET /v1/product/categories/`
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Electronics",
      "image": "https://api.domain.com/media/cat_elec.png",
      "is_trending": true
    }
  ]
  ```

### Product Details
- **Endpoint**: `GET /v1/product/<id>/`
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Iphone 15 Pro",
    "price": "999.00",
    "category": 1,
    "category_name": "Electronics",
    "main_image": "https://api.domain.com/media/iphone15.jpg",
    "description": "The latest Apple smartphone...",
    "images": [
      "https://api.domain.com/media/iphone15_1.jpg",
      "https://api.domain.com/media/iphone15_2.jpg"
    ],
    "color": "Titanium",
    "reviews": [
      {
        "id": 1,
        "user": "alice",
        "rating": 5,
        "comment": "Amazing phone!",
        "created_at": "2024-01-01T12:00:00Z"
      }
    ],
    "average_rating": 4.8
  }
  ```

### Add Review
- **Endpoint**: `POST /v1/product/<id>/reviews/` (**Protected**)
- **Request Body**:
  ```json
  {
    "rating": 5,
    "comment": "Perfect!"
  }
  ```

---

## 4. Installment Orders

### Create Order Request
- **Endpoint**: `POST /v1/order/` (**Protected**)
- **Note**: This creates an order from the user's current **Cart**.
- **Request Body**:
  ```json
  {
    "down_payment": "200.00",
    "installment_duration_months": 12
  }
  ```
- **Notes**: `installment_duration_months` must be one of: `6, 9, 12, 18, 24`.
- **Response**: Returns the full Order Request object (see Detail below).

### List My Orders
- **Endpoint**: `GET /v1/order/` (**Protected**)
- **Response**:
  ```json
  [
    {
      "id": 10,
      "status": "IN_PROGRESS",
      "total_price": "1200.00",
      "request_sent_time": "2024-01-02T10:00:00Z"
    }
  ]
  ```
- **Status Values**: `IN_PROGRESS`, `ACCEPTED`, `DENIED`, `CANCELLED`.

### Order Detail
- **Endpoint**: `GET /v1/order/<id>/` (**Protected**)
- **Response**:
  ```json
  {
    "id": 10,
    "status": "IN_PROGRESS",
    "total_price": "1200.00",
    "down_payment": "200.00",
    "installment_duration_months": 12,
    "request_sent_time": "2024-01-02T10:00:00Z",
    "admin_notes": null,
    "items": [
      {
        "id": 5,
        "product": { "id": 1, "name": "Iphone 15 Pro", "price": "999.00", ... },
        "quantity": 1,
        "price_at_time": "999.00"
      }
    ],
    "payment_schedules": [
      {
        "id": 1,
        "due_date": "2024-02-02",
        "amount": "83.33",
        "status": "UPCOMING",
        "payment_date": null
      }
    ]
  }
  ```

### View Specific Payment Schedule
- **Endpoint**: `GET /v1/order/payment-schedule/<id>/` (**Protected**)
- **Response**: A single payment schedule object (same as in the list above).

---

## 5. Error Handling

| Status Code | Meaning | Typical Body |
| :--- | :--- | :--- |
| `200/201` | Success | JSON Object/List |
| `400` | Validation Error | `{"field_name": ["Error description"]}` |
| `401` | Unauthorized | `{"detail": "Authentication credentials were not provided."}` |
| `403` | Forbidden | `{"detail": "You do not have permission to perform this action."}` |
| `404` | Not Found | `{"detail": "Not found."}` |
