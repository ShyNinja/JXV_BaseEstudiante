"""BASE EDUCATIVA INSEGURA. Corregir los TODO antes de la entrega."""
import json
from pathlib import Path
from datetime import datetime
from seguridad import crear_hash
from seguridad import verificar_clave

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"

def cargar_inventario():

    #Chequa si existe el file y que el formato se valido
    try:
        with DATOS.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(" >> Error: El archivo de el inventario no se encuentra.")
        return None
    
    except json.JSONDecodeError:
        print(" >> Error: El archivo JSON tiene un formato inválido.")
        return None

    #Devuelve el inventario
    return json.loads(DATOS.read_text(encoding="utf-8"))

def guardar_inventario(productos):

    #Guarda el producto
    DATOS.write_text(json.dumps(productos, indent=2), encoding="utf-8")

def registrar_evento(usuario, accion, resultado, **detalles):
    #Crea el mensanje que va a estar escrito en los LOGS
    currentTime = datetime.now().strftime("%d/%b/%Y %I:%M.%S %p")
    logMessage = currentTime + " | " + usuario + " | " + accion + " | " + resultado

    #Si hay detalles, los va incluir en mensaje de log
    if (detalles):
        logMessage += " | " + json.dumps(detalles)

    #Abre el JSON file para adnadir la linea del log
    with LOG.open("a", encoding="utf-8") as file:
        file.write(json.dumps(logMessage) + "\n")

    pass

def autenticar(nombre, clave):
    usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))

    #Verifica en cada usurio si el password y user coinciden
    for usuario in usuarios:
        #Verifica que el nombre y es password sean iguales
        if (verificar_clave(usuario["usuario"], nombre) and verificar_clave(usuario["clave"], clave)):

            #Registro el evento de login correctamente
            registrar_evento(nombre, "Login", "Exitoso")

            return {"usuario": nombre, "rol": usuario["rol"]}

    #Registrado el usuario que fallo
    registrar_evento(nombre, "Login", "Fallado")            
    print(" >> Credenciales incorrectos.")

    return None

def ValidarSesion(sesion, valida):
    #Verifica que la sesion enviadas coincidan
    if (sesion["rol"] == valida):
        return True
    else:
        return False

def IsValidString(inputString):
    #Checks that there is a string
    if not inputString:
        print(" >> Por favor escribrir algo")
        return False
        
    #Checks if there are any empty spaces
    elif " " in str(inputString):
        print(" >> Espacio detectado! No se puede escribir un espacio")
        return False
    
    else:
        return True

def IsValidInt(inputInt):
    #Validates the string
    if not IsValidString(inputInt):
        return False
    else:
        #Checks that it's an int
        try:
            inputInt = int(inputInt)
            return True
        except ValueError:
            # If conversion fails, it remains a standard text string
            print(" >> Por favor escribir un numero")
            return False
        
def consultar_inventario(sesion):

    #Verifica si la session es valida
    if not (sesion):
        print(" >> No tiene permiso para accesar esta funcion")
        return False

    #Verifica que exista un file
    productos = None
    if (productos == cargar_inventario() ):
        return False

    productos = cargar_inventario()
    for producto in productos:
        print(producto["id"], producto["nombre"], producto["cantidad"])

def modificar_cantidad(sesion, identificador, entrada):
    #Verifica si hay una session
    if not (sesion):
        print(" >> No hay una sesion activa")
        return False
    
    #Verifica si la session es valida
    if(ValidarSesion(sesion, "admin") == False):
        print(" >> No tiene permiso para accesar esta funcion")
        return False
        
    cantidad = entrada

    #Verifica que exista un file
    productos = None
    if (productos == cargar_inventario() ):
        return False
    
    productos = cargar_inventario()
    for producto in productos:
        if producto["id"] == identificador:
            anterior = producto["cantidad"]
            producto["cantidad"] = cantidad

            #Recolecta y verifica que el dato es un int valido
            if IsValidInt(cantidad):
                #Validad que la cantidad este en el rango correcto
                cantidad = int(cantidad)

                #Si la cantidad no es valida, no hace el cambio y lo rehistra en el log
                if cantidad < 0 or cantidad > 1000:
                    print(" >> No es un numero dentro del rango")
                    registrar_evento(
                        sesion["usuario"], "Modificar", "Fallado",
                        producto=identificador, anterior=anterior, nueva=cantidad
                    )
                    return False
            else:
                print(" >> No es un valor valido")
                return False

            #Guarda el cambio
            guardar_inventario(productos)
            registrar_evento(
                sesion["usuario"], "Modificar", "Exitoso",
                producto=identificador, anterior=anterior, nueva=cantidad
            )
            print(" ++ Cantidad actualizada.")
            return True
        
    #Informa al usurio que el producto es inexiste
    registrar_evento(
                sesion["usuario"], "Modificar", "Fallado"
    )
    print("Producto inexiste")
    return False

def main():
    print("Inventario académico — BASE CON DEBILIDADES")

    productos = cargar_inventario()

    print("Estudiante:", input("Escriba su nombre: "))

    sesion = None

    while True:

        if sesion is None:
            
            nombre = input("Usuario (o salir): ")
            if nombre == "salir":

                #Registra que el usuario desconocido cerro la session
                registrar_evento("usuario desconocido", "Salio de la session", "Exitoso")

                break
            sesion = autenticar(nombre, input("Contraseña de prueba: "))
            continue
        print("1. Consultar | 2. Modificar | 3. Cerrar sesión | 0. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            #Registra que el usuario abrio el inventario
            registrar_evento(
                sesion["usuario"], "Consulto el inventario", "Exitoso"
            )

            #Ensena el inventario
            consultar_inventario(sesion)

        elif opcion == "2":
            identificador = input("ID del producto: ")
            entrada = input("Nueva cantidad: ")
            modificar_cantidad(sesion, identificador, entrada)

        elif opcion == "3":

            #Registra que el usuario cerro session
            registrar_evento(sesion["usuario"], "Cerro la session", "Exitoso")

            sesion = None

        elif opcion == "0":

            #Registra que el usuario salio session
            registrar_evento(
                sesion["usuario"], "Salio de la session", "Exitoso"
            )

            break

        else:
            print(" >> Opción inválida.")


if __name__ == "__main__":
    main()
