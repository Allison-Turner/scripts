#! /usr/bin/env python3

import pandas

df = pandas.read_csv(filepath_or_buffer="/home/allison/Desktop/ipv4_and_ipv6_records.csv", header=0)
num_rows = len(df)

cols = [col for col in df]
num_cols = len(cols)

row_sep = "\n|-\n"

out_str = "{| class=\"wikitable sortable\"" + row_sep

for i in range(num_cols):
    out_str += "! "
    out_str += cols[i]
    if i < (num_cols - 1):
        out_str += " !"

out_str += row_sep

for i in range(num_rows):
    for j in range(num_cols):
        out_str += "| "
        out_str += str(df.iloc[i, j])
        if j < (num_cols - 1):
            out_str += " |"

    if i < (num_rows - 1):
        out_str += row_sep

out_str += "\n|}"

print(out_str)