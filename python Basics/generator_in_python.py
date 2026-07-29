'''
A generator is a special kind of function that uses yield instead of return. It doesn't create all values at once. Instead, 
it produces one value at a time, pauses, and continues from the same place when asked again. This makes it very memory efficient.

usecase in islamic knowlege chatbot"
n Python, using yield instead of return turns a function into a Generator.

Here is what it means in 

ingest.py (line 130)
:

1. Memory Efficiency (RAM Optimization)
Your Hadith dataset contains over 34,000 records.

With return: You would have to load, parse, and store all 34,000 Document objects into memory at once as a huge list, consuming a large amount of RAM.
With yield: It works one item at a time (Lazily). It creates 1 Document, hands it to the caller, pauses execution, and waits until the next document is requested before continuing the loop.
2. return vs yield
return	yield
Returns all results at once and ends the function.	Emits one item, pauses the function, and resumes for the next item.
Returns a List stored in RAM.	Returns a Generator / Iterator.
3. Why LangChain Uses It
In LangChain, all custom loaders implementing 

BaseLoader
 require a lazy_load() method that yields Document objects one by one:

python
def lazy_load(self) -> Iterator[Document]:
    for record in data:
        # Yields one document at a time without loading everything in memory
        yield Document(page_content=..., metadata=...)

'''

def simple_generator():
    print("First value")
    yield 1
    
    print("Second value")
    yield 2
    
    print("Third value")
    yield 3

print("-----------EXAMPLE 1----------- ")
for num in simple_generator():
    print(num)


print("-----------EXAMPLE 2----------- ")

import pandas as pd

df = pd.read_csv("transaction.csv")             # Suppose you have a 20 GB CSV.

'''
here what happen

transactions.csv (20 GB)

↓

RAM

↓

💥 Out of Memory

'''
#with generator

def read_csv(file):                                   
    with open(file) as f:
        next(f)  #skip header
        for line in f:
            yield line   #yields one line at a time

def process(row):
    print(row)

for row in read_csv("transactions.csv"):
    process(row)

'''
Memory usage

Read one line

↓

Process

↓

Forget it

↓

Read next line

Only one row is in memory.

'''
