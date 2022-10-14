"""
Utilities.

Authors: caobinbin(caobinbin@live.com)
Date:    2017/10/03
"""


import sys
import logging
import functools

from PyQt6 import QtGui
import numpy as np


"""Logging configuration."""
log_conf = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(message)s",
            "date_fmt": "%Y-%m-%d %H:%M:%S"
        },  
        "multiprocessing": {
            "format": "%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(message)s",
            "date_fmt": "%Y-%m-%d %H:%M:%S"
        }   
    },  
    "handlers": {
        # "file": {
        #     "class": "logging.FileHandler",
        #     "filename": "runtime.log",
        #     "level": "DEBUG",
        #     "formatter": "standard"
        # },  
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard"
        },  
        # "mp_file": {
        #     "class": "logging.FileHandler",
        #     "filename": "runtime.log",
        #     "level": "INFO",
        #     "formatter": "multiprocessing"
        # },
        "mp_console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "multiprocessing"
        }  
    },
    "root": {
        # "handlers": ["console", "file"],
        "handlers": ["console"],
        "level": "DEBUG"
    },
    "loggers": {
        "multiprocessing": {
            # "handlers": ["mp_console", "mp_file"],
            "handlers": ["mp_console"],
            "level": "INFO"
        }
    }
}


def dumpargs(func):
    """This decorator dumps out the arguments passed to a function before calling it.
    """
    argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
    fname = func.__qualname__

    def echo_func(*args, **kwargs):
        arguments = []
        if len(argnames) > 0:
            if argnames[0] != 'self':
                arguments.append((argnames[0], args[0]))
            for k, v in zip(argnames[1:], args[1:]):
                arguments.append((k, v))
        for k, v in kwargs.items():
            arguments.append((k, v))
        message = '{}({})'.format(fname, ', '.join('{}={}'.format(e[0], str(e[1]))
            for e in arguments))
        logging.debug(message)
        return func(*args, **kwargs)

    return echo_func


def singleton(cls):
    """Singleton class decorator."""

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it =  cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls
