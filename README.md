# Umbrella Sampling

Program to set up a 2D umbrella sampling simulation using Amber.

To run this code, you need to use Python3.

Currently only works by running on the command line, updating for use in Jupyter notebooks/python scripts.

Currently only sets up the diagonal, will be expanded to fill out the surface.

## How to use

Type the following into the command line to use. The additional restraints file is not a mandatory input:

```bash
$ UmbrellaSampling2.py -v <cv_file> -c <rcs_file> -m <md_file> -r <restraint_file> -s <restart> -p <parameter>
```
#### Collective variable file
```bash
-v <cv_file>, --cvs <cv_file>
```
Format for a distance between two atoms: 
```bash
<atom1> <atom2> <fc>
```
Format for an angle: 
```bash
<atom1> <atom2> <atom3> <fc>
```
Format for a dihedral: 
```bash
<atom1> <atom2> <atom3> <atom4> <fc>
```
Format for a difference between two distances (atom1-atom2) - (atom3-atom4): 
```bash
<atom1> <atom2> <atom3> <atom4> 1 -1 <fc>
```
The atom numbers are those from the PDB. One row per CV, final column is the force constant.

#### RC file
```bash
-c <rcs_file>, --rcs <rcs_file>
```
File containing RC values in two columns along the initial MEP guess (i.e. surface diagonal). Space or tab separates each column. 
RC columns must be in the same order as CV file rows.

#### MD file
```bash
-m <md_file>, --md <md_file>
```
File containing information for MD run including QM/MM information. Option nmropt=1 must be included.

#### Additional restraints file
```bash
-r <restraint_file>, --rest <restraint_file> 
```
  
Restraints file in Amber format. This is not a mandatory, only if your system requires extra restraints. 

#### Amber restart file
```bash
-s <restart>, --rst <restart>
```
Restart file in Amber format to start US from. Usually chosen from QM/MM or MM MD.

#### Amber parameter file
```bash
-p PARM, --parm PARM
```
Parameter file of the system in Amber format
