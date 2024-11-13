import redis
import threading
from collections import deque
from typing import List

cache = redis.Redis(host='localhost', port=6379, db=0)

class Graph:
    def __init__(self, is_directed):
        self.graph = {}
        self.directed = is_directed
        
    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []
            
    def add_edge(self, vertex1: int, vertex2: int) -> None:
        if vertex1 not in self.graph:
            self.add_vertex(vertex1)
            
        if vertex2 not in self.graph:
            self.add_vertex(vertex2)
            
        if vertex2 not in self.graph[vertex1]:
            self.graph[vertex1].append(vertex2)
        
            if not self.directed and vertex1 not in self.graph[vertex2]:
                self.graph[vertex2].append(vertex1)
        
    def remove_edge(self, vertex1: int, vertex2: int) -> None:
        if vertex1 in self.graph and vertex2 in self.graph[vertex1]:
            self.graph[vertex1].remove(vertex2)
        
        if (self.directed and
            vertex2 in self.graph and
            vertex1 in self.graph[vertex2]
            ): 
            self.graph[vertex2].remove(vertex1)
        
    def remove_vertex(self, vertex: int) -> None:
        if vertex in self.graph:
            for adj in self.graph[vertex]:
                self.graph[adj].remove(vertex)
                
            del self.graph[vertex]
        
    def display(self):
        for vertex, edges in self.graph.items():
            print(f"{vertex} : {edges}")
    
    def bfs(self, start):
        cache_key = f"bfs:{start}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return eval(cached_result)
        
        vals = []
        q = deque()
        visited = set()
        visited.add(start)
        
        starting_node = start if start in self.graph else next(iter(self.graph))
        
        q.append(starting_node)
        
        while q:
            node = q.popleft()
            vals.append(node)
            
            for adj in self.graph[node]:
                if adj not in visited:
                    q.append(adj)
                    visited.add(adj)

        cache.set(cache_key, str(vals))
        return vals
    
    def dfs(self, start: int) -> List[int]:
        cache_key = f"dfs:{start}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return eval(cached_result)

        vals = []
        visited = {start}
        result = self.dfs_recur(vals, visited, start)
        
        cache.set(cache_key, str(result))
        return result
        
    def dfs_recur(self, vals, visited, node: int):
        vals.append(node)
        
        for adj in self.graph[node]:
            if adj not in visited:
                visited.add(adj)
                self.dfs_recur(vals, visited, adj)
        
        return vals

def run_bfs(graph, start):
    bfs_output = graph.bfs(start)
    print("BFS output:", bfs_output)

def run_dfs(graph, start):
    dfs_output = graph.dfs(start)
    print("DFS output:", dfs_output)

def main():

    num_vertices = 5
    
    g = Graph(is_directed=False)
    for vertex in range(1, num_vertices + 1):
        g.add_vertex(vertex)
    
    for vertex1 in range(1, num_vertices + 1):
        for vertex2 in range(1, num_vertices + 1):
            if vertex1 != vertex2:
                g.add_edge(vertex1, vertex2)
    
    g.display()
    
    bfs_thread = threading.Thread(target=run_bfs, args=(g, 1))
    dfs_thread = threading.Thread(target=run_dfs, args=(g, 1))
    
    bfs_thread.start()
    dfs_thread.start()
    
    bfs_thread.join()
    dfs_thread.join()
    
    print("Both BFS and DFS computations are complete.")

if __name__ == "__main__":
    main()
