# API Reference

Complete documentation for the FastAPI backend endpoints.

**Base URL:** `http://localhost:8000`  
**API Documentation:** `http://localhost:8000/docs` (Swagger UI)

---

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Authentication Flow

1. **Register** → `POST /auth/signup` (no auth required)
2. **Login** → `POST /auth/login` (returns JWT token)
3. **Use Token** → Include in `Authorization: Bearer <token>` header
4. **Token Expires** → Re-authenticate via login

---

## Endpoints

### Root Endpoints

#### GET /
Health check for the server.

**Response:**
```json
{
  "message": "FastAPI server is running successfully!"
}
```

#### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "ok"
}
```

---

### Authentication Endpoints

#### POST /auth/signup
Register a new user account.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "message": "User created successfully.",
  "tokens": 10
}
```

**Errors:**
- `500`: Internal server error (e.g., username already exists)

---

#### POST /auth/login
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "username": "string",
  "tokens": 10,
  "is_admin": false
}
```

**Errors:**
- `401`: Invalid username or password

---

#### GET /auth/tokens/{username}
Get token balance for a user. 🔒 Requires authentication.

**Path Parameters:**
- `username`: Username to check

**Response (200):**
```json
{
  "username": "string",
  "tokens": 10
}
```

**Errors:**
- `403`: Not authorized to view other users' tokens
- `404`: User not found

---

#### POST /auth/add_tokens
Add tokens to a user account (simulates purchase). 🔒 Requires authentication.

**Request Body:**
```json
{
  "username": "string",
  "tokens": 50
}
```

**Response (200):**
```json
{
  "message": "Successfully added 50 tokens",
  "new_balance": 60
}
```

**Errors:**
- `400`: Token amount must be positive
- `403`: Not authorized to add tokens to other accounts
- `404`: User not found or update failed

---

#### GET /auth/secure
Protected route example. 🔒 Requires authentication.

**Response (200):**
```json
{
  "message": "Welcome username!",
  "roles": ["user"],
  "issued_at": 1700000000,
  "expires_at": 1700003600
}
```

---

#### GET /auth/ping
Health check for auth router.

**Response (200):**
```json
{
  "message": "auth_router is active"
}
```

---

### Model Endpoints

#### POST /models/train
Train a machine learning model from uploaded CSV file. 🔒 Requires authentication.

**Cost:** 1 token (refunded on failure)

**Request (multipart/form-data):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | CSV file with training data |
| model_name | string | Yes | Name for the trained model |
| feature_columns | string | Yes | Comma-separated feature column names |
| label_column | string | Yes | Target/label column name |
| test_size | float | No | Test set proportion (default: 0.2) |
| model_type | string | No | Model algorithm (default: "linear_regression") |
| evaluation_strategy | string | No | "cv" or "holdout" (default: "cv") |
| cv_folds | int | No | Cross-validation folds (default: 5) |
| cv_repeats | int | No | CV repetitions (default: 1) |
| stratify | bool | No | Stratify split (default: true) |
| primary_metric | string | No | Primary metric for evaluation |

**Supported Model Types:**
- `linear_regression` - Linear Regression (regression)
- `logistic_regression` - Logistic Regression (classification)
- `decision_tree` - Decision Tree Classifier
- `random_forest` - Random Forest Classifier
- `knn` - K-Nearest Neighbors
- `svm` - Support Vector Machine (linear kernel)
- `kernel_svm` - Kernel SVM (RBF kernel)

**Response (200):**
```json
{
  "status": "success",
  "message": "Model 'my_model' trained",
  "metadata": {
    "model_name": "my_model",
    "model_type": "logistic_regression",
    "feature_columns": ["feature1", "feature2"],
    "label_column": "target",
    "metrics": {
      "accuracy_mean": 0.95,
      "f1_weighted_mean": 0.94,
      "precision_weighted_mean": 0.95,
      "recall_weighted_mean": 0.95
    },
    "evaluation": {
      "strategy": "cv",
      "cv_folds": 5
    },
    "preprocessing": {
      "numeric_columns": ["feature1"],
      "categorical_columns": ["feature2"],
      "transformations": {...}
    }
  },
  "tokens_deducted": 1
}
```

**Errors:**
- `400`: Validation error (invalid columns, model type, etc.)
- `402`: Insufficient tokens
- `500`: Training failed

---

#### POST /models/predict
Make a prediction using a trained model. 🔒 Requires authentication.

**Cost:** 5 tokens (refunded on failure)

**Request Body:**
```json
{
  "model_name": "my_model",
  "features": {
    "feature1": 5.1,
    "feature2": "category_a"
  }
}
```

**Response (200) - Classification:**
```json
{
  "prediction": "class_a",
  "probabilities": {
    "class_a": 0.85,
    "class_b": 0.15
  },
  "tokens_deducted": 5
}
```

**Response (200) - Regression:**
```json
{
  "prediction": 42.5,
  "tokens_deducted": 5
}
```

**Errors:**
- `400`: Validation error (missing features, wrong types)
- `402`: Insufficient tokens
- `404`: Model not found
- `500`: Prediction failed

---

#### GET /models
Get list of all trained models. 🔒 Requires authentication.

**Response (200):**
```json
{
  "status": "success",
  "models": [
    {
      "model_name": "my_model",
      "model_type": "logistic_regression",
      "feature_columns": ["feature1", "feature2"],
      "label_column": "target",
      "created_at": "2025-11-27T10:00:00",
      "metrics": {...}
    }
  ],
  "count": 1
}
```

---

#### GET /models/{model_name}
Get details of a specific model. 🔒 Requires authentication.

**Path Parameters:**
- `model_name`: Name of the model

**Response (200):**
```json
{
  "status": "success",
  "model": {
    "model_name": "my_model",
    "model_type": "logistic_regression",
    "feature_columns": ["feature1", "feature2"],
    "label_column": "target",
    "metrics": {...},
    "preprocessing": {...},
    "evaluation": {...},
    "hyperparameters": {...}
  }
}
```

**Errors:**
- `404`: Model not found

---

#### DELETE /models/{model_name}
Delete a trained model. 🔒 Requires authentication.

**Path Parameters:**
- `model_name`: Name of the model to delete

**Response (200):**
```json
{
  "status": "success",
  "message": "Model 'my_model' deleted successfully"
}
```

**Errors:**
- `404`: Model not found

---

### Admin Endpoints

All admin endpoints require the `admin` role in the JWT token.

#### GET /auth/users
Get all users (admin only). 🔒 Requires admin authentication.

**Response (200):**
```json
{
  "users": [
    {
      "user_id": 1,
      "username": "admin",
      "tokens": 100,
      "is_admin": true,
      "created_at": "2025-11-27T10:00:00"
    }
  ]
}
```

**Errors:**
- `403`: Admin access required

---

#### POST /auth/users
Create a new user (admin only). 🔒 Requires admin authentication.

**Request Body:**
```json
{
  "username": "newuser",
  "password": "password123",
  "tokens": 50,
  "is_admin": false
}
```

**Response (200):**
```json
{
  "message": "User 'newuser' created successfully",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "newuser",
  "tokens": 50,
  "is_admin": false
}
```

---

#### PUT /auth/users/{username}
Update user details (admin only). 🔒 Requires admin authentication.

**Path Parameters:**
- `username`: Username to update

**Request Body (all fields optional):**
```json
{
  "new_username": "updated_name",
  "new_password": "new_password",
  "new_tokens": 100,
  "new_is_admin": true
}
```

**Response (200):**
```json
{
  "message": "User 'username' updated successfully"
}
```

---

#### DELETE /auth/users/{username}
Delete a user (admin only). 🔒 Requires admin authentication.

**Path Parameters:**
- `username`: Username to delete

**Response (200):**
```json
{
  "message": "User 'username' deleted successfully"
}
```

**Errors:**
- `400`: Cannot delete your own account
- `404`: User not found

---

#### GET /auth/usage_logs
Get usage logs. 🔒 Requires authentication.

**Query Parameters:**
- `username` (optional): Filter by username (admin can see all)
- `limit` (optional): Maximum logs to return (default: 50)

**Response (200):**
```json
{
  "logs": [
    {
      "log_id": 1,
      "username": "user1",
      "action": "MODEL_TRAINING",
      "tokens_changed": -1,
      "status": "SUCCESS",
      "timestamp": "2025-11-27T10:00:00",
      "details": "Trained logistic_regression model 'my_model'"
    }
  ],
  "count": 1
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input or validation error |
| 401 | Unauthorized - Invalid or missing authentication |
| 402 | Payment Required - Insufficient tokens |
| 403 | Forbidden - Not authorized for this action |
| 404 | Not Found - Resource does not exist |
| 422 | Unprocessable Entity - Request validation failed |
| 500 | Internal Server Error - Server-side error |

---

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider adding:
- Request rate limits per user
- Concurrent training limits
- Daily token usage caps

---

*Last Updated: 2025-11-27*
