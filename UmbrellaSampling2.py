#!/usr/bin/env python3
# Umbrella sampling program
# 05/03/2021

import os
import argparse


def parse_cvs(cvs):
    """

    :param cvs: file containing the collective variables
    :return: list of lists, each list contains the iat string and the force constant
    """

    rcs_for_return = []

    with open(cvs) as cvs_file:
        lines = cvs_file.readlines()
        for line in lines:
            # distance
            if len(line.split()) == 3:
                rcs_for_return.append([f"iat={line.split()[0]},{line.split()[1]}", line.split()[2]])
            # angle
            elif len(line.split()) == 4:
                rcs_for_return.append([f"iat={line.split()[0]},{line.split()[1]},{line.split()[2]}", line.split()[3]])
            # dihedral
            elif len(line.split()) == 5:
                rcs_for_return.append([f"iat={line.split()[0]},{line.split()[1]},{line.split()[2]},{line.split()[3]}", line.split()[4]])

            # difference between two distances
            elif len(line.split()) == 7:
                rcs_for_return.append([f"iat={line.split()[0]},{line.split()[1]},{line.split()[2]},{line.split()[3]}, rstwt={line.split()[4]},{line.split()[5]}", line.split()[6]])

    return rcs_for_return


def create_restraints_file(window, rest_file, iats):
    """

    :param iats:
    :param window:
    :param rest_file:
    :return:
    """

    restraints = open(f"rc{window.split()[0]}_{window.split()[1]}/rc{window.split()[0]}_{window.split()[1]}.RST", "w+")

    restraints.write(f"""# US window restraints
&rst, {iats[0][0]},
r1={window.split()[0]} - 2,r2={window.split()[0]},r3={window.split()[0]},r4={window.split()[0]} + 2,
rk2={iats[0][1]},rk3={iats[0][1]},
 /
&rst, {iats[1][0]},
r1={window.split()[1]} - 2,r2={window.split()[0]},r3={window.split()[0]},r4={window.split()[0]} + 2,
rk2={iats[1][1]},rk3={iats[1][1]},
 /""")

    if rest_file is None:
        pass
    else:
        with open(rest_file, "r") as add_rest:
            lines = add_rest.readlines()
            restraints.writelines(lines)

    restraints.close()


def create_md_file(window, md_file):
    """

    :param window: the umbrella sampling window defined by the restrained value of the CVs
    :param md_file: template input md file
    :return:
    """
    new_md_file = open(f"rc{window.split()[0]}_{window.split()[1]}/{md_file}", "w+")

    with open(md_file, "r") as template:
        template_lines = template.readlines()
        new_md_file.writelines(template_lines)
        new_md_file.write(f"""&wt type='DUMPFREQ, istep1=1 /
    &wt type='END' /
DISANG=rc{window.split()[0]}_{window.split()[1]}.RST
DUMPAVE=rc{window.split()[0]}_{window.split()[1]}.tra
""")

    new_md_file.close()


def create_folders(rcs, md_file, rest_file, cvs):
    """

    :param cvs:
    :param rcs:
    :param md_file:
    :param rest_file:
    :return creates folders in which the MD is run for each window. Contains MD and restraint file:
    """

    lines = open(rcs, "r").readlines()

    iat_list = parse_cvs(cvs)

    for line in lines:
        os.system(f"mkdir rc{line.split()[0]}_{line.split()[1]}")
        create_md_file(line, md_file)
        create_restraints_file(line, rest_file, iat_list)


def new_restart_file(rc_2d, rc_line, md_file):
    """

    :param rc_2d:
    :param rc_line:
    :param md_file:
    :return:
    """

    lines = open(rc_2d, "r").readlines()
    ind = lines.index(rc_line)
    return f"../rc{lines[ind-1].split()[0]}_{lines[ind-1].split()[1]}/{md_file[:-2]}.rst7"


def write_amber_command(rc_2d, md_file, restart, parameter):
    """

    :param rc_2d:
    :param md_file:
    :param restart:
    :param parameter:
    :return:
    """

    return f"""cd $PBS_O_WORKDIR/rc{rc_2d.split()[0]}_{rc_2d.split()[1]}
$AMBERHOME/bin/sander.MPI -O -i {md_file} -o {md_file[:-2]}.log -p ../{parameter} -c ../{restart} -x {md_file[:-2]}.nc -r {md_file[:-2]}.rst7
"""


def write_submission_file(rcs, md_file, restart, parameter):
    """

    :param rcs:
    :param md_file:
    :param restart:
    :param parameter:
    :return:
    """

    with open("Diagonal_US.qsub", "w+") as subscript:
        subscript.write(f"""#!/bin/bash
#
#PBS -l select=1:ncpus=24:mem=20gb
#PBS -l walltime=72:00:00
#PBS -N Diagonal_US

module load apps/amber/18

""")

        rc_lines = open(rcs, "r").readlines()

        for line in rc_lines:
            if line == rc_lines[0]:
                subscript.write(write_amber_command(line, md_file, restart, parameter))
            else:
                subscript.write(write_amber_command(line, md_file, new_restart_file(rcs, line, md_file), parameter))


def main():

    parser = argparse.ArgumentParser(description="Setup QM/MM umbrella sampling for a 2D surface")
    parser.add_argument(
       "-v",
       "--cvs",
       help="File containing collective variables as atoms numbers from PDB. One row per CV, final column containing force constant"
    )

    parser.add_argument(
       "-c",
       "--rcs",
       help="File containing RC values in two columns along the initial MEP guess (i.e. surface diagonal)."
    )

    parser.add_argument(
       "-m",
       "--md",
       help="File containing information for MD run including QM/MM information. Option nmropt=1 must be included."
    )

    parser.add_argument(
       "-r",
       "--rest",
       help="Additional restraint file in Amber format"
    )

    parser.add_argument(
       "-s",
       "--rst",
       help="Restart file in Amber format to start US from"
    )

    parser.add_argument(
       "-p",
       "--parm",
       help="Parameter file in Amber format to start US from"
    )

    args = parser.parse_args()

    write_submission_file(args.rcs, args.md, args.rst, args.parm)
    create_folders(args.rcs, args.md, args.rest, args.cvs)


if __name__ == "__main__":
    main()



