import pymongo

class Todo:
    def __init__(self, text, name, done, gid):
        self.text = text
        self.name = name
        self.id = -1 
        self.done = done
        self.gid = gid
    
    def setId(self, id):
        self.id = id

    def __str__(self):
        return f'{self.text}\nby {self.name}\nComplete {self.done}'

class Database:
    def __init__(self, username, password):
        self.client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.cvrxt.mongodb.net/?retryWrites=true&w=majority")
        self.todos = self.client.get_database('DiscordBot').get_collection('Todos')

    def insertTodo(self, Todo):
        self.todos.insert_one({
            'text': Todo.text,
            'name': Todo.name,
            'done': Todo.done,
            'gid': Todo.gid
        })
    
    def deleteTodo(self, id):
        self.todos.delete_one({'_id': id})
    
    def getTodos(self, gid):
        temp = []
        for t in self.todos.find({"gid": str(gid)}):
            print(t)
            todo = Todo(t['text'], t['name'], t['done'],t['gid'])
            todo.setId(t['_id'])
            temp.append(todo)
        return temp

if __name__ == "__main__":
    db = Database('ilias', "")
    t = db.getTodos()[0]
    print(t)


    
    
    
