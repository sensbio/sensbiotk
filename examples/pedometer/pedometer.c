/* This file implements the pedometer parameters
 *
 * \date April 04, 2014
 * \author Roger Pissard-Gibollet  <roger.pissard.at.inria.fr>
 *
 * INRIA PTL HikoB-Pedometer demo
 * Copyright (C) 2014 INRIA
 */

#include <stdio.h>
#include <math.h>
#include "pedometer.h"
#include "freefall.h"


void pedometer_setparam(count_steps_config_t steps_params, 
			free_fall_config_t fall_params) {

  countstep_setparam(steps_params);
  freefall_setparam(fall_params);
}


void pedometer(int k, float sig[3], int *step, int * state, float *debug)
{
  float norm;

  /*
   1 - Compute norm 
  */
  norm = sig[0]*sig[0] + sig[1]*sig[1] + sig[2]*sig[2];
  norm = sqrt(norm);
  /*
   2 - Compute step numbers
  */
  countstep(k, norm, step);
  /*
   3 - Compute state activity
  */
  freefall(k, norm, state);

  debug = 0 ;
}
