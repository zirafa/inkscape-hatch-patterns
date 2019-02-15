from string import Template
import math

# Convert millimeters to Inkscape units
SCALE = 96/25.4 


# Simple black line with 0.25 mm line thickness
SVG_PATH = """  <path
     style="stroke:#000000;stroke-width:0.25mm"
     d="M $X1,$Y1 $X2,$Y2"/>
"""


# Bare format of a pattern
SVG_PATTERN = """<pattern id="$PatternID"
inkscape:stockid="$Inkscape"
x="0" y="0" width="$Width" height="$Height"
patternUnits="userSpaceOnUse">
$PatternContent</pattern>
"""

def PatternHatch45(hatch, inkscape, pitch):

	margin = SCALE
	width = math.sqrt(2)*pitch*SCALE

	patternContent =Template(SVG_PATH).substitute(X1= -margin, Y1=  margin, X2=  margin, Y2= -margin)
	patternContent+=Template(SVG_PATH).substitute(X1= -margin, Y1=width+margin, X2=width+margin, Y2= -margin)
	patternContent+=Template(SVG_PATH).substitute(X1=width-margin, Y1=width+margin, X2=width+margin, Y2=width-margin)
	
	return Template(SVG_PATTERN).substitute(PatternID = hatch, Inkscape = inkscape, 
		Width = width, Height= width, PatternContent= patternContent)


def PatternHatch135(hatch, inkscape, pitch):

	margin = SCALE
	width = math.sqrt(2)*pitch*SCALE

	patternContent =Template(SVG_PATH).substitute(X1= width-margin, Y1= -margin, X2= width+margin, Y2= margin)
	patternContent+=Template(SVG_PATH).substitute(X1= -margin, Y1= -margin, X2= width+margin, Y2= width+margin)
	patternContent+=Template(SVG_PATH).substitute(X1= -margin, Y1= width-margin, X2= margin, Y2= width+margin)
	
	return Template(SVG_PATTERN).substitute(PatternID = hatch, Inkscape = inkscape, 
		Width = width, Height= width, PatternContent= patternContent)


def PatternHatchCross(hatch, inkscape, pitch):

	margin = SCALE
	width = math.sqrt(2)*pitch*SCALE

	patternContent =Template(SVG_PATH).substitute(X1= -margin, Y1= width+margin, X2= width+margin, Y2= -margin)
	patternContent+=Template(SVG_PATH).substitute(X1= -margin, Y1= -margin, X2= width+margin, Y2= width+margin)
	
	return Template(SVG_PATTERN).substitute(PatternID = hatch, Inkscape = inkscape, 
		Width = width, Height= width, PatternContent= patternContent)


def Rectangle(x, y, hatch):	
	# Simple rectangle filled with a pattern
	SVG_RECT = """<rect fill="url(#$Hatch)" stroke="black" stroke-width="0.5mm" x="$X" y="$Y" width="$Width" height="$Height" rx="$R" ry="$R" />
	"""

	return Template(SVG_RECT).substitute(Hatch=hatch, X=SCALE*x, Y=SCALE*y, Width=SCALE*16, Height=SCALE*16, R=SCALE*2)


def Text(x, y, text):
	# Simple center aligned text
	SVG_TEXT = """<text
	  style="font-size:14pt;font-family:Calibri;text-align:center;text-anchor:middle;fill:#000000;stroke:none"
	  x="$X"
	  y="$Y">
	  <tspan
		x="$X"
		y="$Y">$Text</tspan></text>
	"""

	return Template(SVG_TEXT).substitute(Text=text, X=SCALE*x, Y=SCALE*y)


# Main program
patterns=''
content=''
x=1.5

for pitch in [2**(i/4) for i in range(13)]:

	content += Text(x+8, 4, '%.1f' % pitch)
	
	hatchName = 'Hatch%.1fx045' % pitch
	inkscapeName = 'Hatch %.1f x 45°' % pitch
	patterns += PatternHatch45(hatchName, inkscapeName, pitch)
	content += Rectangle(x, 6,hatchName)

	hatchName = 'Hatch%.1fx135' % pitch
	inkscapeName = 'Hatch %.1f x -45°' % pitch
	patterns += PatternHatch135(hatchName, inkscapeName, pitch)
	content += Rectangle(x, 26,hatchName)

	hatchName = 'HatchCross%.1f' % pitch
	inkscapeName = 'Cross hatch %.1f' % pitch
	patterns += PatternHatchCross(hatchName, inkscapeName, pitch)
	content += Rectangle(x, 46,hatchName)

	x+=20

# Bare format of an SVG file, patterns and content need to be filled in
SVG_GENERAL = """<svg width="920" height="225" xmlns="http://www.w3.org/2000/svg">
<defs>
$Patterns
</defs>
$Content
</svg>"""

svg = Template(SVG_GENERAL).substitute(Patterns=patterns, Content=content)

open('HatchPatterns.svg', encoding='utf-8', mode='w').write(svg)
open('Defs.txt', encoding='utf-8', mode='w').write(patterns)
