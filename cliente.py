import time
import asyncio
import threading
import Botslixmpp
from getpass import getpass

serverip = "192.168.56.1"
port = 5222

def session(client, stop):
    while True:
        client.process(forever=True, timeout=3)
        if stop(): 
            break

    client.close_conection()
    return

def cliente():
    while True:
        print('\nMenu pruncipal' +
              '\n\t1. Registrar una nueva cuenta en el servidor' +
              '\n\t2. Iniciar sesión con una cuenta ' +
              '\n\t3. Eliminar la cuenta del servidor' +
              '\n\t4. Salir')
        opmenu = int(input('Seleccione una opción '))

        if opmenu < 1 or opmenu > 4:
            print("Opcion no valida,\nSeleccione una opción ")
            continue
        break
    
    # Create account
    if opmenu == 1:
        print('\nRegistro de una cuenta')
        jid = input("Nombre de la cuenta: ")
        password = input("Password: ")

        xmpp = Botslixmpp.EchoRegisterBot(jid, password)
        xmpp.connect(address=(serverip, port))
        xmpp.process(forever=False)
    
    # Singin
    if opmenu == 2:
        print('\nIniciar sesión')
        jid = input("Cuenta: ")
        password = input("Password: ")
        status = 'chat'
        message = "available"

        xmpp = Botslixmpp.EchoClientBot(jid, password, status, message)
        xmpp.connect(address=(serverip, port))

        stop_session = False
        theads = threading.Thread(target = session, args=(xmpp, lambda : stop_session,))
        theads.start()

        time.sleep(3)

        if xmpp.disconected:
            print('Conectando...')
            time.sleep(5)
            if xmpp.disconected:
                print("\nNo se pudo conectar con el servidor\n")
                stop_session = True
                theads.join()
                return

        while True:
            print('\nMenu de cuenta' +
                '\n\t1.Lista de contactos' +
                '\n\t2.Agregar un usuario a los contactos' +
                '\n\t3.Ver mis conversaciones' +
                '\n\t4.Mensaje directo a cualquier usuario/contacto' +
                #'\n\t5.Participar en conversaciones grupales' +
                #'\n\t6.Definir mensaje de presencia' +
                #'\n\t7.Enviar/recibir notificaciones' +
                #'\n\t8.Enviar/recibir archivos +'
                '\n\t9.Cerrar sesión y salir')
            opcontacto = int(input('Seleccione una opción: '))

            if opcontacto < 1 or opcontacto > 9:
                print("Opcion no valida,\nSeleccione una opción: ")
                continue
            
            if opcontacto == 1:
                xmpp.get_contacts()
        
            if opcontacto == 2:
                new_contact = input("Añadir contacto: ")
                xmpp.new_contact(new_contact)
            
            if opcontacto == 3:
                chats = xmpp.get_chats()

                if len(chats.keys()) == 0:
                    print("No hay ningun chat")
                    continue
                
                index = 1
                print("Chats abiertos:")
                for key in chats.keys():
                    print("    " + str(index) + ". Chat con " + key)
                    index += 1

            if opcontacto == 4:
                to = input("Para: ")
                message = input("Mensaje: ")
                xmpp.direct_message(to, message)
                print("Mensaje enviado...")
            
            if opcontacto == 9:
                stop_session = True
                theads.join()
                break

    elif opmenu == 3:
        print('\nEliminar cuenta del servidor')
        jid = input("Cuenta: ")
        password = input("Password: ")
        xmpp = Botslixmpp.EchoUnregisterBot(jid, password)
        xmpp.connect(address=(serverip, port))
        xmpp.process(forever=False)

    elif opmenu == 4:
        return

cliente()
exit(1)
