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
    for name_fits_ts in names_fits_ts:
        if os.path.exists(name_fits_ts)==False:
            os.symlink(name_dir+name_fits_ts, name_fits_ts)
    if os.path.exists(name_fits_ts_combine)==False:
        os.symlink(name_dir+name_fits_ts_combine, name_fits_ts_combine)

    # FFT
    print('Perfoming FFT...', end='', flush=True)
    if dos['FFT']==True:
        # Normal data
        for name_fits_ts, name_fits_ft in zip(names_fits_ts, names_fits_ft):
            name_infits=name_fits_ts
            name_outfits=name_fits_ft
            cmd='python do_fft.py {0} {1}'.format(name_infits, name_outfits)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

        # Combined data
        name_infits=name_fits_ts_combine
        name_outfits=name_fits_ft_combine
        cmd='python do_fft.py {0} {1}'.format(name_infits, name_outfits)
        tokens=shlex.split(cmd)
        subprocess.run(tokens)
    print('Done!')

    # PSD
    print('Calculating power spectrum...', end='', flush=True)
    if dos['PSD']==True:
        for name_fits_ft, name_fits_psd in zip(names_fits_ft, names_fits_psd):
            # Normal data
            name_infits=name_fits_ft
            name_outfits=name_fits_psd
            cmd='python do_calc_psd.py {0} {1} {2}'.format(name_infits, name_outfits, rebin)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

        # Combined data
        name_infits=name_fits_ft_combine
        name_outfits=name_fits_psd_combine
        cmd='python do_calc_psd.py {0} {1} {2}'.format(name_infits, name_outfits, rebin)
        tokens=shlex.split(cmd)
        subprocess.run(tokens)
    print('Done!')

    # CSD
    print('Calculating cross spectrum...', end='', flush=True)
    if dos['CSD']==True:
        for name_fits_ft, name_fits_psd, name_fits_csd in zip(names_fits_ft, names_fits_psd, names_fits_csd):
            # Normal data
            name_infits_ft=name_fits_ft
            name_infits_psd=name_fits_psd
            name_infits_ft_ref=name_fits_ft_combine
            name_infits_psd_ref=name_fits_psd_combine
            name_outfits=name_fits_csd
            cmd='python do_calc_csd.py {0} {1} {2} {3} {4} {5}'\
                .format(name_infits_ft, name_infits_psd, name_infits_ft_ref, name_infits_psd_ref, name_outfits, rebin)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)
    print('Done!')

    # ------------ #
    # --- Plot --- #
    # ------------ #
    # PSD
    print('Plotting power spectrum...', end='', flush=True)
    if dos_plot['PSD']==True:
        for name_fits_psd, name_pdf_psd in zip(names_fits_psd, names_pdf_psd):
            # Normal data
            name_infits=name_fits_psd
            name_outpdf=name_pdf_psd
            cmd='python do_draw_psd.py {0} {1}'.format(name_infits, name_outpdf)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

        # Combined data
            name_infits=name_fits_psd_combine
            name_outpdf=name_pdf_psd_combine
            cmd='python do_draw_psd.py {0} {1}'.format(name_infits, name_outpdf)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)
    print('Done!')

    # CSD
    print('Plotting cross spectrum...', end='', flush=True)
    if dos_plot['CSD']==True:
        for name_fits_csd, name_pdf_csd_real, name_pdf_csd_imag, name_pdf_csd_abs, name_pdf_csd_phase, name_pdf_csd_time in zip(names_fits_csd, names_pdf_csd_real, names_pdf_csd_imag, names_pdf_csd_abs, names_pdf_csd_phase, names_pdf_csd_time):
            # Real part
            name_infits=name_fits_csd
            name_outpdf=name_pdf_csd_real
            cmd='python do_draw_csd_real.py {0} {1}'.format(name_infits, name_outpdf)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

            # Imaginary part
            name_infits=name_fits_csd
            name_outpdf=name_pdf_csd_imag
            cmd='python do_draw_csd_imag.py {0} {1}'.format(name_infits, name_outpdf)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

            # Amplitude
            name_infits=name_fits_csd
            name_outpdf=name_pdf_csd_abs
            cmd='python do_draw_csd_abs.py {0} {1}'.format(name_infits, name_outpdf)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

            # Phase lag
            name_infits=name_fits_csd
            name_outpdf=name_pdf_csd_phase
            cmd='python do_draw_csd_phase.py {0} {1}'.format(name_infits, name_outpdf)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)

            # Time lag
            name_infits=name_fits_csd
            name_outpdf=name_pdf_csd_time
            cmd='python do_draw_csd_time.py {0} {1}'.format(name_infits, name_outpdf)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)
    print('Done!')

    # ------------- #
    # --- Check --- #
    # ------------- #
    print('Checking power spectrum...', end='', flush=True)
    if dos_check['PSD']==True:
        for df, name_fits_psd, name_pdf_psd_check in zip(dfs, names_fits_psd, names_pdf_psd_check):
            # Normal data
            name_infits=name_fits_psd
            name_outpdf=name_pdf_psd_check
            cmd='python do_check_psd.py {0} {1} {2} {3} {4}'.format(name_infits, name_outpdf, mu, sigma, df)
            tokens=shlex.split(cmd)
            subprocess.run(tokens)
    print('Done!')

if __name__=='__main__':
    main()
