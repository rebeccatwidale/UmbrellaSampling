from UmbrellaSampling import UmbrellaSampling
import os

# You should run this script with Python 3.6 or later


############################################################################################
#################################### User Input section ####################################
############################################################################################

cluster = "BluePebble"
submission_script = "submit_umb_samp"
# the md file should only contain md options and the definition of your qm region and level of theory etc.
md_file = "md2ps.i"
nodes = 1
procs = 24
walltime = "72:00:00"
job_name = "us_test"
# if you are running this on a cluster with no partition specification, set partition=None
partition = None
amber_version = 18
# if you are not interfacing with an external QM package, set interface=None
interface = "Gaussian"
memory = "42gb"
# for running Amber in parallel
# if you are running serial Amber, set mpi_procs = 0
mpi_procs = 0
dimensions = 1.5
rcs = [3.1, 2.2]


############################################################################################
############################################################################################

calculation = UmbrellaSampling(submission_script, md_file, nodes, procs, job_name, partition, amber_version,
                               interface, memory, walltime, dimensions)
calculation.set_cluster(cluster)
calculation.write_restraints_file(100, 3.1, 2, [3, 4])
#print(calculation.executable(mpi_procs))
#os.system("mkdir rc3.1_2.2")
#calculation.write_md_file(rcs)#, 0.5, rc_iats=["hello", "yo"])
