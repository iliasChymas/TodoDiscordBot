from discord.ext import commands
import discord
from db import Database, Todo
from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config['TOKEN']
database = Database(config['DBUSERNAME'], config['DBPASSWORD'])

bot = commands.Bot(command_prefix="!")

def has_role(ctx, role):
    return discord.utils.get(ctx.guild.roles, name=role) in ctx.author.roles
    

@bot.event
async def on_guild_join(guild):
    print(f"{guild.__dir__()}\n")
    print(f"Joined {guild.id} !")


@bot.event
async def on_ready():
    print("Logged in")

@bot.command(name='todos')
@commands.has_role('todo')
async def get_todos(ctx):
    todos = database.getTodos(ctx.guild.id)
    print("GUID: " + str(ctx.guild.id))
    value = 'test'
    for t in todos:
        value += f"[{todos.index(t)}]: " + t.__str__() + '\n' + '\n'
    print(t)
    embed = discord.Embed(title="Todos")
    embed.add_field(name="Todos", value=value)
    await ctx.send(embed=embed)

@get_todos.error
async def get_todos_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You dont have the permissions for this :(")

@bot.command()
@commands.has_role('todo')
async def create_todo(ctx, *args):
    if len(args) != 3:
        await ctx.send("Wrong use of hte command.\nExample: !create_todo 'Buy milk' 'Ilias' 'false' ")
    else:
        todo = Todo(args[0], args[1], args[2].lower() == 'true', str(ctx.guild.id))
        database.insertTodo(todo)
        await ctx.send("Your todo has been uploaded :)")

@create_todo.error
async def create_todo_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You dont have the permissions for this :(")



@bot.command()
@commands.has_role('todo')
async def delete_todo(ctx, arg=-1):
    todos = database.getTodos(ctx.guild.id)
    if arg == -1 and not arg.isnumeric():
        await ctx.send(f"Please provide a valid index for deletion [0-{len(todos)}]")
    else:
        database.deleteTodo(todos[arg].id)
        await ctx.send("Deleted !")

@delete_todo.error
async def delete_todo_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You dont have the permissions for this :(")


bot.run(TOKEN)