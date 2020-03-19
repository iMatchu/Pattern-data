#list写入txt
ipTable = ['158.59.194.213', '18.9.14.13', '58.59.14.21']
fileObject = open('sampleList.txt', 'a')
for ip in ipTable:
	fileObject.write(ip)
	fileObject.write('\n')
fileObject.close()



#dict写入json
import json
dictObj = {
	'andy':{
		'age': 23,
		'city': 'shanghai',
		'skill': 'python'
	},
	'william': {
		'age': 33,
		'city': 'hangzhou',
		'skill': 'js'
	}
}
jsObj = json.dumps(dictObj)
 
fileObject = open('jsonFile.json', 'w')
fileObject.write(jsObj)
fileObject.close()

#用Json写入txt
def __writedata(self,Anchorfreistaat):
    with open('datafile.txt', 'a') as file:
        file.write(json.dumps(Anchorfreistaat)) 
