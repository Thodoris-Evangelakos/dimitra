from typing import List, Tuple

class Perifereia():
    
    def __init__(self, FID:str, per: str, polygons: List[Tuple[float, float]]):
        self.FID = FID
        self.per = per
        self.polygons = polygons

    def __str__(self):
        return(f"FID: {self.FID}, PER: {self.per}, Coord sample: {self.polygons[0][0:2]}...")
    
    def __repr__(self):
        return(f"FID: {self.FID}, PER: {self.per}, Coord sample: {self.polygons[0][0:2]}...")
    
    def verbose(self):
        return(f"FID: {self.FID}, PER: {self.per}, Polygons: {self.polygons}")
    
    def file(self, index):
        path = "regions/"
        filename = f"{path}region{index+1}.csv"
        with open(filename, 'w+') as f:
            for polygon in self.polygons:
                f.write(f"{polygon}\n")