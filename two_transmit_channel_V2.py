# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:18:38 2024

@author: bounc
"""

import adi                                     # Pluto SDR proprietary Library
import matplotlib.pyplot as plt                # data plottting library
import numpy as np                             # math functions library

samp_rate = 2e6                                # The sample rate of the radio (2 MHz).
NumSamples = 2**12                             # Number of samples per buffer (4096). 2^12
rx_lo = 2.4e9                                  # Receive Local Oscillator frequency (2.4 GHz)


