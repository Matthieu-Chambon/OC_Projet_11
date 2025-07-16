import server

class TestPointsDisplay:
    def test_points_display(self):
        app = server.app.test_client()
        response = app.get(
            '/pointsDisplay',
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Points display for all clubs" in response.data
