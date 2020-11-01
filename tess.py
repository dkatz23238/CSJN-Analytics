import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import sys
import pandas as pd

# PATH = "./test-0.png"
PATH = sys.argv[1]
DEBUG = bool(sys.argv[2])
test = cv2.imread(PATH)
font = cv2.FONT_HERSHEY_SIMPLEX
rgb = cv2.cvtColor(test, cv2.COLOR_BGR2RGB)
d = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang="fra")
n_boxes = len(d["level"])
coords = []
for i in range(n_boxes):
    (x, y, w, h, text) = (d["left"][i], d["top"][i],
                          d["width"][i], d["height"][i], d["text"][i])
    coords.append(
        (x, y, w, h, text)
    )
coords = list(filter(lambda x: x[-1] != "", coords))
index = list(range(len(coords)))

raw_text = " ".join([i[-1] for i in coords])
df = pd.DataFrame(coords, columns=["x", "y", "w", "h", "text"], index=index)
df.index.name = "index"
df = df.reset_index()
df = df.sort_values("y")
previous_y = None
line_number = 0
line_numbers = []
for i, row in df.sort_values("y").iterrows():
    if previous_y is None:
        previous_y = row["y"]
        line_numbers.append(line_number)
    else:
        delta = abs(previous_y - row["y"])
        previous_y = row["y"]
        if delta < 30:
            line_numbers.append(line_number)
        else:
            line_number += 1
            line_numbers.append(line_number)

df["line_number"] = line_numbers
df = df.sort_index()

lines = []
for i in df.line_number.unique():
    l_rows = df[df["line_number"] == i]
    t = " ".join(l_rows.text.values.tolist())
    # print(t)
    lines.append(t)

full_text = "\n".join(lines)

print(full_text)
