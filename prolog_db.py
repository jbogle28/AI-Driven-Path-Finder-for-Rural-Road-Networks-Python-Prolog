import os
from pyswip import Prolog

class PrologDB:
    def __init__(self, prolog_file='roads.pl'):
        self.prolog_file = prolog_file
        self.prolog = Prolog()
        self.prolog.consult(self.prolog_file)
    
    def add_location(self, name):

        try:
            list(self.prolog.query(f"add_location('{name}')"))
            self._save_to_file()
            return True
        except Exception as e:
            print(f"Error adding location: {e}")
            return False
    
    def add_road(self, source, dest, distance, road_type, status):
        try:
            query = f"add_road('{source}', '{dest}', {distance}, {road_type}, {status})"
            list(self.prolog.query(query))
            self._save_to_file()
            return True
        except Exception as e:
            print(f"Error adding road: {e}")
            return False
    
    def get_all_locations(self):
        try:
            results = list(self.prolog.query("get_all_locations(Locations)"))
            if results:
                locations = sorted(results[0]['Locations'])
                return locations
            return []
        except Exception as e:
            print(f"Error getting locations: {e}")
            return []
    
    def get_all_roads(self):
        try:
            roads = []
            for result in self.prolog.query("road(S, D, Distance, Type, Status)"):
                roads.append({
                    'source': str(result['S']),
                    'destination': str(result['D']),
                    'distance': float(result['Distance']),
                    'road_type': str(result['Type']),
                    'status': str(result['Status'])
                })
            return roads
        except Exception as e:
            print(f"Error getting roads: {e}")
            return []
    
    def get_road(self, source, dest):
        try:
            query = f"get_road('{source}', '{dest}', Distance, Type, Status)"
            results = list(self.prolog.query(query))
            
            if results:
                r = results[0]
                return {
                    'source': source,
                    'destination': dest,
                    'distance': r['Distance'],
                    'road_type': r['Type'],
                    'status': r['Status']
                }
            return None
        except Exception as e:
            print(f"Error getting road: {e}")
            return None
    
    def update_road_status(self, source, dest, new_status):
        try:
            query = f"update_road_status('{source}', '{dest}', {new_status})"
            list(self.prolog.query(query))
            self._save_to_file()
            return True
        except Exception as e:
            print(f"Error updating road status: {e}")
            return False
    
    def update_road_type(self, source, dest, new_type):
        try:
            query = f"update_road_type('{source}', '{dest}', {new_type})"
            list(self.prolog.query(query))
            self._save_to_file()
            return True
        except Exception as e:
            print(f"Error updating road type: {e}")
            return False
    
    def update_road(self, source, dest, new_distance, new_type, new_status):

        try:
            query = f"update_road('{source}', '{dest}', {new_distance}, {new_type}, {new_status})"
            list(self.prolog.query(query))
            self._save_to_file()
            return True
        except Exception as e:
            print(f"Error updating road: {e}")
            return False
    
    def _save_to_file(self):
        """Save current Prolog state back to file"""
        try:
            # read existing file to preserve predicate code
            with open(self.prolog_file, 'r') as f:
                lines = f.readlines()
            
            # find where predicates start (after road facts)
            predicates_start = 0
            for i, line in enumerate(lines):
                if '% Road connection predicate' in line or 'connected(X, Y)' in line:
                    predicates_start = i
                    break
            predicates_code = ''.join(lines[predicates_start:])
            locations = self.get_all_locations()
            roads = self.get_all_roads()
            with open(self.prolog_file, 'w') as f:
                f.write(":- dynamic road/5.\n")
                f.write(":- dynamic location/1.\n\n")
                # Write locations
                f.write("% Locations\n")
                for loc in locations:
                    f.write(f"location('{loc}').\n")
                f.write("\n")
                # Write roads
                f.write("% Roads: road(Source, Destination, Distance, Type, Status)\n")
                for road in roads:
                    f.write(f"road('{road['source']}', '{road['destination']}', {road['distance']}, {road['road_type']}, {road['status']}).\n")
                f.write("\n")
                # Write back all predicates
                f.write(predicates_code)
            # Reload the file
            self.prolog.consult(self.prolog_file)
            
        except Exception as e:
            print(f"Error saving to file: {e}")
    
    def close(self):
        """Close database connection"""
        print("✓ Prolog database closed")
