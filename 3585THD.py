# Example 6: Harmonic Levels and Total Harmonic Distortion
# From HP 3585A Operating Manual, Appendix 3A.

import pyvisa
import time
import math

resources = pyvisa.ResourceManager()
analyzer = resources.open_resource('GPIB0::8::INSTR', read_termination='\n')

analyzer.write('I1')	# Set input to 1MOhm
#analyzer.write('FA20') # Start Freq 20Hz
#analyzer.write('FB20KZ') # Stop Freq 20kHz
analyzer.write('TB1ESDCL1PUT THE MARKER ON THE PEAK OF THE FUNDAMENTAL')
analyzer.write('L2FREQUENCY. PRESS CONTINUE WHEN READY')
analyzer.control_ren(6) # Return instrument to local control so you can select the fundamental
input('Press <ENTER> to continue')
analyzer.write('SV1S3CN1T5')
B = float(analyzer.read())
analyzer.write('MCMSCN0D2T5')
tempA = analyzer.read()
tempB = tempA.split(',')
F = float(tempB[0])
A = float(tempB[1])
analyzer.write('RB30HZ')
r = []
i = 1
while i < 5:
  if F*(i+1) > 40000000:
    i = 5
  else:
    analyzer.write('CFUPD1T5')
    r.append(float(analyzer.read()))
    i +=1

AA  = math.sqrt(50/1000) * 10**(A/20)

harms = 0
for x in r:
  harms += (math.sqrt(50/1000) * 10**(x/20))**2
thd = ((math.sqrt((harms))) / AA)*100
thddb = 20 * math.log10((thd/100))

analyzer.write("ESDSL1HARMONIC DISTORTION RESULTS IN DB BELOW SIGNAL")
analyzer.write("L2FUNDAMENTAL =        " + str(A) + "       " + str(F))
analyzer.write("L3   HARMONIC 2        " + str(r[0]))
if len(r) > 1:
  analyzer.write("L4   HARMONIC 3        " + str(r[1]))
if len(r) > 2:
  analyzer.write("L5   HARMONIC 4        " + str(r[2]) + "      THD%=  " + '{0:.2f}'.format(thd))
else:
  analyzer.write("L5                            THD%=  " + '{0:.2f}'.format(thd))
if len(r) > 3:
  analyzer.write("L6   HARMONIC 5        " + str(r[3]) + "      THD=  " + '{0:.2f}'.format(thddb))
else:
  analyzer.write("L6                            THD=  " + '{0:.2f}'.format(thddb))



