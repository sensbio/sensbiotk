/* This file implements the pedometer parameters
 *
 * \date April 04, 2014
 * \author Roger Pissard-Gibollet  <roger.pissard.at.inria.fr>
 *
 * INRIA PTL HikoB-Pedometer demo
 * Copyright (C) 2014 INRIA
 */
#ifndef _PEDOMETER_H
#define _PEDOMETER_H

#include "countstep.h"
#include "freefall.h"



void pedometer(int k, float sig[3], int *step, int *state, float *debug);

void pedometer_setparam(count_steps_config_t steps_params, 
			free_fall_config_t fall_params);

#endif
