import sys
import Botslixmpp as Botslixmpp

# import register as register
ipclient = "192.168.56.1"
port = 5222

while True:
    print(
        "\nMenu pruncipal\n\t1. Registrar una nueva cuenta en el servidor\n\t2. Iniciar sesión con una cuenta" +
        "\n\t3. Eliminar la cuenta del servidor\n\t4. Salir")
    op = int(input())

    # validate selected option
    if not 1 > op > 4:
        print('Seleccione una opcion valida')

    # register a new account on the server
    if op == 1:
        jid = input("Cuenta: ")
        password = input("Password: ")

        xmpp = Botslixmpp.EchoRegisterBot(jid, password)
        xmpp.connect(address=(ipclient, port))
        xmpp.process(forever=False)
        xmpp.disconnect()

    # log in with an account on the server
    if op == 2:
        pass

    # delete an account
    if op == 3:
        jid = input("Cuenta: ")
        password = input("Password: ")

        # Start, run and disconnect xmpp client for unregistration
        xmpp = Botslixmpp.EchoUnregisterBot(jid, password)
        xmpp.connect(address=(ipclient, port))
        xmpp.process(forever=False)
        xmpp.disconnect()

        # exit
    if op == 4:
        sys.exit()
