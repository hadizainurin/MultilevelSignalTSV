import math
import csv
import numpy as np
from math import pi

#  Insert value here
e_di = 11.7 * (8.85 * 10 ** -12)  #silicon permitivity
Hint = 0.36 * 10 ** -6  #Interconnect height
Smin = 0.3 * 10 ** -6 #minimum spacing between a metal wire and a TSV
Ww = 0.2 * 10 ** -6  #  Wire width
Sw = 0.2 * 10 ** -6  #  Wire spacing between two parallel wires
Hw = 0.3 * 10 ** -6  #  Wire spacing between two adjacent metal layers in z-direction
Tw = 0.36 * 10 ** -6  #  Metal wire thicknes10
tau = 3.7 #tau constant
#  Cside1
#  Variables and constant
#  Ctt
#alpha = math.exp(-(H+T) / (S + W))
#Create a new file for ctsv and
header = ['width','space', 'height', 'ctt', 'cself', 'ctsv']
with open("output_ctsv_1.csv", "w", encoding='UTF8', newline='') as h:
    writer = csv.writer(h)
    writer.writerow(header)
    h.close()

#Main program
def main():
    ctoptotal()
    cside()
    ctt()
    print("H ", height)
    print("S ", space)
    print("W ", width)
    ctsv()
    f = open("output_ctsv.txt", "a")
    print("H: ", height, file=f)
    print("S: ", space, file=f)
    print("W: ", width, file=f)
    print(ctsv(), file=f)
    f.close()
    f_ctt = open("output_ctt.txt", "a")
    print(ctt(), ",",  file=f_ctt)
    f_cself = open("output_cself.txt", "a")
    print(cself(), ",",  file=f_cself)
    f_ctsv = open("output_ctsv.txt", "a")
    print(ctsv(), ",",  file=f_ctsv)
    f_x = open("output_cx.txt", "a")
    print(width, ",",  file=f_x)
    f_y = open("output_cy.txt", "a")
    print(space, ",",  file=f_y)
    #csv for graph visualization
    data =  [width, space, height, ctt(), cself(), ctsv()]
    #graph ctt
    # So here we will look at some changes
    fctt = open("output_ctsv_1.csv", "a", encoding='UTF8', newline='')   #When height is constant
    #fctt = open("output_ctsv2.csv", "a", encoding='UTF8', newline='')  #when space is constant
    #fctt = open("output_ctsv3.csv", "a", encoding='UTF8', newline='')  #when width is constant
    #csv writer
    writer =csv.writer(fctt)
    writer.writerow(data)
    fctt.close()


#Define multiple wires on Ground Plane that is related to our 3D TSV model
def c_aw_g(W, H):
    c_aw_g_temp = e_di * 1.15 * (W / H)
    #print("c_aw_g_temp", c_aw_g_temp)
    return c_aw_g_temp


def c_fw_g(T, H): #This one Sw is 0
    c_fw_g_temp = e_di * (2.80 * (T / H) ** 0.222)#confirmed manual calculation
    return c_fw_g_temp


#Define Fringe Capacitance
def c_sw_top(W,H,T,S): #This function is for Cfr_2
    A = (e_di / (pi / 2)) #Confirmed manually
    B = math.log((H + n_function(W, S, H, T) * T + math.sqrt(S ** 2 + (n_function(W, S, H, T) * T) ** 2 + (2 * H * n_function(W, S, H, T) * T))) / (S + H)) #Confirmed manually
    C_sw_top = A * B #Confirmed manually
    return C_sw_top

#Very likely this is unnecessary
def c_sw_top2(H, S, S1, T, S2): #This function is for Cfr_2
    A = (e_di / (pi / 2)) #Confirmed manually
    B = math.log((H + n0_function(S1, H, T, S2) * T + math.sqrt(S ** 2 + (n0_function(S1, H, T, S2) * T) ** 2 + (2 * H * n0_function(S1, H, T, S2) * T))) / (S + H)) #Confirmed manually
    C_sw_top2 = A * B #Confirmed manually
    return C_sw_top2

#Noted H = vertical spacing, S = horizontal spacing, W = metal width and T = metal thickeness
def c_top_top(H, S, W, T):
    alpha = math.exp(-(H + T) / (S + W))
    C = ((W * pi * alpha) + (H + T) * (math.log(1 + (2*W/S)) + math.exp(-1 * ((S + T) / (3 * S)))))   #Bypass the inline limit
    Ctoptop = e_di * W * alpha * (math.log((1 + (2 * W / S))) + math.exp(-1 * ((S + T) / (3 * S)))) / C
    return Ctoptop


def n_function(W, S, H, T):
    n = math.exp(W + S - math.sqrt(S**2 + T**2 + (2 * H * T)) / (tau * W))
    return n

def n0_function(S1, H, T, S2):
    n0 = math.exp(-1 * ((math.sqrt(S1**2 + (H + 1/2 * T)**2) + S1) / (2 * S2)) + 1/5)
    return n0

#Definition parameter
def l_fr_1(S):
    L_fr_1 = (0.4 * S /2) #effective length affecting fringe capacitance of a TSV
    return L_fr_1


def mw(S):
    Mw_temp = (S / (2 * (Ww + Sw)))  #This is a parameter that need to be changes before running any simulation
    Mw = math.floor(Mw_temp)
    return Mw


def nw(W):
    Nw_temp = (W / (Ww + Sw))
    Nw = math.floor(Nw_temp) #int value
    return Nw


"""
Section A (Ctop = Ctop1 + Ctop2)
# W --> Wtsv, S --> Stsv, H (Constant) --> Htsv
"""
#  Function for Ctop1
def carea1(W):
    #carea1 --> c_aw_g * Wtsv
    Carea1 = c_aw_g(Ww, Hw) * W
    return Carea1


def cfr1(W):
    #c_fw_g(Tw, Hw) * Wtsv
    C_fr_1 = c_fw_g(Tw, Hw) * W
    return C_fr_1


def ctop1(): #Correct Formula Done
    Ctop1 = nw(width) * (carea1(width) + (2 * cfr1(width))) 
    return Ctop1


#Ctop2 section
def c_fr_2():
    #c_fr_2 --> c_sw_top(W,H,T,S) * Ww
    C_fr_2 = c_sw_top(l_fr_1(space), 0, (space/2), Hw) * Ww 
    return C_fr_2


def cs1():
    #cs1 --> c_sw_top(W,H,T,S) * Stsv / 2 , n0_function(S1,H, T S2)
    Cs1 = c_sw_top((Sw/2),(Hw/2), Tw, 0) * (space / 2) * n0_function(0,(Hw/2),Tw,Sw) #This is surrounded by wire therefore c_sw_top * n0
    return Cs1


def cs2():
    #cs2 --> c_sw_top(W,H,T,S)
    Cs2 = (c_sw_top(l_fr_1(space), 0, (space/2), (Hw/2)) * Hw / 2)
    return Cs2


def c_fr_3():
    #Capacitance in parallel, Ctotal = C1 + C2 + ....
    C_fr_3 = cs1() + cs2()
    return C_fr_3


def ctop2():
    Ctop2 = nw(width) * (c_fr_2() + (2 * c_fr_3()))
    return Ctop2


def ctoptotal():
    ctop_total = (ctop1() + ctop2()) / 8  #In an island, TSV Top to bottom is 9
    #Debugging
    print("Stsv: ", space)
    print("Wtsv: ", space)
    #Debugging
    #A  1.0060355389382757e-14 when h,s,w = 5um, 8.942538123895783e-15 for when divide by 9 but 8 is more acceptable
    print("The total top capacitance: ", ctop_total)
    return ctop_total

"""
#  Section B (Cside = Cside1 + Cside2)
#  Noted: m_wire --> The number of loop also referring to m, e.g: cs4(m) --> cs4(m_wire)
"""
#  Cside1
def c_fr_4(m_wire):
    W = (l_fr_1(space) / (2 * mw(space)))
    H = m_wire * Sw + (m_wire - 1) * Ww  #abs(m_wire * Sw + (m_wire - 1) * Ww)
    T = Ww
    S = (Hw + (2 * m_wire - 1) * l_fr_1(space) / (2 * mw(space)))
    #   c_fr_4 --> c_sw_top(W,H,T,S) * Wtsv, Noted we put: abs to H so that it always return positive value
    C_fr_4 = c_sw_top(W, H, T, S) * width  #c_sw_top(W, H, T, S)
    #   WORKING print("C_fr_4_temp", C_fr_4_temp)
    return C_fr_4


def c_fr_5(m_wire):
    H = abs(m_wire * Sw + (m_wire - 1) * Ww)
    S = (Hw + m_wire * (l_fr_1(space)/mw(space)))
    W = (l_fr_1(space) / (4 / mw(space)))
    T = Ww
    #   c_fr_5 --> c_top_top(H,S,W,T)* Wtsv
    C_fr_5 = c_top_top(H, S, W, T) * width
    return C_fr_5


def cside1():
    Cside1 = 0
    #   m_wire will always start at 1 as default value
    for m_wire in range(mw(space)):
        Cside1_temp = (c_fr_4(m_wire) + 2 * c_fr_5(m_wire))
        #Cside1 = Cside1_temp
        Cside1 = Cside1 + Cside1_temp
        return Cside1


#  Cside2 section
def cs3():
    #  cs3 * Ww with cs3 -->c_sw_top(W,H,T,S)
    Cs3 = c_sw_top((space / 2), Hw, (space / 2), 0) * Ww
    return Cs3


def Cs4(m_wire):
    W = (l_fr_1(space) / (2 * mw(space)))
    S = (Hw + (2 * m_wire - 1) * (l_fr_1(space) / (2 * mw(space))))
    T = Ww
    H = (m_wire * Sw + (m_wire - 1) * Ww)  #abs((m_wire * Sw + (m_wire - 1) * Ww))
    #  Cs4(m) = cs4(m) * Stsv2 with cs4(m) -->c_sw_top(W,H,T,S)
    Cs4 = c_sw_top(W, H, T, S) * (space / 2)
    return Cs4


def c_fr_6(m_wire):
    C_fr_6 = cs3() + Cs4(m_wire) #Total parallel capacitance
    return C_fr_6


def cs5():
    #Cs5 = cs5 * (Stsv / 2) with cs5 -->c_sw_top(W,H,T,S)
    Cs5 = c_sw_top(Sw / 2, Hw, Tw, 0) * (space / 2)
    return Cs5


def cs6():
    #Cs6 = cs6 * Sw with cs6 -->c_sw_top(W,H,T,S)
    Cs6 = c_sw_top(space / 2, 0, space / 2, Hw) * Sw
    return Cs6


#####Cs7 Function
def cs7(m_wire):
    W = (l_fr_1(space) / (2 * mw(space)))
    S = Sw + (2*m_wire - 1) * (l_fr_1(space) / (2 * mw(space)))
    T = Sw
    H = abs(m_wire * Sw + (m_wire - 1) * Ww)  #abs(m_wire * Sw + (m_wire - 1) * Ww)
    #Cs7 = cs7 * Stsv / 2 with cs7 -->c_sw_top(W,H,T,S)
    Cs7 = c_sw_top(W, H, T, S) * (space / 2)
    return Cs7


def c_fr_7(m_wire):
    C_fr_7 = cs5() + cs6() + cs7(m_wire)
    return C_fr_7


def cside2():
    Cside2 = 0
    for m_wire in range(mw(space)):
        Cside2_temp = (c_fr_6(m_wire) + 2 * c_fr_7(m_wire)) #mth wire
        Cside2 = Cside2 + Cside2_temp
        return Cside2


#   The overall side capacitance
def cside():
    Cside = (cside1() + cside2())
    print("The total side capacitance: ", Cside)
    return Cside


def cself():
    Cself = ctoptotal() + cside()
    print("The self capacitance: ", Cself)
    return Cself

"""
Section 3 (Ctt)
K_corner if <4.0 then K = 2 else
"""
def cc1():
    #   Cc1 = e_di * (((Htsv - 2 * L_fr_1) * Wtsv) / Stsv)
    #   This calculation has a way for to become negative if height < width
    Cc1 = e_di * (((height - 2 * l_fr_1(space)) * width) / space)
    return Cc1


def cc2():
    #Kcorner calculation
    B = (height / space) #Htsv / Stsv
    if B <= 4.0:
        Kcorner = 1/2 * height / space
    else:
        Kcorner = 2
    #   print("Kcorner", Kcorner)
    #Cc2 = (e_di / (pi * math.sqrt(2))) * Htsv * Kcorner
    Cc2 = (e_di / (pi * math.sqrt(2))) * height * Kcorner
    return Cc2

def ctt():
    Ctt = 4 * (cc1() + cc2())  #Surrounding capacitance
    print("The surrounding capacitance: ", Ctt)
    return Ctt
    #   Testing purpose
    #print("Cc1 Cc2 Ctt1", Cc1, Cc2, Ctt1)
    #Cc3 = (e_di * ((Htsv - 2 * Hint - 2 * L_fr_2) * Wtsv) / Stsv)
    #Cc4 = (e_di / (pi * math.sqrt(2)) * Htsv * Kcorner)
    #Ctt2 = 4 * (Cc3 + Cc4)
    #print("Cc3 Cc4 Ctt2", Cc3, Cc4, Ctt2)
    #Ctt = Ctt1 + Ctt2

#Capacitance Metal Wires Connected to TSV
def c_aw_w():
    C_AW_W = (e_di * (0.03 * (Ww/Tw) + 0.83 * (Tw/Hw) - 0.07 * (Tw/Hw) **0.222) * (Sw/Hw) ** -1.34)
    return C_AW_W


#Overall Program
def ctsv():
    Ctsv = (ctoptotal() + cside() + ctt()) #Ctt2 is for top,bottom and side
    print("Total capacitance of TSV: ", Ctsv)
    return Ctsv

#Main Input Configuration (Noted: Changed in the format of (desire_input, max_input, increment))
space = 5.0 * 10 **-6 #Constant width due to limitation of size of TSV (or TSV Diameter)
#for height in np.arange(20.0 * 10 **-6, 105 * 10 **-6, 5 * 10 **-6): #TSV Length
#space = 20.0 * 10 **-6 #Constant width due to limitation of size of TSV (or TSV Diameter)
width = 5.0 * 10 **-6 #height
for height in np.arange(5.0 * 10 **-6, 20 * 10 **-6, 1 * 10 **-6): #TSV Pitch
    main()

#for height in np.arange(20.0 * 10 **-6, 105 * 10 **-6, 5 * 10 **-6): #TSV Length
#    for space in np.arange(20.0 * 10 **-6, 185 * 10 **-6, 5 * 10 **-6): #TSV Pitch
#        main()


#Rtsv
#Dtsv = R. C --> multilelvel signlaing
#MCF is not included for now