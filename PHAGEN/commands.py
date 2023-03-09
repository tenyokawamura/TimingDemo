import os
import subprocess
import shlex
import time
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from parameters import *

def main():
    # ---------------- #
    # ----- Main ----- #
    # ---------------- #
    # Symbolic link
    for name_fits_psd in names_fits_psd:
        if os.path.exists(name_fits_psd)==False:
            os.symlink(name_dir+name_fits_psd, name_fits_psd)
    for name_fits_csd in names_fits_csd:
        if os.path.exists(name_fits_csd)==False:
            os.symlink(name_dir+name_fits_csd, name_fits_csd)
    if os.path.exists(name_fits_psd_combine)==False:
        os.symlink(name_dir+name_fits_psd_combine, name_fits_psd_combine)

    # --- PHA --- #
    print('Creating PHA file for power spectrum...', end='', flush=True)
    if dos['PSD']==True:
        # Normal data
        for name_fits_psd, name_pha_psd in zip(names_fits_psd, names_pha_psd):
            name_infits=name_fits_psd
            name_outpha=name_pha_psd
            cmd='python do_fits2pha_psd.py {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'\
                .format(name_infits, name_outpha, name_rmf, name_arf, i_f_min, i_f_max, sys_err_psd, f_min, f_max, n_bin)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

        # Combined data
        name_infits=name_fits_psd_combine
        name_outpha=name_pha_psd_combine
        cmd='python do_fits2pha_psd.py {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'\
            .format(name_infits, name_outpha, name_rmf, name_arf, i_f_min, i_f_max, sys_err_psd, f_min, f_max, n_bin)
        tokens=shlex.split(cmd)
        subprocess.run(tokens)
    print('Done!')

    print('Creating PHA file for cross spectrum...', end='', flush=True)
    if dos['CSDR']==True:
        for name_fits_csd, name_pha_csd_real in zip(names_fits_csd, names_pha_csd_real):
            name_infits=name_fits_csd
            name_outpha=name_pha_csd_real
            cmd='python do_fits2pha_csd_real.py {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'\
                .format(name_infits, name_outpha, name_rmf, name_arf, i_f_min, i_f_max, sys_err_psd, f_min, f_max, n_bin)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

    if dos['CSDI']==True:
        for name_fits_csd, name_pha_csd_imag in zip(names_fits_csd, names_pha_csd_imag):
            name_infits=name_fits_csd
            name_outpha=name_pha_csd_imag
            cmd='python do_fits2pha_csd_imag.py {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'\
                .format(name_infits, name_outpha, name_rmf, name_arf, i_f_min, i_f_max, sys_err_psd, f_min, f_max, n_bin)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

    if dos['CSDA']==True:
        for name_fits_csd, name_pha_csd_abs in zip(names_fits_csd, names_pha_csd_abs):
            name_infits=name_fits_csd
            name_outpha=name_pha_csd_abs
            cmd='python do_fits2pha_csd_abs.py {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'\
                .format(name_infits, name_outpha, name_rmf, name_arf, i_f_min, i_f_max, sys_err_psd, f_min, f_max, n_bin)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

    if dos['CSDP']==True:
        for name_fits_csd, name_pha_csd_phase in zip(names_fits_csd, names_pha_csd_phase):
            name_infits=name_fits_csd
            name_outpha=name_pha_csd_phase
            cmd='python do_fits2pha_csd_phase.py {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'\
                .format(name_infits, name_outpha, name_rmf, name_arf, i_f_min, i_f_max, sys_err_psd, f_min, f_max, n_bin)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

    if dos['CSDT']==True:
        for name_fits_csd, name_pha_csd_time in zip(names_fits_csd, names_pha_csd_time):
            name_infits=name_fits_csd
            name_outpha=name_pha_csd_time
            cmd='python do_fits2pha_csd_time.py {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'\
                .format(name_infits, name_outpha, name_rmf, name_arf, i_f_min, i_f_max, sys_err_psd, f_min, f_max, n_bin)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)
    print('Done!')

    # --- RMF --- #
    print('Creating RMF file...', end='', flush=True)
    if dos['RMF']==True:
        name_outrmf=name_rmf
        cmd='python do_generate_rmf.py {0} {1} {2} {3}'\
            .format(name_outrmf, f_min, f_max, n_bin)
        tokens=shlex.split(cmd)
        subprocess.run(tokens)
    print('Done!')

    # --- ARF --- #
    print('Creating ARF file...', end='', flush=True)
    if dos['ARF']==True:
        name_outarf=name_arf
        cmd='python do_generate_arf.py {0} {1} {2} {3}'\
            .format(name_outarf, f_min, f_max, n_bin)
        tokens=shlex.split(cmd)
        subprocess.run(tokens)
    print('Done!')

if __name__=='__main__':
    main()
