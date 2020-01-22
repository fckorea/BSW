#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Check Hardening
# Purpose:
# Python version: 3.7.3
#
# Author:    fckorea
#
# Created:    2019-07-27
# (c) fckorea 2019
#-------------------------------------------------------------------------------

import sys
from optparse import OptionParser
import logging
import logging.handlers
import json
import traceback

PROG_NAME = 'Check Hardening'
PROG_VER = '1.0'
LOGGER = None
LOG_FILENAME = ('%s.log' % (PROG_NAME.replace(' ', '-').lower()))
CONFIG = {}

#=============================== Main Functions ===============================#
def fnMain(argOptions, argArgs):
    global LOGGER

    try:
        return True
    except:
        raise

#=============================== Config & Init Function ===============================#
def fnGetConfig(argConfigFilePath):
    global LOGGER
    global CONFIG

    try:
        if os.path.isfile(argConfigFilePath):
            CONFIG = json.loads(open(argConfigFilePath, encoding='UTF8').read())
            LOGGER.debug(' * Read config data')
            return True
        else:
            LOGGER.error(' * Config file not found.')
    except:
        LOGGER.error(' *** Error read config file.')
        LOGGER.debug(traceback.format_exc())
    
    return False

#=============================== OptionParser Functions ===============================#
def fnSetOptions():
    global PROG_VER

    parser = None

    # Ref. https://docs.python.org/2/library/optparse.html#optparse-reference-guide
    options = [
        { 'Param': ('-c', '--config'), 'action': 'store', 'type': 'string', 'dest': 'o_sConfigFilePath', 'default': 'config.conf', 'metavar': '<Config file path>', 'help': 'Set config file path.\t\tdefault) config.conf (contents type is JSON)' },
        { 'Param': ('-v', '--verbose'), 'action': 'store_true', 'dest': 'o_bVerbose', 'default': False, 'metavar': '<Verbose Mode>', 'help': 'Set verbose mode.\t\tdefault) False' },
        { 'Param': ('-t', '--true'), 'action': 'store_true', 'dest': 'o_bTrue', 'default': False, 'metavar': '<Bool>', 'help': 'Set bool.\t\tdefault) False' },
        { 'Param': ('-f', '--false'), 'action': 'store_false', 'dest': 'o_bFalse', 'default': True, 'metavar': '<Bool>', 'help': 'Set bool.\t\tdefault) True' },
        { 'Param': ('-s', '--string'), 'action': 'store', 'type': 'string', 'dest': 'o_sString', 'metavar': '<String>', 'help': 'Set string.' },
        { 'Param': ('-i', '--int'), 'action': 'store', 'type': 'int', 'dest': 'o_iInt', 'metavar': '<Int>', 'help': 'Set int.' },
    ]
    usage = '%prog [options] <File or Dir path>\n\tex) %prog test\\'

    parser = OptionParser(usage = usage, version = '%prog ' + PROG_VER)

    for option in options:
        param = option['Param']
        del option['Param']
        parser.add_option(*param, **option)

    return parser

def fnGetOptions(argParser):
    if len(sys.argv) == 1:
        return argParser.parse_args(['--help'])

    if len(argParser.parse_args()[1]) == 0:
        return argParser.parse_args(['--help'])

    return argParser.parse_args()

def fnInit(argOptions):
    global PROG_NAME
    global LOGGER
    global LOG_FILENAME

    LOGGER = logging.getLogger(PROG_NAME.replace(' ', ''))

    if argOptions.o_bVerbose is True:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(levelname)s] - %(filename)s:%(lineno)s\t- %(asctime)s - %(message)s')
    
    file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when='midnight', backupCount=7, encoding='UTF-8')
    file_handler.suffix = '%Y%m%d'
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)

    return True

if __name__ == '__main__':
    parser = fnSetOptions()
    (parsed_options, argvs) = fnGetOptions(parser)
    if fnInit(parsed_options):
        LOGGER.info('Start %s...' % (PROG_NAME))
        if fnGetConfig(parsed_options.o_sConfigFilePath):
            LOGGER.info('Config file("%s")' % (parsed_options.o_sConfigFilePath))
            fnMain(parsed_options, argvs)
        LOGGER.info('Terminate %s...' % (PROG_NAME))
