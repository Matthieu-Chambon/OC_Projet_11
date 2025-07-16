from server import pointsDisplay, app
import server
import pytest

class TestPointsDisplay:
    """
    Test cases for displaying points for clubs.
    """
    def test_points_display(self, mocker):
        with app.test_request_context(
            '/pointsDisplay', method='GET'
        ):
            mocker.patch(
                'server.clubs', 
                [
                    {
                        "name": "Club A",
                        "email": "clubA@example.com",
                        "points":"10"
                    }
                ]
            )
            
            mock_render = mocker.patch('server.render_template', return_value='mocked_template')
            
            response = pointsDisplay()
            
            assert response == 'mocked_template'
            
            mock_render.assert_called_once_with(
                'points_display.html',
                clubs=server.clubs
            )