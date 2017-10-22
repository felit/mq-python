import pandas as pd

d = {'col1': ['11', '1-1', '3', '4', '5'], 'col2': ['22', '2-2', '3', '4', '5']}
df = pd.DataFrame(data=d, index=["row1", "row2", "row3", "row4", "row5"])
print df.index
print df.values
print 'columns: %s' % df.columns
print df.head(2)
print df.sort_values(by='col2')

data2 = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
df2 = pd.DataFrame(data2)
print df2.T
print pd.DataFrame(data2, index=['first', 'second']).T
