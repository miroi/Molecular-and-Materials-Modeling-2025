#!/usr/bin/env python
from ase import Atoms
from ase.calculators.espresso import Espresso, EspressoProfile
import os
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
sys.stdout.flush() 

# ==============================================
# ASE DFPT Raman calculation
# Note: LDA + Norm-conserving psp needed for Raman
# ==============================================

# ==============================================
# 1. Quantum Espresso input parameters
# ==============================================
pseudopotentials = {'Si': 'Si.pz-vbc.UPF'} 

# SCF input parameters
scf_input_data = {
    'control': {
        'calculation': 'scf',
        'prefix': 'si_scf',
        'outdir': './tmp'
    },
    'system': {
        'ecutwfc': 30,
        'ecutrho': 240,
        'occupations': 'fixed',
        'ibrav': 0,
        'nat': 2,
        'ntyp': 1
    },
    'electrons': {
        'conv_thr': 1.0e-8
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

# Post-processing commands (don't run in parallel)
dynmat_command = f'{qe_bin}/bin/dynmat.x < dynmat.in > dynmat.out 2>&1'

pw_profile = EspressoProfile(
    command=pw_command,
    pseudo_dir='./'
)

# ==============================================
# 3. Atomic Structure 
# ==============================================
atoms = Atoms(
    symbols=['Si', 'Si'],
    positions=[
        [0.000000000, 0.000000000, 0.000000000], 
        [1.357500000, 1.357500000, 1.357500000]
    ],
    cell=[
        [0.000000000, 2.715000000, 2.715000000],
        [2.715000000, 0.000000000, 2.715000000],
        [2.715000000, 2.715000000, 0.000000000]
    ],
    pbc=[True, True, True]
)

# ==============================================
# 4. SCF calculation
# ==============================================
print("\nRunning SCF calculation...", flush=True)
os.makedirs('tmp', exist_ok=True)

scf_calc = Espresso(
    profile=pw_profile,
    pseudopotentials=pseudopotentials,
    input_data=scf_input_data,
    kpts=(2, 2, 2)
)
atoms.calc = scf_calc
total_energy = atoms.get_potential_energy()
print(f"  Total energy: {total_energy:.6f} eV", flush=True)

# ==============================================
# 5. DFPT phonon calculation (Gamma only)
# ==============================================
print("\nRunning DFPT phonon calculation...", flush=True)

with open('ph.in', 'w') as f:
    f.write("""&INPUTPH
   tr2_ph = 1.0e-12,
   prefix = 'si_scf',
   outdir = './tmp',
   amass(1) = 28.0855,
   epsil = .true.,
   trans = .true.,
   lraman = .true.,
   fildyn = 'si.dyn',
   ldisp = .false.
/
0.0 0.0 0.0
""")

try:
    subprocess.run(f"{ph_command} < ph.in > ph.out 2>&1", shell=True, check=True)
    print("  DFPT Phonon calculation completed successfully", flush=True)
except subprocess.CalledProcessError as e:
    print(f"Error running phonon calculation: {e}", flush=True)
    sys.exit(1)

# ==============================================
# 6. Raman Calculation 
# ==============================================
print("\nCalculating Raman spectra...", flush=True) 

with open('dynmat.in', 'w') as f:
    f.write("""&INPUT
   fildyn = 'si.dyn',
   asr = 'crystal',
/
""")

try:
    subprocess.run(dynmat_command, shell=True, check=True)
    print("  Raman calculation completed successfully", flush=True)
except subprocess.CalledProcessError as e:
    print(f"Error running dynmat calculation: {e}", flush=True)
    sys.exit(1)

except Exception as e:
    print(f"Error in plotting: {e}", flush=True)