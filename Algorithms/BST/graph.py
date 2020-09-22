from collections import deque
import memory_profiler as mem 
from memory_profiler import profile

GRAPH={
    'A':['B', 'F'],
    'B':['C', 'I', 'G'],
    'C':['B', 'I', 'D'],
    'D':['C', 'I', 'G', 'H', 'E'],
    'E':['D', 'H', 'F'],
    'F':['A', 'G', 'E'],
    'G':['B', 'F', 'H', 'D'],
    'H':['G', 'D', 'E'],
    'I':['B', 'C', 'D'],
}

class Queue(object):
    def __init__(self):
        self._deque=deque()

    def push(self, val):
        return self._deque.append(val)

    def pop(self):
        return self._deque.popleft()
    
    def __len__(self):
        return len(self._deque)



def bfs(graph, start):
    search_queue = Queue()
    search_queue.push(start)
    searched=set()  # 保存访问过的结点
    while search_queue:
        cur_node=search_queue.pop()
        if cur_node not in searched:
            print(cur_node)
            # print(searched)
            searched.add(cur_node)
            for node in graph[cur_node]:
                search_queue.push(node)


DFS_SEARCHED=set()

@profile
def dfs(graph, start):
    if start not in DFS_SEARCHED:
        print(start)
        DFS_SEARCHED.add(start)
    for node in graph[start]:
        if node not in DFS_SEARCHED:
            dfs(graph, node)



if __name__=="__main__":
    print(f'内存前：{mem.memory_usage()}')
    print('BFS: ')
    bfs(GRAPH, 'A')
    print('DFS: ')
    dfs(GRAPH,'A')
    print(f'内存后：{mem.memory_usage()}')
    
