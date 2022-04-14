import math
from cmath import sqrt
import array as arr
from math import pi
#TSV CONFIGURATION
width = 60 * 10 ** -6 #TSV diameter = 20 um
height = 20 * 10 ** -6 #TSV Length = 20 um
Cc = 2.29E-15 #TSV Pitch = 60 um (This is based on our assumption where we assume that the pitch is between two corner of TSV)
Cs = 1.63E-13
Ctsv= 1.60E-13
N = 4 #Number of TSV

#END OF CONFIGURATION#
"""DEPRECATED BUT MIGHT BE INCLUDED IN FUTURE VERSION"""
Vn_i = 1
Vn_f = 0.5
Cs = 1.25 * 10 ** -6
MCF = 4
# h = n-1, j = n
#Transition Energy Model Estimation
#Noted TSV + Wires
#Ebus = Eself+ Ecoupling

#Coupling-Transition Energy
#Ecoupling = Cc * ((Vn_f[n-1] - Vn_f[n])**2 + (Vn_f[n] - Vn_f[n-1]) * (Vn_i[n-1] - Vn_i[n])) #Cc is coupling capacitance that we obtained from other equation

#Overall Energy
#Cc from other formula
#Emax = (n-2) * Cself * Vdd ** 2 + (n - 1) * 2 * Cc * Vdd**2
#Power bus
#Assuming in statistical power estimation
# It seems previous works assume that TSV MOS capacitance is used for TSV capacitance
#Fixed Values
e_ox = 3.9
e_si = 11.7 * (8.85 * 10 ** -12)
t_ox = 118.20 * 10 ** -9 #where Esi is relative permittivity of Si substrate and Eox is the permittivity of oxide layer.
ltsv = 20 * 10 ** -6
R_ox = 20 #maximum SiO2 radius and depletion radius
R_metal = 2 #copper radius
Rmax = 2 #Maximum radius

# The parasitic capacitance of TSV mainly contain two parts which are the capacitance of oxide layer and depletion layer
Ctsvacc = Cox = (2 * pi * e_ox * ltsv) / math.log(R_ox/R_metal)
Cdepmin = (2 * pi * e_si * ltsv) / math.log(Rmax/R_ox)
Cs = (Cox * Cdepmin) / math.log(Rmax / R_ox) #Assuming Cs is the tsv self-coupling capacitance
#Self-transition Energy
V_f = 1.1 #Supply Voltage
#Eself = Cs * (V_f[n] * (V_f[n] - V_i[n]))#I think its has to being implemented differently
"""END OF DEPRECATION"""

#Multilevel signaling section
#Vdd for multilevel can be at Vdd or 1/3
ftsv = 1 * 10 ** 9
Vdd = arr.array('d', [1.1, 0.733, 0.367, 0]) #Default Supply Voltage is 1.1
print("This is the current Voltage = ", Vdd)


#Binary signaling
Pcs = N * ftsv * 1/4 * Cs * Vdd[0] **2
Pcc = (N - 1) * ftsv * 1/2 * Cc *Vdd[0]**2
Ptsv = Pcs + Pcc  # Assuming Pcc as coupling and Pcs self-transition capacitance
print("Pcs", Pcs)
print("Pcc", Pcc)

#The N-TSV bus employing multilevel signaling
Pcs2 = N * ftsv/2 * 5/36 * Cs * Vdd[0]**2
Pcc2 = (N-1) * ftsv/2 * 5/18 * Cc * Vdd[0]**2
Ptsv2 = Pcs2 + Pcc2

#N/2-TSV Employing multilevel signaling
Pcs6 = N/2 * ftsv * 5/36 * Cs * Vdd[0]**2
Pcc6 = (N/2 - 1) * ftsv * 5/18 * Cc * Vdd[0]**2
Ptsv3 = Pcs6 + Pcc6 #Equation

print("Power Calculation.....")
print("Ptsv binary signaling", Ptsv)
print("N-TSV with multi-level signaling", Ptsv2)
print("N/2-TSV with multi-level signaling", Ptsv3)

preduce1 = -100 * (Ptsv2 - Ptsv) / Ptsv
preduce2 = -100 * (Ptsv3 - Ptsv) / Ptsv
print("Percentage Reduction for N-bus with multi-level signaling", preduce1)
print("Percentage Reduction for N/2-bus with multi-level signaling", preduce2)


#Section Rtsv
#The power of TSV are
#Assume Rtsv is square shape
p_tsv = 1.68 * 10 ** -9 #resistivity of copper
ltsv = 20 * 10 ** -6 #length of tsv (height of tsv)
r = 10 * 10 ** -6   #radius of tsv = half of width of TSV = W/2
Atsv = r ** 2 #Area of tsv
Rtsv = (p_tsv * ltsv / Atsv)
print("The TSV resistance is: ", Rtsv)
#Assuming the resistance of wires and capacitance are based on M4-M6 metal layer
#When tsv pitch = 20 um
Rwire = 428 * 10 ** -6
Cwire = 0.171 * 10 ** -15
#Wirelength is the summation of width, height and depth (which is the summation of height of all tiers within the 3D Bounding Box)
print("ctsv", Ctsv,"cwire", Cwire)
TSV_WL = (Rtsv * Ctsv) / (Rwire * Cwire) #TSV EQUIVALENRT wirelength
Wire_WL = 1.844 * 10 ** -3 #Based on 3D NoC Simulator setup
#depth = 3*height
WL = TSV_WL + Wire_WL
print("The WL: ", WL)
#NetDelay
NetDelay = 0.5 * Rwire * Cwire * WL**2 + 0.5 * Rtsv * Ctsv * N **2
print("The Delay of the Interconnect is = ", NetDelay)
#Delay of TSV i
#p_wire = 1.68 * 10 ** -8 #resistivity of copper
#lwire = 3 * 10 ** -6  #length of wire
#Awire = Wwire * Twire