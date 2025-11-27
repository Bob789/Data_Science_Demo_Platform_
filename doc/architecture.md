# Project Architecture - Final_Project_v003

## Overview
This is a **Machine Learning Model Training and Prediction Platform** that combines:
- **Streamlit** frontend for user interaction
- **FastAPI** backend for model training, prediction, and authentication
- **Multiple ML Models** (Classification & Regression)
- **JWT Token-based Authentication**
- **PostgreSQL Database** for user management and token tracking

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                          │
│                     (Streamlit - Port 8501)                      │
├─────────────────────────────────────────────────────────────────┤
│  • Dashboard Page                                                │
│  • Train Model Page                                              │
│  • Predict Page                                                  │
│  • Admin Page                                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│                    (FastAPI - Port 8000)                         │
├─────────────────────────────────────────────────────────────────┤
│  Routers:                                                        │
│  • /auth - Authentication & Token Management                     │
│  • /models - Model Training & Prediction                         │
└────┬───────────────────┬──────────────────┬────────────────────┘
     │                   │                  │
     │                   │                  │
     ▼                   ▼                  ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────────┐
│   AUTH      │  │   MODEL      │  │    LOGGING       │
│  SERVICES   │  │  SERVICES    │  │    SERVICE       │
├─────────────┤  ├──────────────┤  ├──────────────────┤
│• JWT        │  │• Training    │  │• Request logs    │
│• Token      │  │• Prediction  │  │• Error logs      │
│• User       │  │• Validation  │  │• Model logs      │
└──────┬──────┘  └───────┬──────┘  └──────────────────┘
       │                 │
       │                 │
       ▼                 ▼
┌─────────────┐  ┌──────────────────────────────────┐
│  DATABASE   │  │        CORE ML ENGINE            │
│ (PostgreSQL)│  ├──────────────────────────────────┤
├─────────────┤  │ • Data Handler (CSV)             │
│• users      │  │ • Preprocessing Pipeline         │
│• usage_logs │  │ • Model Manager (Save/Load)      │
└─────────────┘  │ • Evaluation (Metrics)           │
                 └─────────┬────────────────────────┘
                           │
                           ▼
                 ┌──────────────────────────────────┐
                 │         MODEL LAYER              │
                 ├──────────────────────────────────┤
                 │ Classification Models:           │
                 │ • Logistic Regression            │
                 │ • Decision Tree                  │
                 │ • Random Forest                  │
                 │ • K-Nearest Neighbors            │
                 │ • Support Vector Machine (SVM)   │
                 │ • Kernel SVM (RBF)              │
                 │                                  │
                 │ Regression Models:               │
                 │ • Linear Regression              │
                 └─────────┬────────────────────────┘
                           │
                           ▼
                 ┌──────────────────────────────────┐
                 │       FILE STORAGE               │
                 ├──────────────────────────────────┤
                 │ • app_fastapi/models/trained/    │
                 │   └── [model_name].pkl           │
                 │ • app_fastapi/models/metadata/   │
                 │   └── [model_name]_metadata.json │
                 │ • app_fastapi/logs/              │
                 │   └── app.log                    │
                 └──────────────────────────────────┘
```

---

## Component Responsibilities

### 1. **Streamlit Frontend (app_streamlit/)**
**Purpose:** User interface for interacting with the ML platform

**Responsibilities:**
- Display model training interface with parameter selection
- Show model prediction interface with input fields
- Visualize training metrics and results
- Handle user authentication flow
- Manage admin panel for user management

**Key Components:**
- `app_streamlit.py` - Main application entry point
- `pages/train_page.py` - Model training interface
- `pages/predict_page.py` - Model prediction interface
- `pages/dashboard.py` - Overview of trained models
- `pages/admin_page.py` - User management
- `components/api_client.py` - HTTP client for FastAPI backend

**Communication:** Makes REST API calls to FastAPI backend (port 8000)

---

### 2. **FastAPI Backend (app_fastapi/)**
**Purpose:** Core API server handling all business logic

**Responsibilities:**
- Authenticate users and manage JWT tokens
- Process model training requests
- Handle prediction requests
- Validate input data
- Log all operations
- Manage model lifecycle

**Key Files:**
- `app_fastapi.py` - Main FastAPI application
- `database_manager.py` - Database operations

#### 2.1 **Routers (app_fastapi/routers/)**
**Purpose:** API endpoint definitions

- `auth_router.py` - Authentication endpoints (`/auth/*`)
  - `/auth/login` - User login
  - `/auth/ping` - Token validation
  - `/auth/tokens` - List user tokens

- `models_router.py` - Model management endpoints (`/models/*`)
  - `/models/train` - Train new model
  - `/models/predict/{model_name}` - Make predictions
  - `/models/` - List all models
  - `/models/{model_name}` - Get model details
  - `/models/{model_name}` - Delete model

#### 2.2 **Services (app_fastapi/services/)**
**Purpose:** Business logic implementation

- `jwt_handler.py` - JWT token creation and validation
- `auth_dependency.py` - Authentication middleware
- `user_service.py` - User CRUD operations
- `token_service.py` - Token management
- `model_service.py` - Model training and prediction orchestration
- `logger_service.py` - Centralized logging

#### 2.3 **Core ML Engine (app_fastapi/core/)**
**Purpose:** Machine learning core functionality

- `data_handler.py` - CSV loading and validation
- `preprocessing.py` - Feature engineering and data transformation
- `evaluation.py` - Model evaluation metrics (accuracy, RMSE, etc.)
- `model_manager.py` - Model persistence (save/load)

#### 2.4 **Model Layer (app_fastapi/services/models/)**
**Purpose:** ML model implementations

- `base_model.py` - Universal training/prediction template
- `config.py` - Model configurations and parameters
- Individual model files:
  - `linear_regression.py`
  - `logistic_regression.py`
  - `decision_tree.py`
  - `random_forest.py`
  - `knn.py`
  - `svm.py`
  - `kernel_svm.py`

---

### 3. **Database Layer**
**Purpose:** Persistent data storage

**Technology:** PostgreSQL (via `database_manager.py`)

**Tables:**
- `users` - User accounts (username, hashed password, tokens, admin status, created_at)
- `usage_logs` - Activity tracking (action, tokens_changed, status, timestamp, details)

**Operations:**
- User authentication
- Token balance management
- Usage logging
- User management (admin only)

---

### 4. **Token System (JWT)**
**Purpose:** Secure, stateless authentication

**Flow:**
1. User logs in with username/password
2. Server validates credentials against database
3. Server generates JWT token with expiration
4. Token stored in database and returned to client
5. Client includes token in all subsequent requests
6. Server validates token before processing requests
7. Token can be revoked by admin or expires automatically

**Security Features:**
- Passwords hashed with bcrypt
- Tokens expire after configured time
- Tokens can be revoked
- Role-based access control (admin/user)

---

### 5. **Logging System**
**Purpose:** Track all system operations

**Log Files:** `app_fastapi/logs/app.log`

**Logged Events:**
- API requests (timestamp, endpoint, user)
- Authentication attempts (success/failure)
- Model training start/completion
- Predictions made
- Errors and exceptions
- Token operations

**Log Format:**
```
[TIMESTAMP] [LEVEL] [MODULE] - Message
```

---

## Data Flow Diagrams

### Training Flow
```
User (Streamlit)
    │
    │ 1. Upload CSV + Select features
    │
    ▼
FastAPI /models/train
    │
    │ 2. Validate JWT token
    │
    ▼
Model Service
    │
    ├─→ 3. Load & validate CSV (data_handler)
    │
    ├─→ 4. Preprocess data (preprocessing)
    │       │
    │       ├─ Handle missing values
    │       ├─ Encode categorical features
    │       └─ Scale numerical features
    │
    ├─→ 5. Train model (base_model)
    │       │
    │       ├─ Create sklearn Pipeline
    │       ├─ Fit model on data
    │       └─ Evaluate with CV/Holdout
    │
    ├─→ 6. Save model (model_manager)
    │       │
    │       ├─ Serialize pipeline → .pkl
    │       └─ Save metadata → .json
    │
    └─→ 7. Return metrics to user
```

### Prediction Flow
```
User (Streamlit)
    │
    │ 1. Select model + Input features
    │
    ▼
FastAPI /models/predict/{model_name}
    │
    │ 2. Validate JWT token
    │
    ▼
Model Service
    │
    ├─→ 3. Load model (model_manager)
    │       │
    │       ├─ Load pipeline from .pkl
    │       └─ Load metadata from .json
    │
    ├─→ 4. Preprocess input
    │       │
    │       └─ Apply same transformations as training
    │
    ├─→ 5. Make prediction
    │       │
    │       ├─ pipeline.predict()
    │       └─ pipeline.predict_proba() (if supported)
    │
    └─→ 6. Return prediction to user
            │
            ├─ Predicted value
            └─ Probabilities (classification)
```

### Authentication Flow
```
User (Streamlit)
    │
    │ 1. Enter username/password
    │
    ▼
FastAPI /auth/login
    │
    ├─→ 2. Query user from database
    │
    ├─→ 3. Verify password (bcrypt)
    │
    ├─→ 4. Generate JWT token
    │
    ├─→ 5. Store token in database
    │
    └─→ 6. Return token to client
            │
            ▼
Client stores token
    │
    │ For each API request:
    │
    ├─→ Include token in Authorization header
    │
    ▼
FastAPI middleware
    │
    ├─→ Validate token signature
    │
    ├─→ Check token not expired
    │
    ├─→ Verify token exists in database
    │
    └─→ Allow/Deny request
```

---

## Technology Stack

### Backend
- **Framework:** FastAPI 0.100+
- **ML Library:** scikit-learn
- **Data Processing:** pandas, numpy
- **Authentication:** PyJWT
- **Password Hashing:** passlib (bcrypt)
- **Database:** PostgreSQL (psycopg2)
- **Server:** Uvicorn (ASGI)

### Frontend
- **Framework:** Streamlit
- **HTTP Client:** requests
- **Data Visualization:** Built-in Streamlit components

### Testing
- **Framework:** pytest
- **HTTP Testing:** httpx (TestClient)

---

## Security Features

1. **Authentication**
   - JWT-based stateless authentication
   - Secure password hashing (bcrypt)
   - Token expiration

2. **Authorization**
   - Role-based access control (admin/user)
   - Protected endpoints require valid tokens

3. **Data Validation**
   - Input validation on all endpoints
   - Type checking with Pydantic models
   - File upload validation

4. **Logging**
   - All operations logged
   - Failed authentication attempts tracked
   - Error tracking for debugging

---

## File Storage Structure

```
Final_Project_v003/
├── app_fastapi/
│   ├── models/
│   │   ├── trained/           # Serialized model pipelines (.pkl)
│   │   └── metadata/          # Model metadata (.json)
│   ├── logs/                  # Application logs
│   └── data/
│       └── uploads/           # Temporary CSV uploads (if needed)
├── app_streamlit/             # Frontend application
├── tests/                     # Unit and integration tests
└── doc/                       # Documentation (this file)
```

---

## Deployment

### Development
```bash
# Terminal 1: Start FastAPI backend
cd app_fastapi
uvicorn app_fastapi:app --reload --port 8000

# Terminal 2: Start Streamlit frontend
cd app_streamlit
streamlit run app_streamlit.py --server.port 8501
```

### Production Considerations
- Use environment variables for secrets
- Enable HTTPS/TLS
- Set up proper CORS policies
- Use production WSGI server (Gunicorn)
- Implement rate limiting
- Add request/response logging
- Set up monitoring and alerting

---

## Extension Points

The architecture supports easy extension:

1. **New ML Models:** Add to `app_fastapi/services/models/` and register in `config.py`
2. **New Endpoints:** Add routers in `app_fastapi/routers/`
3. **New Frontend Pages:** Add to `app_streamlit/pages/`
4. **New Preprocessing:** Extend `preprocessing.py`
5. **New Metrics:** Extend `evaluation.py`

---

## Performance Considerations

- **Model Training:** Runs synchronously (consider async for production)
- **Model Storage:** File-based (consider model registry for scale)
- **Database:** PostgreSQL (production-ready)
- **Caching:** No caching implemented (consider Redis)
- **Concurrency:** Limited by synchronous operations

---

## Related Documentation

- [API Reference](api_reference.md) - Complete endpoint documentation
- [Database Schema](database_schema.md) - Tables and relationships
- [Streamlit Pages](streamlit_pages.md) - Detailed UI documentation
- [Deployment Guide](deployment.md) - Production deployment instructions

---

*Last Updated: 2025-11-27*
