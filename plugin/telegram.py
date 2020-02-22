#!/usr/bin/python
# -*- coding: utf-8 -*-
"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        telegram.py
@date:        20.02.2020
@author:      Jan Speller
@description: Telegram Plugin
"""
import logging
from plugin.pluginBase import PluginBase

# ###################### #
# Custom plugin includes #
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, NetworkError)
import telegram
# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(PluginBase):
    """!Description of the Plugin"""

    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def onLoad(self):
        """!Called by import of the plugin"""
        self.bot = telegram.Bot(token=self.config.get("botToken", default=""))
        pass

    def pocsag(self, bwPacket):
        """!Called on POCSAG alarm

        @param bwPacket: bwPacket instance"""
        msg = bwPacket.get("ric") + " (" + bwPacket.get("subric") + ")\n" + bwPacket.get("message")
        if bwPacket.get("lat") is not None and bwPacket.get("lng") is not None:
            (lat, lng) = (bwPacket.get("lat"), bwPacket.get("lng"))
        
        for chatId in self.config.get("chatIds", default=[]):
            try:
                # Send Message via Telegram
                self.bot.send_message(chat_id=chatId, text=msg)
                
                # Send Location via Telegram if lat and lng are defined
                if lat is not None and lng is not None:
                    self.bot.sendLocation(chat_id=chatId, latitude=lat, longitude=lng)
            except Unauthorized:
                logging.error("Error while sending Telegram Message, please Check your api-key")
            except (TimedOut, NetworkError):
                logging.error("Error while sending Telegram Message, please Check your connectivity")
            except (BadRequest, TelegramError):
                logging.error("Error while sending Telegram Message")
            except Exception as e:
                logging.error("Unknown Error while sending Telegram Message: " + str(type(e).__name__) + ": " + str(e))
        pass
