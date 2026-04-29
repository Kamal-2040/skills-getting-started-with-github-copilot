"""Integration tests for unregister endpoint"""


class TestUnregisterEndpoint:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_from_activity(self, client):
        """Test that a student can unregister from an activity"""
        email = "teststudent1@mergington.edu"

        # First, sign up for an activity
        signup_response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200

        # Verify signup was successful
        activities = client.get("/activities").json()
        assert email in activities["Chess Club"]["participants"]

        # Now unregister
        unregister_response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200

        # Verify unregister was successful
        activities = client.get("/activities").json()
        assert email not in activities["Chess Club"]["participants"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant"""
        email = "teststudent2@mergington.edu"

        # Sign up
        client.post(
            "/activities/Basketball Team/signup",
            params={"email": email}
        )

        # Get initial participant count
        activities = client.get("/activities").json()
        initial_count = len(activities["Basketball Team"]["participants"])

        # Unregister
        response = client.post(
            "/activities/Basketball Team/unregister",
            params={"email": email}
        )
        assert response.status_code == 200

        # Get updated participant count
        activities = client.get("/activities").json()
        final_count = len(activities["Basketball Team"]["participants"])

        # Verify count decreased by 1
        assert final_count == initial_count - 1

    def test_unregister_from_multiple_activities(self, client):
        """Test that a student can independently unregister from different activities"""
        email = "teststudent3@mergington.edu"

        # Sign up for two activities
        client.post(
            "/activities/Swimming Club/signup",
            params={"email": email}
        )
        client.post(
            "/activities/Robotics Club/signup",
            params={"email": email}
        )

        # Verify both signups
        activities = client.get("/activities").json()
        assert email in activities["Swimming Club"]["participants"]
        assert email in activities["Robotics Club"]["participants"]

        # Unregister from one activity
        response = client.post(
            "/activities/Swimming Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200

        # Verify unregistered from one but still in the other
        activities = client.get("/activities").json()
        assert email not in activities["Swimming Club"]["participants"]
        assert email in activities["Robotics Club"]["participants"]
