import fileinput
import json
from lib.json_extension import JsonTool
import os

SENDRECEIPT="{\"jsonrpc\":\"2.0\",\"method\":\"sendReceipt\",\"params\":{\"recipient\":[\"**recipient**\"],\"targetTimestamp\":**targetTimestamp**,\"type\":\"read\"}, \"id\":\"**ID**\"}"

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

                    srcnumbertpl    = jtool.trygetvalue(received, 'params/envelope/sourceNumber')
                    srccommandtpl   = jtool.trygetvalue(received, 'params/envelope/dataMessage/message')
                    srctimestamptpl = jtool.trygetvalue(received, 'params/envelope/timestamp')

                    if srcnumbertpl[0] and \
                       srccommandtpl[0] and \
                       srctimestamptpl[0]:

                        SENDRECEIPT.replace('**recipient**', srcnumbertpl[1], 1)
                        SENDRECEIPT.replace('**targetTimestamp**', srcnumbertpl[1], 1)
                        SENDRECEIPT.replace('**ID**', srctimestamptpl[1], 1)
                        #os.system('echo \'' + SENDRECEIPT + '\' | socat STDIN UNIX-CONNECT:/tmp/signal_cli.send')
                        os.system('echo \'' + SENDRECEIPT + '\' | socat STDIN UNIX-CONNECT:/tmp/signal_cli.send')

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
