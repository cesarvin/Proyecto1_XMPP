# codigo basado en: https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/
# Title: Slixmpp Documentation
# Description: Slixmpp Documentation with python examples

import asyncio
import sys
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
        ClientXMPP.__init__(self, jid, password)

        self.jid = jid
        self.status = status
        self.message = message
        self.session = False

        # Set the client to auto authorize and subscribe when
        # a subcription event is recieved
        self.roster.auto_authorize = True
        self.roster.auto_subscribe = True

        # Plugins
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping

        # Set the events' handlers
        self.add_event_handler("session_start", self.session_start)

    async def session_start(self, event):
        self.send_presence(pshow=self.status, pstatus=self.message)

        try:
            await self.get_roster()
            self.session = True
        except:
            self.disconnect()

    @staticmethod
    def session_thread(xmpp, stop):
        while True:
            xmpp.process(forever=True)

            if stop():
                break

        xmpp.get_disconnected()
        return
