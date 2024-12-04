from queue import Queue
from typing import Tuple
"""

example facts:
  m = 3.28 ft
  ft = 12 in 
  ft = 12 in
  hr = 60 min
  min = 60 sec
example queries:
  2 m = ? in --> answer = 78.72
  13 in = ? m --> answer = 0.330 (roughly)
  13 in = ? hr --> "not convertible!"


Facts: string, float, string, tuple (1, unit1, count, unit2) 
Query: float, string, string, tuple (count, unit1, unit2)
"""
class Edge:
    def __init__(self, unit: str, conversion_rate: float):
        self.unit = unit
        self.conversion_rate = conversion_rate

class Node:
    def __init__(self, unit: str):
        self.edges = []
        self.unit = unit 
        
    def add_edge(self, edge: Edge):
        self.edges.append(edge)

class Converter:
    
    def __init__(self):
        self.parents = {}
        self.ranks = {}
        self.graph = {} # unit : Node(unit)
        
    def union_(self, unit1: str, unit2: str) -> None:
        
        parent1 = self.find(unit1)
        parent2 = self.find(unit2)
        
        if (parent1 != parent2):
            
            if self.ranks[parent1] > self.ranks[parent2]:
                self.parents[parent2] = parent1
                
            elif self.ranks[parent2] > self.ranks[parent1]:
                self.parents[parent1] = parent2
                
            elif self.ranks[parent1] == self.ranks[parent2]:
                self.parents[parent2] = parent1
                self.ranks[parent1] += 1
        
    def find(self, unit: str) -> str:
        if self.parents[unit] != unit:
            self.parents[unit] = self.find(self.parents[unit])
        
        return self.parents[unit]
        
        # 1 2 3
        # 1 1 2
        

    # tuple (str, float, str)
    def add_conversion(self, fact: Tuple[str, float, str]):
        
        unit1, rate1, unit2 = fact 
        
        if unit1 not in self.parents:
            self.parents[unit1] = unit1
            self.ranks[unit1] = 0
            self.graph[unit1] = Node(unit1)
            
        if unit2 not in self.parents:
            self.parents[unit2] = unit2
            self.ranks[unit2] = 0
            self.graph[unit2] = Node(unit2)
            
        rate2 = 1 / rate1 
        
        edge_1_to_2 = Edge(unit2, rate1)
        edge_2_to_1 = Edge(unit1, rate2)
        
        self.graph[unit1].add_edge(edge_1_to_2)
        self.graph[unit2].add_edge(edge_2_to_1)
        
        self.union_(unit1, unit2)
        
    # tuple (float, str, str)
    def answer_query(self, query: Tuple[float, str, str]) -> float:
        
        quantity1, unit1, unit2 = query
        
        if unit1 not in self.parents or unit2 not in self.parents:
            return float('-inf')
        
        parent1 = self.find(unit1)
        parent2 = self.find(unit2)
        
        if parent1 != parent2:
            return -1
        
        visited = set()
        
        q = Queue()
        
        q.put((quantity1, unit1))
        
        while q:
            quantity, unit = q.get()
            
            visited.add(unit)
            
            if unit == unit2:
                return quantity

            for edge in self.graph[unit].edges:
                if edge.unit not in visited:
                    next_quantity = quantity * edge.conversion_rate 
                    q.put((next_quantity, edge.unit))
        

                
    


def main():
    
    converter = Converter()
    
    converter.add_conversion(("m", 3.28, "ft"))
    converter.add_conversion(("ft", 12, "in"))
    converter.add_conversion(("hr", 60, "min"))
    converter.add_conversion(("min", 60, "sec"))
    
    print(converter.answer_query((2, "m", "in")))
    print(converter.answer_query((1, "hr", "m")))
    print(converter.answer_query((13, "in", "m")))
    print(converter.answer_query((13, "in", "hr")))


if __name__ == "__main__":
    main()









