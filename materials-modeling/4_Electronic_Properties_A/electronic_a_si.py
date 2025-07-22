#!/usr/bin/env python
from ase import Atoms
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.io import write
import os
import numpy as np
import subprocess
import shutil
import sys
sys.stdout.flush()  

# ==============================================
# ASE electronic properties 
# ==============================================
#
# ==============================================
# 1. Quantum Espresso Input Parameters
# ==============================================
pseudopotentials = {
    'Si': 'Si.upf'
}

input_data = {
    'control': {
        'prefix': 'Si_Electronic_A',
        'outdir': './tmp',
        'verbosity': 'low',
        'tstress': True,
        'tprnfor': True,
        'wf_collect': True,
        'disk_io': 'high'
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

# Main QE calculation 
#pw_command = f'{qe_bin}/bin/pw.x'
pw_command = f'mpirun -np 4 {qe_bin}/bin/pw.x'

# Serial post-processing commands for fast execution
pp_command = f"{qe_bin}/bin/pp.x < pp.in > pp.out 2>&1"
dos_command = f"{qe_bin}/bin/dos.x < dos.in > dos.out 2>&1"

# Memory intensive Parallel post-processing commands (run in one node only)
#projwfc_command = f'{qe_bin}/bin/projwfc.x < projwfc.in > projwfc.out 2>&1'
projwfc_command = f'mpirun -np 4 {qe_bin}/bin/projwfc.x < projwfc.in > projwfc.out 2>&1'

profile = EspressoProfile(
    command=pw_command,
    pseudo_dir='./'
)

# ==============================================
# 3. Atomic Structure
# ==============================================
atoms = Atoms(
    symbols=['Si']*2,
    positions=[ # positions in Angstrom
        [1.3669840665567621, 4.1009521996702860, 4.1009521996702860],
        [0.0000000000000000, 0.0000000000000000, 0.0000000000000000]
    ],
    cell=[ # positions in Angstrom
        [-0.0000000000000000, 2.7339681331135242, 2.7339681331135242],
        [2.7339681331135242, 0.0000000000000000, 2.7339681331135242],
        [2.7339681331135242, 2.7339681331135242, 0.0000000000000000]
    ],
    pbc=[True, True, True]
)
# ==============================================
# 4. Calculator Configuration 
# ==============================================
calc = Espresso(
    profile=profile,
    pseudopotentials=pseudopotentials,
    input_data=input_data,
    kpts=(15,15,15)  
)
atoms.calc = calc

# ==============================================
# 6. Run SCF Calculation
# ==============================================
print("\nRunning SCF calculation...", flush=True)
os.makedirs('tmp', exist_ok=True)
total_energy = atoms.get_potential_energy()
print(f"  Total energy: {total_energy:.6f} eV", flush=True)

# ==============================================
# 7. Calculate electronic properties
# ==============================================
# setup qe_tool
def run_qe_tool(command, input_file, tool_name):
    """Run QE tool with input file and redirect output to file"""
    try:
        with open(input_file, 'r') as fin:
            subprocess.run(command, shell=True, stdin=fin, check=True)
        print(f"  {tool_name} completed successfully", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {tool_name}: {e}", flush=True)
        return False

# 7.1. Charge density calculation
print("\n1. Calculating charge density...", flush=True)
with open('pp.in', 'w') as f:
    f.write(f"""&INPUTPP
    prefix = '{input_data['control']['prefix']}',
    outdir = './tmp',
    filplot = 'charge_density',
    plot_num = 0
/
&PLOT
    iflag = 3,
    output_format = 6,
    fileout = 'charge_density.cube'
/
""")
run_qe_tool(pp_command, 'pp.in', 'pp.x')

# 7.2. TDOS calculation
print("\n2. Calculating DOS...", flush=True)
with open('dos.in', 'w') as f:
    f.write(f"""&DOS
    prefix = '{input_data['control']['prefix']}',
    outdir = './tmp',
    Emin = -20, Emax = 20, DeltaE = 0.01,
    ngauss = 0,
    degauss = 0.02,
    fildos = 'total_dos.dat'
/
""")
run_qe_tool(dos_command, 'dos.in', 'dos.x')

# 7.3. PDOS calculation
print("\n3. Calculating PDOS...", flush=True)
with open('projwfc.in', 'w') as f:
    f.write(f"""&PROJWFC
    prefix = '{input_data['control']['prefix']}',
    outdir = './tmp',
    ngauss = 0,
    degauss = 0.02,
    DeltaE = 0.01,
    Emin = -20,
    Emax = 20,
    filpdos = 'pdos',
    filproj = 'projections'
/
""")
run_qe_tool(projwfc_command, 'projwfc.in', 'projwfc.x')

# 7.4. Organize and process PDOS files
print("\n4. Organizing and processing PDOS files...", flush=True)
os.makedirs('pdos_results', exist_ok=True)
for fname in os.listdir('.'):
    if fname.startswith('pdos.') or fname.startswith('projections'):
        shutil.move(fname, os.path.join('pdos_results', fname))
print("  PDOS files moved to pdos_results directory", flush=True)

# 7.5. Löwdin population analysis 
print("\n6. Extracting Löwdin charges...", flush=True)
lowdin_file = 'lowdin.out'
spilling = None

try:
    with open('projwfc.out', 'r') as f:
        lines = f.readlines()
    
    # Find and save Löwdin charges section
    with open(lowdin_file, 'w') as out_f:
        out_f.write("Löwdin Charges from projwfc.out:\n")
        out_f.write("================================\n")
        
        in_section = False
        for line in lines:
            if "Lowdin Charges:" in line:
                in_section = True
            elif "Spilling Parameter:" in line:
                spilling = float(line.split()[-1])
                out_f.write(f"\nSpilling Parameter: {spilling:.6f}\n")
                break
            
            if in_section:
                out_f.write(line)
    
    print(f"  Löwdin charges saved to {lowdin_file}", flush=True)
    if spilling is not None:
        print(f"  Spilling parameter: {spilling:.6f} (values <0.05 are good)", flush=True)
except Exception as e:
    print(f"Error extracting Löwdin charges: {str(e)}", flush=True)

print("\n=== Electronic Structure Analysis Complete ===", flush=True)
print("Generated files:", flush=True)
print("- Charge density: charge_density.cube", flush=True)
print("- Total DOS: total_dos.dat", flush=True)
print("- PDOS files: pdos_results/", flush=True)
print("- Löwdin Charges: lowdin.out", flush=True)