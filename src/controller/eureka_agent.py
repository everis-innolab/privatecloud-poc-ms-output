# -*- encoding: utf8 -*-
import random
from threading import Thread, Event
import time
from src.constants import EUREKA_HEARTBEAT_INTERVAL


class EurekaAgent():

    def __init__(self, ec_client, logger):
        self.ec_client = ec_client
        self.heart_beat_thread = None
        self.heart_beat_stop_flag = None
        self.__logger = logger

    def register_in_eureka(self):
        self.ec_client.register()
        time.sleep(2)
        self.ec_client.take_back_to_service()
        time.sleep(2)
        self.__start_heartbeat_thread()

    def de_register_in_eureka(self):
        self.__logger.info("Trying to de-register in eureka")
        self.ec_client.de_register()
        self.__stop_heartbeat_thread()
        self.__logger.info("De-register complete")

    def __start_heartbeat_thread(self):
        self.heart_beat_stop_flag = Event()
        self.heart_beat_thread =  MyThread(
            self.heart_beat_stop_flag, EUREKA_HEARTBEAT_INTERVAL,
            self.ec_client.heartbeat, self.__logger
        )
        self.heart_beat_thread.start()

    def __stop_heartbeat_thread(self):
        if self.heart_beat_stop_flag is not None:
            self.heart_beat_stop_flag.set()
        else:
            self.__logger.info("heart_beat_stop_flag was None, avoiding set")

class MyThread(Thread):

    def __init__(self, event, time_interval_in_segs, function, logger):
        Thread.__init__(self)
        self.stopped = event
        self.time_interval_in_segs = time_interval_in_segs
        self.function = function
        self.logger = logger

    def run(self):
        while not self.stopped.wait(self.time_interval_in_segs):
            try:
                self.function()
            except:
                self.logger.exception("Error al enviar el heartBeat")
