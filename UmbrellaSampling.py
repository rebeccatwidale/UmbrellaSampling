import os


class UmbrellaSampling:
    def __init__(self, submission_script, md_file, nodes, procs, job_name, partition, amber_version,
                 interface, memory, walltime, dimension):
        self.cluster = None
        self.submission_script = submission_script
        self.md_file = md_file
        self.nodes = nodes
        self.procs = procs
        self.job_name = job_name
        self.partition = partition
        self.amber_version = amber_version
        self.interface = interface
        self.memory = memory
        self.walltime = walltime
        self.dimension = dimension

    def __repr__(self):
        """
        When the class is called, prints the following text
        """
        return "Have fun umbrella sampling!"

    def set_cluster(self, cluster):
        """
        Checks if the cluster name is correct
        """

        # checks if the use input is correct
        if cluster not in ["BluePebble", "Bluecrystal Phase 4", "Bluecrystal Phase 3", "Coulson"]:

            raise NameError("""Sorry, this is not an HPC cluster on which you can run this script. Possible clusters are:
            Bluecrystal Phase 4 
            Bluecrystal Phase 3
            BluePebble
            Coulson
            """)

        # assigns the cluster variable from user input
        else:
            self.cluster = cluster

    def write_submission_script_header_bp(self):
        """
        Writes submission script based on user defined input for BluePebble
        """

        # checks the number of processors to see if possible for BluePebble
        if not self.procs / self.nodes <= 24:
            raise AssertionError("Incorrect number of processors: BluePebble allows 24 per node.")

        # opens the submission file named by user input
        with open(self.submission_script + ".qsub", "w+") as subscript:
            subscript.write(f"""#!/bin/bash
#
#PBS -l select={self.nodes}:ncpus={self.procs}:mem={self.memory}
#PBS -l walltime={self.walltime}
#PBS -N {self.job_name}

module load apps/amber/{self.amber_version}
""")
            # checks if the external QM interface is with Gaussian
            if self.interface == "Gaussian":

                # load Gaussian module on BluePebble
                subscript.write("module load apps/gaussian/16\n")

            # checks if the external QM interface is with Orca
            elif self.interface == "Orca":

                # writes a header for BluePebble and uses user defined inputs for system specifications
                subscript.write("module load apps/orca/4.2.0\n")

            # checks if Amber will be interfaced with an external QM package
            elif self.interface is None:
                pass

            # if a QM package is requested other than Gaussian or Orca for running on BluePebble, an error is thrown
            else:
                raise NameError(f"Sorry, this QM package is not available on {self.cluster}. Try Gaussian or Orca")

            # writes a working directory path
            subscript.write("\ncd $PBS_O_WORKDIR\n")

    def write_submission_script_header_bc4(self):
        """
        Writes submission script based on user defined input for Bluecrystal Phase 4
        """
        #  checks if the node number is correct for Bluecrystal Phase 4
        if not self.procs / self.nodes <= 28:
            raise AssertionError("Incorrect number of processors: Bluecrystal Phase 4 allows 28 per node.")

        # opens the submission file named by user input
        with open(self.submission_script + ".slurm", "w+") as subscript:

            # writes a header for Bluecrystal Phase 4 and uses user defined inputs for system specifications
            subscript.write(f"""#!/bin/bash
#
#SBATCH -p {self.partition}
#SBATCH -J {self.job_name}
#SBATCH --time={self.walltime}
#SBATCH --nodes={self.nodes}
#SBATCH --ntasks-per-node={self.procs}
#SBATCH --mem={self.memory}

module load apps/amber{self.amber_version}
""")

            # checks if the external QM interface is with Gaussian
            if self.interface == "Gaussian":
                subscript.write(f"module load apps/gaussian/16\n")

            # checks if the external QM interface is with Orca
            elif self.interface == "Orca":
                subscript.write("module load apps/orca/4.2.0\n")

            # checks if Amber will be interfaced with an external QM package
            elif self.interface is None:
                pass
            # if a QM package is requested other than Gaussian or Orca for running on Bluecrystal Phas 4,
            # an error is thrown
            else:
                raise NameError(f"""Sorry, this QM package is not available on {self.cluster}. Try:
Gaussian
Orca
    """)
            # writes a working directory path
            subscript.write("cd $SLURM_SUBMIT_DIR\n")

    def write_submission_script_header_bc3(self):
        """
        Writes submission script based on user defined input for Bluecrystal Phase 3
        """

        #  checks if the node number is correct for Bluecrystal Phase 3
        if not self.procs / self.nodes <= 28:
            raise AssertionError("Incorrect number of processors: Bluecrystal Phase 3 allows 28 per node.")

            # writes a header for Bluecrystal Phase 3 and uses user defined inputs for system specifications
        with open(self.submission_script + ".qsub", "w+") as subscript:
            subscript.write(f"""#!/bin/bash
#PBS -l nodes={self.nodes}:ppn={self.procs}
#PBS -l walltime={self.walltime}
#PBS -q {self.partition}
#PBS -N {self.job_name}

module load apps/amber-{self.amber_version}

cd $PBS_O_WORKDIR
""")
            # checks if Amber will be interfaced with an external QM package
            if self.interface is None:
                pass

            # if a QM package is requested on Bluecrystal Phase 3 an error is thrown
            else:
                raise NameError(f"Sorry, no QM packages are available on {self.cluster}.")

    def write_submission_script_header_coulson(self):
        """
        Writes submission script based on user defined input for Coulson
        """

        #  checks if the node number is correct for Coulson
        if not self.procs / self.nodes <= 16:
            raise ValueError("Incorrect number of processors: Coulson allows 16 per node.")


            # opens submission script for coulson
        with open(self.submission_script + ".slurm", "w+") as subscript:
            subscript.write(f"""#!/bin/bash
#
#SBATCH -J {self.job_name}
#SBATCH --time={self.walltime}
#SBATCH --nodes={self.nodes}
#SBATCH --ntasks-per-node={self.procs}
#SBATCH --mem={self.memory}

module load apps/amber/{self.amber_version}

cd $SLURM_SUBMIT_DIR
""")

            # checks for an interface with an external package
            if self.interface is None:
               pass

            # no external packages available on Coulson - raises error
            else:
                raise NameError(f"Sorry, no QM packages are available on {self.cluster}.")

    def executable(self, mpi):
        """
        prints out the executable of Amber for use in the submission script
        """

        # checks for running sander in parallel - if mpi = 0, assigns non-parallel executable
        if mpi == 0:
            return "$AMBERHOME/bin/sander "

        # checks for running sander in parallel and correct user input
        elif mpi != 0 and type(mpi) == int:

            # assigns BluePebble parallel executable
            if self.cluster == "BluePebble":
                return "mpiexec $AMBER/bin/sander.MPI"

            # assigns parallel executable for all other clusters
            else:
                return "mpirun -np " + str(mpi) + " $AMBER/bin/sander.MPI"

        # raises error if number of parallelised processors is impossible with given user input
        else:
            raise ValueError(f"""This is not a possible number of mpi processors.
Try and integer value between 0 and {self.procs}""")

    def set_dimension(self, dimension):
        """
        Checks if the cluster name is correct
        """

        # checks if the use input is correct
        if dimension != 1 or dimension != 2:

            raise ValueError(f"This is not a possible dimension of this script. Try 1 or 2 dimensions.")

        # assigns the cluster variable from user input
        else:
            self.dimension = dimension

    def get_reaction_coords(self, rc_file):
        """
        Opens file that reads reaction coordinates

        File should have the following format
        X X
        Y Y Y
        where X and Y are atoms using the Amber atom mask syntax
        Two atoms = bond
        Three atoms = angle
        Four atoms = dihedral
        """

        with open(rc_file, "r") as f:
            pass

    def write_restraints_file(self, force_constant, rc_window, well_size, rc_iats):
        """
        Writes a restraints file for the particular reaction coordinate
        """
         # for 1D umbrella sampling, only 1 number needed for defining folders and files
        if self.dimension == 1:
            restraints = open(f"rc{rc_window}/rc{rc_window}.RST", "w+")

        # for 2D umbrella sampling, 2 numbers needed for defining folders and files
        elif self.dimension == 2:
            restraints = open(f"rc{rc_window[0]}_{rc_window[1]}/rc{rc_window[0]}_{rc_window[1]}.RST", "w+")

        # writes a restraint file for US window
        restraints.write(f"# {self.job_name} US window restraints #")

        # loops through dimensions to allow for either 1 or 2 dimensions
        for d in range(self.dimension):

            # writes the harmonic restraints to the restraint file in amber format
            restraints.write(f"""
&rst, {rc_iats[d]},
 r1={rc_window[d]} - {well_size},r2={rc_window[d]},r3={rc_window[d]},r4={rc_window[d]} + {well_size},
 rk2={force_constant},rk3={force_constant},
 /""")

        # checks if a restraints file exists for additional restraints on the system
        if os.path.exists("./restraints.RST"):

            # adds the additional restraints to the US window restraints file
            with open("./restraints.RST", "r") as add_rest:
                lines = add_rest.readlines()

                # checks if the additional restraints file is empty
                if lines == 0:
                    raise Exception("Your additional restraints file is empty.")

                # writes the lines from the additional restraints file to the US window restraint file
                else:
                    restraints.writelines(lines)

        # closes the US window restraints file
        restraints.close()

    def write_md_file(self, rc_window):
        """
        Writes an md input file in the reaction coordinate directory
        """
        # for 1 dimensional US
        if self.dimension == 1:

            # open MD file in window folder
            new_md_file = open(f"rc{rc_window}/{self.md_file}", "w+")

        # for 2 dimensional US
        elif self.dimension == 2:

            # open MD file in window folder
            new_md_file = open(f"rc{rc_window[0]}_{rc_window[1]}/{self.md_file}", "w+")

        try:
            with open(f"{self.md_file}", "r") as template:
                template_lines = template.readlines()
                new_md_file.writelines(template_lines)
                new_md_file.write("""&wt type='DUMPFREQ, istep1=1 /
&wt type='END' /""")
                if self.dimension == 1:
                    new_md_file.write(f"""DISANG=rc{rc_window}.RST
DUMPAVE=rc{rc_window}.tra
                    """)
                elif self.dimension == 2:
                    new_md_file.write(f"""DISANG=rc{rc_window[0]}_{rc_window[1]}.RST
DUMPAVE=rc{rc_window[0]}_{rc_window[1]}.tra
                    """)

        except FileNotFoundError:
            print(f"{self.md_file}, your template file, is not in this directory.")

    def generate_input(self, rc1_start, rc1_end, rc1_step, rc2_start=None, rc2_end=None, rc2_step=None):
        UmbrellaSampling.write_submission_script_header(self)
        rc1 = rc1_start
        if self.dimension == 1:
            while True:
                if rc1 == rc1_end + rc1_step:
                    break
                else:
                    os.system(f"mkdir rc{rc1}")
                    with open(self.submission_script, "a+") as sub:
                        pass
