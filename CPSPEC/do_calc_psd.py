import numpy as np 
import astropy.io.fits as fits
from sys import argv

def main():
    # ----- Main ----- #
    name_infits =argv[1]
    name_outfits=argv[2]
    rebin       =float(argv[3])

    # --- Calculate periodograms --- #
    hdus=fits.open(name_infits)

    n_seg=len(hdus)-1
    first=True
    for i_seg in range(n_seg):
        fs =hdus[i_seg+1].data['FREQ']
        fts=hdus[i_seg+1].data['FT']

        # Mean count rate
        mu=hdus[i_seg+1].header['MU']
        # Timing interval
        dt=hdus[i_seg+1].header['DT']
        # Number of data
        n_bin=hdus[i_seg+1].header['NBIN']

        # Normalization of power spectrum
        norm=2.*dt/((mu**2)*n_bin)

        # Power spectrum
        psds=norm*(np.abs(fts)**2)

        if first==True:
            first=False
            psdss=psds
            fs_record=fs
            dt_record=dt
            n_bin_record=n_bin
            mus=mu # Mean count rate [counts/s]
        else:
            psdss=np.vstack((psdss, psds))
            mus=np.append(mus, mu)
    hdus.close()

    fs=fs_record
    dt=dt_record
    n_bin=n_bin_record

    # --- Rebin --- #
    dfs=(fs-np.roll(fs, 1))/2.
    dfs[0]=(fs[1]-fs[0])/2.
    fs_min=fs-dfs
    fs_max=fs+dfs

    f_mid_min=0.
    f_mid_max=fs[0]
    psdss_t=psdss.T

    if rebin>1.:
        first=True
        while True:
            is_merge=np.where((f_mid_min<fs)&(fs<=f_mid_max))[0]
            if len(is_merge)==0:
                if f_mid_min>fs[-1]:
                    break
            else:
                n_fbin=len(is_merge)
                fs_min_merge=fs_min[is_merge]
                fs_max_merge=fs_max[is_merge]
                psds_merge  =np.ravel(psdss_t[is_merge])

                f_min_rebin=fs_min_merge[0]
                f_max_rebin=fs_max_merge[-1]
                psd_rebin=np.mean(psds_merge)
                dpsd_rebin=np.sqrt(np.var(psds_merge)/len(psds_merge))

                if first==True:
                    first=False
                    fs_min_rebin=f_min_rebin
                    fs_max_rebin=f_max_rebin
                    psds_rebin  =psd_rebin
                    dpsds_rebin =dpsd_rebin
                    ns_fbin     =n_fbin
                    ns_seg      =n_seg
                else:
                    fs_min_rebin=np.append(fs_min_rebin, f_min_rebin)
                    fs_max_rebin=np.append(fs_max_rebin, f_max_rebin)
                    psds_rebin  =np.append(psds_rebin,   psd_rebin)
                    dpsds_rebin =np.append(dpsds_rebin,  dpsd_rebin)
                    ns_fbin     =np.append(ns_fbin,      n_fbin)
                    ns_seg      =np.append(ns_seg,       n_seg)

            f_mid_min=f_mid_max
            f_mid_max*=rebin

    elif rebin==1.:
        fs_min_rebin=fs_min
        fs_max_rebin=fs_max
        first=True
        for psds_merge in zip(psdss_t):
            psds_merge=np.ravel(psds_merge)
            n_fbin=1
            psd_rebin=np.mean(psds_merge)
            dpsd_rebin=np.sqrt(np.var(psds_merge)/len(psds_merge))
            if first==True:
                first=False
                psds_rebin  =psd_rebin
                dpsds_rebin =dpsd_rebin
                ns_fbin     =n_fbin
                ns_seg      =n_seg
            else:
                psds_rebin  =np.append(psds_rebin,   psd_rebin)
                dpsds_rebin =np.append(dpsds_rebin,  dpsd_rebin)
                ns_fbin     =np.append(ns_fbin,      n_fbin)
                ns_seg      =np.append(ns_seg,       n_seg)

    fs_rebin =(fs_min_rebin+fs_max_rebin)/2.
    dfs_rebin=(fs_max_rebin-fs_min_rebin)/2.

    mu_ave=np.mean(mus)
    # ----- Write results ----- #
    hdu_ext=fits.BinTableHDU.from_columns([\
        fits.Column(name='F',    format='f4', array=fs_rebin),\
        fits.Column(name='DF',   format='f4', array=dfs_rebin),\
        fits.Column(name='PSD',  format='f4', array=psds_rebin),\
        fits.Column(name='DPSD', format='f4', array=dpsds_rebin),\
        fits.Column(name='NBIN', format='i4', array=ns_fbin),\
        fits.Column(name='NSEG', format='i4', array=ns_seg),\
        ])
    hdu_ext.header['DT']  =(dt,    'Timing interval')
    hdu_ext.header['NBIN']=(n_bin, 'Number of bin per segment')
    hdu_ext.header['RATE']=(mu_ave, 'Mean count rate [counts/s]')
    hdu_pri=fits.PrimaryHDU(data=None, header=None)
    hdus=fits.HDUList([hdu_pri, hdu_ext])
    hdus.writeto(name_outfits, overwrite=True)

if __name__=='__main__':
    main()
