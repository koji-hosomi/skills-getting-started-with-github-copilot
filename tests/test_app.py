"""
API endpoint tests for the Mergington High School Activities application.
Tests follow the AAA (Arrange-Act-Assert) pattern for clarity and maintainability.
"""

import pytest
from src.app import app, activities


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_success(self, client):
        """Test that activities endpoint returns all activities with correct structure"""
        # ARRANGE
        expected_activity_keys = {"description", "schedule", "max_participants", "participants"}
        
        # ACT
        response = client.get("/activities")
        data = response.json()
        
        # ASSERT
        assert response.status_code == 200
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data
        assert set(data["Chess Club"].keys()) == expected_activity_keys
    
    def test_get_activities_returns_participant_counts(self, client):
        """Test that activities include participant lists"""
        # ARRANGE
        # No setup needed - activities fixture provides default data
        
        # ACT
        response = client.get("/activities")
        data = response.json()
        
        # ASSERT
        assert response.status_code == 200
        assert "Chess Club" in data
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
        assert len(data["Chess Club"]["participants"]) == 2
    
    def test_get_activities_empty_participant_list(self, client):
        """Test that activities with no participants have empty list"""
        # ARRANGE
        # Basketball Club starts with empty participants list
        
        # ACT
        response = client.get("/activities")
        data = response.json()
        
        # ASSERT
        assert response.status_code == 200
        assert "Basketball Club" in data
        assert isinstance(data["Basketball Club"]["participants"], list)
        assert len(data["Basketball Club"]["participants"]) == 0


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client):
        """Test successful signup for an activity"""
        # ARRANGE
        test_email = "newstudent@mergington.edu"
        test_activity = "Basketball Club"
        
        # ACT
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert test_email in activities[test_activity]["participants"]
        assert response.json()["message"] == f"Signed up {test_email} for {test_activity}"
    
    def test_signup_duplicate_fails(self, client):
        """Test that duplicate signup is rejected"""
        # ARRANGE
        test_email = "michael@mergington.edu"  # Already signed up for Chess Club
        test_activity = "Chess Club"
        
        # ACT
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_activity_not_found(self, client):
        """Test that signup fails for non-existent activity"""
        # ARRANGE
        test_email = "student@mergington.edu"
        test_activity = "Nonexistent Club"
        
        # ACT
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_adds_to_participants_list(self, client):
        """Test that signup properly adds email to participants list"""
        # ARRANGE
        test_email = "alice@mergington.edu"
        test_activity = "Art Club"
        initial_count = len(activities[test_activity]["participants"])
        
        # ACT
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert len(activities[test_activity]["participants"]) == initial_count + 1
        assert activities[test_activity]["participants"][-1] == test_email
    
    def test_signup_multiple_students_different_activities(self, client):
        """Test that multiple students can sign up for different activities"""
        # ARRANGE
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # ACT
        response1 = client.post(f"/activities/{activity1}/signup", params={"email": email1})
        response2 = client.post(f"/activities/{activity2}/signup", params={"email": email2})
        
        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email1 in activities[activity1]["participants"]
        assert email2 in activities[activity2]["participants"]


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client):
        """Test successful unregistration from an activity"""
        # ARRANGE
        test_email = "michael@mergington.edu"
        test_activity = "Chess Club"
        assert test_email in activities[test_activity]["participants"]
        
        # ACT
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert test_email not in activities[test_activity]["participants"]
        assert response.json()["message"] == f"Unregistered {test_email} from {test_activity}"
    
    def test_unregister_participant_not_found(self, client):
        """Test that unregister fails for non-existent participant"""
        # ARRANGE
        test_email = "nonexistent@mergington.edu"
        test_activity = "Chess Club"
        
        # ACT
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()
    
    def test_unregister_activity_not_found(self, client):
        """Test that unregister fails for non-existent activity"""
        # ARRANGE
        test_email = "student@mergington.edu"
        test_activity = "Nonexistent Club"
        
        # ACT
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_removes_from_participants_list(self, client):
        """Test that unregister properly removes email from participants list"""
        # ARRANGE
        test_email = "emma@mergington.edu"
        test_activity = "Programming Class"
        initial_count = len(activities[test_activity]["participants"])
        assert test_email in activities[test_activity]["participants"]
        
        # ACT
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert len(activities[test_activity]["participants"]) == initial_count - 1
        assert test_email not in activities[test_activity]["participants"]
    
    def test_unregister_then_signup_again(self, client):
        """Test that a student can signup again after unregistering"""
        # ARRANGE
        test_email = "john@mergington.edu"
        test_activity = "Gym Class"
        
        # ACT - Unregister
        unregister_response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        
        # ACT - Sign up again
        signup_response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # ASSERT
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        assert test_email in activities[test_activity]["participants"]


class TestEdgeCasesAndValidation:
    """Tests for edge cases and validation scenarios"""
    
    def test_signup_with_special_characters_in_email(self, client):
        """Test signup with special characters in email"""
        # ARRANGE
        test_email = "student+tag@mergington.edu"
        test_activity = "Track and Field"
        
        # ACT
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert test_email in activities[test_activity]["participants"]
    
    def test_signup_activity_name_with_spaces(self, client):
        """Test signup with activity name containing spaces"""
        # ARRANGE
        test_email = "student@mergington.edu"
        test_activity = "Basketball Club"
        
        # ACT
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert test_email in activities[test_activity]["participants"]
    
    def test_signup_multiple_to_same_activity(self, client):
        """Test that multiple different students can sign up for same activity"""
        # ARRANGE
        email1 = "alice@mergington.edu"
        email2 = "bob@mergington.edu"
        email3 = "charlie@mergington.edu"
        test_activity = "Science Club"
        initial_count = len(activities[test_activity]["participants"])
        
        # ACT
        response1 = client.post(f"/activities/{test_activity}/signup", params={"email": email1})
        response2 = client.post(f"/activities/{test_activity}/signup", params={"email": email2})
        response3 = client.post(f"/activities/{test_activity}/signup", params={"email": email3})
        
        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert len(activities[test_activity]["participants"]) == initial_count + 3
        assert email1 in activities[test_activity]["participants"]
        assert email2 in activities[test_activity]["participants"]
        assert email3 in activities[test_activity]["participants"]
    
    def test_case_sensitive_email_signup(self, client):
        """Test that email signup is case-sensitive for duplicate detection"""
        # ARRANGE
        test_activity = "Drama Club"
        email_lowercase = "newstudent@mergington.edu"
        email_uppercase = "NEWSTUDENT@MERGINGTON.EDU"
        
        # ACT
        response1 = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": email_lowercase}
        )
        response2 = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": email_uppercase}
        )
        
        # ASSERT - Both should succeed as emails are treated case-sensitively
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email_lowercase in activities[test_activity]["participants"]
        assert email_uppercase in activities[test_activity]["participants"]
    
    def test_availability_count_after_signup(self, client):
        """Test that availability spot count decreases after signup"""
        # ARRANGE
        test_email = "student@mergington.edu"
        test_activity = "Debate Club"
        
        # ACT - Get activities before signup
        response_before = client.get("/activities")
        data_before = response_before.json()
        spots_before = data_before[test_activity]["max_participants"] - len(data_before[test_activity]["participants"])
        
        # ACT - Signup
        client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # ACT - Get activities after signup
        response_after = client.get("/activities")
        data_after = response_after.json()
        spots_after = data_after[test_activity]["max_participants"] - len(data_after[test_activity]["participants"])
        
        # ASSERT
        assert spots_after == spots_before - 1
    
    def test_unregister_increases_availability(self, client):
        """Test that availability spots increase after unregistration"""
        # ARRANGE
        test_email = "daniel@mergington.edu"
        test_activity = "Chess Club"
        
        # ACT - Get activities before unregister
        response_before = client.get("/activities")
        data_before = response_before.json()
        spots_before = data_before[test_activity]["max_participants"] - len(data_before[test_activity]["participants"])
        
        # ACT - Unregister
        client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        
        # ACT - Get activities after unregister
        response_after = client.get("/activities")
        data_after = response_after.json()
        spots_after = data_after[test_activity]["max_participants"] - len(data_after[test_activity]["participants"])
        
        # ASSERT
        assert spots_after == spots_before + 1
