import os
import json

# --------------------------------------------------------
# Pywal Colors
# --------------------------------------------------------

colors = os.path.expanduser('~/.cache/wal/colors.json')
colordict = json.load(open(colors))

ColorsDict = {f"color{i}":colordict['colors'][f'color{i}'] for i in range(16)}
