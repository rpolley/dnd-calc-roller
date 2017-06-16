import json
loadedmodules = {}
def loadconfig(name, path=""):
	fname = path+name+".json"
	f = open(fname)
	loadedmodules[name] = json.load(f, object_hook=handle_objs)

def handleobjs(json_obj):
	if("ref" in json_obj):
		return getref(json_obj["ref"])
	return {key.replace(" ", "_"),value for key,value in json_obj.items()}

def getref(name):
	path = name.split(".")
	curr = loadedmodules
	for item in path:
		if(item in curr):
			curr = curr[item]
		else:
			 return (lambda: getref(name))

	return curr

