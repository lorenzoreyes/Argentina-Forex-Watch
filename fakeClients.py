import pandas as pd
import datetime as dt
import random
from faker import Faker

fake = Faker()

# lets generate a random client excel info
names = []
for _ in range(10):
    names.append(fake.name())
    
#  Pass it as a DataFrame
clients = pd.DataFrame(names,columns=['Names'],index=range(len(names)))

clients['Emails'] = ([i + '@gmail.com' for i in [i.replace(' ','') for i in names]])

clients.to_csv('FakeClients.csv')
