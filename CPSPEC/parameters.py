# ----------------------------- #
# ---------- Setting ---------- #
# ----------------------------- #

# ----------------------------------- #
# ----- Original power spectrum ----- #
# ----------------------------------- #
# Cutoff frequency of PSD [Hz]
dfs=[1., 10.]
# Average value of time series
mu=1.
# Standard deviation of time series
sigma=0.2

# -------------------- #
# ----- Filename ----- #
# -------------------- #
# directory name of data
name_dir='../TSGenerator/'

# Filename (time series)
names_fits_ts =['data_df{0:04}Hz.fits'.format(int(df)) for df in dfs]
# Filename (Fourier transform)
names_fits_ft =['data_df{0:04}Hz_fft.fits'.format(int(df)) for df in dfs]
# Filename (power spectrum)
names_fits_psd=['data_df{0:04}Hz_psd.fits'.format(int(df)) for df in dfs]
# Filename (cross spectrum)
names_fits_csd=['data_df{0:04}Hz_csd.fits'.format(int(df)) for df in dfs]

# Filename (combined time series)
name_fits_ts_combine='data_combine.fits'
# Filename (Fourier transform for the combined time series)
name_fits_ft_combine='data_combine_ft.fits'
# Filename (power spectrum for the combined time series)
name_fits_psd_combine='data_combine_psd.fits'

# PDF Filename (power spectrum)
names_pdf_psd=['data_df{0:04}Hz_psd.pdf'.format(int(df)) for df in dfs]
# PDF Filename (power spectrum for check)
names_pdf_psd_check=['data_df{0:04}Hz_psd_check.pdf'.format(int(df)) for df in dfs]
# PDF Filename (cross spectrum)
names_pdf_csd_real =['data_df{0:04}Hz_csd_real.pdf'.format(int(df)) for df in dfs]
names_pdf_csd_imag =['data_df{0:04}Hz_csd_imag.pdf'.format(int(df)) for df in dfs]
names_pdf_csd_abs  =['data_df{0:04}Hz_csd_abs.pdf'.format(int(df)) for df in dfs]
names_pdf_csd_phase=['data_df{0:04}Hz_csd_phase.pdf'.format(int(df)) for df in dfs]
names_pdf_csd_time =['data_df{0:04}Hz_csd_time.pdf'.format(int(df)) for df in dfs]

# PDF Filename (power spectrum for the combined time series)
name_pdf_psd_combine='data_combine_psd.pdf'

# ------------------------------------------- #
# ----- Power spectrum / Cross spectrum ----- #
# ------------------------------------------- #
# Rebin factor for power spectrum and cross spectrum
rebin=1.2

# ------------------- #
# ----- Command ----- #
# ------------------- #
# Dos and don'ts
dos      ={'FFT': True, 'PSD': True, 'CSD': True}
dos_plot ={'PSD': True, 'CSD': True}
dos_check={'PSD': True}
