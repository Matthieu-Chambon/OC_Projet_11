from server import showSummary, app
import server

class TestAuthentication:

    def test_valid_email_returns_welcome(self, mocker):
        with app.test_request_context(
            '/showSummary', method='POST', data={'email': 'john@simplylift.co'}
        ):
            mocker.patch(
                'server.clubs', 
                [
                    {"name": "Simply Lift",
                     "email": "john@simplylift.co",
                     "points":"13"}
                ]
            )
            mocker.patch('server.competitions', [])
            
            mock_render = mocker.patch('server.render_template', return_value='mocked_template')

            response = showSummary()
            
            assert response == 'mocked_template'

            mock_render.assert_called_once_with(
                'welcome.html',
                club={"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
                competitions=[]
            )
        
    def test_invalid_email_redirects_with_flash(self, mocker):
        with app.test_request_context(
            '/showSummary', method='POST', data={'email': 'invalid@email.com'}
        ):
            mocker.patch('server.clubs', [])
            mocker.patch('server.competitions', [])
            mock_flash = mocker.patch('server.flash')
            mock_redirect = mocker.patch('server.redirect')
            mock_url_for = mocker.patch('server.url_for', return_value='/')
            
            response = showSummary()
            
            assert response == mock_redirect.return_value

            mock_flash.assert_called_once_with("Adresse email inconnue, veuillez réessayer.")
            mock_redirect.assert_called_once_with(mock_url_for.return_value)