# ExcelLambdaDataVals
Use Lambda to generate a spill range of all posible multi level data validations from an input table.
This is useful if your tool is data driven and you want updates to the data to automatically show up in the datavalidations.
This is also especially useful if the inputs are in a table and users can add new rows to the table.

You can think of this as building a tree, where the last column passed in is the bottom node as an array.

```
=LAMBDA(datatable, LET(
Y,LAMBDA(G,data,LET(
dcols,COLUMNS(data),
filler, MAKEARRAY(MAX(dcols-1,0),1,LAMBDA(x,y,"")),
labels, UNIQUE(CHOOSECOLS(data,1)),
dv, IF(dcols=1,
UNIQUE(data),
LET(
d_2,REDUCE("__";,labels, LAMBDA(acc,label, LET(
lower, G(G,FILTER(DROP(data,0,1), CHOOSECOLS(data,1)=label)),
lbls2, MAKEARRAY(1,COLUMNS(lower),LAMBDA(x,y,label)),
out, HSTACK(acc,VSTACK(lbls2,lower)),
out
))
),
out,HSTACK(VSTACK(filler,labels),DROP(d_2,0,1)),
out)
),
dv
)),
F,LAMBDA(X, Y(Y,X)),
ans,F(datatable),
ans))(Table1[[column1]:[Column3]])
```

You can also use `VSTACK()`, `chosecols()`, `filter()`, etc. to build the datatable on the fly if your data has extra columns, or is in the wrong order.

This is basically an attempt to mimic the python code in excel.
If there is only 1 column in the data return it.
Otherwise, grab the first column, get the unique values.
Add those to the output.
Filter the remaining colums for each value, and pass to self again.
Add the node of the tree to the top of the return.

DROP(), CHOOSECOLS(), and CHOOSE() + SEQUENCE() get pretty close to pythons list slicers, but having those in excel would be amazing. 
Having a for loop, instead of needing to abuse REDUCE() would 

# FindDataVal
```
=LAMBDA(range,filterlist,LET( d,range, f,filterlist, lc, COUNTA(f), o, OFFSET(d,0,0,lc),m,MMULT(TRANSPOSE((o=f)*1),SEQUENCE(lc,,1,0)), c, MATCH(lc,m,0)-1, os, OFFSET(d,lc,c,ROWS(d)-lc,1), oc, COUNT(os) + COUNTIF(os,"?*&"), ot,OFFSET(d,lc,c,oc,1), IF(oc&lt;1,INDEX(d,1,1),ot)))(I16#,VSTACK(I11,I12,I13))
```
It's important to keep the finder short enough that it fits in the "use formula" version of a datavalidation list. That is why the varibule naming is so bad here.

# Sample Data
Here is some sample data

| T1 | T2 | T3 | T4 |
| --- | --- | --- | --- |
| A | Pink | Steel | Box |
| A | Pink | Steel | Bag |
| A | Pink | Al | Box |
| A | Purple | AL | Box |
| A | Purple | AL | Bag |
| A | Purple | Cu | Crate |
| A | Purple | Cu | Pallet |
| A | Purple | Mg | Bag |
| B | Purple | Mg | Box |
| A | Purple | Mg | Pallet |
| A | Purple | Mg | Crate |
| B | Orange | Steel | Box |
| B | Orange | Steel | Bag |
| B | Orange | Steel | Bag |
| B | Orange | AL | Box |
| B | Green | AL | Box |
| C | Green | AL | Bag |
| C | Green | Cu | Crate |
| B | Green | Cu | Pallet |

# Sample Output
Github Markdown requires column headers, LAMBDA function does not output the header row, just the data.
Also github markdown won't let you have a blank cell, so watch out these all have a non-blank printable space (NBSP) in them.

| col | col | col | col | col | col | col | col | col | col | col | col | col | col | col | col | col | col | col | col | col | col |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| &nbsp; | A | A | A | A | A | A | A | A | B | B | B | B | B | B | B | B | B | C | C | C | C |
| &nbsp; | &nbsp; | Pink | Pink | Pink | Purple | Purple | Purple | Purple | &nbsp; | Purple | Purple | Orange | Orange | Orange | Green | Green | Green | &nbsp; | Green | Green | Green |
| &nbsp; | &nbsp; | &nbsp; | Steel | Al | &nbsp; | AL | Cu | Mg | &nbsp; | &nbsp; | Mg | &nbsp; | Steel | Al | &nbsp; | AL | Cu | &nbsp; | &nbsp; | AL | Cu |
| A | Pink | Steel | Box | Box | AL | Box | Crate | Bag | Purple | Mg | Box | Steel | Box | Box | AL | Box | Pallet | Green | AL | Bag | Crate |
| B | Purple | Al | Bag | #N/A | Cu | Bag | Pallet | Pallet | Orange | #N/A | #N/A | Al | Bag | #N/A | Cu | #N/A | #N/A | #N/A | Cu | #N/A | #N/A |
| C | #N/A | #N/A | #N/A | #N/A | Mg | #N/A | #N/A | Crate | Green | #N/A | #N/A | #N/A | #N/A | #N/A | #N/A | #N/A | #N/A | #N/A | #N/A | #N/A | #N/A |

# Tree Visulization
A tree visuliation of the output table, it's a bit easier to see what is going on.
The output also includes a column for each of the daughter nodes for each level.

```
         A                             B                     C
       /    \                      /   |     \               |
      /      \                 /       |        \            |          
  Pink       Purple       Purple   Orange    Green        Green
  /  \      /   |   \        |      /  \      /   \        / \
Steel AL  AL   Cu    Mg      Mg   Steel AL   AL   Cu     Al   Cu
 |    |   |     |     |       |     |    |    |    |      |    |
Box   Box Box Crate  Bag     Box   Box  Box  Box Pallet  Bag Crate
Bag       Bag Pallet Box           Bag
                     Pallet
                     Crate
```
