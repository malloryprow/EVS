#!/bin/bash
# modulefile for EVS send component, mail step

set -x

module use /apps/ops/para/libs/modulefiles/compiler/intel/${intel_ver}
export HPC_OPT=/apps/ops/para/libs
module use /apps/dev/modulefiles
module load PrgEnv-intel/${PrgEnvintel_ver}
module load intel/${intel_ver}
module load ve/evs/${ve_evs_ver}
module load prod_util/${prod_util_ver}
module list

set -x
