import os
import subprocess
import shlex
import time
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from parameters import *

def main():
    # ------------ #
    # --- Main --- #
    # ------------ #
    # --- Simulate data --- #
    print('Simulating time series...')
    if dos['simulate']==True:
        for df, name_fits_ts in zip(dfs, names_fits_ts):
            name_outfits=name_fits_ts
            cmd='python do_simulate_data.py {0} {1} {2} {3} {4} {5} {6}'\
                .format(name_outfits, dt, n_bin, n_seg, mu, sigma, df)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)
    print('Done!')

    # --- Combine data --- #
    print('Combining time series...', end='', flush=True)
    if dos['combine']==True:
        name_infits_slow=names_fits_ts[0]
        name_infits_fast=names_fits_ts[1]
        name_outfits    =name_fits_ts_combine
        cmd='python do_combine_data.py {0} {1} {2} {3}'\
            .format(name_infits_slow, name_infits_fast, name_outfits, t_delay)
        tokens=shlex.split(cmd)
        subprocess.run(tokens)
    print('Done!')
    
    # ------------ #
    # --- Plot --- #
    # ------------ #
    print('Plotting sample time series...', end='', flush=True)
    # --- Simulated data --- #
    if dos_plot['simulate']==True:
        for name_fits_ts, name_pdf_ts in zip(names_fits_ts, names_pdf_ts):
            name_infits=name_fits_ts 
            name_outpdf=name_pdf_ts
            cmd='python do_draw_data.py {0} {1}'.format(name_infits, name_outpdf)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

    # --- Combined data --- #
    if dos_plot['combine']==True:
        name_infits=name_fits_ts_combine
        name_outpdf=name_pdf_ts_combine
        cmd='python do_draw_data.py {0} {1}'.format(name_infits, name_outpdf)
        tokens=shlex.split(cmd)
        subprocess.run(tokens)
    print('Done!')

if __name__=='__main__':
    main()
