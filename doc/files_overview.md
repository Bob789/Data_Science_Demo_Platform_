# Files Overview - Data Science Demo Platform

This document provides a comprehensive overview of all Python files in the project, organized by category.

**Total Python Files:** 43

---

## FastAPI Backend

### Core Module

#### 1. evaluation.py
- **Full Path:** `Final_Project_v003/app_fastapi/core/evaluation.py`
- **Purpose:** Provides comprehensive evaluation functions for both classification and regression models. Supports holdout validation and cross-validation strategies with metrics calculation and baseline comparisons.
- **Inputs:**
  - Trained estimator (Pipeline or sklearn model)
  - Feature matrix (X) and labels (y)
  - Evaluation parameters (test_size, cv_folds, cv_repeats, random_state, stratify)
- **Outputs:**
  - Dictionary of metrics (accuracy, precision, recall, F1, confusion matrix for classification; R², RMSE, MAE for regression)
  - Baseline comparison metrics
  - Formatted metrics summary string

#### 2. data_handler.py
- **Full Path:** `Final_Project_v003/app_fastapi/core/data_handler.py`
- **Purpose:** Handles CSV file loading and validation. Divides columns into numeric and categorical types for preprocessing.
- **Inputs:**
  - File path to CSV
  - List of feature column names
  - Label column name
- **Outputs:**
  - Full DataFrame
  - Feature matrix (X) as DataFrame
  - Label series (y)
  - Lists of numeric and categorical column names

#### 3. preprocessing.py
- **Full Path:** `Final_Project_v003/app_fastapi/core/preprocessing.py`
- **Purpose:** Creates sklearn Pipelines with proper preprocessing (imputation, scaling, one-hot encoding) to prevent data leakage. Generates preprocessing metadata for transparency.
- **Inputs:**
  - DataFrame with data
  - List of feature columns
  - Boolean flag for feature scaling
- **Outputs:**
  - ColumnTransformer with complete preprocessing pipeline
  - Preprocessing metadata dictionary

#### 4. model_manager.py
- **Full Path:** `Final_Project_v003/app_fastapi/core/model_manager.py`
- **Purpose:** Manages model persistence - saving/loading trained models and their metadata to/from disk using joblib and JSON.
- **Inputs:**
  - Model name (string identifier)
  - Trained estimator (for saving)
  - Metadata dictionary (for saving)
- **Outputs:**
  - Saved .pkl model files and .json metadata files
  - Loaded estimator objects
  - List of all available models with metadata
  - Success/error messages for delete operations

#### 5. __init__.py
- **Full Path:** `Final_Project_v003/app_fastapi/core/__init__.py`
- **Purpose:** Package initialization file for core modules.
- **Inputs:** None
- **Outputs:** None

---

### Services - Models

#### 6. base_model.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/base_model.py`
- **Purpose:** Central template for all model training and prediction. Orchestrates data loading, preprocessing, training, evaluation, and persistence for any model type. Handles label encoding for classification models.
- **Inputs:**
  - File path, model name, model type
  - Feature/label columns
  - Training parameters (test_size, evaluation_strategy, cv_folds, etc.)
  - Optional hyperparameters
- **Outputs:**
  - Complete metadata dictionary with model info, metrics, preprocessing details, hyperparameters
  - Prediction results with predicted value and probabilities (if applicable)

#### 7. config.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/config.py`
- **Purpose:** Central configuration registry defining all supported model types with their estimator classes, default parameters, and capabilities (scaling needs, probability support, label encoding).
- **Inputs:**
  - Model type string (e.g., "linear_regression", "random_forest")
- **Outputs:**
  - Configuration dictionary for requested model type
  - Raises ValueError for unsupported models

#### 8. _evaluation.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/_evaluation.py`
- **Purpose:** Alternative evaluation module with similar functionality to core/evaluation.py but with slightly different metric naming conventions.
- **Inputs:**
  - Estimator, features (X), labels (y)
  - Evaluation parameters
- **Outputs:**
  - Metrics dictionaries for classification and regression

#### 9. linear_regression.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/linear_regression.py`
- **Purpose:** Wrapper for Linear Regression model that delegates to base_model with model_type="linear_regression".
- **Inputs:** Training/prediction parameters (passed to base_model)
- **Outputs:** Training metadata or prediction results from base_model

#### 10. logistic_regression.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/logistic_regression.py`
- **Purpose:** Wrapper for Logistic Regression model that delegates to base_model with model_type="logistic_regression".
- **Inputs:** Training/prediction parameters (passed to base_model)
- **Outputs:** Training metadata or prediction results from base_model

#### 11. decision_tree.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/decision_tree.py`
- **Purpose:** Wrapper for Decision Tree Classifier that delegates to base_model with model_type="decision_tree".
- **Inputs:** Training/prediction parameters (passed to base_model)
- **Outputs:** Training metadata or prediction results from base_model

#### 12. random_forest.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/random_forest.py`
- **Purpose:** Wrapper for Random Forest Classifier that delegates to base_model with model_type="random_forest".
- **Inputs:** Training/prediction parameters (passed to base_model)
- **Outputs:** Training metadata or prediction results from base_model

#### 13. knn.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/knn.py`
- **Purpose:** Wrapper for K-Nearest Neighbors Classifier that delegates to base_model with model_type="knn".
- **Inputs:** Training/prediction parameters (passed to base_model)
- **Outputs:** Training metadata or prediction results from base_model

#### 14. svm.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/svm.py`
- **Purpose:** Wrapper for Support Vector Machine with linear kernel that delegates to base_model with model_type="svm".
- **Inputs:** Training/prediction parameters (passed to base_model)
- **Outputs:** Training metadata or prediction results from base_model

#### 15. kernel_svm.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/kernel_svm.py`
- **Purpose:** Wrapper for Kernel SVM (RBF) that delegates to base_model with model_type="kernel_svm".
- **Inputs:** Training/prediction parameters (passed to base_model)
- **Outputs:** Training metadata or prediction results from base_model

#### 16. __init__.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/models/__init__.py`
- **Purpose:** Registers all model modules in MODEL_REGISTRY dictionary for dynamic model dispatching.
- **Inputs:** None
- **Outputs:** MODEL_REGISTRY dictionary mapping model type strings to their modules

---

### Services - Business Logic

#### 17. model_service.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/model_service.py`
- **Purpose:** High-level service layer that dispatches training/prediction requests to appropriate model modules via MODEL_REGISTRY. Provides unified API for all model operations.
- **Inputs:**
  - CSV file path, model configuration, model type
  - Model name and prediction data
- **Outputs:**
  - Training metadata
  - Prediction results
  - List of all models
  - Model details
  - Delete confirmation messages

#### 18. user_service.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/user_service.py`
- **Purpose:** Handles user authentication operations including password hashing with bcrypt, password verification, and user creation in the database.
- **Inputs:**
  - Username and password strings
  - Plain text password for verification
- **Outputs:**
  - Hashed password string
  - Boolean verification result
  - Database insertion confirmation
  - User record tuple from database

#### 19. jwt_handler.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/jwt_handler.py`
- **Purpose:** Manages JWT token creation and validation for authentication. Configures token expiration and handles encoding/decoding with proper error handling.
- **Inputs:**
  - Subject (username) and roles list for token creation
  - JWT token string for decoding
- **Outputs:**
  - Signed JWT access token
  - Decoded token payload dictionary
  - HTTPException for invalid/expired tokens

#### 20. auth_dependency.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/auth_dependency.py`
- **Purpose:** FastAPI dependency for protecting routes with JWT authentication. Extracts and validates JWT tokens from Authorization headers.
- **Inputs:**
  - HTTPAuthorizationCredentials from Authorization header
- **Outputs:**
  - Decoded token claims dictionary (username in 'sub', roles, timestamps)
  - HTTPException for authentication failures

#### 21. token_service.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/token_service.py`
- **Purpose:** Manages token-based payment system for operations. Validates token balances, deducts tokens for operations (train=1, predict=5), handles refunds on failures, and logs all transactions.
- **Inputs:**
  - Username, operation type (train/predict), optional refund reason
- **Outputs:**
  - Boolean success status
  - Token cost for operations
  - HTTPException for insufficient tokens
  - Database usage logs

#### 22. logger_service.py
- **Full Path:** `Final_Project_v003/app_fastapi/services/logger_service.py`
- **Purpose:** Centralized logging service with file rotation. Logs authentication events, model operations, token transactions, and errors to both file and console.
- **Inputs:**
  - Log messages, usernames, operation details, success flags
- **Outputs:**
  - Log entries written to rotating log files (10MB max, 5 backups)
  - Console output for real-time monitoring

---

### Routers

#### 23. auth_router.py
- **Full Path:** `Final_Project_v003/app_fastapi/routers/auth_router.py`
- **Purpose:** FastAPI router handling all authentication and user management endpoints including signup, login, token management, and admin user CRUD operations with proper role-based access control.
- **Inputs:**
  - User credentials (username, password)
  - Token addition requests
  - User creation/update/delete requests (admin only)
- **Outputs:**
  - JWT access tokens with roles
  - Token balance information
  - User management confirmations
  - Usage logs
  - Success/error responses

#### 24. models_router.py
- **Full Path:** `Final_Project_v003/app_fastapi/routers/models_router.py`
- **Purpose:** FastAPI router for model training, prediction, and management endpoints. All operations are JWT-protected and use token-based payment with automatic refunds on failures.
- **Inputs:**
  - Uploaded CSV files with training configuration
  - Model names and feature dictionaries for prediction
  - Model names for retrieval/deletion
- **Outputs:**
  - Training metadata with performance metrics
  - Prediction results with token deduction
  - Model lists and details
  - Delete confirmations
  - Usage logs and error messages

#### 25. __init__.py
- **Full Path:** `Final_Project_v003/app_fastapi/routers/__init__.py`
- **Purpose:** Package initialization file for routers.
- **Inputs:** None
- **Outputs:** None

---

### Main Application

#### 26. app_fastapi.py
- **Full Path:** `Final_Project_v003/app_fastapi/app_fastapi.py`
- **Purpose:** Main FastAPI application entry point. Configures the FastAPI app, includes routers with prefixes, and provides root and health check endpoints.
- **Inputs:** None (server startup)
- **Outputs:**
  - FastAPI application instance
  - HTTP responses for root and health endpoints
  - Swagger UI documentation at /docs

#### 27. database_manager.py
- **Full Path:** `Final_Project_v003/app_fastapi/database_manager.py`
- **Purpose:** Complete PostgreSQL database management layer with connection pooling, automatic database creation, table management, and all CRUD operations for users and usage logs. Uses context managers for safe connection handling.
- **Inputs:**
  - Database configuration (from environment variables)
  - User data for CRUD operations
  - Usage log data
  - Query parameters
- **Outputs:**
  - Database connections (via context manager)
  - User records and lists
  - Token balance updates
  - Usage log records
  - Admin status checks
  - Success/error messages

#### 28. app_fastapi_app_fastapi.py
- **Full Path:** `Final_Project_v003/app_fastapi/app_fastapi_app_fastapi.py`
- **Purpose:** Alternative FastAPI application file with custom OpenAPI schema configuration for Bearer token authentication in Swagger UI.
- **Inputs:** None (server startup)
- **Outputs:**
  - FastAPI application with enhanced OpenAPI documentation
  - Custom security schemes for JWT Bearer tokens

#### 29. __init__.py
- **Full Path:** `Final_Project_v003/app_fastapi/__init__.py`
- **Purpose:** Package initialization file for FastAPI application.
- **Inputs:** None
- **Outputs:** None

---

## Streamlit Frontend

### Main Application

#### 30. app_streamlit.py
- **Full Path:** `Final_Project_v003/app_streamlit/app_streamlit.py`
- **Purpose:** Main Streamlit application providing authentication UI, server status checking, navigation sidebar, and page routing. Initializes database and manages session state for logged-in users.
- **Inputs:**
  - User credentials for login/signup
  - Page navigation selections
- **Outputs:**
  - Login/signup interface
  - Main application UI with navigation
  - Server connectivity status
  - Session state management

---

### Components

#### 31. api_client.py
- **Full Path:** `Final_Project_v003/app_streamlit/components/api_client.py`
- **Purpose:** API client wrapper class that handles all HTTP requests to the FastAPI backend. Manages JWT tokens in session state, provides methods for authentication, model operations, and admin functions with automatic error handling.
- **Inputs:**
  - API endpoint parameters (username, password, files, model names, etc.)
  - Base URL (defaults to localhost:8000)
- **Outputs:**
  - HTTP response dictionaries
  - Session state updates (tokens, username, admin status)
  - Error messages and status codes

#### 32. utils.py
- **Full Path:** `Final_Project_v003/app_streamlit/components/utils.py`
- **Purpose:** Utility functions for Streamlit components (currently minimal/empty).
- **Inputs:** Various utility function parameters
- **Outputs:** Utility function results

---

### Pages

#### 33. dashboard.py
- **Full Path:** `Final_Project_v003/app_streamlit/pages/dashboard.py`
- **Purpose:** Dashboard page displaying token balance, trained models overview, usage history, and a complete credit card payment form for token purchase (demo - no real charges). Shows activity statistics and model performance metrics.
- **Inputs:**
  - Token purchase amount
  - Credit card details (demo only)
  - User confirmation
- **Outputs:**
  - Token balance metrics
  - Trained models list with expandable details
  - Usage logs table
  - Activity statistics (trains, predictions, tokens spent)
  - Purchase confirmation and balance updates

#### 34. train_page.py
- **Full Path:** `Final_Project_v003/app_streamlit/pages/train_page.py`
- **Purpose:** Model training interface allowing CSV upload, data preview, column selection, model type selection (7 options), and training configuration. Displays comprehensive performance metrics with support for both holdout and cross-validation strategies.
- **Inputs:**
  - CSV file upload
  - Feature and label column selections
  - Model type selection
  - Model name and test size
- **Outputs:**
  - Data preview and shape information
  - Training progress indicators
  - Performance metrics (accuracy, F1, R², RMSE, etc.)
  - Confusion matrix visualization
  - Preprocessing details
  - Token deduction confirmation

#### 35. predict_page.py
- **Full Path:** `Final_Project_v003/app_streamlit/pages/predict_page.py`
- **Purpose:** Prediction interface for selecting trained models and providing feature values. Supports manual input via number fields or JSON import. Shows model information and prediction results with probability distributions.
- **Inputs:**
  - Model selection from dropdown
  - Feature values (via input fields or JSON)
- **Outputs:**
  - Model information display
  - Feature input interface
  - Prediction results
  - Probability distributions (for classification)
  - Token deduction confirmation

#### 36. admin_page.py
- **Full Path:** `Final_Project_v003/app_streamlit/pages/admin_page.py`
- **Purpose:** Comprehensive admin panel (admin role required) for complete user management (create, view, update, delete), token distribution visualization, system activity logs, and model management. Includes safety features like preventing self-deletion.
- **Inputs:**
  - User management selections and forms
  - Filter and sort parameters
  - Deletion confirmations
- **Outputs:**
  - User list table with filters and sorting
  - User creation/update/deletion confirmations
  - Generated JWT tokens for new users
  - Token distribution charts and statistics
  - System-wide activity logs with filtering
  - Model overview and deletion interface

---

### Package Initialization

#### 37. __init__.py
- **Full Path:** `Final_Project_v003/app_streamlit/__init__.py`
- **Purpose:** Package initialization file for Streamlit application.
- **Inputs:** None
- **Outputs:** None

---

## Tests

#### 38. conftest.py
- **Full Path:** `Final_Project_v003/tests/conftest.py`
- **Purpose:** Pytest configuration file that adds project root to Python path ensuring imports work correctly in test files.
- **Inputs:** None (pytest initialization)
- **Outputs:** Modified sys.path for test discovery

#### 39. test_api_endpoints.py
- **Full Path:** `Final_Project_v003/tests/test_api_endpoints.py`
- **Purpose:** Integration tests for FastAPI endpoints including health checks, authentication flows (login success/failure cases), and protected routes. Uses FastAPI TestClient for request simulation.
- **Inputs:**
  - Test credentials and payloads
  - API endpoint paths
- **Outputs:**
  - Test assertions (pass/fail)
  - Coverage of authentication edge cases
  - JWT token validation tests

#### 40. test_model_service.py
- **Full Path:** `Final_Project_v003/tests/test_model_service.py`
- **Purpose:** Comprehensive unit tests for all 7 model types covering training, prediction, metadata validation, and CRUD operations. Uses pytest fixtures for temporary CSV file creation and automatic cleanup.
- **Inputs:**
  - Temporary CSV files (regression and classification)
  - Model configuration parameters
- **Outputs:**
  - Test assertions for all model types
  - Metadata structure validation
  - Prediction accuracy tests
  - Error handling verification
  - Model cleanup confirmation

---

## Root Files

#### 41. run_server.py
- **Full Path:** `Final_Project_v003/run_server.py`
- **Purpose:** Simple script containing the uvicorn command to start the FastAPI server. Serves as documentation for the server startup command.
- **Inputs:** None
- **Outputs:** Server startup command (comment only)

#### 42. setup_admin.py
- **Full Path:** `Final_Project_v003/setup_admin.py`
- **Purpose:** Interactive CLI tool for setting up admin users. Lists all users, allows granting/revoking admin privileges, and provides confirmation prompts for safety. Ensures database tables exist before operations.
- **Inputs:**
  - Username selection
  - Confirmation prompts (yes/no)
- **Outputs:**
  - User list with admin status
  - Admin privilege grant/revoke confirmations
  - Database update confirmations
  - Instructions for logout/login

#### 43. demo_model_architecture.py
- **Full Path:** `Final_Project_v003/demo_model_architecture.py`
- **Purpose:** Demonstration script showcasing the multi-model architecture. Creates sample datasets, trains Linear Regression and Logistic Regression models, makes predictions, and displays the MODEL_REGISTRY with all supported models.
- **Inputs:** None (generates sample data internally)
- **Outputs:**
  - Console output showing training results
  - Prediction examples
  - Model registry listing
  - Performance metrics
  - Automatic model cleanup

---

## Summary Statistics

### By Category:
- **FastAPI Core:** 5 files
- **FastAPI Services (Models):** 11 files
- **FastAPI Services (Business Logic):** 6 files
- **FastAPI Routers:** 3 files
- **FastAPI Main:** 3 files
- **Streamlit Components:** 2 files
- **Streamlit Pages:** 4 files
- **Streamlit Main:** 1 file
- **Streamlit Package:** 1 file
- **Tests:** 3 files
- **Root Scripts:** 3 files
- **Package Init Files:** 1 file

### By Functionality:
- **Model Architecture:** 11 files (base_model, config, 7 model wrappers, 2 evaluation modules)
- **Data Processing:** 3 files (data_handler, preprocessing, model_manager)
- **Authentication & Security:** 4 files (user_service, jwt_handler, auth_dependency, token_service)
- **API Layer:** 3 files (2 routers, main app)
- **UI Layer:** 7 files (main app, 4 pages, 2 components)
- **Database:** 1 file (database_manager)
- **Utilities & Tools:** 5 files (logger, setup_admin, demo, run_server, tests)
- **Package Management:** 9 files (__init__.py files)

### Key Architectural Patterns:
1. **Dispatcher Pattern:** MODEL_REGISTRY dynamically routes to model implementations
2. **Template Pattern:** base_model.py provides unified training/prediction for all models
3. **Service Layer:** Business logic separated from routing and data access
4. **Pipeline Pattern:** Sklearn pipelines prevent data leakage in preprocessing
5. **Repository Pattern:** database_manager encapsulates all database operations
6. **Dependency Injection:** FastAPI Depends() for JWT authentication
7. **Factory Pattern:** model_service dispatches to appropriate model modules

---

## Notes

- All file paths use the project root as the base: `Final_Project_v003/`
- The architecture follows clean separation: Core (ML logic) → Services (business logic) → Routers (API) → Frontend (UI)
- Token-based payment system ensures fair resource usage
- Comprehensive logging tracks all operations for audit trails
- Role-based access control (admin vs. user) protects sensitive operations
- Automatic refunds on failures ensure users aren't charged for failed operations
- The system supports 7 ML models: Linear/Logistic Regression, Decision Tree, Random Forest, KNN, SVM, Kernel SVM

---

*Generated on 2025-11-17*
*Total Python Files Documented: 43*
