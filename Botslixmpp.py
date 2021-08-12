# codigo basado en: https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/
# Title: Slixmpp Documentation
# Description: Slixmpp Documentation with python examples

import asyncio
import sys
import threading
import time
import xml.etree.ElementTree as ET
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class EchoRegisterBot(ClientXMPP):
    def __init__(self, jid, password):
        """
        init register bot
        args: jid, password
        """
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)

        # If you wanted more functionality, here's how to register plugins:
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0004')  # Data forms
        self.register_plugin('xep_0066')  # Out-of-band Data
        self.register_plugin('xep_0077')  # In-band Registration

        # Here's how to access plugins once you've registered them:
        self['xep_0030'].add_feature('echo_demo')

        self.add_event_handler("register", self.register_account)


    async def session_start(self):
        """
        session start
        args: self
        """
        self.send_presence()
        await self.get_roster()

    async def register_account(self, iq):
        """
        register new account
        args: self, iq(stanza)
        """
        # Set stanza attributes
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        # create account
        try:
            await resp.send()
            print("\nCuenta creada %s" % self.boundjid)
            await self.disconnect()
        except IqError as e:
            print("\nError al registrar la cuenta %s" % e.iq['error']['text'])
            await self.disconnect()


class EchoUnregisterBot(ClientXMPP):
    def __init__(self, jid, password):
        """
        init unregister bot
        args: jid, password
        """
        ClientXMPP.__init__(self, jid, password)

        # If you wanted more functionality, here's how to register plugins:
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0004')  # Data forms
        self.register_plugin('xep_0066')  # Out-of-band Data
        self.register_plugin('xep_0077')  # In-band Registration

        self.add_event_handler("session_start", self.session_start)
        # self.add_event_handler("message", self.message)

    async def session_start(self, event):
        """
        session start
        args: self, event
        """
        # Send presence
        self.send_presence()
        await self.get_roster()
        await self.unregister_account()

    async def unregister_account(self):
        """
        unregister account
        args: self
        """
        # Set stanza attributes
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.user
        resp['password'] = self.password
        resp['register']['remove'] = 'remove'
        # Delete account
        try:
            await resp.send()
            print("\nCuenta eliminada %s" % self.boundjid)
            await self.disconnect()
        except IqError as e:
            print("\nError al eliminar la cuenta %s" % e.iq['error']['text'])
            await self.disconnect()

class EchoClientBot(ClientXMPP):
    def __init__(self, jid, password, status, message):
        """
        init client bot
        args: self, jid, password, status, message
        """
        ClientXMPP.__init__(self, jid, password)
        
        self.jid = jid
        self.status = status
        self.account_message = message
        self.disconected = True
        self.messages = {}
        
        self.roster.auto_authorize = True
        self.roster.auto_subscribe = True
        
        # Handlers
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        
        # Plugins
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0133') # Service administration
        self.register_plugin('xep_0199') # XMPP Ping

    async def start(self, event):
        """
        Start conection function
        args: self, event
        """
        self.send_presence(pshow=self.status, pstatus=self.account_message)
        try:
            await self.get_roster()
            self.disconected = False
            print("\nUsuario conectado: " + self.jid)
        except:
            self.disconnect()

    def close_conection(self):
        """
        Close conectigon function
        args: self
        """
        pres = self.Presence()
        pres['type'] = 'unavailable'
        pres.send()

    def message(self, message):
        """
        get messages function
        args, message
        """        
        if message['type'] in ('chat', 'normal'):
            print('mensajes')
            de = str(message['from'])
            de = de[:de.index("@")]
            message = str(message['body'])

            if de in self.messages.keys():
                self.messages[de]["messages"].append(de + ": " + message)
            else:
                self.messages[de] = {"messages":[de + ": " + message]}

            if self.current_chat_with == de:
                print(de + ": " + message)
            else:
                print("*** message recieved from  " + de + " ***")

    def direct_message(self, to, message):
        """
        Send direct message function
        args to, message
        """
        self.send_message(mto=to, mbody=message, mtype='chat', mfrom=self.jid)
        
        para = to[:to.index("@")]
        de = self.jid[:self.jid.index("@")]

        if para in self.messages.keys():
            self.messages[para]["messages"].append(de + ": " + message)
        else:
            self.messages[para] = {"messages":[de + ": " + message]}

    def get_contacts(self):
        """
        get contacts function
        args self
        """
        try:
            self.get_roster()
        except IqError as err:
            print('IqError')
        except IqTimeout:
            print('IqTimeout')

        print('Buscando contactos...\n')
        groups = self.client_roster.groups()

        for group in groups:
            for jid in groups[group]:
                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    if pres['status']:
                        status = pres['status']

                print(jid + ' - ' + status)
    
    def get_chats(self):
        """
        return all chats
        args self
        """
        return self.messages
    
    def new_contact(self, to):
        """
        Add new contact function
        args to
        """
        try:
            self.send_presence_subscription(to, self.jid, 'subscribe')
            print("\nContacto agregado!\n")
        except:
            print("\nError al agregar")

  