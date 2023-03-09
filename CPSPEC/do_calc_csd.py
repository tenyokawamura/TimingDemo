import numpy as np 
import astropy.io.fits as fits
from sys import argv

def main():
    # ----- Main ----- #
    name_infits_fft    =argv[1]
    name_infits_psd    =argv[2]
    name_infits_fft_ref=argv[3]
    name_infits_psd_ref=argv[4]
    name_outfits       =argv[5]
    rebin              =float(argv[6])

    hdus_fft_ref=fits.open(name_infits_fft_ref)
    hdus_psd_ref=fits.open(name_infits_psd_ref)

    hdus=fits.open(name_infits_fft)
    n_seg=len(hdus)-1

    first=True
    for i_seg in range(n_seg):
        fs     =hdus_fft_ref[i_seg+1].data['FREQ']
        fts_ref=hdus_fft_ref[i_seg+1].data['FT']
        fts    =hdus        [i_seg+1].data['FT']

        # Mean count rate
        mu_ref=hdus_fft_ref[i_seg+1].header['MU']
        mu    =hdus        [i_seg+1].header['MU']
        # Timing interval
        dt=hdus_fft_ref    [i_seg+1].header['DT']
        # Number of data
        n_bin=hdus_fft_ref [i_seg+1].header['NBIN']
        # Normalization of power spectrum
        norm=2.*dt/((mu*mu_ref)*n_bin)

        # Cross spectrum
        csds=norm*np.conjugate(fts_ref)*fts

        if first==True:
            first=False
            csdss=csds
            fs_record=fs
            dt_record=dt
            n_bin_record=n_bin
        else:
            csdss=np.vstack((csdss, csds))
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
    csdss_t=csdss.T

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
                csds_merge  =np.ravel(csdss_t[is_merge])

                f_min_rebin=fs_min_merge[0]
                f_max_rebin=fs_max_merge[-1]
                f_mid_rebin=(f_min_rebin+f_max_rebin)/2.
                csd_rebin=np.mean(csds_merge)
                csd_re_rebin=np.real(csd_rebin)
                csd_im_rebin=np.imag(csd_rebin)
                csd_ab_rebin=np.abs(csd_rebin)
                csd_ph_rebin=np.angle(csd_rebin)
                csd_ti_rebin=csd_ph_rebin/(2.*np.pi*f_mid_rebin)

                if first==True:
                    first=False
                    fs_min_rebin=f_min_rebin
                    fs_max_rebin=f_max_rebin
                    csds_re_rebin=csd_re_rebin
                    csds_im_rebin=csd_im_rebin
                    csds_ab_rebin=csd_ab_rebin
                    csds_ph_rebin=csd_ph_rebin
                    csds_ti_rebin=csd_ti_rebin
                    ns_fbin     =n_fbin
                    ns_seg      =n_seg
                else:
                    fs_min_rebin =np.append(fs_min_rebin,  f_min_rebin)
                    fs_max_rebin =np.append(fs_max_rebin,  f_max_rebin)
                    csds_re_rebin=np.append(csds_re_rebin, csd_re_rebin)
                    csds_im_rebin=np.append(csds_im_rebin, csd_im_rebin)
                    csds_ab_rebin=np.append(csds_ab_rebin, csd_ab_rebin)
                    csds_ph_rebin=np.append(csds_ph_rebin, csd_ph_rebin)
                    csds_ti_rebin=np.append(csds_ti_rebin, csd_ti_rebin)
                    ns_fbin      =np.append(ns_fbin,       n_fbin)
                    ns_seg       =np.append(ns_seg,        n_seg)

            f_mid_min=f_mid_max
            f_mid_max*=rebin

    elif rebin==1.:
        fs_min_rebin=fs_min
        fs_max_rebin=fs_max
        first=True
        for f, csds_merge in zip(fs, csdss_t):
            f_mid_rebin=f
            csds_merge=np.ravel(csds_merge)
            n_fbin=1
            csd_rebin=np.mean(csds_merge)
            csd_re_rebin=np.real(csd_rebin)
            csd_im_rebin=np.imag(csd_rebin)
            csd_ab_rebin=np.abs(csd_rebin)
            csd_ph_rebin=np.angle(csd_rebin)
            csd_ti_rebin=csd_ph_rebin/(2.*np.pi*f_mid_rebin)
            if first==True:
                first=False
                csds_re_rebin=csd_re_rebin
                csds_im_rebin=csd_im_rebin
                csds_ab_rebin=csd_ab_rebin
                csds_ph_rebin=csd_ph_rebin
                csds_ti_rebin=csd_ti_rebin
                ns_fbin     =n_fbin
                ns_seg      =n_seg
            else:
                csds_re_rebin=np.append(csds_re_rebin, csd_re_rebin)
                csds_im_rebin=np.append(csds_im_rebin, csd_im_rebin)
                csds_ab_rebin=np.append(csds_ab_rebin, csd_ab_rebin)
                csds_ph_rebin=np.append(csds_ph_rebin, csd_ph_rebin)
                csds_ti_rebin=np.append(csds_ti_rebin, csd_ti_rebin)
                ns_fbin     =np.append(ns_fbin,      n_fbin)
                ns_seg      =np.append(ns_seg,       n_seg)

    fs_rebin =(fs_min_rebin+fs_max_rebin)/2.
    dfs_rebin=(fs_max_rebin-fs_min_rebin)/2.

    fs=fs_rebin
    dfs=dfs_rebin
    csds_re=csds_re_rebin
    csds_im=csds_im_rebin
    csds_ab=csds_ab_rebin
    csds_ph=csds_ph_rebin
    csds_ti=csds_ti_rebin

    # --- Calculate error --- #
    hdus=fits.open(name_infits_psd)
    psds_ref=hdus_psd_ref[1].data['PSD']
    psds    =hdus        [1].data['PSD']
    hdus.close()

    # d(Re[CSD(f)])
    numes=psds_ref*psds+(csds_re**2)-(csds_im**2)
    numes*=(numes>=0) # Numerator in \sqrt must not be negative.
    dcsds_re=np.sqrt(numes/(2.*ns_fbin*ns_seg))

    # d(Im[CSD(f)])
    numes=psds_ref*psds-(csds_re**2)+(csds_im**2)
    numes*=(numes>=0) # Numerator in \sqrt must not be negative.
    dcsds_im=np.sqrt(numes/(2.*ns_fbin*ns_seg))

    # d(|CSD(f)|)
    dcsds_ab=np.sqrt(psds_ref*psds/(ns_fbin*ns_seg))

    # d(Arg[CSD(f)])
    g2s=(csds_ab**2)/(psds_ref*psds) # Assuming N>=500 (Ingram 2019)
    g2s=g2s*(g2s<=1.)+1.*(g2s>1.) # Coherence cannot be larger than unity
    dcsds_ph=np.sqrt((1.-g2s)/(2.*g2s*ns_fbin*ns_seg))

    # d(Arg[CSD(f)]/2\pi f)
    dcsds_ti=dcsds_ph/(2.*np.pi*fs)

    # ----- Write results ----- #
    hdu_ext=fits.BinTableHDU.from_columns([\
        fits.Column(name='F',     format='f4', array=fs),\
        fits.Column(name='DF',    format='f4', array=dfs),\
        fits.Column(name='CSDR',  format='f4', array=csds_re),\
        fits.Column(name='CSDI',  format='f4', array=csds_im),\
        fits.Column(name='CSDA',  format='f4', array=csds_ab),\
        fits.Column(name='CSDP',  format='f4', array=csds_ph),\
        fits.Column(name='CSDT',  format='f4', array=csds_ti),\
        fits.Column(name='G2',    format='f4', array=g2s),\
        fits.Column(name='DCSDR', format='f4', array=dcsds_re),\
        fits.Column(name='DCSDI', format='f4', array=dcsds_im),\
        fits.Column(name='DCSDA', format='f4', array=dcsds_ab),\
        fits.Column(name='DCSDP', format='f4', array=dcsds_ph),\
        fits.Column(name='DCSDT', format='f4', array=dcsds_ti),\
        fits.Column(name='NBIN',  format='i4', array=ns_fbin),\
        fits.Column(name='NSEG',  format='i4', array=ns_seg)\
        ])
    hdu_ext.header['DT']  =(dt,    'Timing interval')
    hdu_ext.header['NBIN']=(n_bin, 'Number of bin per segment')
    hdu_pri=fits.PrimaryHDU(data=None, header=None)
    hdus=fits.HDUList([hdu_pri, hdu_ext])
    hdus.writeto(name_outfits, overwrite=True)
    hdus_fft_ref.close()
    hdus_psd_ref.close()

if __name__=='__main__':
    main()
