# ----------------------------- #
# ---------- Setting ---------- #
# ----------------------------- #

# -------------------------- #
# ----- Power spectrum ----- #
# -------------------------- #
# Cutoff frequency of PSD [Hz]
dfs=[1., 10.]
# Average value of time series
mu=1.
# Standard deviation of time series
sigma=0.2

# -------------------- #
# ----- Filename ----- #
# -------------------- #
# Filename (time series)
names_fits_ts =['data_df{0:04}Hz.fits'.format(int(df)) for df in dfs]
# Filename (combined time series)
name_fits_ts_combine='data_combine.fits'

# PDF Filename (time series)
names_pdf_ts =['data_df{0:04}Hz_sample.pdf'.format(int(df)) for df in dfs]
# PDF Filename (combined time series)
name_pdf_ts_combine='data_combine_sample.pdf'

# ----------------------- #
# ----- Time series ----- #
# ----------------------- #
# Sampling interval [s]
dt=2.**(-7)
# Number of bins in one segment
n_bin=2**13
# Number of segments
n_seg=40

# Delay time [s]
t_delay=0.2

# ------------------- #
# ----- Command ----- #
# ------------------- #
# Dos and don'ts
dos={'simulate': True, 'combine': True}
dos_plot={'simulate': True, 'combine': True}

