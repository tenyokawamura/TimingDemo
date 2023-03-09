# ----------------------------- #
# ---------- Setting ---------- #
# ----------------------------- #

# ----------------------------------- #
# ----- Original power spectrum ----- #
# ----------------------------------- #
# Cutoff frequency of PSD [Hz]
dfs=[1., 10.]

# -------------------- #
# ----- Filename ----- #
# -------------------- #
# Directory name of data
name_dir='../CPSPEC/'

# FITS filename (power spectrum)
names_fits_psd=['data_df{0:04}Hz_psd.fits'.format(int(df)) for df in dfs]
# FITS filename (cross spectrum)
names_fits_csd=['data_df{0:04}Hz_csd.fits'.format(int(df)) for df in dfs]

# PHA filename (power spectrum)
names_pha_psd=['data_df{0:04}Hz_psd.pha'.format(int(df)) for df in dfs]
# PHA filename (cross spectrum)
# Real
names_pha_csd_real =['data_df{0:04}Hz_csd_real.pha'.format(int(df)) for df in dfs]
# Imaginary
names_pha_csd_imag =['data_df{0:04}Hz_csd_imag.pha'.format(int(df)) for df in dfs]
# Amplitude
names_pha_csd_abs  =['data_df{0:04}Hz_csd_abs.pha'.format(int(df)) for df in dfs]
# Phase lag
names_pha_csd_phase=['data_df{0:04}Hz_csd_phase.pha'.format(int(df)) for df in dfs]
# Time lag
names_pha_csd_time =['data_df{0:04}Hz_csd_time.pha'.format(int(df)) for df in dfs]

# FITS filename (power spectrum for the combined time series)
name_fits_psd_combine='data_combine_psd.fits'

# PHA filename (power spectrum for the combined time series)
name_pha_psd_combine='data_combine_psd.pha'

name_rmf='data.rmf'
name_arf='data.arf'

# ---------------------------- #
# ----- XSPEC parameters ----- #
# ---------------------------- #
# Systematic error [x 100 %]
sys_err_psd      =0.
sys_err_csd_real =0.
sys_err_csd_imag =0.
sys_err_csd_abs  =0.
sys_err_csd_phase=0.
sys_err_csd_time =0.
# Minimum frequency index imprinted on a PHA file
i_f_min=0   
# Maximum frequency index imprinted on a PHA file (-1: Maximum value)
i_f_max=-1
# Minimum frequency covered in response files
f_min=1.e-2 #[Hz]
# Maximum frequency covered in response files
f_max=1.e2  #[Hz]
# Number of frequency bins covered in response files
n_bin=1000 #[-]

# ------------------- #
# ----- Command ----- #
# ------------------- #
# Dos and don'ts
dos={'PSD': True, 'CSDR': True, 'CSDI': True, 'CSDA': True, 'CSDP': True, 'CSDT': True, 'RMF': True, 'ARF': True}
