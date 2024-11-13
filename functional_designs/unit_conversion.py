import queue
from typing import Tuple
"""

example facts:
  m = 3.28 ft
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
    def __init__(self, rate: float, unit: str):
        self.rate = rate
        self.unit = unit

class Node:
    
    def __init__(self, unit: str):
        self.unit = unit
        self.edges = []
        
    def add_edge(self, rate: float, unit: str) -> None:
        self.edges.append(Edge(rate, unit))

class Converter:
    
    def __init__(self):
        self.graph = {} # unit : unit node 
        self.ranks = {} # unit : rank
        self.parents = {} # unit : parent unit
        
    def find(self, unit: str) -> str:
        if self.parents[unit] != unit:
            self.parents[unit] = self.find(self.parents[unit])
        return self.parents[unit]
        
    def union_(self, unit1: str, unit2: str) -> None:
        parent1, parent2 = self.find(unit1), self.find(unit2)
        
        if parent1 != parent2:
            if self.ranks[parent1] == self.ranks[parent2]:
                self.ranks[parent1] += 1
                self.parents[parent2] = parent1
                
            elif self.ranks[parent1] > self.ranks[parent2]:
                self.parents[parent2] = parent1
            
            else:
                self.parents[parent1] = parent2
    
    
    def answer_query(self, query: Tuple[float, str, str]) -> float:
        
        amount1, unit1, unit2 = query
        
        if (not unit1 or
            not unit2 or
            unit1 not in self.graph or
            unit2 not in self.graph
            ):
            
            return -1
        
        parent1, parent2 = self.find(unit1), self.find(unit2)
        
        if parent1 != parent2:
            return -1
        
        q = queue.Queue() # unit, amount
        q.put((unit1, amount1))
        
        while q:
            unit, amount = q.get()
            
            if unit == unit2:
                return amount
            
            node = self.graph[unit]
            
            for edge in node.edges:
                rate = edge.rate
                next_unit = edge.unit
                q.put((next_unit, rate * amount))
                
    def add_conversion(self, fact: Tuple[str, float, str]) -> None:

        unit1, rate1, unit2 = fact
        rate2 = 1 / rate1
        
        if not unit1 or not unit2:
            return 
        
        if unit1 not in self.graph:
            self.ranks[unit1] = 0
            self.parents[unit1] = unit1
            self.graph[unit1] = Node(unit1)
            
        if unit2 not in self.graph:
            self.ranks[unit2] = 0
            self.parents[unit2] = unit2
            self.graph[unit2] = Node(unit2)
            
        node1, node2 = self.graph[unit1], self.graph[unit2]
        
        node1.add_edge(rate1, unit2)
        node2.add_edge(rate2, unit1)
        
        self.union_(unit1, unit2)
        

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