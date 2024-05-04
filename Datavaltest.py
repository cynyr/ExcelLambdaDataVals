data = [
["A","Pink","Steel","Box"],
["A","Pink","Steel","Bag"],
["A","Pink","Al","Box"],
["A","Purple","AL","Box"],
["A","Purple","AL","Bag"],
["A","Purple","Cu","Crate"],
["A","Purple","Cu","Pallet"],
["A","Purple","Mg","Bag"],
["A","Purple","Mg","Box"],
["A","Purple","Mg","Pallet"],
["A","Purple","Mg","Crate"],
["B","Orange","Steel","Box"],
["B","Orange","Steel","Bag"],
["B","Orange","Al","Box"],
["B","Green","AL","Box"],
["C","Green","AL","Bag"],
["C","Green","Cu","Crate"],
["B","Green","Cu","Pallet"],
]









def tree (data):
    if len(data) == 1:
        return data
    elif isinstance(data[0], list):
        if len(data[0]) == 1:
            return [[x[0] for x in data]]
        else:
            us = list(set([x[0] for x in data]))
            a = []
            a.append(["" for x in range(len(data[0])-1)]+us)
            for u in us:
                l = tree([x[1:] for x in data if x[0]==u])
                for x in l:
                    a.append([u]+x)
            return a

if __name__ == "__main__":
    import pandas as pd
    import polars as pl
    data3 = [
        ["A","Pink","Steel","Box"],
        ["A","Pink","Steel","Bag"],
    ]
    t = tree(data)
    print("==========================")
    [print(x) for x in t]
    print("==========================")

    #playing with dataframes here for maybe doing this in excel-python in the future.
    df = pd.DataFrame(t).transpose()
    print (df)

    #this is the polars way of doing this. the zip() provides unique column names. 
    # without the column names the concat fails thinking there is already a column with
    # that nome. This could work if we went back through t and padded columns to all be
    # the same length. Pandas just sort of fixes this.
    ldf = [pl.DataFrame({str(col):x}) for x,col in zip(t, range(len(t)))]
    df3 = pl.concat(items=ldf,how="horizontal")
    print(df3)