<<<<<<< HEAD
# -*- coding: utf-8 -*-

from main import MainGabarito   


def name():
    return "check feiÃ§Ãµes"
def description():
    return "mostra cada uma das feiÃ§Ãµes da camada ativa"
def version():
    return "Version 0.1"

def classFactory(iface):
    return MainGabarito(iface)

def qgisMinimumVersion():
    return "2.0"
def author():
    return "Felipe Diniz e jossan costa"
def email():
    return "me@hotmail.com"
def icon():
    return "icon.png"
=======
# -*- coding: latin1 -*-

from main import MainGabarito   


def name():
  return "check feições"
def description():
  return "mostra cada uma das feições da camada ativa"
def version():
  return "Version 0.1"

def classFactory(iface):
  from main import MainGabarito
  return MainGabarito(iface)

def qgisMinimumVersion():
  return "2.0"
def author():
  return "Felipe Diniz"
def email():
  return "me@hotmail.com"
def icon():
  return "icon.png"
>>>>>>> branch 'master' of https://github.com/desenv-1dl/gabarito

## any other initialisation needed
