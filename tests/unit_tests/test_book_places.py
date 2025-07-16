from server import purchasePlaces, app
import server
import pytest

class TestBookPlaces:
    """
    Test cases for booking places in competitions.
    """
    @pytest.fixture()
    def setup_method(self, mocker):
        mocker.patch(
            'server.competitions', 
            [
                {
                    'name': 'Competition A',
                    'date': '2020-03-27 10:00:00',
                    'numberOfPlaces': '20'
                }
            ]
        )
        
        mocker.patch(
            'server.clubs', 
            [
                {
                    'name': 'Club 1',
                    'email': 'club-1@email.com',
                    'points': '15'
                }
            ]
        )
        
        self.mock_template = mocker.patch('server.render_template')
        self.mock_flash = mocker.patch('server.flash')
        
        self.mock_open = mocker.mock_open()
        mocker.patch('builtins.open', self.mock_open)
        mocker.patch('json.dump')

    def test_book_places_success(self, setup_method):
        with app.test_request_context(
            '/purchasePlaces', method='POST', data={
                'competition': 'Competition A',
                'club': 'Club 1',
                'places': '2'
            }
        ):

            response = purchasePlaces()
            
            assert server.clubs[0]['points'] == '13'
            self.mock_template.assert_called_once_with(
                'welcome.html',
                club=server.clubs[0],
                competitions=server.competitions
            )
            self.mock_flash.assert_called_once_with("Great-booking complete!")

    def test_book_places_not_enough_points(self, setup_method):
        with app.test_request_context(
            '/purchasePlaces', method='POST', data={
                'competition': 'Competition A',
                'club': 'Club 1',
                'places': '16'
            }
        ):
            response = purchasePlaces()
            
            assert server.clubs[0]['points'] == '15'
            self.mock_template.assert_called_once_with(
                'booking.html',
                club=server.clubs[0],
                competition=server.competitions[0],
                total_places_booked=0
            )
            self.mock_flash.assert_called_once_with('You do not have enough points to book this competition.')
            
    def test_book_places_negative_number(self, setup_method):
        with app.test_request_context(
            '/purchasePlaces', method='POST', data={
                'competition': 'Competition A',
                'club': 'Club 1',
                'places': '-2'
            }
        ):
            response = purchasePlaces()

            assert server.clubs[0]['points'] == '15'
            self.mock_template.assert_called_once_with(
                'booking.html',
                club=server.clubs[0],
                competition=server.competitions[0],
                total_places_booked=0
            )
            self.mock_flash.assert_called_once_with('You must book at least one place.')
    
    def test_book_more_than_12_places(self, setup_method):
        pass
        with app.test_request_context(
            '/purchasePlaces', method='POST', data={
                'competition': 'Competition A',
                'club': 'Club 1',
                'places': '15'
            }
        ):
            response = purchasePlaces()
            
            assert server.clubs[0]['points'] == '15'
            self.mock_template.assert_called_once_with(
                'booking.html',
                club=server.clubs[0],
                competition=server.competitions[0],
                total_places_booked=0
            )
            self.mock_flash.assert_called_once_with('You cannot book more than 12 places for a single competition.')
            

class TestGetPlacesBooked:
    """
    Test cases for the total_places_booked() function.
    """
    @pytest.fixture()
    def setup_method(self, mocker):
        mocker.patch(
            'server.competitions', 
            [
                {
                    'name': 'Competition A',
                    'date': '2020-03-27 10:00:00',
                    'numberOfPlaces': '20'
                },
                {
                    'name': 'Competition B',
                    'date': '2020-04-15 12:00:00',
                    'numberOfPlaces': '30',
                    'bookings': [
                        {
                            'club': 'Club 1',
                            'places': 10
                        }
                    ]
                }
            ]
        )
        
        mocker.patch(
            'server.clubs', 
            [
                {
                    'name': 'Club 1',
                    'email': 'club-1@email.com',
                    'points': '15'
                }
            ]
        )
    
    def test_get_places_booked_no_booking(self, setup_method):
        assert server.total_places_booked(server.competitions[0], server.clubs[0]) == 0
        assert "bookings" in server.competitions[0]
        assert server.competitions[0]["bookings"] == []
        
    def test_get_places_booked_with_booking(self, setup_method):
        assert server.total_places_booked(server.competitions[1], server.clubs[0]) == 10
