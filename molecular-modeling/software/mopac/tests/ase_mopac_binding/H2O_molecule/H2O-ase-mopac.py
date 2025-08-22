#
#  https://wiki.fysik.dtu.dk/ase/ase/calculators/mopac.html
#

from ase.build import molecule
from ase.calculators.mopac import MOPAC
import os

os.environ["ASE_MOPAC_COMMAND"] = "/home/milias/work/software/mopac/mopac-23.1.2-linux/bin/mopac  PREFIX.mop 1> /dev/null"
print("variable ASE_MOPAC_COMMAND=",os.environ["ASE_MOPAC_COMMAND"],"\n")

water = molecule('H2O')

print(water.get_positions() )
#atoms.calc = MOPAC(label='H2O',method='PM7',task='free_energy',magmom='singlet')
#atoms.calc = MOPAC(label='H2O',method='PM6',magmom='singlet',task='')
#atoms.calc = MOPAC(label='H2O',method='PM6',magmom='singlet',task='PRECISE ')
#atoms.calc = MOPAC(label='H2O',method='PM6',magmom='singlet',task='PRECISE ')

#works
water.calc = MOPAC(label='H2O',method='PM6',magmom='singlet',task='PRECISE ',charge=0,relscf=0.1)

print("H2O MOPAC energy :",water.get_potential_energy() )

eigs = water.calc.get_eigenvalues()
print("H2O MOPAC eigs:", eigs)

homo, lumo = water.calc.get_homo_lumo_levels()
print("H2O MOPAC HOMO=", homo, " LUMO=", lumo)

#print (MOPAC.read_results('final_hof'))
#print (MOPAC.read_results['free_energy'])

print(dir(MOPAC))
#print(MOPAC.get_final_heat_of_formation())
print(water.calc.get_final_heat_of_formation())
print(water.calc.methods)
print(water.calc.get_property('dipole'))
print(water.calc.get_property('free_energy'))
#print(water.calc.get_property('magmom'))
print("water.calc.get_atoms()=",water.calc.get_atoms())
print("water.calc.get_atoms()=",water.calc.get_atoms().symbols)
print("water.calc.get_atoms()=",water.calc.get_atoms().numbers)
print("water.calc.get_atoms()=",water.calc.get_atoms().positions)
#print("water.calc.get_atoms()=",water.calc.get_atoms.get_position())

#print("water.calc.read_atoms()=",water.calc.read_atoms(water))

print("water.calc.get_dipole_moment()=",water.calc.get_dipole_moment())
#print("water.calc.get_potential_energies()=",water.calc.get_potential_energies())

print("water.calc.get_default_parameters = ",water.calc.get_default_parameters())
print("water.calc.implemented_properties= ",water.calc.implemented_properties)

#atoms=MOPAC.read_atoms('H2O')

#print(MOPAC.read_atoms('H2O').get_positions() )
#print(water.get_positions() )
#print(water.positions )

