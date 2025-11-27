# Streamlit Pages Documentation

Detailed documentation for each page in the Streamlit frontend application.

---

## Overview

The Streamlit frontend provides an intuitive interface for:
- User authentication (login/signup)
- Model training and prediction
- Token management and purchase
- System administration (admin users only)

**Main Application:** `app_streamlit/app_streamlit.py`  
**Default Port:** 8501

---

## Application Structure

```
app_streamlit/
├── app_streamlit.py          # Main entry point with auth flow
├── components/
│   ├── api_client.py         # HTTP client for FastAPI backend
│   └── utils.py              # Utility functions
└── pages/
    ├── dashboard/
    │   ├── dashboard.py      # Main dashboard view
    │   └── purchase_form.py  # Token purchase component
    ├── train_page/
    │   ├── train_page.py     # Model training interface
    │   └── metrics_display.py # Metrics visualization
    ├── admin_page/
    │   ├── admin_page.py     # Admin panel entry point
    │   ├── user_management.py # User CRUD operations
    │   └── admin_analytics.py # Charts and statistics
    └── predict_page.py       # Prediction interface
```

---

## Authentication Flow

### Login Page
**Location:** `app_streamlit.py` → `login_page()`

**Purpose:** User authentication and registration.

**Features:**
- Server status indicator (online/offline)
- Login form with username/password
- Signup form for new users
- Connection troubleshooting instructions

**Session State:**
- `logged_in`: Boolean login status
- `username`: Current user's username
- `tokens`: Token balance
- `is_admin`: Admin privilege flag
- `access_token`: JWT for API calls

**User Flow:**
1. Check server connection status
2. Enter credentials in Login tab
3. OR create account in Signup tab
4. On success → redirect to Dashboard

---

## Dashboard Page

**Location:** `pages/dashboard/dashboard.py`

### Purpose
Central hub showing user statistics, models, and activity history.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Dashboard                                                  │
├─────────────────────────────────────────────────────────────┤
│  Token Balance                                              │
│  ┌─────────────┬─────────────────┬─────────────────────┐    │
│  │ Available   │ Training Cost   │ Prediction Cost     │    │
│  │ 45 tokens   │ 1 token/model   │ 5 tokens/request    │    │
│  └─────────────┴─────────────────┴─────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  💳 Purchase Tokens                                         │
│  [Credit card form - simulated payment]                     │
├─────────────────────────────────────────────────────────────┤
│  Your Models                                                │
│  ├── model_name_1 [expandable details]                      │
│  ├── model_name_2 [expandable details]                      │
│  └── model_name_3 [expandable details]                      │
├─────────────────────────────────────────────────────────────┤
│  Recent Activity                                            │
│  [Table: Timestamp | Action | Tokens | Status | Details]    │
├─────────────────────────────────────────────────────────────┤
│  Quick Stats                                                │
│  ┌─────────────┬─────────────────┬─────────────────────┐    │
│  │ Models      │ Predictions     │ Tokens Spent        │    │
│  │ Trained: 3  │ Made: 15        │ 78 tokens           │    │
│  └─────────────┴─────────────────┴─────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Components

#### Token Balance Section
- Displays current token balance
- Shows cost information
- Real-time updates after operations

#### Purchase Form (`purchase_form.py`)
- Simulated credit card payment
- Token package selection
- Card validation (demo only - no real charges)

#### Models Section
- Lists all trained models
- Expandable cards with:
  - Model type and configuration
  - Feature/label columns
  - Performance metrics
  - Training timestamp

#### Activity Section
- Recent usage logs (last 20 entries)
- Filterable by action type
- Timestamps in local format

#### Quick Stats
- Total models trained
- Predictions made
- Tokens spent

### Backend Integration
| Component | API Endpoint |
|-----------|--------------|
| Token Balance | `GET /auth/tokens/{username}` |
| Purchase | `POST /auth/add_tokens` |
| Models List | `GET /models` |
| Activity Logs | `GET /auth/usage_logs` |

---

## Train Page

**Location:** `pages/train_page/train_page.py`

### Purpose
Upload CSV data and train machine learning models.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Train Model                                                │
│  ℹ️ Training a model costs 1 token                          │
├─────────────────────────────────────────────────────────────┤
│  📁 Upload CSV file                                         │
│  [Drag and drop or browse]                                  │
├─────────────────────────────────────────────────────────────┤
│  Data Preview                                               │
│  [First 10 rows displayed]                                  │
│  Shape: 1000 rows x 5 columns                               │
├─────────────────────────────────────────────────────────────┤
│  Configuration                                              │
│  ┌──────────────────────┬──────────────────────┐            │
│  │ Feature Columns (X)  │ Label Column (y)     │            │
│  │ [Multi-select]       │ [Single select]      │            │
│  └──────────────────────┴──────────────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  Model Configuration                                        │
│  Model Type: [Dropdown - 7 options]                         │
│  ┌──────────────────────┬──────────────────────┐            │
│  │ Model Name           │ Test Set Size        │            │
│  │ [model_20251127...]  │ [Slider 10-50%]      │            │
│  └──────────────────────┴──────────────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  [🚀 Train Model]                                           │
├─────────────────────────────────────────────────────────────┤
│  Model Performance (after training)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Classification: Accuracy, Precision, Recall, F1      │   │
│  │ OR                                                    │   │
│  │ Regression: R², RMSE, MAE                             │   │
│  └──────────────────────────────────────────────────────┘   │
│  [Debug: Raw Metrics] [Preprocessing Details]               │
└─────────────────────────────────────────────────────────────┘
```

### Supported Model Types

| Model | Type | Use Case |
|-------|------|----------|
| Linear Regression | Regression | Continuous numeric targets |
| Logistic Regression | Classification | Binary/multi-class categories |
| Decision Tree | Classification | Interpretable classification |
| Random Forest | Classification | Ensemble method |
| K-Nearest Neighbors | Classification | Instance-based learning |
| SVM (Linear) | Classification | Linear decision boundary |
| Kernel SVM (RBF) | Classification | Non-linear decision boundary |

### Metrics Display (`metrics_display.py`)

**Classification Metrics:**
- Accuracy (overall correctness)
- Precision (positive predictive value)
- Recall (sensitivity)
- F1 Score (harmonic mean)
- Confusion Matrix (optional)

**Regression Metrics:**
- R² Score (coefficient of determination)
- RMSE (root mean squared error)
- MAE (mean absolute error)

### Backend Integration
| Action | API Endpoint |
|--------|--------------|
| Train Model | `POST /models/train` |
| Get Token Balance | `GET /auth/tokens/{username}` |

---

## Predict Page

**Location:** `pages/predict_page.py`

### Purpose
Make predictions using trained models.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Make Predictions                                           │
│  ℹ️ Making a prediction costs 5 tokens                      │
├─────────────────────────────────────────────────────────────┤
│  Select Model: [Dropdown with trained models]               │
├─────────────────────────────────────────────────────────────┤
│  Model Information                                          │
│  Type: Logistic Regression                                  │
│  Features: feature1, feature2, feature3                     │
│  Label: target                                              │
├─────────────────────────────────────────────────────────────┤
│  Enter Feature Values                                       │
│  ┌──────────────────────┐                                   │
│  │ feature1: [input]    │                                   │
│  │ feature2: [input]    │                                   │
│  │ feature3: [input]    │                                   │
│  └──────────────────────┘                                   │
│  OR                                                         │
│  [📋 Import from JSON]                                      │
├─────────────────────────────────────────────────────────────┤
│  [🔮 Predict]                                               │
├─────────────────────────────────────────────────────────────┤
│  Prediction Result                                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Predicted: class_a                                    │   │
│  │ Probabilities:                                        │   │
│  │   class_a: 85%  ████████████████████                 │   │
│  │   class_b: 15%  ████                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Features
- Dynamic model selection
- Auto-generated input fields based on model features
- JSON import for batch features
- Probability visualization for classification

### Backend Integration
| Action | API Endpoint |
|--------|--------------|
| List Models | `GET /models` |
| Model Details | `GET /models/{model_name}` |
| Make Prediction | `POST /models/predict` |

---

## Admin Page

**Location:** `pages/admin_page/admin_page.py`

### Purpose
System administration for users with admin privileges.

### Access Control
- Only visible to users with `is_admin: true`
- Access denied message for non-admin users

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Admin Panel                                                │
│  Comprehensive user management and system administration    │
├─────────────────────────────────────────────────────────────┤
│  User Management                                            │
│  Action: [View Users ▼]                                     │
│  ───────────────────────                                    │
│  [Content based on selected action]                         │
├─────────────────────────────────────────────────────────────┤
│  Token Distribution                                         │
│  [Bar chart of user token balances]                         │
│  Statistics: Total, Average, Median, Max, Min               │
├─────────────────────────────────────────────────────────────┤
│  System Activity Log                                        │
│  [Filterable activity table]                                │
│  Filters: Action type, Status                               │
├─────────────────────────────────────────────────────────────┤
│  Trained Models                                             │
│  [Model list with delete buttons]                           │
└─────────────────────────────────────────────────────────────┘
```

### User Management Actions

#### View Users (`user_management.py`)
- Sortable user table
- Filter by username, admin status
- Token balance overview

#### Create User
- Username and password fields
- Initial token balance
- Admin privilege toggle
- Generated JWT token displayed

#### Update User
- Select user from dropdown
- Modify any field (all optional)
- Password change option

#### Delete Users
- Checkbox selection
- Bulk delete support
- Self-deletion prevention
- Confirmation required

### Analytics (`admin_analytics.py`)

#### Token Distribution
- Bar chart visualization
- Statistical summary
- Export capability

#### Usage Logs
- Full system activity
- Filter by action type
- Success/failure breakdown

#### Model Management
- All trained models
- Delete functionality
- Usage statistics

### Backend Integration
| Action | API Endpoint |
|--------|--------------|
| List Users | `GET /auth/users` |
| Create User | `POST /auth/users` |
| Update User | `PUT /auth/users/{username}` |
| Delete User | `DELETE /auth/users/{username}` |
| Usage Logs | `GET /auth/usage_logs` |
| List Models | `GET /models` |
| Delete Model | `DELETE /models/{model_name}` |

---

## Session State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `logged_in` | bool | User authentication status |
| `username` | str | Current user's username |
| `tokens` | int | Current token balance |
| `is_admin` | bool | Admin privilege flag |
| `access_token` | str | JWT for API authentication |
| `page` | str | Current page selection |

---

## Error Handling

### Connection Errors
- Server status indicator
- Retry mechanism
- Detailed error messages

### API Errors
- Token deduction failures
- Validation errors
- Server errors with user-friendly messages

### Authentication Errors
- Automatic logout on token expiry
- Session clear on auth failure

---

*Last Updated: 2025-11-27*
