#
#  https://wiki.fysik.dtu.dk/ase/ase/calculators/mopac.html
#

from ase.build import molecule
from ase.calculators.mopac import MOPAC
import os

os.environ["ASE_MOPAC_COMMAND"] = "/home/milias/work/software/mopac/mopac-23.1.2-linux/bin/mopac  PREFIX.mop 1> /dev/null"
print(os.environ["ASE_MOPAC_COMMAND"])

atoms = molecule('H2O')
#atoms.calc = MOPAC(label='H2O',method='PM7',task='free_energy',magmom='singlet')
atoms.calc = MOPAC(label='H2O',method='PM6')

print("H2O MOPAC energy :",atoms.get_potential_energy() )

eigs = atoms.calc.get_eigenvalues()
print("H2O MOPAC eigs:", eigs)

#somos = atoms.calc.get_somo_levels()
#print(" MOPAC somos:", somos)


homo, lumo = atoms.calc.get_homo_lumo_levels()

print("H2O MOPAC  homo, lumo", homo, lumo)

