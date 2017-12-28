import svgwrite
from svgwrite import mm
import numpy as np

#all measurements are in mm
BOARD_WIDTH_NOUNITS = 750
BOARD_HEIGHT_NOUNITS = 450
BOARD_RADIUS_NOUNITS = 220
FIELD_RADIUS_NOUNITS = 17
STROKE_WIDTH_CUT_NOUNITS = 0.1
STROKE_WIDTH_ENGRAVE_NOUNITS = 2
LINE_WIDTH = 3*mm #width of the line connecting the game fields
LINE_FIELD_SEP = 2 #space between connecting line and game fields

BOARD_LOCATION_NOUNITS = (BOARD_WIDTH_NOUNITS/2,BOARD_HEIGHT_NOUNITS/2)

BOARD_LOCATION = ((BOARD_WIDTH_NOUNITS/2)*mm,(BOARD_HEIGHT_NOUNITS/2)*mm)
BOARD_RADIUS = BOARD_RADIUS_NOUNITS*mm
BOARD_WIDTH = BOARD_WIDTH_NOUNITS*mm
BOARD_HEIGHT = BOARD_HEIGHT_NOUNITS*mm

FIELD_RADIUS = FIELD_RADIUS_NOUNITS*mm

STROKE_WIDTH_CUT = STROKE_WIDTH_CUT_NOUNITS*mm
STROKE_WIDTH_ENGRAVE = STROKE_WIDTH_ENGRAVE_NOUNITS*mm
STROKE_COLOR_CUT = svgwrite.rgb(255, 0, 0, '%')
STROKE_COLOR_ENGRAVE = svgwrite.rgb(0, 0, 255, '%')

CUT_CIRCLES = [6,10,14,18,20,24,26,30,34] #circles on the board to be cut instead of engraved (by index)

#settings for spiral form
K = 32 #scale factor for how much spiral is spread
DIST = 59 #sets the distance between each field
BOARD_X_NOUNITS,BOARD_Y_NOUNITS = BOARD_LOCATION_NOUNITS
N_FIELDS = 31+5 #number of fields

patches = [] # contains svg objects to be drawn
theta=0
#cache information about previous fields for drawing lines in between
prev_location_nounits = (0,0)
prev_width_nounits = 0
width_nounits = 0

#draws a line between circle at given location and the previous one
def draw_line(circle_location_nounits):
    dx = prev_location_nounits[0]-circle_location_nounits[0]
    dy = prev_location_nounits[1]-circle_location_nounits[1]
    line_length = np.sqrt(dx**2+dy**2)
    dx_new = dx*((width_nounits+FIELD_RADIUS_NOUNITS+LINE_FIELD_SEP)/line_length)
    dy_new = dy*((width_nounits+FIELD_RADIUS_NOUNITS+LINE_FIELD_SEP)/line_length)
    dx_prev_new = dx*((prev_width_nounits+FIELD_RADIUS_NOUNITS+LINE_FIELD_SEP)/line_length)
    dy_prev_new = dy*((prev_width_nounits+FIELD_RADIUS_NOUNITS+LINE_FIELD_SEP)/line_length)
    new_prev_location_nounits = ((prev_location_nounits[0]-dx_prev_new)*mm,(prev_location_nounits[1]-dy_prev_new)*mm)
    new_location = ((circle_location_nounits[0]+dx_new)*mm,(circle_location_nounits[1]+dy_new)*mm)
    line = dwg.line(new_prev_location_nounits, new_location, stroke=STROKE_COLOR_ENGRAVE,stroke_width=LINE_WIDTH)
    patches.append(line)

#draws a circle at the given location
def draw_circle(location_nounits, j):
    location = (location_nounits[0]*mm, location_nounits[1]*mm)
    color = STROKE_COLOR_ENGRAVE
    color_nounits = STROKE_WIDTH_CUT_NOUNITS
    width = STROKE_WIDTH_ENGRAVE
    width_nounits = STROKE_WIDTH_ENGRAVE_NOUNITS
    # laser cut these given fields
    if(j in CUT_CIRCLES):
        color = STROKE_COLOR_CUT
        width = STROKE_WIDTH_CUT
        width_nounits = STROKE_WIDTH_CUT_NOUNITS
    disc = dwg.circle(center=location,r=FIELD_RADIUS, stroke=color, stroke_width=width, fill='none')

dwg = svgwrite.Drawing('board.svg', (BOARD_WIDTH,BOARD_HEIGHT))
dwg.add(dwg.circle(center=BOARD_LOCATION,r=BOARD_RADIUS, stroke=STROKE_COLOR_CUT, stroke_width=STROKE_WIDTH_CUT, fill='none')) # big circle for the board

# add fields in spiral form
for j in range(1,N_FIELDS+1):
    r = K*j**0.5
    theta += DIST/r
    x = BOARD_X_NOUNITS + r*np.cos(theta)
    y = BOARD_Y_NOUNITS + r*np.sin(theta)

    location_nounits = (x,y)
    draw_circle(location_nounits, j)

    if(j>1):
        draw_line(location_nounits)

    prev_location_nounits = location_nounits
    prev_width_nounits = width_nounits

for c in patches: dwg.add(c)
dwg.save()
