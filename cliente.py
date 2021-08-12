import os
import sys
import threading

import Botslixmpp as Botslixmpp

# import register as register
serverip = "192.168.56.1"
port = 5222

while True:
    print('\nMenu pruncipal' +
          '\n\t1. Registrar una nueva cuenta en el servidor' +
          '\n\t2. Iniciar sesión con una cuenta ' +
          '\n\t3. Eliminar la cuenta del servidor' +
          '\n\t4. Salir')
    op = int(input('Seleccione una opción:'))

    # validate selected option
    if 0 > op < 5:
        print('Seleccione una opcion valida')

    # register a new account on the server
    if op == 1:
        print('\nRegistro de una cuenta')
        jid = input("Nombre de la cuenta: ")
        password = input("Password: ")

        xmpp = Botslixmpp.EchoRegisterBot(jid, password)
        xmpp.connect(address=(serverip, port))
        xmpp.process(forever=False)
        xmpp.disconnect()

    # log in with an account on the server
    if op == 2:
        print('\nIniciar sesión')
        jid = input("Cuenta: ")
        password = input("Password: ")
        status = 'chat'
        message = "available"

        session = False
        while not session:

            xmpp = Botslixmpp.EchoClientBot(jid, password, status, message)
            xmpp.connect(address=(serverip, port))

            stop_threads = False
            threads = threading.Thread(target=Botslixmpp.EchoClientBot.session_thread,
                                       args=(xmpp, lambda: stop_threads,))
            threads.start()

            while not xmpp.session:
                pass

            while True:
                print('\nMenu de cuenta' +
                      '\n\t1.Mostrar todos los usuarios/contactos y su estado' +
                      '\n\t2.Agregar un usuario a los contactos' +
                      '\n\t3.Mostrar detalles de contacto de un usuario' +
                      '\n\t4.Comunicación 1 a 1 con cualquier usuario/contacto' +
                      '\n\t5.Participar en conversaciones grupales' +
                      '\n\t6.Definir mensaje de presencia' +
                      '\n\t7.Enviar/recibir notificaciones' +
                      '\n\t8.Enviar/recibir archivos +'
                      '\n\t9.Cerrar sesión y salir')
                sop = int(input('Seleccione una opción:'))

                # validate selected option
                if 0 > sop < 10:
                    print('Seleccione una opcion valida')

                if sop == 1:
                    pass

                if sop == 2:
                    pass

                if sop == 3:
                    pass

                if sop == 4:
                    pass

                if sop == 5:
                    pass

                if sop == 6:
                    pass

                if sop == 7:
                    pass

                if sop == 8:
                    pass

                if sop == 9:
                    stop_threads = True
                    threads.join()
                    os._exit(0)
                    break


    # delete an account
    if op == 3:
        print('\nEliminar cuenta')
        jid = input("Cuenta a eliminar: ")
        password = input("Password: ")

        # Start, run and disconnect xmpp client for unregistration
        xmpp = Botslixmpp.EchoUnregisterBot(jid, password)
        xmpp.connect(address=(serverip, port))
        xmpp.process(forever=False)
        xmpp.disconnect()

        # exit
    if op == 4:
        sys.exit()
