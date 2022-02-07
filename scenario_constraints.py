#!/usr/bin/python3

import pypsa
from pypsa.opt import Constraint as Con
import pandas as pd


def devplan_scenario_constraints(n,snapshots,limits=None,flexibility=0.1):
    carrier_constraints = ['wind', 'solar', 'hydro', 'bioenergy',
                           'hard coal', 'oil', 'ocgt', 'nuclear', 'hydro ror']
    
    for constraint in limits.index:
        if constraint in carrier_constraints:
            if constraint == 'hydro':
                index = n.storage_units[n.storage_units['carrier']==constraint].index
                setattr(n.model,constraint+"_limit_low",Con(expr=sum(n.model.storage_p_nom[name] \
                                                          for name in index) >= limits[constraint] * (1.-flexibility)))
                setattr(n.model,constraint+"_limit_up",Con(expr=sum(n.model.storage_p_nom[name] \
                                                          for name in index) <= limits[constraint] * (1.+flexibility)))
            else:
                index = n.generators[n.generators['carrier']==constraint].index
                setattr(n.model,constraint+"_limit_low",Con(expr=sum(n.model.generator_p_nom[name] \
                                                          for name in index) >= limits[constraint] * (1.-flexibility)))
                setattr(n.model,constraint+"_limit_up",Con(expr=sum(n.model.generator_p_nom[name] \
                                                          for name in index) <= limits[constraint] * (1.+flexibility)))
    return



def devplan_set_constraints(network, snapshots):
    return devplan_scenario_constraints(network, snapshots, limits = limits, flexibility = flexibility)



def renewable_scenario_constraints(n,snapshots,limits=None,flexibility=0.1):
    carrier_constraints = ['hydro', 'nuclear', 'hydro ror']
    
    for constraint in limits.index:
        if constraint in carrier_constraints:
            if constraint == 'hydro':
                index = n.storage_units[n.storage_units['carrier']==constraint].index
                setattr(n.model,constraint+"_limit_low",Con(expr=sum(n.model.storage_p_nom[name] \
                                                          for name in index) >= limits[constraint] * (1.-flexibility)))
                setattr(n.model,constraint+"_limit_up",Con(expr=sum(n.model.storage_p_nom[name] \
                                                          for name in index) <= limits[constraint] * (1.+flexibility)))
            else:
                index = n.generators[n.generators['carrier']==constraint].index
                setattr(n.model,constraint+"_limit_low",Con(expr=sum(n.model.generator_p_nom[name] \
                                                          for name in index) >= limits[constraint] * (1.-flexibility)))
                setattr(n.model,constraint+"_limit_up",Con(expr=sum(n.model.generator_p_nom[name] \
                                                          for name in index) <= limits[constraint] * (1.+flexibility)))
    return



def renewable_set_constraints(network, snapshots):
    return renewable_scenario_constraints(network, snapshots, limits = limits, flexibility = flexibility)
