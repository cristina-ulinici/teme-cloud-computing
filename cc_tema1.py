#python 3.6
import urllib.request as u
import json

url = "https://favqs.com/api/qotd"

j_data = u.urlopen(url).read()
quote = json.loads(j_data)
q = quote['quote']['body']
a = quote['quote']['author']


print("\n\n")
print("Quote of the day: ")
print('"' + q + '"')
print(a)

author = a.replace(" ", "+")


url = "http://openlibrary.org/search.json?author=" + author
j_data = u.urlopen(url).read()
data = json.loads(j_data)
docs = data["docs"]

text = ""
books = []
for doc in docs:
	text = text + doc["title"] + " "
	books.append(doc["title"])

print("\n\n")
print("Publications: ")
# for i in range(1, 20):
# 	print(books[i])
for i in books:
	print(i)

text = text.replace(" ", "+")

text = text.encode("ascii", "ignore").decode("ascii")
url = "http://ws.detectlanguage.com/0.2/detect?q=" + text +"&key=f417d92d93a03c826724acb0a47fae82"
j_data = u.urlopen(url).read()
data = json.loads(j_data)

det = data["data"]["detections"]

langs = []
for d in det:
	langs.append(d["language"])

print("\n\n")
print("Languages: "),
for i in langs:
	print(i),
