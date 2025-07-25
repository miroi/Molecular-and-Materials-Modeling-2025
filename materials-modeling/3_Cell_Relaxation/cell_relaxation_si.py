#!/usr/bin/env python
from ase import Atoms
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.io import write
from ase.optimize import BFGS
import numpy as np
import sys
from ase.filters import UnitCellFilter 
sys.stdout.flush()

# ==============================================
# ASE full relxation (unitcell + atom) 
# ==============================================

# ==============================================
# 1. Quantum Espresso Input Parameters
# ==============================================
pseudopotentials = {'Si': 'Si.upf'} 

input_data = {
    'control': {
        'calculation': 'scf',
        'prefix': 'si',
        'outdir': './tmp',
        'verbosity': 'low',
        'tstress': True,
        'tprnfor': True
    },
    'system': {
        'ecutwfc': 65,
        'occupations': 'smearing',
        'smearing': 'gauss',
        'degauss': 0.01,
        'ibrav': 0,
        'nat': 2,
        'ntyp': 1
    },
    'electrons': {
        'conv_thr': 1.0e-10
    }
}

# ==============================================
# 2. Machine-specific command setup
# ==============================================
# Set QE bin directory 
#qe_bin = "/home/dsen/work/bin/qe-7.4.1_serial"
qe_bin = "/home/dsen/work/bin/qe-7.4.1"

# Job commands
#pw_command = f'{qe_bin}/bin/pw.x'
#ph_command = f'{qe_bin}/bin/ph.x'
pw_command = f'mpirun -np 4 {qe_bin}/bin/pw.x'
ph_command = f'mpirun -np 4 {qe_bin}/bin/ph.x'

pw_profile = EspressoProfile(
    command=pw_command,
    pseudo_dir='./'
)

# ==============================================
# 3. Atomic Structure 
# ==============================================
atoms = Atoms(
    symbols=['Si']*2,
    positions=[
        [1.3574500000, 4.0723500000, 4.0723500000],
        [0.0000000000, 0.0000000000, 0.0000000000]
    ],
    cell=[
        [0.0000000000, 2.7149000000, 2.7149000000],
        [2.7149000000, 0.0000000000, 2.7149000000],
        [2.7149000000, 2.7149000000, 0.0000000000]
    ],
    pbc=[True, True, True]
)

# ==============================================
# 4. Define Calculator Configuration
# ==============================================
calc = Espresso(
    profile=pw_profile,
    pseudopotentials=pseudopotentials,
    input_data=input_data,
    kpts=(15,15,15)  # Fixed k-points
)
atoms.calc = calc

# ==============================================
# 5. Cell Relaxation
# ==============================================
print("\nStarting cell relaxation by ASE", flush=True)

# Setup full cell relaxation
ucf = UnitCellFilter(atoms)

# Create a trajectory file to store relaxation steps
from ase.io.trajectory import Trajectory
traj = Trajectory('relaxation.traj', 'w', atoms)

# Pass the Trajectory object to BFGS 
opt = BFGS(ucf, trajectory=traj, logfile='relaxation.log')

try:
    opt.run(fmax=0.01) # Convergence criterion: max force < 0.01 eV/Å
        
    # Get final results
    relaxed_atoms = ucf.atoms
    final_energy = relaxed_atoms.get_potential_energy()
    forces = opt.atoms.get_forces() # From ASE relaxation steps
    qe_style_forces = relaxed_atoms.get_forces() 
    stress = relaxed_atoms.get_stress()
     
    # Analysis
    force_norms = np.linalg.norm(forces, axis=1)  # Euclidean norms
    max_force = np.max(force_norms)               # ASE-style max norm
    max_qe_force = np.max(np.abs(qe_style_forces)) # Max component across all atoms/directions
    pressure = -np.sum(stress[:3]) * 1602.1766208 / 3

    # Print results
    print("\nFinal results", flush=True)    
    print(f"  Total Energy                  : {final_energy:>12.6f} eV", flush=True)
    print(f"  ASE-style max force (norm)    : {max_force:>8.6f} eV/Å", flush=True)
    print(f"  QE-style max force            : {max_qe_force:>8.6f} eV/Å", flush=True)
    print(f"  Pressure                      : {pressure:>8.6f} kbar", flush=True)

    # Save final structure
    write('final_relaxed_structure.vasp', relaxed_atoms, format='vasp', direct=False)
    print("\nFinal relaxed structure saved to: final_relaxed_structure.vasp", flush=True)

except Exception as e:
    print(f"\nRelaxation failed: {str(e)}", flush=True)
    print("Check output files for error details", flush=True)
finally:
    traj.close()
    print("\nRelaxation complete", flush=True)