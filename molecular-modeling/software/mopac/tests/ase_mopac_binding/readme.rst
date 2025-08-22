=========
MOPAC-ASE
=========

set config file
----------------
 ~/.config/ase/config.ini

[abinit]
command = mpiexec /usr/bin/abinit
pp_paths = /usr/share/abinit/psp

[espresso]
command = mpiexec /usr/bin/pw.x
pseudo_path = /usr/share/espresso/pseudo/

[mopac]
command =  /opt/mopac/bin/mopac


milias@DESKTOP-7OTLCGO:~/work/git-projects/Molecular-and-Materials-Modeling-2025/molecular-modeling/software/mopac/tests/ase_mopac_binding/.ase info --calculators mopac
Configuration
-------------

Loaded: /home/milias/.config/ase/config.ini

mopac
  Name:     MOPAC
  Import:   ase.calculators.mopac.MOPAC
  Type:     FileIOCalculator (legacy)

  Configured by section [mopac]:
    command = /home/milias/work/software/mopac/mopac-23.1.2-linux/bin/mopac
    configvars = {}


run test
~~~~~~~~
export ASE_MOPAC_COMMAND="/home/milias/work/software/mopac/mopac-23.1.2-linux/bin/mopac  PREFIX.mop 1> /dev/null"

milias@DESKTOP-7OTLCGO:~/work/git-projects/open-collection/theoretical_chemistry/software/mopac/buildup_on_servers/wsl2_win11_VictusNB/test_runs/ase-run/.python test-ase-mopac.py
O2 MOPAC energy : 0.018604067855432505
O2 MOPAC eigs: [-32.47747 -30.29819 -18.27909 -16.23277 -16.23277 -11.23338 -11.23338
   1.75701]
O2 MOPAC somos: [-11.23338 -13.84258]
O2 MOPAC  homo, lumo -11.23338 -0.20378

