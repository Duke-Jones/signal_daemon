import fileinput
import json
from lib.json_extension import JsonTool
import os

if __name__ == '__main__':

    with open('signalprocessor.json') as user_file:
        configuration = json.loads(user_file.read())

    if configuration['signalprocessor'] != '1.0':
        raise KeyError('configuration file is not valid !')

    for line in fileinput.input():
        line = line.replace('\n', '')

        if line == 'quit':
            break
        else:
            try:
                received = json.loads(line)
            except:
                received = ""

            if received != '':
                jtool = JsonTool()
                if jtool.trygetvalue(received, 'jsonrpc') == (True, '2.0') and \
                   jtool.trygetvalue(received, 'method') == (True, 'receive'):

                    srcnumbertpl  = jtool.trygetvalue(received, 'params/envelope/sourceNumber')
                    srccommandtpl = jtool.trygetvalue(received, 'params/envelope/dataMessage/message')
                    srcsendertpl  = jtool.trygetvalue(received, 'params/envelope/sourceNumber')

                    if srcnumbertpl[0] and \
                       srccommandtpl[0] and \
                       srcsendertpl[0]:

                        cfgcommandtpl = jtool.trygetvalue(configuration, 'commands/' + srccommandtpl[1])
                        cfgallowedtpl = jtool.trygetvalue(configuration, 'commands/' + srccommandtpl[1] + '/allowed_to/' + srcnumbertpl[1])
                        cfgexecutetpl = jtool.trygetvalue(configuration, 'commands/' + srccommandtpl[1] + '/execute')
                        cfganswertpl  = jtool.trygetvalue(configuration, 'commands/' + srccommandtpl[1] + '/answer')

                        if cfgcommandtpl[0] and \
                           cfgallowedtpl[0] and cfgallowedtpl[1] and \
                           cfgexecutetpl[0]:

                            os.system('echo \'' + cfgexecutetpl[1] + '\'')

                            if cfganswertpl[0]:
                                os.system('echo \'' + cfganswertpl[1] + '\'')
