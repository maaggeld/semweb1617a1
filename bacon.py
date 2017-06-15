#!/usr/bin/python
# -*- coding: utf-8 -*-



from urllib.request import urlopen,Request
from urllib.parse import urlencode
import json

endpoint = "http://data.linkedmdb.org/sparql?"

#sparqlq = """
#PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
#SELECT ?fname ?ftime WHERE {
#?film movie:actor <http://data.linkedmdb.org/resource/actor/29704> .
#?film movie:runtime ?ftime .
#?film rdfs:label ?fname .
#}
#"""


firstname = input('Enter a firstname: ')

sparqlq = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
SELECT ?actor_name ?actor_id WHERE {
?actor movie:actor_actorid ?actor_id .
?actor movie:actor_name ?actor_name .
filter(regex(?actor_name, '"""+firstname+""" ',"i"))
}
"""


# params sent to server
params = { 'query': sparqlq }
# create appropriate param string
paramstr = urlencode(params)

# create GET http request object with params appended
req = Request(endpoint+paramstr)
#print(endpoint+paramstr)
# request specific content type
req.add_header('Accept','application/sparql-results+json')
# dispatch request
page = urlopen(req)
# get results and close
text = page.read().decode('utf-8')
page.close()


# convert to json object
jso = json.loads(text)


actors = []

# iterate over results
for binding in jso['results']['bindings']:
	# for every column in binding
	name = ""
	for bname,bcontent in binding.items():
		#print(bname,bcontent['value'])
		if bname=="actor_name":
			name = bcontent['value']
		elif bname == "actor_id":
			actors.append([bcontent['value'], name])

i=0
for actor in actors:
	print (i,actor[1])
	i+=1

s = int(input("Type a number to select an actor: "))

print (actors[s])


sparqlq = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
SELECT ?mid ?actname ?mtitle ?mactor  WHERE {
?film movie:filmid ?mid.
?film movie:actor ?mactor.
?film rdfs:label ?mtitle.
?film movie:actor <http://data.linkedmdb.org/resource/actor/"""+actors[s][0]+"""> .
?mactor movie:actor_name ?actname.
?mactor movie:actor_actorid ?aid.
FILTER(?aid!="""+actors[s][0]+""")
}
"""

# params sent to server
params = { 'query': sparqlq }
# create appropriate param string
paramstr = urlencode(params)

# create GET http request object with params appended
req = Request(endpoint+paramstr)
#print(endpoint+paramstr)
# request specific content type
req.add_header('Accept','application/sparql-results+json')
# dispatch request
page = urlopen(req)
# get results and close
text = page.read().decode('utf-8')
page.close()



# convert to json object
jso = json.loads(text)
# iterate over results
for binding in jso['results']['bindings']:
	# for every column in binding
	line = ""
	for bname,bcontent in binding.items():
		if bname == "actname":
			line = bcontent['value'] + ", "
		elif bname == "mtitle":
			print (line, bcontent['value'])
