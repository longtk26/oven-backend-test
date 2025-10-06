# Product Management & File Upload API

A Django REST API for product management and file uploads with custom HashMap implementation and hierarchical file tree structure.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture & Design](#architecture--design)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Development Commands](#development-commands)
- [Testing](#testing)
- [Custom Data Structures](#custom-data-structures)
- [Configuration](#configuration)
- [Docker Deployment](#docker-deployment)

## Project Overview

This project implements a comprehensive RESTful API for:

- **Product Management**: Full CRUD operations for products with validation and error handling
- **File Upload System**: Advanced file upload with hierarchical organization up to 5 levels deep
- **Custom Data Structures**: From-scratch HashMap implementation for efficient file tree operations
- **Product-File Associations**: Link files to products with metadata tracking

## Architecture & Design

The application follows Clean Architecture principles with clear separation of concerns:

### Design Patterns
- **Repository Pattern**: Data access abstraction layer
- **Service Layer Pattern**: Business logic encapsulation
- **Factory Pattern**: Dependency injection and service creation
- **Decorator Pattern**: Request/response validation

### Layers
1. **Presentation Layer**: Views and serializers for API endpoints
2. **Business Logic Layer**: Services containing domain logic
3. **Data Access Layer**: Repositories for database operations
4. **Model Layer**: Django models representing data entities

## Technology Stack

### Core Framework
- **Django 5.2.7**: Web framework
- **Django REST Framework 3.16.0**: RESTful API toolkit
- **PostgreSQL**: Primary database with Docker support
- **Python 3.10**: Programming language

### Development Tools
- **uv**: Fast Python package manager
- **Docker & Docker Compose**: Containerization
- **Pydantic Settings**: Configuration management
- **Custom HashMap**: No external dependencies implementation

### Testing
- **Django Test Framework**: Unit and integration testing
- **Mock**: Test isolation and dependency mocking

## Project Structure

```
backend-test/
├── apis/                          # Main Django application
│   ├── config/                    # Configuration management
│   │   ├── config.py              # Pydantic settings
│   │   └── __init__.py
│   ├── exceptions/                # Custom exceptions
│   │   ├── exceptions.py          # Exception classes
│   │   ├── exception_handler.py   # Global exception handler
│   │   ├── error_codes.py         # Error code enums
│   │   └── __init__.py
│   ├── models/                    # Database models
│   │   ├── products_model.py      # Product entity
│   │   ├── files_model.py         # File storage entity
│   │   ├── product_files_model.py # Many-to-many relationship
│   │   └── __init__.py
│   ├── repositories/              # Data access layer
│   │   ├── products_repository.py # Product data operations
│   │   ├── files_repository.py    # File data operations
│   │   └── __init__.py
│   ├── serializer/                # Request/response validation
│   │   ├── products_serializer.py # Product API schemas
│   │   ├── files_serializer.py    # File API schemas
│   │   └── __init__.py
│   ├── service/                   # Business logic layer
│   │   ├── products_service.py    # Product business logic
│   │   ├── files_service.py       # File business logic
│   │   ├── test_products_service.py # Service unit tests
│   │   └── __init__.py
│   ├── views/                     # API endpoints
│   │   ├── products_view.py       # Product CRUD endpoints
│   │   ├── files_view.py          # File upload endpoints
│   │   └── __init__.py
│   ├── routes/                    # URL routing
│   │   ├── products_route.py      # Product URLs
│   │   ├── files_route.py         # File URLs
│   │   └── __init__.py
│   ├── migrations/                # Database migrations
│   ├── factory.py                 # Dependency injection factory
│   ├── apps.py                    # Django app configuration
│   └── __init__.py
├── libs/                          # Custom libraries
│   ├── hashmap/                   # Custom HashMap implementation
│   │   ├── hashmap.py             # HashMap class with chaining
│   │   ├── test_hashmap.py        # Comprehensive HashMap tests
│   │   └── __init__.py
│   ├── file_tree/                 # File tree structure
│   │   ├── file_tree.py           # Tree implementation using HashMap
│   │   └── __init__.py
│   ├── repositories/              # Base repository classes
│   │   ├── base_repository.py     # Common database operations
│   │   └── __init__.py
│   ├── decorators/                # Custom decorators
│   │   ├── serializer_decorator.py # Validation decorators
│   │   └── __init__.py
│   ├── serializer/                # Common serializers
│   │   ├── paginate_serializer.py # Pagination schemas
│   │   └── __init__.py
│   ├── response.py                # Response utilities
│   └── __init__.py
├── core/                          # Django project configuration
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Root URL configuration
│   ├── wsgi.py                    # WSGI application
│   ├── asgi.py                    # ASGI application
│   ├── color_log_format.py        # Custom logging formatter
│   └── __init__.py
├── local_files/                   # File upload storage
├── docker-compose.yml             # Docker services configuration
├── Dockerfile                     # Multi-stage container build
├── Makefile                       # Development commands
├── requirements.txt               # Python dependencies
├── manage.py                      # Django management script
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore patterns
└── .dockerignore                  # Docker ignore patterns
```

## Features

### ✅ Core Features

#### Product Management
- **Create Product**: Add new products with name, description, and price
- **List Products**: Paginated product listing with search and filtering
- **Get Product**: Retrieve detailed product information
- **Update Product**: Partial product updates using PATCH
- **Delete Product**: Soft or hard delete operations

#### File Management
- **File Upload**: Single file upload with folder organization
- **Tree Structure**: Hierarchical file organization (max 5 levels)
- **Product Association**: Link files to specific products
- **File Validation**: Size limits (50MB), type detection, and security checks
- **Storage Management**: Local file storage with path organization

#### Data Structures
- **Custom HashMap**: Complete implementation with dynamic resizing
- **File Tree**: Efficient tree structure using HashMap for O(1) lookups
- **Collision Handling**: Chain-based collision resolution

### ✅ Advanced Features

#### API Design
- **RESTful Endpoints**: Standard HTTP methods and status codes
- **Request Validation**: Comprehensive input validation with error messages
- **Response Serialization**: Consistent JSON response format
- **Error Handling**: Global exception handling with custom error codes

#### Data Management
- **Pagination**: Configurable page size and navigation
- **Search & Filtering**: Multi-field search capabilities
- **Database Indexing**: Optimized queries with proper indexes
- **Transactions**: ACID compliance for data integrity

## API Endpoints

### Products API
```
POST   /api/products           # Create product
GET    /api/products           # List products (paginated)
GET    /api/products/{id}      # Get product details
PATCH  /api/products/{id}      # Update product
DELETE /api/products/{id}      # Delete product
```

### Files API
```
POST   /api/files/upload       # Upload file with optional product association
```

### Request/Response Examples

#### Create Product
```bash
POST /api/products
Content-Type: application/json

{
  "name": "Sample Product",
  "description": "A comprehensive product description",
  "price": "29.99"
}
```

#### Upload File
```bash
POST /api/files/upload
Content-Type: multipart/form-data

form-data:
  file: [binary file data]
  folder_path: "documents/2024"
  product_id: "550e8400-e29b-41d4-a716-446655440000"
  file_type: "documentation"
```

## Prerequisites

Before setting up the project, ensure you have:

- **Python 3.10+**: Required for the Django application
- **uv**: Fast Python package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Docker & Docker Compose**: For containerized database
- **PostgreSQL**: Database (via Docker or local installation)
- **Git**: Version control

### Installing uv

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip
pip install uv
```

## Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd backend-test
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your database credentials
# DB_NAME=backend_test_db
# DB_USER=postgres
# DB_PASSWORD=your_secure_password
# DB_HOST=localhost
# DB_PORT=5432
```

### 3. Install Dependencies
```bash
# Install Python dependencies using uv
uv sync

# Or install from requirements.txt
uv pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Start PostgreSQL with Docker
docker-compose up -d db

# Wait for database to be ready, then run migrations
make mgup
```

### 5. Run Application
```bash
# Start development server
make run

# Or manually
uv run python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Development Commands

The project includes a Makefile with common development tasks:

```bash
# Database Operations
make newmg          # Create new migrations
make mgup           # Apply migrations

# Development
make run            # Start development server
make test           # Run all tests

# Individual commands (using uv)
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py runserver
uv run python manage.py test
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test modules
uv run python manage.py test libs.hashmap.test_hashmap
uv run python manage.py test apis.service.test_products_service
uv run python manage.py test libs.file_tree

# Run with verbose output
uv run python manage.py test --verbosity=2
```

### Test Coverage

The project includes comprehensive tests for:

- **HashMap Implementation**: All operations, edge cases, collision handling
- **Product Service**: CRUD operations, validation, error scenarios
- **File Tree Structure**: Tree operations, depth limits, path handling
- **API Endpoints**: Request validation, response formatting
- **Repository Layer**: Database operations, error handling

### Test Structure
```
tests/
├── libs/hashmap/test_hashmap.py      # HashMap unit tests
├── apis/service/test_products_service.py # Service layer tests
└── [additional test files]
```

## Custom Data Structures

### HashMap Implementation

**Location**: `libs/hashmap/hashmap.py`

A complete HashMap implementation built from scratch with:

#### Features
- **Dynamic Resizing**: Automatically doubles capacity when load factor exceeds 0.75
- **Collision Resolution**: Chaining with linked lists for handling hash collisions
- **Hash Function**: Custom string-based hash function with good distribution
- **Full API**: `put()`, `get()`, `remove()`, `contains()`, `keys()`, `values()`, `items()`

#### Performance
- **Average Time Complexity**: O(1) for all core operations
- **Worst Case**: O(n) when many collisions occur
- **Space Complexity**: O(n) where n is the number of elements

#### Usage Example
```python
from libs.hashmap import HashMap

# Create HashMap
hashmap = HashMap()

# Basic operations
hashmap.put("key1", "value1")
value = hashmap.get("key1")
hashmap.remove("key1")

# Utility methods
keys = hashmap.keys()
values = hashmap.values()
items = hashmap.items()
```

### File Tree Structure

**Location**: `libs/file_tree/file_tree.py`

Hierarchical file organization using the custom HashMap:

#### Features
- **Tree Structure**: Support for nested folders up to 5 levels deep
- **Fast Lookups**: O(1) file access using HashMap indexing
- **Path Management**: Automatic parent directory creation
- **JSON Export**: Complete tree structure in JSON format

#### Usage Example
```python
from libs.file_tree import FileTreeStructure

# Create file tree
tree = FileTreeStructure(max_depth=5)

# Add files
tree.add_file("documents/2024/report.pdf", file_size=1024)
tree.add_file("images/logo.png", file_size=2048)

# Get tree structure
structure = tree.to_tree_dict()
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Database Configuration
DB_NAME=backend_test_db
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432
```

### Django Settings

Key configuration in `core/settings.py`:

- **Database**: PostgreSQL with connection pooling
- **File Storage**: Local file system with configurable paths
- **Logging**: Colored console output with custom formatter
- **REST Framework**: Custom exception handling and pagination

## Docker Deployment

### Development with Docker

```bash
# Start all services
docker-compose up

# Start only database
docker-compose up -d db

# Build and run application
docker-compose up --build backend
```

### Production Deployment

The included `Dockerfile` uses multi-stage builds for optimized production images:

1. **Builder Stage**: Installs dependencies and compiles packages
2. **Production Stage**: Minimal runtime image with security best practices

```bash
# Build production image
docker build -t product-api:latest .

# Run with environment variables
docker run -d \
  --name product-api \
  -p 8000:8000 \
  --env-file .env \
  product-api:latest
```

### Docker Features
- **Multi-stage builds** for smaller production images
- **Non-root user** for enhanced security
- **Health checks** for container monitoring
- **Volume mounting** for persistent file storage

