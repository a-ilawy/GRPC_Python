import grpc
from concurrent import futures
import time

import todo_pb2
import todo_pb2_grpc


#  act as database
todos = []

class ToDoService(todo_pb2_grpc.ToDoServiceServicer):
    def CreateToDo(self, request, context):
        todo = todo_pb2.ToDo(ID=len(todos)+1, task = request.task, done = False)
        todos.append(todo)
        return todo_pb2.ToDoResponse(todo=todo)
    
    def GetToDos(self, request, context):
        return todo_pb2.getToDosResponse(todos = todos)
    
    def EditTodo(self, request, context):
      
        for i, t in enumerate(todos):
            if t.ID == request.ID:
                todos[i] = todo_pb2.ToDo(ID=t.ID, task=t.task, done=request.done)
                return todo_pb2.ToDoResponse(todo=todos[i])
      
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Todo item not found')
        return todo_pb2.ToDoResponse()


    

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_ToDoServiceServicer_to_server(ToDoService(), server)
    server.add_insecure_port('[::]:5030')
    server.start()
    print("Server running on port 5030...")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop(0)

if __name__ == '__main__':
    server()

