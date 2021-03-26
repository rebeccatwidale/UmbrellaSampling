3 ps NPT QMMM MD of system
&cntrl
 imin=0,                        ! Not a minimisation run
 irest=1,                       ! Restart simulation
 ntx=5,                         ! Read coordinates velocities
 nscm=1000,                     ! Reset COM every 1000 steps
 nstlim=3000, dt=0.001,         ! Run MD for 2 ps with a timestep of 1 fs
 ntpr=50, ntwx=50,              ! Write the trajectory every 10 ps and the energies every 10 ps
 ioutfm=1,                      ! Use Binary NetCDF trajectory format (better)
 iwrap=0,                       ! No wrapping will be performed
 ntxo=2,                        ! NetCDF file
 cut=12.0,                      ! 12 angstrom non-bond cut off
 ntp=1,                         ! Isotropic pressure regulation
 pres0=1.01325,                 ! Reference pressure in bars
 taup=1.0,                      ! Pressure relaxation time (in ps)
 barostat=2,                    ! MC barostat
 ntt=1,                         ! Temperature regulation using langevin dynamics
 tempi=310.0,                   ! Initial thermostat temperature in K
 temp0=310.0,                   ! Final thermostat temperature in K
 ig=-1,                         ! Randomize the seed for the pseudo-random number generator
 nmropt=1,
 ifqnt=1                        ! Turn on qmmm
/
&qmmm
 qmmask='@1278-1288,1305-1315,1332-1337,1344-1354,2357-2367,3372-3382,3964-4000'
 qmcharge=1,
 qm_theory='DFTB3',
 qmshake=0,
 qm_ewald=1,
 qm_pme=1
/