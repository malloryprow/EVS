#PBS -N jevs_mesoscale_nam_grid2obs_stats_00
#PBS -j oe
#PBS -S /bin/bash
#PBS -q "dev"
#PBS -A VERF-DEV
#PBS -l walltime=4:59:00
#PBS -l place=vscatter:exclhost,select=3:ncpus=128:ompthreads=1
#PBS -l debug=true
#PBS -V

set -x
  export model=evs
  export machine=WCOSS2

# ECF Settings
  export SENDECF=YES
  export SENDCOM=YES
  export KEEPDATA=YES
  export SENDDBN=NO
  export SENDDBN_NTC=
  export SENDMAIL=YES
  export job=${PBS_JOBNAME:-jevs_mesoscale_grid2obs_stats}
  export jobid=$job.${PBS_JOBID:-$$}
  export SITE=$(cat /etc/cluster_name)
  export USE_CFP=YES
  export nproc=128

# General Verification Settings
  export NET="evs"
  export STEP="stats"
  export COMPONENT="mesoscale"
  export RUN="atmos"
  export VERIF_CASE="grid2obs"
  export MODELNAME="nam" 

  export envir="prod"
  export evs_run_mode="production"

# EVS Settings
  export HOMEevs=/lfs/h2/emc/vpppg/noscrub/${USER}/EVS


# EVS configuration
  export config=$HOMEevs/parm/evs_config/mesoscale/config.evs.prod.${STEP}.${COMPONENT}.${RUN}.${VERIF_CASE}.${MODELNAME}

source $HOMEevs/versions/run.ver
module reset
module load prod_envir/${prod_envir_ver}
source $HOMEevs/modulefiles/${COMPONENT}/${COMPONENT}_${STEP}.sh
export evs_ver=v1.0.0
evs_ver_2d=$(echo $evs_ver | cut -d'.' -f1-2)

export MET_CONFIG="${MET_PLUS_PATH}/parm/met_config"
export PYTHONPATH=$HOMEevs/ush/$COMPONENT:$PYTHONPATH

# In production the following will be deleted (DATAROOT will be used instead, which already exists in the environment)
  export DATAROOT=/lfs/h2/emc/stmp/$USER/evs_test/$envir/tmp

# Developer Settings
  export COMIN=/lfs/h2/emc/vpppg/noscrub/${USER}/$NET/$evs_ver_2d
  export COMOUT=/lfs/h2/emc/vpppg/noscrub/${USER}/$NET/$evs_ver_2d/$STEP/$COMPONENT

  export vhr=${vhr:-${vhr}}
  export maillist="roshan.shrestha@noaa.gov,alicia.bentley@noaa.gov"
  # export maillist="firstname.lastname@noaa.gov"

# Job Settings and Run
. ${HOMEevs}/jobs/JEVS_MESOSCALE_STATS
