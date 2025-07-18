from locust import HttpUser, task, between
    

class PerformanceTest(HttpUser):
    wait_time = between(0.1, 1)
    
    @task
    def index(self):
        self.client.get('/')
     
    @task
    def competitions_list(self):
        self.client.post(
            '/showSummary',
            data={'email': 'club-1@email.com'}
        )
        
    @task(3)
    def purchase_places(self):
        self.client.post(
            '/purchasePlaces', data={
                'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': '1'
            }
        )
        
    @task
    def book(self):
        self.client.get(
            '/book/Spring Festival/Simply Lift'
        )
        
    @task
    def points_display(self):
        self.client.get(
            '/pointsDisplay'
        )
