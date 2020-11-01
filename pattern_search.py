import re
import glob
import json
PATH = "./2019/*/*.txt"
files = glob.glob(PATH)

data = []


c1 = "art. (?P<article>\\d+)°? del (?P<instrument>Código Procesal)"
c2 = "art. (?P<article>\\d+)°? del (?P<instrument>Código Laboral)"
c3 = "art. (?P<article>\\d+)°? del (?P<instrument>Código Penal)"
c3bis = "art. (?P<article>\\d+) de la (?P<instrument>Constitución\sNacional)"

c4 = "(?P<article>\\d+)°? de la (?P<instrument>(ley|Ley)\s\\d+\.\\d+)"
c4bis = "(?P<article>\\d+)°? de la (?P<instrument>(ley|Ley)\s[A-z]+)"
c4ter = "(?P<article>\\d+)°? de la (?P<instrument>(ley|Ley)\sde\s\w+\s\w+((\s\w+)?){0,5})"
c41 = "(?P<article>\\d+) de la (?P<instrument>(ley|Ley) \\d+)"
c5 = "art. (?P<article>\\d+)°? de la (?P<law>(ley|Ley)\s\\d+\.\\d+)"
c6 = "\\(Fallos: (?P<fallo>\d+:\d+(;)?)"
c7 = "(?P<fallo>\d{2,3}:\d{2,4}(;)?)"
c8 = "arts\. (?P<art1>\\d+( bis)?).?\s(?P<art2>\d+( bis)?)\sy\s(?P<art3>\d+( bis)?)\sde\sla(?P<instrument>\sConstitución\sNacional)"
c8bis = "(?P<menem>arts\.\s\d+\sy\s\d+\sde\sla\sConstitución\sNacional)"

# patterns = []
patterns = [c1, c2, c3, c3bis, c4, c4bis, c4ter, c41, c5, c8]

for f in files:
    with open(f) as fo:
        f_data = fo.read().replace("\n", " ")
    data.append(
        {
            "file_name": f,
            "text": f_data
        }
    )

records = {}
instruments = []
for i, d in enumerate(data):
    for pattern in patterns:
        matches = [m.groupdict() for m in re.finditer(pattern, d["text"])]
        for m in matches:
            if "instrument" in m:
                instruments.append(m["instrument"])
            if "law" in m:
                instruments.append(m["law"])
        if len(matches) > 1:
            records[files[i]] = matches

with open("export.json", "w") as f:
    f.write(
        json.dumps(records)
    )
