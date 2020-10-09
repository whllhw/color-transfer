# coding: utf-8
import logging


def get_log(cls):
    log = logging.getLogger(cls.__name__)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s %(name)s %(filename)s:%(lineno)d %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    log.setLevel(logging.DEBUG)
    log.addHandler(console)
    return log
