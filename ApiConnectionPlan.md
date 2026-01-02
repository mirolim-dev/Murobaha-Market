# Murobaha Market API Connection Plan

This document provides a general guide for integrating various clients (Web, Mobile, Telegram Bot) with the Murobaha Market Django REST API.

## Base URL
- **Local Development**: `http://localhost:8000/api`
- **Production**: `https://api.yourdomain.com/api`

---

## 1. Authentication (JWT)

The API uses **JSON Web Tokens (JWT)** for secure communication. Clients must obtain tokens by logging in and include the Access Token in the headers of all protected requests.

### Authentication Endpoints
- **Obtain Token**: `POST /token/`
  - Body: `{"username": "your_username", "password": "your_password"}`
  - Returns: `{"access": "ACCESS_TOKEN", "refresh": "REFRESH_TOKEN"}`
- **Refresh Token**: `POST /token/refresh/`
  - Body: `{"refresh": "REFRESH_TOKEN"}`
  - Returns: A new `access` token.

### Header Requirement
For all protected endpoints, include the following header:
```http
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 2. Core API Endpoints

### User & Account
- `GET /v1/account/profile/` (Protected): Retrieve the authenticated user's profile details.
- `PATCH /v1/account/profile/` (Protected): Update profile information.

### Products & Catalog
- `GET /v1/product/`: List all available products.
- `GET /v1/product/categories/`: List all product categories.
- `GET /v1/product/<id>/`: Retrieve details for a specific product.
- `POST /v1/product/<id>/reviews/` (Protected): Add a review to a product.

### Installment Orders
- `GET /v1/order/` (Protected): List the user's order requests and their statuses.
- `POST /v1/order/` (Protected): Create a new installment order request.
- `GET /v1/order/<id>/` (Protected): Detailed view of a specific order.
- `GET /v1/order/payment-schedule/<id>/` (Protected): View the payment schedule for an approved order.

---

## 3. Client Implementation Tips

### Web (e.g., Next.js, React)
- **Token Storage**: Store the `refresh` token in an `HttpOnly` cookie for security and the `access` token in memory/state.
- **Interceptors**: Use Axios interceptors to automatically attach the `Authorization` header and handle 401 (Unauthorized) errors by attempting a token refresh.

### Mobile (e.g., Flutter, React Native)
- **Secure Storage**: Use `flutter_secure_storage` or `react-native-encrypted-storage` to save tokens.
- **Offline Cache**: Cache product lists locally for better performance in low-connectivity areas.

### Telegram Bot (e.g., Python-Telegram-Bot, Aiogram)
- **User Linking**: Map the Telegram `user_id` to the Django `User` (requires a custom linking endpoint or storing the Telegram ID in the User Profile).
- **Session Management**: Handle the JWT flow within your bot's middleware to ensure tokens are refreshed before they expire.

---

## 4. Error Handling

The API returns standard HTTP status codes:
- `200 OK`: Success (GET/PATCH).
- `201 Created`: Success (POST).
- `400 Bad Request`: Input validation errors.
- `401 Unauthorized`: Missing or invalid token.
- `403 Forbidden`: Authenticated but lack permission.
- `404 Not Found`: Resource does not exist.
