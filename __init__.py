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

## any other initialisation needed
