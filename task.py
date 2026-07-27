import argparse
import json
from datetime import datetime as dt
from pathlib import Path 

# Task manager CLI
# Add, Update, and Delete tasks
# Mark a task as in progress or done
# List all tasks    
# List all tasks that are done
# List all tasks that are not done
# List all tasks that are in progress

def main():
    
    parser = argparse.ArgumentParser(
        description="Gestor de tareas en CLI - Una herramienta para gestionar tus tareas diarias"
    )

    # los subcomandos se definen acá
    subparsers = parser.add_subparsers(dest="comando", required=True, help="Acción a realizar")

    # subcomando 'add'
    parserAdd = subparsers.add_parser('add', help="Agregar tarea")
    parserAdd.add_argument("titulo", type=str, help= "Titulo de la tarea")
    parserAdd.add_argument(
        "--status",
        type=str,
        choices=["todo", "in-progress", "done"],
        default="todo",
        help="Estatus de la tarea"
    )

    # subcomando 'list'
    parserList = subparsers.add_parser('list', help="Muestra todas las tareas")
    parserList.add_argument(
        "type",
        nargs="?",
        choices=["all", "todo", "in-progress", "done"],
        default="all",
        help="Tipo de tarea a mostrar"
    )

    # subcomando 'mark-in-progress'
    parserMarkInProgress = subparsers.add_parser('mark-in-progress', help="Marca una tarea que estás haciendo")
    parserMarkInProgress.add_argument(
        "id",
        type=int,
        help="Número de la tarea a marcar"
    )

    # subcomando 'mark-done'
    parserMarkDone = subparsers.add_parser('mark-done', help="Marcar una tarea como lista")
    parserMarkDone.add_argument(
        "id",
        type=int,
        help="Número de la tarea a marcar"
    )

    # subcomando 'update'
    parserUpdate = subparsers.add_parser('update', help="Actualizar el título de una tarea")
    parserUpdate.add_argument(
        "id",
        type=int,
        help="Número de la tarea a actualizar"
    )
    parserUpdate.add_argument(
        "titulo",
        type=str,
        help="Nuevo título de la tarea"
    )

    parserDelete = subparsers.add_parser('delete', help="Eliminar una tarea en específico")
    parserDelete.add_argument(
        "id",
        type = int,
        help="Número de la tarea a eliminar"
    )

    args = parser.parse_args()

    if args.comando == 'add':
        addTask(args.titulo, args.status)
    elif args.comando == 'list':
        showTasks(args.type)
    elif args.comando == 'mark-in-progress':
        mark(args.id, 'in-progress')
    elif args.comando == 'mark-done':
        mark(args.id, 'done')
    elif args.comando == 'update':
        update(args.id, args.titulo)
    elif args.comando == 'delete':
        delete(args.id)

def addTask(titulo, status):

    tareas = getTasks()
    today = dt.now().strftime("%Y-%m-%d %H:%M:%S")

    # date = re.sub(r"\.\d+", "", string) otra manera

    id = max([t['id'] for t in tareas], default=0) + 1

    # ó
    # tareaID = []
    # for t in tareas:
        # tareaID.append(t['id'])

    nuevaTarea = {
        "id": id,
        "titulo": titulo,
        "status": status,
        "createdAt": today,
        "updatedAt": today
    }

    tareas.append(nuevaTarea)


    saveTask(tareas)

    print(f"Tarea agregada con éxito (ID: {nuevaTarea['id']})")

def saveTask(tareas):
        
    textoJSON = json.dumps(tareas, indent=4)    
    rutaArchivo = Path("storage.json")
    rutaArchivo.write_text(textoJSON, encoding='utf-8')

def showTasks(status):

    tareas = getTasks()

    tareasFiltradas = [ t for t in tareas if status == "all" or t['status'] == status ]

    if not tareasFiltradas:
        print(f"No hay tareas con el estatus '{status}'")
        return
    
    mensajes = {
        "todo": "Mostrando todas las tareas por hacer...", 
        "in-progress": "Mostrando todas las tareas que estas haciendo...",
        "done": "Mostrando todas las tareas hechas..."
    }

    print(mensajes.get(status, "Mostrando todas las tareas"))

    for tarea in tareasFiltradas:
        print(f"Tarea {tarea['id']}: {tarea['titulo']}")
                       
def getTasks():

    rutaArchivo = Path("storage.json")

    if rutaArchivo.exists():
        contenido = rutaArchivo.read_text(encoding='utf-8')
        tareas = json.loads(contenido)
        # print(tareas)
        return tareas
    
    return []

def mark(id, status):

    tareas = getTasks()
    encontrada = False

    for tarea in tareas:
        if tarea['id'] == id:
            tarea['status'] = status
            encontrada = True
            break

    if encontrada:
        saveTask(tareas)
    else:
        print(f"No se encontró la tarea con ID {id}.")

def update(id, titulo):

    tareas = getTasks()
    encontrada = False
    
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['titulo'] = titulo
            tarea['updatedAt'] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            encontrada = True
            break
    
    if encontrada:
        saveTask(tareas)
        print(f"Tarea {id} actualizada con éxito.")
    else:
        print(f"No se encontró la tarea con ID {id}.")

def delete(id):
    
    tareas = getTasks()
    encontrada = False

    for tarea in tareas:
        if tarea['id'] == id: # si el id de la tarea de la lista es igual al id que se pasa, entra al condicional
            tareas.remove(tarea) # elimina el primer elemento de la lista
            encontrada = True
            break

    if encontrada:
        saveTask(tareas)
        print(f"Tarea {id} eliminada con éxito.")
    else:
        print(f"No se encontró la tarea con ID {id}.")

if __name__ == "__main__":
    main()
