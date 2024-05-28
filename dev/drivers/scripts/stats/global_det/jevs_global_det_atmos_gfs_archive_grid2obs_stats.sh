#PBS -N jevs_global_det_atmos_gfs_archive_grid2obs_stats_00
#PBS -j oe
#PBS -S /bin/bash
#PBS -q dev
#PBS -A VERF-DEV
#PBS -l walltime=01:30:00
#PBS -l place=vscatter:exclhost,select=1:ncpus=128:ompthreads=1:mem=275GB
#PBS -l debug=true

set -x

cd $PBS_O_WORKDIR

export model=evs
export HOMEevs=/lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_gfsv17/EVS

export SENDCOM=YES
export SENDMAIL=NO
export KEEPDATA=YES
export job=${PBS_JOBNAME:-jevs_global_det_atmos_gfs_archive_grid2obs_stats}
export jobid=$job.${PBS_JOBID:-$$}
export SITE=$(cat /etc/cluster_name)
export vhr=00

source $HOMEevs/versions/run.ver
module reset
module load prod_envir/${prod_envir_ver}
source $HOMEevs/dev/modulefiles/global_det/global_det_stats.sh

evs_ver_2d=$(echo $evs_ver | cut -d'.' -f1-2)

export machine=WCOSS2
export USE_CFP=YES
export nproc=128

export MAILTO='alicia.bentley@noaa.gov,mallory.row@noaa.gov'

export envir=dev
export NET=evs
export STEP=stats
export COMPONENT=global_det
export RUN=atmos
export VERIF_CASE=grid2obs
export MODELNAME=gfs

export DATAROOT=/lfs/h2/emc/stmp/$USER/evs_test/$envir/tmp
export TMPDIR=$DATAROOT
export COMIN=/lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_gfsv17/$NET/$evs_ver_2d
export COMOUT=/lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_gfsv17/$NET/$evs_ver_2d/$STEP/$COMPONENT

export config=$HOMEevs/parm/evs_config/global_det/config.evs.dev.${STEP}.${COMPONENT}.${RUN}.${VERIF_CASE}.${MODELNAME}_archive

export evs_run_mode=standalone
export ACCOUNT=VERF-DEV
export QUEUE=dev
export QUEUESHARED=dev_shared
export QUEUESERV=dev_transfer
export PARTITION_BATCH=
export METviewer_AWS_scripts_dir=/lfs/h2/emc/vpppg/save/emc.vpppg/verification/metplus/metviewer_aws_scripts
export archive_obs_data_dir=/lfs/h2/emc/vpppg/noscrub/emc.vpppg/verification/global/archive/obs_data
export COMINgfs=/lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_gfsv17/gfs
export COMINobsproc=/lfs/h1/ops/prod/com/obsproc/$obsproc_ver
export COMINccpa=/lfs/h1/ops/prod/com/ccpa/$ccpa_ver

# CALL executable job script here
$HOMEevs/jobs/JEVS_GLOBAL_DET_STATS

######################################################################
# Purpose: This does the statistics work for the global deterministic
#          atmospheric grid-to-observations component for GFS
######################################################################
