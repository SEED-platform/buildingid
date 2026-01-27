# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

import os
import sys

buildingid_abspath_ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, buildingid_abspath_)
sys.path.remove(buildingid_abspath_)
del buildingid_abspath_
