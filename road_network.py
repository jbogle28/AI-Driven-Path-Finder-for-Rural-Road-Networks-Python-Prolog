class RoadNetwork:
    def __init__(self, db_manager):
        self.db = db_manager
        self.prolog = db_manager.prolog
    
    def get_locations(self):
        return self.db.get_all_locations()
    
    def dijkstra(self, start, goal, criteria='distance'):
        prolog_criteria = criteria
        
        query = f"dijkstra_path('{start}', '{goal}', Path, Distance, {prolog_criteria})"
        
        try:
            results = list(self.prolog.query(query))
            if results:
                path = results[0]['Path']
                distance = results[0]['Distance']
                return path, distance
        except Exception as e:
            print(f"Prolog query failed: {e}")
            pass
        
        return None, None
    
    def bfs(self, start, goal):
        query = f"bfs_path('{start}', '{goal}', Path)"
        try:
            results = list(self.prolog.query(query))
            if results:
                return results[0]['Path']
        except:
            pass
        
        return None
    
    def calculate_path_stats(self, path):
        if not path or len(path) < 2:
            return 0
        total_distance = 0
        for i in range(len(path) - 1):
            road = self.db.get_road(path[i], path[i+1])
            if road:
                total_distance += road['distance']
        
        return total_distance
    
    def get_road_details(self, source, dest):
        return self.db.get_road(source, dest)
    
    def find_path(self, start, goal, criteria='distance'):
        if start == goal:
            return None, None
        path, cost = self.dijkstra(start, goal, criteria)
        
        if path:
            distance = self.calculate_path_stats(path)
            return path, distance
        
        return None, None
    
    def find_path_bfs(self, start, goal):
        if start == goal:
            return None, None
        
        path = self.bfs(start, goal)
        
        if path:
            distance = self.calculate_path_stats(path)
            return path, distance
        
        return None, None
