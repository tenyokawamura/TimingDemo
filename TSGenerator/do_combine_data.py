from tsgeneration import *
import sys
from sys import argv
# -------------------------------------------------- #
#   z(t) = x(t) + y(t-t_delay)                       #
#     x(t): fast variability component               #
#     y(t): slow variability component               #
# -------------------------------------------------- #
def main():
    # ----- Main ----- #
    name_infits_slow=argv[1]
    name_infits_fast=argv[2]
    name_outfits    =argv[3]
    t_delay         =float(argv[4])

    hdus_slow=fits.open(name_infits_slow)
    hdus_fast=fits.open(name_infits_fast)
    n_seg=len(hdus_slow)-1
    for i_seg in range(n_seg):
        ts       =hdus_slow[i_seg+1].data['TIME']
        data_slow=hdus_slow[i_seg+1].data['DATA']
        data_fast=hdus_fast[i_seg+1].data['DATA']

        # Start time [s]
        t_min=hdus_slow[i_seg+1].header['TMIN']
        # End time [s]
        t_max=hdus_slow[i_seg+1].header['TMAX']
        # Sampling interval [s]
        dt   =hdus_slow[i_seg+1].header['DT']
        # Total time [s]
        ct   =hdus_slow[i_seg+1].header['T']
        # Number of bins [s]
        n_bin=hdus_slow[i_seg+1].header['NBIN']
        # Minimum frequency [Hz]
        f_min=hdus_slow[i_seg+1].header['FMIN']
        # Maximum frequency [Hz]
        f_max=hdus_slow[i_seg+1].header['FMAX']

        i_delay=int(round(t_delay/dt))
        data=data_fast+np.roll(data_slow, i_delay)

        if i_seg==0:
            datas=[data]
        else:
            datas=np.vstack((datas, data))
    hdus_slow.close()
    hdus_fast.close()

    # ----- Write data ----- #
    for i_seg in range(n_seg):
        hdu_ext=fits.BinTableHDU.from_columns([\
            fits.Column(name='TIME',   format='f4', array=ts),\
            fits.Column(name='DATA',   format='f4', array=datas[i_seg])])
        hdu_ext.header['TMIN']=(t_min, 'Start time')
        hdu_ext.header['TMAX']=(t_max, 'End time')
        hdu_ext.header['DT']  =(dt   , 'Timing interval')
        hdu_ext.header['T']   =(ct   , 'Total duration')
        hdu_ext.header['NBIN']=(n_bin, 'Number of bin per segment')
        hdu_ext.header['FMIN']=(f_min, 'Minimum frequency')
        hdu_ext.header['FMAX']=(f_max, 'Maximum frequency')

        if i_seg==0:
            hdu_pri=fits.PrimaryHDU(data=None, header=None)
            hdus=fits.HDUList([hdu_pri, hdu_ext])
        else:
            hdus.append(hdu_ext)
    hdus.writeto(name_outfits, overwrite=True)

if __name__=='__main__':
    main()
