HF molecule
===========

r(HF)
~~~~~~
re(exp) = 0.917	Ang (https://cccbdb.nist.gov/)

re(UFF) = 0.986 Ang
re(MMFF94) = 0.939 Ang <-- better force-field

vib. freq.
~~~~~~~~~~
exp: 4138 cm-1 (Google AI search_
PM7: 3995.84 cm-1
B3LYP/6-31G* : 3976.278 cm-1


Hf(298.15K)
~~~~~~~~~~
exp:  -273.30 +/- 0.70 kJ/mol
PM7:  -259.13887 KJ/MOL

S(298.15K)
~~~~~~~~~
exp: 173.78 J.K-1.mol-1	
PM7:  41.3663 CAL/K/MOL = 173.0765992 J.K-1.mol-1
 (we can calculate G = H - T.S)

dipole moment
~~~~~~~~~~~~~
exp :  1.827 D (https://cccbdb.nist.gov/exp2x.asp?casno=7664393&charge=0 )
PM7:   1.454 D 
B3LYP/6-31G* : 1.859 D

polarizability (isotropic)
~~~~~~~~~~~~~~~~~~~~~~~~~~
exp: 0.800 Å3 (https://cccbdb.nist.gov/exp2x.asp?casno=7664393&charge=0 )
PM7: 0.81538 ANG.**3
B3LYP/6-31G* :  2.8542698 a0**3 = 0.423 ANG.**3 (THE SAME AS IN https://cccbdb.nist.gov/polcomp2x.asp )
B3LYP/d-aug-cc-pvdz : 5.9076153 a0**3 = .8757389844567 = 0.876  ANG.**3

Apply the cubed factor: So, 1 \(a_{0}^{3}\) is approximately 0.148239 \(Ang^{3}\).

MO of HF
~~~~~~~~~
PM7  - see the spredsheet

IP1
~~~

exp: 16.03 eV
HF PM7: -259.13887 KJ/MOL

HF(+) PM7 ROHF:  1228.02109 KJ/MOL
      PM7 UHF:   1225.81666 KJ/MOL

  IP1(PM7,RHF) = E(HF+)-E(HF)=1228.02109-(-259.13887) kJ/mol= 15.4133 eV

  IP1(PM7,UHF) = E(HF+)-E(HF)=1225.81666-(-259.13887) kJ/mol = 1484.95553kJ/mol = 15.390483468 eV



