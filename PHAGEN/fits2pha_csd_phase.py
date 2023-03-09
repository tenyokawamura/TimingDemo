import numpy as np 
import astropy.io.fits as fits
import sys 
from sys import argv
import os
def main():
    # ----- Setting ----- #
    # --- #
    # Data
    e_ref_min=2.
    e_ref_max=4.
    es_min=[2., 4., 8.,  16., 32., 64. ]
    es_max=[4., 8., 16., 32., 64., 128.]
    sys_err=0. # Systematic error [x 100 %]
    i_f_min=0  # Minimum frequency index imprinted on a PHA file. 
    i_f_max=34 # Maximum frequency index imprinted on a PHA file.
    name_infits_def='./flux_signal_csd.fits'
    name_outpha_def='./flux_signal_csd_phase.pha'
    # Response
    name_rmf='timing_spectrum.rmf'
    name_arf='timing_spectrum.arf'
    f_min=1.e-2 #[Hz]
    f_max=1.e2  #[Hz]
    n_bin=1000 #[-]
    # --- #

    # ----- Set time/frequency ----- #
    fs=np.geomspace(f_min, f_max, n_bin+1)

    fs_min=fs
    fs_max=np.roll(fs, -1)
    # Delete the maximum bin
    fs_min=fs_min[:-1]
    fs_max=fs_max[:-1]
    
    fs=(fs_min+fs_max)/2.
    dfs=(fs_max-fs_min)/2.

    n_ch=len(fs_min)

    # ----- Main ----- #
    for i_e, (e_min, e_max) in enumerate(zip(es_min, es_max)):
        name_infits=name_infits_def.replace('_csd.fits', '_{0:04}keV_{1:04}keV_{2:04}keV_{3:04}keV_csd.fits'.format(int(e_ref_min), int(e_ref_max), int(e_min), int(e_max)))
        name_outpha=name_outpha_def.replace('_csd_phase.pha', '_{0:04}keV_{1:04}keV_{2:04}keV_{3:04}keV_csd_phase.pha'.format(int(e_ref_min), int(e_ref_max), int(e_min), int(e_max)))

        # --------------------- #
        # ----- Read data ----- #
        # --------------------- #
        hdus=fits.open(name_infits)
        fs_mid_data=hdus[1].data['F']
        dfs_data   =hdus[1].data['DF']
        csds_ph    =hdus[1].data['CSDP']
        dcsds_ph   =hdus[1].data['DCSDP']
        hdus.close()
        csds_ph*=-1

        fs_min_data=fs_mid_data-dfs_data
        fs_max_data=fs_mid_data+dfs_data
        
        # ----- Limit range ----- #
        fs_min_data=fs_min_data[i_f_min:i_f_max]
        fs_max_data=fs_max_data[i_f_min:i_f_max]
        csds_ph    =csds_ph    [i_f_min:i_f_max]
        dcsds_ph   =dcsds_ph   [i_f_min:i_f_max]

        first=True
        for f_min_data, f_max_data in zip(fs_min_data, fs_max_data):
            chs=np.where((f_min_data<fs) & (fs<=f_max_data))[0]
            ch_rebin_min=chs[0]
            ch_rebin_max=chs[-1]
            df_rebin=np.sum(2.*dfs[chs])
            if first==True:
                dfs_rebin=df_rebin
                chs_rebin_min=ch_rebin_min
                chs_rebin_max=ch_rebin_max
                first=False
            else:
                dfs_rebin=np.append(dfs_rebin, df_rebin)
                chs_rebin_min=np.append(chs_rebin_min, ch_rebin_min)
                chs_rebin_max=np.append(chs_rebin_max, ch_rebin_max)
            
        # -------------------- #
        # ----- Make PHA ----- #
        # -------------------- #
        # ----- PRIMARY ----- #
        hdu_pri=fits.PrimaryHDU(data=None, header=None)

        # ----- SPECTRUM ----- #
        chs=np.arange(n_ch)
        rates=np.zeros(n_ch) # P(f) (power spectrum)
        stats_err=np.zeros(n_ch) # dP(f) (error)
        syses_err=np.zeros(n_ch) # dP(f) (error)
        qualities=np.zeros(n_ch)
        groupings=-np.ones(n_ch)

        groupings[0]=1 # asked by XSPEC
        for ch_rebin_min, ch_rebin_max, csd_ph, dcsd_ph, df_rebin\
        in zip(chs_rebin_min, chs_rebin_max, csds_ph, dcsds_ph, dfs_rebin):
            rates[ch_rebin_min]=csd_ph*df_rebin 
            stats_err[ch_rebin_min]=dcsd_ph*df_rebin
            syses_err[ch_rebin_min]=sys_err
            groupings[ch_rebin_min]=1
        groupings[chs_rebin_max[-1]+1]=1
        for ch in range(chs_rebin_min[0]):
            qualities[ch]=5
        for ch in range(chs_rebin_max[-1]+1, len(chs)):
            qualities[ch]=5
        hdu_spe=\
        fits.BinTableHDU.from_columns([fits.Column(name='CHANNEL',  format='i4', array=chs),\
                                       fits.Column(name='RATE',     format='f4', array=rates),\
                                       fits.Column(name='STAT_ERR', format='f4', array=stats_err),\
                                       fits.Column(name='SYS_ERR',  format='f4', array=syses_err),\
                                       fits.Column(name='GROUPING', format='i2', array=groupings),\
                                       fits.Column(name='QUALITY',  format='i2', array=qualities)])

        hdu_spe.header['TUNIT2']='count/s'
        hdu_spe.header['EXTNAME']='SPECTRUM'
        hdu_spe.header['HDUCLASS']='OGIP'
        hdu_spe.header['HDUVERS1']='1.2.0'
        hdu_spe.header['HDUVERS']='1.2.0'
        hdu_spe.header['HDUCLAS3']='RATE'
        hdu_spe.header['TLMIN1']=0
        hdu_spe.header['TLMAX1']=n_ch-1
        hdu_spe.header['TELESCOP']='PREFLOW'
        hdu_spe.header['INSTRUME']='PREFLOW'
        hdu_spe.header['FILTER']='NONE'
        hdu_spe.header['AREASCAL']=1.0
        hdu_spe.header['BACKFILE']='none'
        hdu_spe.header['BACKSCAL']=1.0
        hdu_spe.header['CORRFILE']='none'
        hdu_spe.header['CORRSCAL']=1.0
        hdu_spe.header['RESPFILE']=name_rmf
        hdu_spe.header['ANCRFILE']=name_arf
        hdu_spe.header['DETCHANS']=n_ch
        hdu_spe.header['CHANTYPE']='PHA'
        hdu_spe.header['POISSERR']=False
        hdu_spe.header['STAT_ERR']=0
        hdu_spe.header['SYS_ERR']=0
        hdu_spe.header['GROUPING']=0
        hdu_spe.header['QUALITY']=0
        hdu_spe.header['HDUCLAS1']='SPECTRUM'
        hdu_spe.header['DATAMODE']='PHOTON'
        # Exposure [s]: As long as 'RATE' is used instead of 'COUNT', 
        # any positive value should be fine.
        # But, 1 sec is the safest.
        hdu_spe.header['EXPOSURE']=1 
        hdu_spe.header['OBJECT']='PREFLOW'

        # ----- Write ----- #
        hdus_out=fits.HDUList([hdu_pri, hdu_spe])
        hdus_out.writeto(name_outpha, overwrite=True)

if __name__=='__main__':
    main()
