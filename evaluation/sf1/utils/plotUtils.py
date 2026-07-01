import numpy as np
import matplotlib.pyplot as plt


clrsep = 'blue'
stysep = '-'



clrpg = 'black'
# clrdk = '#FFD700'
clrdk = 'black'

postmarker = 'o'
duckmarker = '*'
# clrgp = "#E88699"
# clrgd = "#E88699"
# clrgp= "#FC8416"
clrgp = "#D64C2F"
clrgd = "#D64C2F"



clrsd = "#5E548E"

clrsp = "#55916C"

clrlk = "#7A9A01"

clrpr = "#00B4D8"

hatchp1 = "x"
hatchp2 = "++"

FIG_HEIGHT = 5
FIG_WIDTH = 15
FONT_SIZE = 30
LINE_WIDTH = 3

def getBarDistributeOffsets(totalWidth, NBars):
    totalWidth = 0.8 # 0.8 of plot width
    barWidth = totalWidth / NBars
    offsets = np.linspace(-totalWidth/2 + barWidth/2, totalWidth/2 - barWidth/2, NBars)
    return offsets

def checkDataNums(data: list, mustBe: int):
    if len(data) != mustBe:
        print(f"Error: Data length {len(data)} does not match the required length {mustBe}. Data: {data}")
        exit()