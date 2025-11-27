# Comprehensive Functions Overview

This document provides detailed documentation for **every function** in the Data Science Demo Platform project. Each function includes its name, location, purpose, parameters, return type, logic explanation, and primary use cases.

---

## Table of Contents

1. [FastAPI Core Functions](#1-fastapi-core-functions)
   - [Data Handler](#11-data-handler)
   - [Preprocessing](#12-preprocessing)
   - [Evaluation](#13-evaluation)
   - [Model Manager](#14-model-manager)
2. [Model Functions](#2-model-functions)
   - [Base Model](#21-base-model)
   - [Config](#22-config)
   - [Evaluation Module](#23-evaluation-module-_evaluationpy)
   - [Model Registry](#24-model-registry)
3. [Service Functions](#3-service-functions)
   - [Model Service](#31-model-service)
   - [User Service](#32-user-service)
   - [JWT Handler](#33-jwt-handler)
   - [Auth Dependency](#34-auth-dependency)
   - [Token Service](#35-token-service)
   - [Logger Service](#36-logger-service)
4. [Router Endpoint Functions](#4-router-endpoint-functions)
   - [Auth Router](#41-auth-router)
   - [Models Router](#42-models-router)
5. [Database Functions](#5-database-functions)
6. [FastAPI Application Functions](#6-fastapi-application-functions)
7. [Streamlit Functions](#7-streamlit-functions)
   - [Main App](#71-main-app-app_streamlitpy)
   - [API Client](#72-api-client)
   - [Dashboard Page](#73-dashboard-page)
   - [Train Page](#74-train-page)
   - [Predict Page](#75-predict-page)
   - [Admin Page](#76-admin-page)
   - [Utils](#77-utils)
8. [Test Functions](#8-test-functions)
   - [Test API Endpoints](#81-test-api-endpoints)
   - [Test Model Service](#82-test-model-service)
   - [Conftest](#83-conftest)
9. [Utility Scripts](#9-utility-scripts)
   - [Setup Admin](#91-setup-admin)
   - [Run Server](#92-run-server)

---

## 1. FastAPI Core Functions

### 1.1 Data Handler

**File:** `app_fastapi/core/data_handler.py`

#### `load_and_validate_csv()`

- **Purpose:** Loads a CSV file and validates that specified columns exist
- **Parameters:**
  - `file_path` (str): Path to the CSV file
  - `feature_columns` (List[str]): List of feature column names
  - `label_column` (str): Name of the label column
- **Returns:** Tuple[pd.DataFrame, pd.DataFrame, pd.Series] - (full DataFrame, features X, labels y)
- **Logic:** Reads CSV using pandas, checks for missing columns, extracts feature and label columns, and returns them separately
- **Use Cases:** Called at the start of model training to load and validate user-uploaded CSV data

#### `get_column_types()`

- **Purpose:** Divides columns into numeric and categorical types
- **Parameters:**
  - `df` (pd.DataFrame): Original DataFrame
  - `feature_columns` (List[str]): List of feature column names
- **Returns:** Tuple[List[str], List[str]] - (numeric columns, categorical columns)
- **Logic:** Iterates through feature columns and uses pandas dtype detection to classify each as numeric or categorical
- **Use Cases:** Used by preprocessing module to determine which transformations to apply to each column type

---

### 1.2 Preprocessing

**File:** `app_fastapi/core/preprocessing.py`

#### `create_preprocessor()`

- **Purpose:** Creates a complete scikit-learn preprocessing pipeline
- **Parameters:**
  - `df` (pd.DataFrame): Original DataFrame
  - `feature_columns` (List[str]): List of features to process
  - `scale_features` (bool): Whether to apply StandardScaler (default: True)
- **Returns:** ColumnTransformer - Preprocessing pipeline object
- **Logic:** Identifies numeric and categorical columns, creates separate pipelines for each (imputation + optional scaling for numeric; imputation + one-hot encoding for categorical), combines them into a ColumnTransformer
- **Use Cases:** Called during model training to create preprocessing steps that are bundled into the final model pipeline, preventing data leakage

#### `get_preprocessing_metadata()`

- **Purpose:** Returns information about preprocessing transformations applied
- **Parameters:**
  - `df` (pd.DataFrame): Original DataFrame
  - `feature_columns` (List[str]): List of features
  - `scale_features` (bool): Whether scaling was applied (default: True)
- **Returns:** dict - Metadata dictionary with preprocessing details
- **Logic:** Extracts column types and documents which transformers were applied to each type, formatted as a dictionary
- **Use Cases:** Called after training to store preprocessing information in model metadata for transparency and debugging

---

### 1.3 Evaluation

**File:** `app_fastapi/core/evaluation.py`

#### `supports_proba()`

- **Purpose:** Checks if a model supports probability predictions
- **Parameters:**
  - `estimator` - Model or pipeline object
- **Returns:** bool - True if model has `predict_proba` method
- **Logic:** Extracts final estimator from pipeline if needed, checks for `predict_proba` attribute using hasattr
- **Use Cases:** Used before attempting to calculate metrics that require probabilities (log loss, ROC AUC)

#### `evaluate_classification_holdout()`

- **Purpose:** Evaluates classification model using train/test split
- **Parameters:**
  - `estimator` - Model/pipeline to evaluate
  - `X` - Features
  - `y` - Labels
  - `test_size` (float): Test set proportion (default: 0.2)
  - `random_state` (int): Random seed (default: 42)
  - `stratify` (bool): Whether to stratify split (default: True)
- **Returns:** Dict[str, Any] - Dictionary of metrics
- **Logic:** Splits data, trains model on training set, predicts on both sets, calculates metrics (accuracy, precision, recall, F1, confusion matrix), adds advanced metrics if probability predictions available, computes baseline
- **Use Cases:** Main evaluation function for classification models when using holdout validation strategy

#### `evaluate_classification_cv()`

- **Purpose:** Evaluates classification model using cross-validation
- **Parameters:**
  - `estimator` - Model/pipeline to evaluate
  - `X` - Features
  - `y` - Labels
  - `n_splits` (int): Number of CV folds (default: 5)
  - `n_repeats` (int): Number of repetitions (default: 1)
  - `random_state` (int): Random seed (default: 42)
- **Returns:** Dict[str, Any] - Dictionary of metrics with means and stds
- **Logic:** Creates RepeatedStratifiedKFold CV object, runs cross_validate with multiple scorers, calculates mean and std for each metric, handles negative metrics by flipping signs, computes baseline
- **Use Cases:** Main evaluation function for classification models when using cross-validation strategy

#### `evaluate_regression_holdout()`

- **Purpose:** Evaluates regression model using train/test split
- **Parameters:**
  - `estimator` - Model/pipeline to evaluate
  - `X` - Features
  - `y` - Labels
  - `test_size` (float): Test set proportion (default: 0.2)
  - `random_state` (int): Random seed (default: 42)
- **Returns:** Dict[str, Any] - Dictionary of metrics
- **Logic:** Splits data, trains model, predicts on both sets, calculates R², RMSE, MAE on train and test sets, computes baseline RMSE
- **Use Cases:** Main evaluation function for regression models when using holdout validation strategy

#### `evaluate_regression_cv()`

- **Purpose:** Evaluates regression model using cross-validation
- **Parameters:**
  - `estimator` - Model/pipeline to evaluate
  - `X` - Features
  - `y` - Labels
  - `n_splits` (int): Number of CV folds (default: 5)
  - `n_repeats` (int): Number of repetitions (default: 1)
  - `random_state` (int): Random seed (default: 42)
- **Returns:** Dict[str, Any] - Dictionary of metrics with means and stds
- **Logic:** Creates RepeatedKFold CV object, runs cross_validate with R², RMSE, MAE scorers, calculates mean and std for each metric, flips negative metric signs, computes baseline
- **Use Cases:** Main evaluation function for regression models when using cross-validation strategy

#### `format_metrics_summary()`

- **Purpose:** Creates a human-readable summary of metrics
- **Parameters:**
  - `metrics` (Dict[str, Any]): Metrics dictionary
  - `model_type` (str): Type of model
  - `eval_strategy` (str): Evaluation strategy used
- **Returns:** str - Formatted summary string
- **Logic:** Determines if model is classification or regression, selects appropriate metrics based on strategy (CV or holdout), formats as readable string with percentages/decimals
- **Use Cases:** Called to generate user-friendly metric summaries displayed in API responses and UI

---

### 1.4 Model Manager

**File:** `app_fastapi/core/model_manager.py`

#### `save_model()`

- **Purpose:** Saves trained model and metadata to disk
- **Parameters:**
  - `model_name` (str): Name for the model
  - `estimator` - Trained pipeline/model object
  - `metadata` (Dict): Model metadata
- **Returns:** None
- **Logic:** Uses joblib to serialize model to pkl file, adds timestamp and file reference to metadata, saves metadata as JSON file
- **Use Cases:** Called after successful model training to persist model for later use

#### `load_model()`

- **Purpose:** Loads a trained model from disk
- **Parameters:**
  - `model_name` (str): Name of model to load
- **Returns:** Loaded model/pipeline object
- **Logic:** Constructs file path, checks existence, uses joblib to deserialize pkl file, raises FileNotFoundError if not found
- **Use Cases:** Called when making predictions to load the trained model

#### `load_metadata()`

- **Purpose:** Loads model metadata from JSON file
- **Parameters:**
  - `model_name` (str): Name of model
- **Returns:** Dict - Model metadata
- **Logic:** Constructs metadata file path, reads JSON file, returns parsed dictionary, returns minimal dict if file doesn't exist
- **Use Cases:** Called to retrieve model information for display or prediction

#### `list_all_models()`

- **Purpose:** Returns list of all saved models with metadata
- **Parameters:** None
- **Returns:** List[Dict] - List of model metadata dictionaries
- **Logic:** Scans models directory for pkl files, loads metadata for each, handles errors gracefully, returns list of metadata dicts
- **Use Cases:** Called by API endpoint to display available models to users

#### `delete_model()`

- **Purpose:** Deletes model and its metadata files
- **Parameters:**
  - `model_name` (str): Name of model to delete
- **Returns:** Dict - Success message
- **Logic:** Constructs file paths, checks existence, removes pkl and json files, raises error if model not found
- **Use Cases:** Called by delete endpoint to remove unwanted models

---

## 2. Model Functions

### 2.1 Base Model

**File:** `app_fastapi/services/models/base_model.py`

#### `train_model()`

- **Purpose:** Universal training function that works for all model types
- **Parameters:**
  - `file_path` (str): Path to CSV file
  - `model_name` (str): Name for the model
  - `model_type` (str): Type of model to train
  - `feature_columns` (List[str]): Feature column names
  - `label_column` (str): Label column name
  - `test_size` (float): Test set size (default: 0.2)
  - `random_state` (int): Random seed (default: 42)
  - `evaluation_strategy` (str): "cv" or "holdout" (default: "cv")
  - `cv_folds` (int): Number of CV folds (default: 5)
  - `cv_repeats` (int): Number of CV repeats (default: 1)
  - `stratify` (bool): Whether to stratify (default: True)
  - `primary_metric` (Optional[str]): Main metric to track
  - `**kwargs` - Additional hyperparameters
- **Returns:** Dict - Complete metadata dictionary
- **Logic:** Gets model config, loads and validates data, handles label encoding if needed, creates preprocessing pipeline, instantiates estimator with parameters, builds complete pipeline, evaluates using appropriate strategy, fits final model if using CV, saves model and returns metadata
- **Use Cases:** Main entry point for all model training, called by model_service.train_model_from_csv()

#### `predict()`

- **Purpose:** Universal prediction function for all model types
- **Parameters:**
  - `model_name` (str): Name of trained model
  - `data` (dict): Feature values as dictionary
- **Returns:** Dict - Prediction result with probabilities if available
- **Logic:** Loads model and metadata, prepares input as DataFrame with correct column order, makes prediction, handles class decoding for classification, adds probabilities if model supports them
- **Use Cases:** Main entry point for predictions, called by model_service.predict_with_model()

---

### 2.2 Config

**File:** `app_fastapi/services/models/config.py`

#### `get_model_config()`

- **Purpose:** Returns configuration for a specific model type
- **Parameters:**
  - `model_type` (str): Type of model (e.g., "linear_regression")
- **Returns:** dict - Model configuration dictionary
- **Logic:** Looks up model type in MODEL_CONFIG dictionary, raises ValueError if not found, returns config with estimator class, default params, scaling needs, etc.
- **Use Cases:** Called by train_model() to get model-specific settings before training

**Global Variable:** `MODEL_CONFIG`
- Dictionary containing configuration for all 7 supported models
- Each entry specifies: estimator_class, default_params, type (classification/regression), needs_scaling, supports_proba, needs_label_encoding, supports_random_state
- Models included: linear_regression, logistic_regression, decision_tree, random_forest, knn, svm, kernel_svm

---

### 2.3 Evaluation Module (_evaluation.py)

**File:** `app_fastapi/services/models/_evaluation.py`

This is an alternative/internal evaluation module with similar functions to core/evaluation.py.

#### `_final_estimator()`

- **Purpose:** Extracts the final estimator from a pipeline
- **Parameters:**
  - `estimator` - Model or pipeline
- **Returns:** Final estimator object
- **Logic:** Checks if estimator is Pipeline, returns last step if so, otherwise returns estimator itself
- **Use Cases:** Helper function used internally to access the actual model within a pipeline

#### `supports_proba()`

- **Purpose:** Checks if model supports probability predictions
- **Parameters:**
  - `estimator` - Model or pipeline
- **Returns:** bool
- **Logic:** Uses _final_estimator() to get actual model, checks for predict_proba attribute
- **Use Cases:** Same as core version, used before attempting probability-based metrics

#### `evaluate_classification_holdout()`

- Similar to core version with minor differences in metric naming (uses "test_precision_weighted" instead of "test_precision")

#### `evaluate_classification_cv()`

- Similar to core version with minor differences in handling negative metrics

#### `evaluate_regression_holdout()`

- Similar to core version, includes both train and test RMSE

#### `evaluate_regression_cv()`

- Similar to core version with explicit handling of negative metric conversions

---

### 2.4 Model Registry

**File:** `app_fastapi/services/models/__init__.py`

**Global Variable:** `MODEL_REGISTRY`
- Dictionary mapping model type strings to their respective module objects
- Contains: linear_regression, logistic_regression, decision_tree, random_forest, knn, svm, kernel_svm
- Each module contains train_model() and predict() functions
- Used by model_service to dynamically route to correct model implementation

---

## 3. Service Functions

### 3.1 Model Service

**File:** `app_fastapi/services/model_service.py`

#### `preprocess_dataframe()`

- **Purpose:** Legacy preprocessing function (kept for backward compatibility)
- **Parameters:**
  - `df` (pd.DataFrame): Input DataFrame
  - `feature_columns` (List[str]): Feature columns
  - `label_column` (str): Label column
- **Returns:** tuple - (X processed, y processed, preprocessing_info dict)
- **Logic:** Applies one-hot encoding to categorical features, fills missing values with mean, converts label to numeric, documents transformations
- **Use Cases:** Deprecated in favor of pipeline-based preprocessing, kept for compatibility

#### `train_model_from_csv()`

- **Purpose:** High-level function to train any model type from CSV
- **Parameters:**
  - `file_path` (str): Path to CSV
  - `model_name` (str): Model name
  - `feature_columns` (List[str]): Features
  - `label_column` (str): Label
  - `test_size` (float): Test size (default: 0.2)
  - `random_state` (int): Random seed (default: 42)
  - `model_type` (str): Model type (default: "linear_regression")
  - `evaluation_strategy` (str): Evaluation strategy (default: "cv")
  - `cv_folds` (int): CV folds (default: 5)
  - `cv_repeats` (int): CV repeats (default: 1)
  - `stratify` (bool): Stratify (default: True)
  - `primary_metric` (Optional[str]): Primary metric
  - `**kwargs` - Additional hyperparameters
- **Returns:** Dict - Model metadata
- **Logic:** Validates model type exists in registry, retrieves corresponding module, delegates to that module's train_model() function
- **Use Cases:** Main entry point called by API router for training requests

#### `predict_with_model()`

- **Purpose:** High-level function to make predictions with any model
- **Parameters:**
  - `model_name` (str): Model name
  - `data` (dict): Feature values
- **Returns:** Dict - Prediction result
- **Logic:** Loads model metadata, identifies model type, retrieves corresponding module, delegates to that module's predict() function
- **Use Cases:** Main entry point called by API router for prediction requests

#### `list_all_models()`

- **Purpose:** Lists all trained models with metadata
- **Parameters:** None
- **Returns:** List[Dict] - List of model metadata
- **Logic:** Scans models directory for pkl files, loads metadata for each, returns list
- **Use Cases:** Called by API to show available models

#### `get_model_details()`

- **Purpose:** Gets detailed information for a specific model
- **Parameters:**
  - `model_name` (str): Model name
- **Returns:** Dict - Model metadata
- **Logic:** Constructs paths, checks existence, loads and returns metadata JSON
- **Use Cases:** Called by API to display model details

#### `delete_model()`

- **Purpose:** Deletes a trained model
- **Parameters:**
  - `model_name` (str): Model to delete
- **Returns:** Dict - Success message
- **Logic:** Removes pkl and json files, returns confirmation
- **Use Cases:** Called by API delete endpoint

---

### 3.2 User Service

**File:** `app_fastapi/services/user_service.py`

#### `hash_password()`

- **Purpose:** Encrypts plain text password using bcrypt
- **Parameters:**
  - `password` (str): Plain text password
- **Returns:** str - Hashed password
- **Logic:** Uses passlib CryptContext with bcrypt to generate secure hash
- **Use Cases:** Called when creating users to store passwords securely

#### `verify_password()`

- **Purpose:** Verifies a plain password against its hash
- **Parameters:**
  - `plain_password` (str): Plain text password
  - `hashed_password` (str): Stored hash
- **Returns:** bool - True if password matches
- **Logic:** Uses passlib to compare plain password with hash, handles backward compatibility
- **Use Cases:** Called during login to authenticate users

#### `create_user()`

- **Purpose:** Adds a new user to the database
- **Parameters:**
  - `username` (str): Username
  - `password` (str): Plain password
- **Returns:** None
- **Logic:** Hashes password, inserts new user with default 10 tokens, commits to database
- **Use Cases:** Called by signup endpoint to register new users

#### `find_user_by_username()`

- **Purpose:** Retrieves user record by username
- **Parameters:**
  - `username` (str): Username to find
- **Returns:** tuple - User record (username, password, tokens) or None
- **Logic:** Executes SELECT query, returns first match
- **Use Cases:** Called during login to verify user exists and get credentials

---

### 3.3 JWT Handler

**File:** `app_fastapi/services/jwt_handler.py`

#### `create_access_token()`

- **Purpose:** Creates a signed JWT token for authentication
- **Parameters:**
  - `subject` (str): Username
  - `roles` (List[str]): User roles (e.g., ["user", "admin"])
- **Returns:** str - Encoded JWT token
- **Logic:** Creates payload with subject, roles, issued at (iat), and expiration (exp) timestamps, signs with secret key using HS256 algorithm
- **Use Cases:** Called after successful login to generate authentication token

#### `decode_token()`

- **Purpose:** Decodes and validates a JWT token
- **Parameters:**
  - `token` (str): JWT token string
- **Returns:** dict - Decoded token payload
- **Logic:** Uses PyJWT to decode token with secret key, validates signature and expiration, raises HTTPException if invalid or expired
- **Use Cases:** Called by auth_dependency to verify tokens on protected endpoints

**Global Variable:** `JWT_CONFIG`
- Dictionary containing JWT configuration from environment variables
- Includes: SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

---

### 3.4 Auth Dependency

**File:** `app_fastapi/services/auth_dependency.py`

#### `get_current_user()`

- **Purpose:** FastAPI dependency that extracts and validates JWT from request
- **Parameters:**
  - `credentials` (HTTPAuthorizationCredentials): Injected by FastAPI security
- **Returns:** dict - Decoded token claims (username, roles, timestamps)
- **Logic:** Extracts bearer token from Authorization header, calls jwt_handler.decode_token(), returns decoded claims, raises HTTPException on errors
- **Use Cases:** Used as dependency in protected route definitions to enforce authentication

**Global Variable:** `security`
- HTTPBearer instance that handles authorization header extraction
- Automatically adds "Authorize" button to Swagger UI

---

### 3.5 Token Service

**File:** `app_fastapi/services/token_service.py`

#### `validate_and_deduct_tokens()`

- **Purpose:** Validates sufficient tokens and deducts cost for operation
- **Parameters:**
  - `username` (str): Username
  - `operation` (str): Operation type ("train", "predict", etc.)
- **Returns:** bool - True if successful
- **Logic:** Gets operation cost, checks user balance, raises error if insufficient, deducts tokens using database function, logs transaction
- **Use Cases:** Called at start of train and predict operations to charge users

#### `get_token_cost()`

- **Purpose:** Returns the token cost for an operation
- **Parameters:**
  - `operation` (str): Operation type
- **Returns:** int - Token cost
- **Logic:** Looks up operation in TOKEN_COSTS dictionary, returns cost or 0
- **Use Cases:** Used to display costs to users and calculate charges

#### `refund_tokens()`

- **Purpose:** Refunds tokens if operation fails after deduction
- **Parameters:**
  - `username` (str): Username
  - `operation` (str): Operation type
  - `reason` (str): Reason for refund (default: "Operation failed")
- **Returns:** None
- **Logic:** Gets operation cost, adds tokens back to user account, logs refund transaction
- **Use Cases:** Called in exception handlers when operations fail after token deduction

**Global Variable:** `TOKEN_COSTS`
- Dictionary mapping operation names to token costs
- train: 1 token, predict: 5 tokens, list_models: 0, get_model: 0

---

### 3.6 Logger Service

**File:** `app_fastapi/services/logger_service.py`

#### `log_info()`

- **Purpose:** Logs informational message
- **Parameters:**
  - `message` (str): Message to log
- **Returns:** None
- **Logic:** Writes info-level message to log file and console
- **Use Cases:** General informational logging

#### `log_warning()`

- **Purpose:** Logs warning message
- **Parameters:**
  - `message` (str): Message to log
- **Returns:** None
- **Logic:** Writes warning-level message to log file and console
- **Use Cases:** Non-critical issues that should be noted

#### `log_error()`

- **Purpose:** Logs error message
- **Parameters:**
  - `message` (str): Message to log
- **Returns:** None
- **Logic:** Writes error-level message to log file and console
- **Use Cases:** Critical errors and exceptions

#### `log_registration()`

- **Purpose:** Logs user registration attempt
- **Parameters:**
  - `username` (str): Username
  - `success` (bool): Whether registration succeeded
- **Returns:** None
- **Logic:** Formats message with REGISTRATION tag, username, and status
- **Use Cases:** Called by signup endpoint

#### `log_login()`

- **Purpose:** Logs user login attempt
- **Parameters:**
  - `username` (str): Username
  - `success` (bool): Whether login succeeded
- **Returns:** None
- **Logic:** Formats message with LOGIN tag, username, and status
- **Use Cases:** Called by login endpoint

#### `log_token_operation()`

- **Purpose:** Logs token add/deduct operation
- **Parameters:**
  - `username` (str): Username
  - `operation` (str): Operation type (add/deduct)
  - `tokens` (int): Number of tokens
  - `success` (bool): Whether operation succeeded
- **Returns:** None
- **Logic:** Formats message with TOKEN_OPERATION tag and details
- **Use Cases:** Called when tokens are added or deducted

#### `log_model_training()`

- **Purpose:** Logs model training operation
- **Parameters:**
  - `username` (str): Username
  - `model_name` (str): Model name
  - `success` (bool): Whether training succeeded
  - `details` (str): Additional details (default: "")
- **Returns:** None
- **Logic:** Formats message with TRAINING tag, user, model, status, and optional details
- **Use Cases:** Called by train endpoint

#### `log_prediction()`

- **Purpose:** Logs prediction operation
- **Parameters:**
  - `username` (str): Username
  - `model_name` (str): Model name
  - `success` (bool): Whether prediction succeeded
  - `details` (str): Additional details (default: "")
- **Returns:** None
- **Logic:** Formats message with PREDICTION tag and details
- **Use Cases:** Called by predict endpoint

#### `log_validation_error()`

- **Purpose:** Logs validation error
- **Parameters:**
  - `operation` (str): Operation that failed
  - `error` (str): Error message
- **Returns:** None
- **Logic:** Formats warning message with VALIDATION_ERROR tag
- **Use Cases:** Called when input validation fails

#### `log_insufficient_tokens()`

- **Purpose:** Logs insufficient token error
- **Parameters:**
  - `username` (str): Username
  - `operation` (str): Operation attempted
  - `required` (int): Tokens required
  - `available` (int): Tokens available
- **Returns:** None
- **Logic:** Formats warning message with token requirement details
- **Use Cases:** Called when user doesn't have enough tokens

**Module-level Setup:**
- Creates logs directory if it doesn't exist
- Configures rotating file handler (10MB max, 5 backups)
- Sets up console handler for real-time monitoring
- Uses format: timestamp | level | message

---

## 4. Router Endpoint Functions

### 4.1 Auth Router

**File:** `app_fastapi/routers/auth_router.py`

#### `signup()`

- **Purpose:** POST /auth/signup - Register new user
- **Parameters:**
  - `user` (UserLogin): Pydantic model with username and password
- **Returns:** dict - Success message and initial token count
- **Logic:** Calls user_service.create_user(), logs registration, handles errors
- **Use Cases:** User registration from frontend

#### `login()`

- **Purpose:** POST /auth/login - Authenticate user and return JWT
- **Parameters:**
  - `user` (UserLogin): Pydantic model with username and password
- **Returns:** dict - Access token, username, token balance, admin status
- **Logic:** Gets user from DB, verifies password, determines roles, generates JWT with roles, returns token and user info
- **Use Cases:** User authentication from frontend

#### `get_tokens()`

- **Purpose:** GET /auth/tokens/{username} - Get user's token balance
- **Parameters:**
  - `username` (str): Username
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Username and token balance
- **Logic:** Verifies user can only check own balance (unless admin), queries database for token count
- **Use Cases:** Displaying token balance in UI

#### `add_tokens()`

- **Purpose:** POST /auth/add_tokens - Add tokens to user account
- **Parameters:**
  - `token_request` (TokenAdd): Username and token amount
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Success message and new balance
- **Logic:** Validates positive amount, checks authorization, updates database, logs transaction, returns new balance
- **Use Cases:** Token purchase/refill functionality

#### `secure_route()`

- **Purpose:** GET /auth/secure - Example protected endpoint
- **Parameters:**
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Welcome message and token details
- **Logic:** Simply returns current user info from decoded JWT
- **Use Cases:** Testing authentication, example for developers

#### `get_all_users()`

- **Purpose:** GET /auth/users - Get all users (admin only)
- **Parameters:**
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - List of users
- **Logic:** Checks for admin role, queries database for all users, returns list
- **Use Cases:** Admin panel user management

#### `create_user_admin()`

- **Purpose:** POST /auth/users - Create new user (admin only)
- **Parameters:**
  - `user` (UserCreate): User details including admin flag
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Success message, user details, and JWT token
- **Logic:** Checks admin role, hashes password, inserts user with specified tokens and admin status, generates JWT for new user, logs operation
- **Use Cases:** Admin creating users with custom settings

#### `update_user_admin()`

- **Purpose:** PUT /auth/users/{username} - Update user (admin only)
- **Parameters:**
  - `username` (str): User to update
  - `user_update` (UserUpdate): Fields to update (all optional)
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Success message
- **Logic:** Checks admin role, hashes password if provided, calls database update function with only non-None fields, logs operation
- **Use Cases:** Admin modifying user settings

#### `delete_user_admin()`

- **Purpose:** DELETE /auth/users/{username} - Delete user (admin only)
- **Parameters:**
  - `username` (str): User to delete
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Success message
- **Logic:** Checks admin role, prevents self-deletion, deletes user from database, logs operation
- **Use Cases:** Admin removing users

#### `get_usage_logs_api()`

- **Purpose:** GET /auth/usage_logs - Get usage logs
- **Parameters:**
  - `username` (str): Optional filter by user (default: None)
  - `limit` (int): Max logs to return (default: 50)
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - List of logs and count
- **Logic:** Checks if admin (can see all) or regular user (own logs only), queries database, converts tuples to dicts, formats timestamps
- **Use Cases:** Displaying activity history in UI

#### `ping_auth()`

- **Purpose:** GET /auth/ping - Health check for auth router
- **Parameters:** None
- **Returns:** dict - Status message
- **Logic:** Simple ping/pong response
- **Use Cases:** Testing router availability

---

### 4.2 Models Router

**File:** `app_fastapi/routers/models_router.py`

#### `train_model()`

- **Purpose:** POST /models/train - Train a machine learning model
- **Parameters:**
  - `file` (UploadFile): CSV file with training data
  - `model_name` (str): Name for the model
  - `feature_columns` (str): Comma-separated feature columns
  - `label_column` (str): Label column name
  - `test_size` (float): Test set size (default: 0.2)
  - `model_type` (str): Model type (default: "linear_regression")
  - `evaluation_strategy` (str): "cv" or "holdout" (default: "cv")
  - `cv_folds` (int): CV folds (default: 5)
  - `cv_repeats` (int): CV repeats (default: 1)
  - `stratify` (bool): Stratify split (default: True)
  - `primary_metric` (str): Primary metric (optional)
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Status, message, metadata, tokens deducted
- **Logic:** Validates and deducts tokens, saves uploaded file, parses feature columns, calls model_service to train, generates metrics summary, logs success, adds usage log entry, returns metadata, refunds tokens on error
- **Use Cases:** Main endpoint for model training from Streamlit UI

#### `predict_model()`

- **Purpose:** POST /models/predict - Make prediction with trained model
- **Parameters:**
  - `request` (PredictRequest): Model name and feature values
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Prediction result with probabilities if available
- **Logic:** Validates and deducts tokens, calls model_service to predict, logs success, adds usage log, returns result with tokens deducted, refunds on error
- **Use Cases:** Making predictions from Streamlit UI

#### `list_models()`

- **Purpose:** GET /models - Get list of all trained models
- **Parameters:**
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Status, models list, count
- **Logic:** Calls model_service.list_all_models(), returns formatted response
- **Use Cases:** Displaying available models in UI

#### `get_model_details()`

- **Purpose:** GET /models/{model_name} - Get details of specific model
- **Parameters:**
  - `model_name` (str): Model name
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Status and model metadata
- **Logic:** Calls model_service.get_model_details(), returns formatted response
- **Use Cases:** Showing model information in UI

#### `delete_model()`

- **Purpose:** DELETE /models/{model_name} - Delete trained model
- **Parameters:**
  - `model_name` (str): Model to delete
  - `current_user` (dict): Injected by auth dependency
- **Returns:** dict - Status and success message
- **Logic:** Calls model_service.delete_model(), adds usage log entry, returns confirmation
- **Use Cases:** Removing unwanted models from UI

---

## 5. Database Functions

**File:** `app_fastapi/database_manager.py`

#### `connect_to_db()`

- **Purpose:** Creates database connection (backward compatibility)
- **Parameters:**
  - `db_config` (dict): Database configuration
- **Returns:** psycopg2 connection or None
- **Logic:** Attempts to connect using psycopg2, returns connection or None on error
- **Use Cases:** Legacy function, use get_connection() instead

#### `create_database_if_not_exists()`

- **Purpose:** Creates target database if it doesn't exist
- **Parameters:** None
- **Returns:** None
- **Logic:** Connects to postgres DB, checks if target DB exists, creates if not, uses autocommit for CREATE DATABASE
- **Use Cases:** Called during startup to ensure database exists

#### `get_connection()`

- **Purpose:** Context manager for database connections (recommended)
- **Parameters:** None
- **Returns:** psycopg2 connection (via yield)
- **Logic:** Attempts connection, creates database if not found, yields connection for use in with statement, automatically closes on exit
- **Use Cases:** All database operations should use this for proper cleanup

#### `create_users_table()`

- **Purpose:** Creates users table if it doesn't exist
- **Parameters:** None
- **Returns:** None
- **Logic:** Executes CREATE TABLE IF NOT EXISTS with all columns (user_id, user_name, user_password, tokens, is_admin, created_at)
- **Use Cases:** Called during startup to initialize database schema

#### `create_usage_logs_table()`

- **Purpose:** Creates usage_logs table for tracking activity
- **Parameters:** None
- **Returns:** None
- **Logic:** Executes CREATE TABLE IF NOT EXISTS with log columns (log_id, user_name, action, tokens_changed, status, timestamp, details)
- **Use Cases:** Called during startup to initialize logging table

#### `add_usage_log()`

- **Purpose:** Logs a usage event
- **Parameters:**
  - `user_name` (str): Username
  - `action` (str): Action performed
  - `tokens_changed` (int): Token change (negative for deduction)
  - `status` (str): Status (SUCCESS/FAILED)
  - `details` (str): Additional details (optional)
- **Returns:** None
- **Logic:** Inserts log entry with timestamp, commits transaction
- **Use Cases:** Called after operations to track activity

#### `get_user_tokens()`

- **Purpose:** Gets user's current token balance
- **Parameters:**
  - `user_name` (str): Username
- **Returns:** int - Token count or None if user not found
- **Logic:** Executes SELECT query for tokens, returns first result
- **Use Cases:** Checking token balance before operations

#### `update_user_tokens()`

- **Purpose:** Updates user token balance (add or subtract)
- **Parameters:**
  - `user_name` (str): Username
  - `tokens_to_add` (int): Amount to add (negative to subtract)
- **Returns:** bool - True if successful
- **Logic:** Executes UPDATE with addition, ensures balance doesn't go negative using WHERE clause, returns True if row updated
- **Use Cases:** Charging for operations, adding purchased tokens

#### `get_usage_logs()`

- **Purpose:** Retrieves usage logs with optional filtering
- **Parameters:**
  - `user_name` (str): Filter by user (optional)
  - `limit` (int): Max logs to return (default: 50)
- **Returns:** List of tuples - Log records
- **Logic:** Builds SELECT query with optional WHERE clause, orders by timestamp DESC, applies limit
- **Use Cases:** Displaying activity history

#### `select_all_users()`

- **Purpose:** Fetches all users from database
- **Parameters:** None
- **Returns:** List of tuples - User records
- **Logic:** Executes SELECT * ordered by user_id
- **Use Cases:** Admin panel user list

#### `add_user()`

- **Purpose:** Registers new user
- **Parameters:**
  - `user_name` (str): Username
  - `user_password` (str): Hashed password
- **Returns:** str - Status message
- **Logic:** Inserts user with ON CONFLICT DO NOTHING, checks rowcount to determine if insert occurred
- **Use Cases:** User registration (prefer user_service.create_user())

#### `update_user()`

- **Purpose:** Updates username
- **Parameters:**
  - `old_name` (str): Current username
  - `new_name` (str): New username
- **Returns:** str - Status message
- **Logic:** Executes UPDATE, checks rowcount
- **Use Cases:** Username changes (use update_user_full() for more options)

#### `update_user_full()`

- **Purpose:** Updates user with any combination of fields
- **Parameters:**
  - `user_name` (str): Username to update
  - `new_username` (str): New username (optional)
  - `new_password` (str): New hashed password (optional)
  - `new_tokens` (int): New token balance (optional)
  - `new_is_admin` (bool): Admin status (optional)
- **Returns:** bool - True if successful
- **Logic:** Builds dynamic UPDATE query with only provided fields, executes, checks rowcount
- **Use Cases:** Admin user editing with selective field updates

#### `delete_user()`

- **Purpose:** Deletes user from database
- **Parameters:**
  - `user_name` (str): Username to delete
- **Returns:** str - Status message
- **Logic:** Executes DELETE, checks rowcount, returns message
- **Use Cases:** Admin user deletion

#### `check_user_is_admin()`

- **Purpose:** Checks if user has admin privileges
- **Parameters:**
  - `user_name` (str): Username
- **Returns:** bool - True if admin
- **Logic:** Queries is_admin column, returns value or False if not found
- **Use Cases:** Authorization checks

#### `set_user_admin()`

- **Purpose:** Grants or revokes admin privileges
- **Parameters:**
  - `user_name` (str): Username
  - `is_admin` (bool): Admin status (default: True)
- **Returns:** str - Status message
- **Logic:** Updates is_admin column, returns message with RETURNING clause
- **Use Cases:** Admin privilege management (setup_admin.py)

#### `get_user_by_name()`

- **Purpose:** Gets complete user record by username
- **Parameters:**
  - `user_name` (str): Username
- **Returns:** tuple - (user_id, user_name, user_password, tokens, is_admin)
- **Logic:** Executes SELECT for specific columns, returns first match
- **Use Cases:** Login process to get user details

#### `clear_usage_logs()`

- **Purpose:** Deletes all usage logs
- **Parameters:** None
- **Returns:** None
- **Logic:** Executes DELETE on entire table, commits
- **Use Cases:** Administrative cleanup

**Global Variable:** `DB_CONFIG`
- Dictionary with database connection parameters from environment variables
- Contains: dbname, user, password, host, port

---

## 6. FastAPI Application Functions

**File:** `app_fastapi/app_fastapi.py`

#### `root()`

- **Purpose:** GET / - Root endpoint
- **Parameters:** None
- **Returns:** dict - Welcome message
- **Logic:** Returns simple JSON response
- **Use Cases:** Testing server is running

#### `health_check()`

- **Purpose:** GET /health - Health check endpoint
- **Parameters:** None
- **Returns:** dict - Status ok
- **Logic:** Returns simple status response
- **Use Cases:** Monitoring, Streamlit connection testing

**Module-level Setup:**
- Creates FastAPI app with title, description, version
- Includes routers for /models and /auth endpoints
- No authentication on root and health endpoints

---

## 7. Streamlit Functions

### 7.1 Main App (app_streamlit.py)

**File:** `app_streamlit/app_streamlit.py`

#### `img_to_base64()`

- **Purpose:** Converts image file to base64 string
- **Parameters:**
  - `path` - Path to image file
- **Returns:** str - Base64 encoded string
- **Logic:** Opens file in binary mode, reads, encodes as base64, decodes to string
- **Use Cases:** Loading icons for display in HTML/markdown

#### `init_session_state()`

- **Purpose:** Initializes Streamlit session state variables
- **Parameters:** None
- **Returns:** None
- **Logic:** Sets default values for logged_in (False) and page ("Dashboard") if not already set
- **Use Cases:** Called at app startup to ensure session state exists

#### `login_page()`

- **Purpose:** Displays login/signup page
- **Parameters:** None
- **Returns:** None
- **Logic:** Shows logo with base64 image, checks server status, displays connection instructions if offline, shows login and signup tabs with forms, calls API on submit, updates session state on success
- **Use Cases:** Authentication UI when user is not logged in

#### `main_app()`

- **Purpose:** Displays main application with navigation
- **Parameters:** None
- **Returns:** None
- **Logic:** Checks server health, shows sidebar with user info and navigation, conditionally shows Admin Panel for admins, routes to selected page, provides logout button
- **Use Cases:** Main UI after successful login

#### `main()`

- **Purpose:** Main application entry point
- **Parameters:** None
- **Returns:** None
- **Logic:** Calls init_session_state(), shows login_page() or main_app() based on logged_in state
- **Use Cases:** Streamlit app execution

**Module-level Setup:**
- Adds project root and app_streamlit to Python path
- Ensures database and tables exist
- Initializes APIClient
- Sets page config (title, icon, layout)

---

### 7.2 API Client

**File:** `app_streamlit/components/api_client.py`

**Class:** `APIClient`

#### `__init__()`

- **Purpose:** Initializes API client
- **Parameters:**
  - `base_url` (str): FastAPI server URL (default: "http://localhost:8000")
- **Returns:** None
- **Logic:** Stores base URL
- **Use Cases:** Creating client instance

#### `_get_headers()`

- **Purpose:** Gets HTTP headers with JWT token
- **Parameters:** None
- **Returns:** Dict - Headers with Authorization if token exists
- **Logic:** Retrieves token from session state, formats as Bearer token
- **Use Cases:** Called internally before authenticated requests

#### `check_server_health()`

- **Purpose:** Checks if server is responding
- **Parameters:** None
- **Returns:** bool - True if server responds
- **Logic:** Sends GET to /health with 2s timeout, returns True if status 200
- **Use Cases:** Connection monitoring

#### `get_server_status()`

- **Purpose:** Gets detailed server status
- **Parameters:** None
- **Returns:** Dict - Status with message and help text
- **Logic:** Attempts health check, returns detailed status dict with error handling for different failure modes
- **Use Cases:** Displaying server status to users

#### `signup()`

- **Purpose:** Registers new user
- **Parameters:**
  - `username` (str): Username
  - `password` (str): Password
- **Returns:** Dict - Success or error
- **Logic:** Posts to /auth/signup, handles connection errors, returns response JSON
- **Use Cases:** User registration

#### `login()`

- **Purpose:** Authenticates user and stores token
- **Parameters:**
  - `username` (str): Username
  - `password` (str): Password
- **Returns:** Dict - Login response or error
- **Logic:** Posts to /auth/login, stores access_token, username, tokens, is_admin in session state on success
- **Use Cases:** User login

#### `logout()`

- **Purpose:** Clears session state
- **Parameters:** None
- **Returns:** None
- **Logic:** Calls st.session_state.clear()
- **Use Cases:** User logout

#### `get_tokens()`

- **Purpose:** Gets token balance for user
- **Parameters:**
  - `username` (str): Username
- **Returns:** Dict - Token balance or error
- **Logic:** Gets from /auth/tokens/{username} with auth headers
- **Use Cases:** Checking balance

#### `add_tokens()`

- **Purpose:** Adds tokens to account
- **Parameters:**
  - `username` (str): Username
  - `tokens` (int): Amount to add
- **Returns:** Dict - New balance or error
- **Logic:** Posts to /auth/add_tokens with auth headers
- **Use Cases:** Token purchase

#### `train_model()`

- **Purpose:** Trains model with uploaded file
- **Parameters:**
  - `file` - File object
  - `model_name` (str): Model name
  - `feature_columns` (str): Comma-separated features
  - `label_column` (str): Label column
  - `test_size` (float): Test size (default: 0.2)
  - `model_type` (str): Model type (default: "linear_regression")
- **Returns:** Dict - Training result or error
- **Logic:** Posts file and data to /models/train as multipart/form-data with auth headers
- **Use Cases:** Model training from UI

#### `predict()`

- **Purpose:** Makes prediction with model
- **Parameters:**
  - `model_name` (str): Model name
  - `features` (Dict): Feature values
- **Returns:** Dict - Prediction result or error
- **Logic:** Posts to /models/predict with JSON payload and auth headers
- **Use Cases:** Making predictions from UI

#### `list_models()`

- **Purpose:** Gets list of trained models
- **Parameters:** None
- **Returns:** Dict - Models list or error
- **Logic:** Gets from /models with auth headers
- **Use Cases:** Displaying available models

#### `get_model_details()`

- **Purpose:** Gets model metadata
- **Parameters:**
  - `model_name` (str): Model name
- **Returns:** Dict - Model details or error
- **Logic:** Gets from /models/{model_name} with auth headers
- **Use Cases:** Showing model information

#### `delete_model()`

- **Purpose:** Deletes trained model
- **Parameters:**
  - `model_name` (str): Model name
- **Returns:** Dict - Success or error
- **Logic:** Sends DELETE to /models/{model_name} with auth headers
- **Use Cases:** Removing models

#### `get_all_users()`

- **Purpose:** Gets all users (admin only)
- **Parameters:** None
- **Returns:** Dict - Users list or error
- **Logic:** Gets from /auth/users with auth headers
- **Use Cases:** Admin panel

#### `create_user_admin()`

- **Purpose:** Creates user (admin only)
- **Parameters:**
  - `username` (str): Username
  - `password` (str): Password
  - `tokens` (int): Initial tokens (default: 10)
  - `is_admin` (bool): Admin status (default: False)
- **Returns:** Dict - Success or error
- **Logic:** Posts to /auth/users with auth headers
- **Use Cases:** Admin user creation

#### `update_user_admin()`

- **Purpose:** Updates user (admin only)
- **Parameters:**
  - `username` (str): Username to update
  - `new_username` (str): New username (optional)
  - `new_password` (str): New password (optional)
  - `new_tokens` (int): New token balance (optional)
  - `new_is_admin` (bool): Admin status (optional)
- **Returns:** Dict - Success or error
- **Logic:** Puts to /auth/users/{username} with only non-None fields
- **Use Cases:** Admin user editing

#### `delete_user_admin()`

- **Purpose:** Deletes user (admin only)
- **Parameters:**
  - `username` (str): Username to delete
- **Returns:** Dict - Success or error
- **Logic:** Sends DELETE to /auth/users/{username} with auth headers
- **Use Cases:** Admin user deletion

#### `get_usage_logs()`

- **Purpose:** Gets usage logs
- **Parameters:**
  - `username` (str): Filter by user (optional)
  - `limit` (int): Max logs (default: 50)
- **Returns:** Dict - Logs list or error
- **Logic:** Gets from /auth/usage_logs with query params and auth headers
- **Use Cases:** Displaying activity logs

---

### 7.3 Dashboard Page

**File:** `app_streamlit/pages/dashboard.py`

#### `show()`

- **Purpose:** Displays dashboard page
- **Parameters:** None
- **Returns:** None
- **Logic:** Shows token balance metrics, credit card purchase form with validation, lists trained models with expandable details, displays usage logs as DataFrame, shows quick statistics
- **Use Cases:** Main dashboard after login

---

### 7.4 Train Page

**File:** `app_streamlit/pages/train_page.py`

#### `show()`

- **Purpose:** Displays model training page
- **Parameters:** None
- **Returns:** None
- **Logic:** Shows file uploader, previews CSV data, provides column selection for features and label, allows model type selection, configures training parameters, trains on button click, displays metrics (classification or regression), shows preprocessing details
- **Use Cases:** Training machine learning models

---

### 7.5 Predict Page

**File:** `app_streamlit/pages/predict_page.py`

#### `show()`

- **Purpose:** Displays prediction page
- **Parameters:** None
- **Returns:** None
- **Logic:** Lists available models, shows model selection dropdown, displays model info, provides input fields for features, supports JSON input, makes prediction on button click, shows result with probabilities if available
- **Use Cases:** Making predictions with trained models

---

### 7.6 Admin Page

**File:** `app_streamlit/pages/admin_page.py`

#### `show()`

- **Purpose:** Displays admin panel (admin only)
- **Parameters:** None
- **Returns:** None
- **Logic:** Checks admin status, provides action selector, routes to appropriate sub-function, shows token distribution charts, displays usage logs with filtering, lists models
- **Use Cases:** System administration

#### `show_users_table()`

- **Purpose:** Displays users table with statistics
- **Parameters:** None
- **Returns:** None
- **Logic:** Fetches users via API, converts to DataFrame, provides filtering and sorting, displays table with metrics
- **Use Cases:** Viewing user list

#### `show_create_user_form()`

- **Purpose:** Form to create new user
- **Parameters:** None
- **Returns:** None
- **Logic:** Shows form with username, password, tokens, admin checkbox, calls API on submit, displays generated JWT token
- **Use Cases:** Admin creating users

#### `show_update_user_form()`

- **Purpose:** Form to update existing user
- **Parameters:** None
- **Returns:** None
- **Logic:** Lists users for selection, shows current values, provides form for updates, only sends non-empty fields to API
- **Use Cases:** Admin editing users

#### `show_delete_users_form()`

- **Purpose:** Form to delete users with checkboxes
- **Parameters:** None
- **Returns:** None
- **Logic:** Shows users with checkboxes, prevents self-deletion, confirms deletion, deletes selected users with progress bar
- **Use Cases:** Admin removing users

#### `show_token_distribution()`

- **Purpose:** Displays token distribution charts
- **Parameters:** None
- **Returns:** None
- **Logic:** Fetches users, creates bar chart of tokens, shows statistics (mean, median, max, min)
- **Use Cases:** Visualizing token economy

#### `show_usage_logs()`

- **Purpose:** Displays system activity logs
- **Parameters:** None
- **Returns:** None
- **Logic:** Fetches logs via API, converts to DataFrame, provides action filtering, shows activity summary metrics
- **Use Cases:** Monitoring system usage

#### `show_models_section()`

- **Purpose:** Displays trained models section
- **Parameters:** None
- **Returns:** None
- **Logic:** Lists models with expandable details, provides delete buttons with confirmation
- **Use Cases:** Managing models

---

### 7.7 Utils

**File:** `app_streamlit/components/utils.py`

This file appears to be empty or minimal (1 line).

---

## 8. Test Functions

### 8.1 Test API Endpoints

**File:** `tests/test_api_endpoints.py`

#### `test_health()`

- **Purpose:** Tests health endpoint
- **Logic:** Sends GET to /health, asserts 200 status

#### `test_root()`

- **Purpose:** Tests root endpoint
- **Logic:** Sends GET to /, asserts successful status

#### `test_auth_ping()`

- **Purpose:** Tests auth router ping
- **Logic:** Sends GET to /auth/ping, asserts 200

#### `test_list_models()`

- **Purpose:** Tests model listing
- **Logic:** Sends GET to /models, asserts 200 and correct response type

#### `test_login_success()`

- **Purpose:** Tests successful login
- **Logic:** Posts valid credentials, asserts 200 and access_token in response

#### `test_login_invalid_username()`

- **Purpose:** Tests login with nonexistent user
- **Logic:** Posts invalid username, asserts 401 status

#### `test_login_invalid_password()`

- **Purpose:** Tests login with wrong password
- **Logic:** Posts valid user with wrong password, asserts 401

#### `test_login_missing_username()`

- **Purpose:** Tests login without username
- **Logic:** Posts without username field, asserts 422 validation error

#### `test_login_missing_password()`

- **Purpose:** Tests login without password
- **Logic:** Posts without password field, asserts 422 validation error

#### `test_login_empty_credentials()`

- **Purpose:** Tests login with empty strings
- **Logic:** Posts empty credentials, asserts 401 or 422

#### `test_login_response_structure()`

- **Purpose:** Tests login response format
- **Logic:** Posts valid credentials, verifies response contains required fields

#### `test_auth_tokens_without_auth()`

- **Purpose:** Tests tokens endpoint without authentication
- **Logic:** Sends GET to /auth/tokens without headers, expects auth required

#### `test_auth_tokens_with_auth()`

- **Purpose:** Tests tokens endpoint with authentication
- **Logic:** Sends GET with Bearer token, expects 200

#### `test_auth_tokens_with_credentials()`

- **Purpose:** Tests tokens with basic auth
- **Logic:** Placeholder for basic auth test

#### `test_train_and_predict_flow()`

- **Purpose:** Tests complete train/predict workflow
- **Logic:** Skipped - would train model, make prediction, delete model

---

### 8.2 Test Model Service

**File:** `tests/test_model_service.py`

#### Fixtures:

##### `sample_regression_csv()`

- **Purpose:** Creates temporary CSV for regression testing
- **Returns:** str - Path to temp file
- **Logic:** Creates DataFrame with linear relationship, saves as temp CSV, yields path, deletes after test

##### `sample_classification_csv()`

- **Purpose:** Creates temporary CSV for classification testing
- **Returns:** str - Path to temp file
- **Logic:** Creates DataFrame with binary classes, saves as temp CSV, yields path, deletes after test

#### Helper Functions:

##### `cleanup_model()`

- **Purpose:** Deletes test model if it exists
- **Parameters:**
  - `model_name` (str): Model to delete
- **Logic:** Tries to delete model, ignores FileNotFoundError

#### Test Functions:

##### `test_model_registry()`

- **Purpose:** Tests MODEL_REGISTRY contains all expected models
- **Logic:** Asserts all 7 model types are present

##### `test_train_linear_regression()`

- **Purpose:** Tests training linear regression model
- **Logic:** Trains model, checks metadata structure, verifies metrics present, cleans up

##### `test_train_logistic_regression()`

- **Purpose:** Tests training logistic regression model
- **Logic:** Trains model, checks classification metrics present

##### `test_predict_linear_regression()`

- **Purpose:** Tests making predictions with linear regression
- **Logic:** Trains model, makes prediction, verifies result structure

##### `test_predict_logistic_regression()`

- **Purpose:** Tests making predictions with logistic regression
- **Logic:** Trains model, makes prediction, verifies classification result with probabilities

##### `test_unsupported_model_type()`

- **Purpose:** Tests error handling for invalid model type
- **Logic:** Attempts to train with unsupported type, expects ValueError

##### `test_list_models()`

- **Purpose:** Tests listing trained models
- **Logic:** Trains model, lists all models, verifies trained model appears

##### `test_get_model_details()`

- **Purpose:** Tests retrieving model details
- **Logic:** Trains model, gets details, verifies structure

##### `test_delete_model()`

- **Purpose:** Tests deleting model
- **Logic:** Trains model, deletes it, verifies it's gone

##### `test_model_type_default()`

- **Purpose:** Tests default model type is linear_regression
- **Logic:** Inspects function signature

##### `test_train_decision_tree()`

- **Purpose:** Tests training decision tree
- **Logic:** Trains decision tree, verifies metrics and hyperparameters

##### `test_train_random_forest()`

- **Purpose:** Tests training random forest
- **Logic:** Trains random forest, verifies metrics

##### `test_train_knn()`

- **Purpose:** Tests training KNN
- **Logic:** Trains KNN, verifies metrics

##### `test_train_svm()`

- **Purpose:** Tests training SVM
- **Logic:** Trains SVM, verifies linear kernel

##### `test_train_kernel_svm()`

- **Purpose:** Tests training kernel SVM
- **Logic:** Trains kernel SVM, verifies RBF kernel

##### `test_predict_decision_tree()`

- **Purpose:** Tests prediction with decision tree
- **Logic:** Trains and predicts, verifies probabilities included

##### `test_predict_random_forest()`

- **Purpose:** Tests prediction with random forest
- **Logic:** Trains and predicts, verifies classification result

##### `test_predict_knn()`

- **Purpose:** Tests prediction with KNN
- **Logic:** Trains and predicts, verifies result structure

##### `test_predict_svm()`

- **Purpose:** Tests prediction with SVM
- **Logic:** Trains and predicts, verifies probabilities

##### `test_predict_kernel_svm()`

- **Purpose:** Tests prediction with kernel SVM
- **Logic:** Trains and predicts, verifies result

---

### 8.3 Conftest

**File:** `tests/conftest.py`

This file contains pytest configuration that adds the project root to Python path, enabling proper imports in tests.

---

## 9. Utility Scripts

### 9.1 Setup Admin

**File:** `setup_admin.py`

#### `list_users()`

- **Purpose:** Displays all users in formatted table
- **Parameters:** None
- **Returns:** List of user tuples
- **Logic:** Queries database, formats and prints table with ID, username, tokens, admin status
- **Use Cases:** Showing users before granting admin

#### `set_admin()`

- **Purpose:** Interactive function to grant/revoke admin privileges
- **Parameters:** None
- **Returns:** None
- **Logic:** Lists users, prompts for username, checks current status, confirms action, calls database function to update
- **Use Cases:** Admin setup from command line

#### `main()`

- **Purpose:** Main entry point for setup script
- **Parameters:** None
- **Returns:** None
- **Logic:** Ensures database exists, creates tables, runs set_admin(), handles errors
- **Use Cases:** Running script from terminal

---

### 9.2 Run Server

**File:** `run_server.py`

This file contains a single comment with the uvicorn command to start the FastAPI server. It's a reference/documentation file rather than executable code.

---

## Summary Statistics

### Total Functions by Category:

- **Core Functions:** 14 functions
- **Model Functions:** 10 functions + 2 helper functions
- **Service Functions:** 26 functions
- **Router Functions:** 14 endpoints + 9 admin endpoints = 23 total
- **Database Functions:** 20 functions
- **Streamlit Functions:** 25+ functions across 7 files
- **Test Functions:** 30+ test functions
- **Utility Functions:** 3 functions

**Grand Total:** 150+ documented functions across the entire project

---

## Function Call Flow Examples

### Training Flow:
1. User uploads CSV in Streamlit → `train_page.show()`
2. Streamlit calls → `api_client.train_model()`
3. API client sends request → `models_router.train_model()`
4. Router validates tokens → `token_service.validate_and_deduct_tokens()`
5. Router calls → `model_service.train_model_from_csv()`
6. Service delegates to → `base_model.train_model()`
7. Base model gets config → `config.get_model_config()`
8. Base model loads data → `data_handler.load_and_validate_csv()`
9. Base model creates pipeline → `preprocessing.create_preprocessor()`
10. Base model evaluates → `evaluation.evaluate_classification_cv()` or `evaluate_regression_cv()`
11. Base model saves → `model_manager.save_model()`
12. Results returned up the chain → displayed in Streamlit

### Prediction Flow:
1. User enters features in Streamlit → `predict_page.show()`
2. Streamlit calls → `api_client.predict()`
3. API client sends request → `models_router.predict_model()`
4. Router validates tokens → `token_service.validate_and_deduct_tokens()`
5. Router calls → `model_service.predict_with_model()`
6. Service delegates to → `base_model.predict()`
7. Base model loads → `model_manager.load_model()`
8. Base model predicts → pipeline.predict()
9. Result returned up the chain → displayed in Streamlit

---

**End of Comprehensive Functions Overview**
