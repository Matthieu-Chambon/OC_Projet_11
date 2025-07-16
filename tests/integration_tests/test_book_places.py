import server
import shutil
import json
import time


class TestBookPlaces:
    def setup_class(cls):
        """
        Load original data from JSON files before running tests.
        """
        with open('clubs.json', 'r') as f:
            clubs_data = json.load(f)
            clubs = clubs_data['clubs']
            cls.original_club = clubs[0]
            
        with open('competitions.json', 'r') as f:
            competitions_data = json.load(f)
            competitions = competitions_data['competitions']
            cls.original_competition = competitions[0]
    
    def setup_method(self):
        """
        Create a backup of the clubs.json file before each test.
        """
        shutil.copyfile('clubs.json', 'clubs_backup.json')
        shutil.copyfile('competitions.json', 'competitions_backup.json')
        server.clubs = server.loadClubs()

    def teardown_method(self):
        """
        Restore the original clubs.json file after each test.
        """
        shutil.move('clubs_backup.json', 'clubs.json')
        shutil.move('competitions_backup.json', 'competitions.json')
        
    def test_book_places_success(self):
        """
        Test booking places successfully and check if points are deducted correctly.
        """
        app = server.app.test_client()
        response = app.post('/purchasePlaces', data={
            'competition': self.original_competition['name'],
            'club': self.original_club['name'],
            'places': '1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data
        assert server.clubs[0]['points'] == str(int(self.original_club['points']) - 1)
        
        with open('clubs.json', 'r') as f:
            clubs_data = json.load(f)
            clubs = clubs_data['clubs']
            club = clubs[0]
            assert club['points'] == str(int(self.original_club['points']) - 1)
            
    def test_book_places_not_enough_points(self):
        """
        Test booking places when the club does not have enough points.
        """
        app = server.app.test_client()
        response = app.post('/purchasePlaces', data={
            'competition': self.original_competition['name'],
            'club': self.original_club['name'],
            'places': str(int(self.original_club['points']) + 1)
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b"You do not have enough points to book this competition." in response.data
        assert server.clubs[0]['points'] == self.original_club['points']
        
        with open('clubs.json', 'r') as f:
            clubs_data = json.load(f)
            clubs = clubs_data['clubs']
            club = clubs[0]
            assert club['points'] == self.original_club['points']
    
    def test_book_places_negative_number(self):
        """
        Test booking places with a negative number of places.
        """
        app = server.app.test_client()
        response = app.post('/purchasePlaces', data={
            'competition': self.original_competition['name'],
            'club': self.original_club['name'],
            'places': '-1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b"You must book at least one place." in response.data
        assert server.clubs[0]['points'] == self.original_club['points']
        
        with open('clubs.json', 'r') as f:
            clubs_data = json.load(f)
            clubs = clubs_data['clubs']
            club = clubs[0]
            assert club['points'] == self.original_club['points']
    
    def test_book_more_than_12_places(self):
        """
        Test booking more than 12 places for a single competition.
        """
        app = server.app.test_client()
        response = app.post('/purchasePlaces', data={
            'competition': self.original_competition['name'],
            'club': self.original_club['name'],
            'places': '13'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b"You cannot book more than 12 places for a single competition." in response.data
        assert server.clubs[0]['points'] == self.original_club['points']

        with open('clubs.json', 'r') as f:
            clubs_data = json.load(f)
            clubs = clubs_data['clubs']
            club = clubs[0]
            assert club['points'] == self.original_club['points']