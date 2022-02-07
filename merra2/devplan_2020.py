#!/usr/bin/python3

import pypsa
import pandas as pd
import numpy as np
import sys
from pypsa.opt import Constraint as Con


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


model = 'fias-model'
data = 'merra2-data'
name = 'vietnam'
fn = './../vietnam_merra2.nc'

attribute = 'devplan'  # or 'renewable'
storage = False
year = 2020

scenarios = pd.read_csv('./../scenario_limits.csv')
scenarios = scenarios.set_index(scenarios['scenario']).drop(columns='scenario').dropna(axis=1)
limits = scenarios.loc[year]
flexibility = 0.1

n = pypsa.Network(fn)

n.loads_t.p_set = n.loads_t.p_set * limits['load_increase']

scenario = '{}_{}'.format(attribute, year)

n.lopf(extra_functionality = devplan_set_constraints,
       snapshots=n.snapshots[:8760],
       solver_name='gurobi',
       solver_options={"threads":32, "method":-1, "crossover":-1},
       formulation='kirchhoff', keep_files=False,
       solver_logfile=sys.argv[1]+'.log')

n.name = name + '_' + scenario
n.export_to_csv_folder('./../' + model + '_' + data + '/' + scenario)
