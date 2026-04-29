"""Integration tests for main API endpoints"""

from fastapi.testclient import TestClient


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities(self, client):
        """Test that GET /activities returns all 9 activities"""
        response = client.get("/activities")
        assert response.status_code == 200

        activities = response.json()
        assert len(activities) == 9

        # Verify expected activities exist
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Swimming Club",
            "Drama Club",
            "Art Workshop",
            "Robotics Club",
            "Debate Team",
        ]
        for activity in expected_activities:
            assert activity in activities

    def test_activity_has_required_fields(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities = response.json()

        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_for_existing_activity(self, client):
        """Test successful signup for an existing activity"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newman1@mergington.edu"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "newman1@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant to the activity"""
        email = "newman2@mergington.edu"
        
        # Sign up for an activity
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200

        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities["Programming Class"]["participants"]
        assert email in participants

    def test_signup_for_multiple_activities(self, client):
        """Test that a student can sign up for multiple activities"""
        email = "newman3@mergington.edu"

        # Sign up for first activity
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200

        # Sign up for second activity
        response2 = client.post(
            "/activities/Drama Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 200

        # Verify both signups succeeded
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Drama Club"]["participants"]


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """Test that GET / redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307

        # Check redirect location
        assert "location" in response.headers
        assert "/static/index.html" in response.headers["location"]
