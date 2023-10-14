import fileinput
import json

if __name__ == '__main__':
    for line in fileinput.input():
        line = line.replace('\n', '')

        if line == 'exit':
            break
        else:
            #print('Input was ' + line)
            try:
                answer = json.loads(line)
            except:
                answer = ""

            if answer != '':
                print(json.dumps(answer, indent=2))
                print(answer['jsonrpc'])
                print(answer['method'])
                print(answer['params']['envelope']['source'])

