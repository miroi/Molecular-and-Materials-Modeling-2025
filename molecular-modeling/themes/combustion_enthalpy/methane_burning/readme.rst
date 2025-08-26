==================
Methane combustion
==================

Hc ... combustion (burning) enthalpy

CH4(g) + 2O2(g) = CO2(g) + 2H2O(g); Hc=-890.4 kJ/mol (exp., internet)


Computation:

Hc=2*Hf(H2O)+Hf(CO2)-Hf(CH4)-2*Hf(O2), BUT:  Hf(O2) = 0 (see Google AI search O2 formation enthalpy )


We need: Hf(H2O)=  ?   Hf(CH4) = ?   Hf(CO2) = ?

PM7 calculations
~~~~~~~~~~~~~~~~
Hf(H2O)=-241.83461 KJ/MOL  (exp. -241.82 kJ/mol)
Hf(CO2)=-353.61378 KJ/MOL  (exp. -393.5 kJ/mol)
Hf(O2)=-35.54888 KJ/MOL  (exp. 0)
Hf(CH4)=-60.26807 KJ/MOL  (exp. −74.9kJmol−1.)

with Hf(O2)=0:
Hc=2*(-241.83461)-353.61378-(-60.26807)-2*(0)=-777.01493 kJ/mol MOPAC  (exp. -890.4 kJ/mol )

with Hf(O2):
Hc=2*(-241.83461)-353.61378-(-60.26807)-2*(-35.54888)=-705.91717 kJ/mol (exp. -890.4 kJ/mol )

NWChem B3LYP/ 6-31G**
~~~~~~~~~~~~~~~~~~~~
CH4: Hf =  -40.524013944002+0.047865 au
CO2: Hf =  -188.580939236330 + 0.014232 au
H2O: Hf =  -76.419737359452 +  0.024187 au
O2:  Hf = -150.320040182134 + 0.006140 au

Hf = 2*Hf(H2O)+Hf(CO2)-Hf(CH4)-2*Hf(O2) 
Hf = (2*(-76.419737359452 +  0.024187)+(-188.580939236330 + 0.014232)-(-40.524013944002+0.047865)-2*(-150.320040182134 + 0.006140))
Hf = -0.253858646964 au = -666.505928375711 kJ/mol  (exp. -890.4 kJ/mol )

