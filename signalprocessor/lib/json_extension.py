class JsonTool:

    def exists(self, jsonobject, path):
        retvalue = False
        p = path.find('/')

        if p > 0:
            current = path[:p]
            newpath = path[p+1:]

            if isinstance(jsonobject, list):
                for item in jsonobject:
                    retvalue = self.exists(item, path)
                    if retvalue:
                        break
            else:
                if current in jsonobject:
                    retvalue = self.exists(jsonobject[current], newpath)
        else:
            if isinstance(jsonobject, list):
                for item in jsonobject:
                    retvalue = self.exists(item, path)
                    if retvalue:
                        break
            else:
                if path in jsonobject:
                    retvalue = True

        return retvalue

    def trygetvalue(self, jsonobject, path):
        retvalue1 = False
        retvalue2 = ''

        if self.exists(jsonobject, path):
            p = path.find('/')

            if p > 0:
                current = path[:p]
                newpath = path[p+1:]

                if isinstance(jsonobject, list):
                    for item in jsonobject:
                        retvalue1, retvalue2 = self.trygetvalue(item, path)
                        if retvalue1:
                            break
                else:
                    retvalue1, retvalue2 = self.trygetvalue(jsonobject[current], newpath)
            else:
                retvalue1 = True
                retvalue2 = jsonobject[path]

        return retvalue1, retvalue2