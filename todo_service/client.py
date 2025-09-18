import grpc
import todo_pb2
import todo_pb2_grpc


def cli_input():
    print('\n\n1- Create new todo')
    print('2- Edit todo')
    option_number = input('\nSelect one: ')
    return int(option_number)


def run():
    with grpc.insecure_channel('localhost:5030') as channel:
        stub = todo_pb2_grpc.ToDoServiceStub(channel)
        while True:
            list_response = stub.GetToDos(todo_pb2.MyVoid())
            print("\n==============================================")
            print("Current ToDo List:")
            print("id || task || state")
            for todo in list_response.todos:
                print(f"{todo.ID}: {todo.task} [{'✔' if todo.done else 'o'}] ")
            print("==============================================")

            opt =  cli_input()

            if opt == 1:
                task = input('Enter a task: ')
                create_response = stub.CreateToDo(todo_pb2.CreateToDoRequest(task = task))
                print(f"Created ToDo: {create_response.todo.ID} - {create_response.todo.task}")
            if opt == 2:
                id = int(input('Enter a task id: '))
                updated_todo = todo_pb2.ToDo(ID=id, done=True)
                response = stub.EditTodo(updated_todo)
                print(f"Updated ToDo: {response.todo.ID} - {response.todo.task} - Done: {response.todo.done}")


if __name__ == '__main__':
    run()