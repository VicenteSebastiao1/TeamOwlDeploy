
import pandas as pd
from books.models import Author

a = Author.objects.all()
print(a) 

filename = "/Users/vicentesebastiao/Desktop/book-review-dataset/AuthorID.xlsx"
data = pd.read_excel(filename)
first_names = data['Unnamed: 1'].values
last_names = data['Unnamed: 2'].values
unique = []
i = -1
for n1 in first_names:
    i+=1
    print(i)
    n2 = last_names[i]
    if n1 is None or n1 == "nan" or n2 is None or n2 == "nan":
        continue
    x = str(n1) + '-' + str(n2)
    if x in unique:
        continue
    unique.append(x)



cnt = 1
for a in unique:
    cnt = cnt + 1
    id = cnt 
    fn= a.split("-")[0]
    ln = a.split("-")[1]
    auth  = Author(first_name=fn,last_name=ln)
    if Author.objects.filter(first_name=fn,last_name=ln):
        continue

    auth.save()


