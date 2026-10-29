# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- Unregister from activities
- Comprehensive test coverage with pytest

## Getting Started

1. Install the dependencies:

   ```
   pip install -r ../requirements.txt
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## Running Tests

The project includes a comprehensive test suite using pytest and the AAA (Arrange-Act-Assert) pattern.

### Install Test Dependencies

Tests require pytest, which can be installed with:

```bash
pip install pytest
```

Or install all dependencies (including test dependencies):

```bash
pip install -r ../requirements.txt
```

### Run Tests

From the project root directory, run:

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests in a specific test class
pytest tests/test_app.py::TestSignupEndpoint -v

# Run a specific test
pytest tests/test_app.py::TestSignupEndpoint::test_signup_success -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Structure

The test suite is organized into test classes by endpoint:

- **TestGetActivities** (3 tests) - Tests for GET `/activities` endpoint
- **TestSignupEndpoint** (5 tests) - Tests for POST `/signup` endpoint
- **TestUnregisterEndpoint** (5 tests) - Tests for DELETE `/unregister` endpoint
- **TestEdgeCasesAndValidation** (6 tests) - Edge cases and validation scenarios

**Total: 19 comprehensive tests**

Each test follows the **AAA (Arrange-Act-Assert)** pattern:

```python
def test_signup_success():
    # ARRANGE: Set up test data
    test_email = "student@mergington.edu"
    test_activity = "Chess Club"
    
    # ACT: Execute the action
    response = client.post(
        f"/activities/{test_activity}/signup",
        params={"email": test_email}
    )
    
    # ASSERT: Verify the results
    assert response.status_code == 200
    assert test_email in app.activities[test_activity]["participants"]
```

### Test Coverage

Tests cover:

- ✅ Successful operations (signup, unregister, list activities)
- ✅ Error cases (duplicate signup, activity not found, participant not found)
- ✅ Edge cases (special characters, case sensitivity, multiple signups)
- ✅ Data integrity (participant lists, availability counts)
- ✅ State management (test isolation with automatic fixture reset)

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister from an activity                                    |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Email address

All data is stored in memory, which means data will be reset when the server restarts.

