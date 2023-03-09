import numpy as np 
import astropy.io.fits as fits
import sys 
from sys import argv
import os
def main():
    # ----- Setting ----- #
    # ----- Main ----- #
    name_infits=argv[1]
    name_outpha=argv[2]
    name_rmf   =argv[3]
    name_arf   =argv[4]
    i_f_min    =int(argv[5])
    i_f_max    =int(argv[6])
    sys_err    =float(argv[7])
    f_min      =float(argv[8])
    f_max      =float(argv[9])
    n_bin      =int(argv[10])

    if i_f_max==-1:
        i_f_max=None

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

    # --------------------- #
    # ----- Read data ----- #
    # --------------------- #
    hdus=fits.open(name_infits)
    fs_mid_data=hdus[1].data['F']
    dfs_data   =hdus[1].data['DF']
    csds_re    =hdus[1].data['CSDR']
    dcsds_re   =hdus[1].data['DCSDR']
    hdus.close()

    fs_min_data=fs_mid_data-dfs_data
    fs_max_data=fs_mid_data+dfs_data
    
    # ----- Limit range ----- #
    fs_min_data=fs_min_data[i_f_min:i_f_max]
    fs_max_data=fs_max_data[i_f_min:i_f_max]
    csds_re    =csds_re    [i_f_min:i_f_max]
    dcsds_re   =dcsds_re   [i_f_min:i_f_max]

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
    for ch_rebin_min, ch_rebin_max, csd_re, dcsd_re, df_rebin\
    in zip(chs_rebin_min, chs_rebin_max, csds_re, dcsds_re, dfs_rebin):
        rates[ch_rebin_min]=csd_re*df_rebin 
        stats_err[ch_rebin_min]=dcsd_re*df_rebin
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
