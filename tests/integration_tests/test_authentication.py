import server

class TestAuthentication:
    def test_authenticate_with_valid_email(self):
        app = server.app.test_client()
        response = app.post(
            '/showSummary',
            data={'email': 'john@simplylift.co'},
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert b"Welcome, john@simplylift.co" in response.data
        
        
    def test_authenticate_with_invalid_email(self):
        app = server.app.test_client()
        response = app.post(
            '/showSummary',
            data={'email': 'invalid@email.com'},
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert "Adresse email inconnue, veuillez réessayer.".encode("utf-8") in response.data