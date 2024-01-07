from typing import List, Tuple

class Perifereia():
    
    def __init__(self, FID:str, per: str, polygons: List[Tuple[float, float]]):
        self.FID = FID
        self.per = per
        self.polygons = polygons

    def __str__(self):
        return(f"FID: {self.FID}, PER: {self.per}, Coord sample: {self.polygons[0:2]}")