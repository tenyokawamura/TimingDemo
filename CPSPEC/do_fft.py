import numpy as np 
import astropy.io.fits as fits
from sys import argv

def main():
    # ----- Main ----- #
    name_infits =argv[1]
    name_outfits=argv[2]

    hdus=fits.open(name_infits)
    n_seg=len(hdus)-1
    first=True
    for i_seg in range(n_seg):
        ts  =hdus[i_seg+1].data['TIME']
        data=hdus[i_seg+1].data['DATA']

        mu=np.mean(data)
        data-=mu

        # Timing interval
        dt=ts[1]-ts[0]
        # Number of data
        n_data=len(ts)

        # Fourier transform
        fts=np.fft.fft(data)
        # Fourier frequency
        fs =np.fft.fftfreq(n=n_data, d=dt)

        # Even
        if n_data%2==0:
            i_max=int((n_data/2))
        # Odd
        elif n_data%2==1:
            i_max=int((n_data-1/2))

        fts=fts[1:i_max]
        fs=fs[1:i_max]

        if first==True:
            first=False
            ftss=fts
            fs_record=fs
            dt_record=dt
            n_data_record=n_data
        else:
            ftss=np.vstack((ftss, fts))
    hdus.close()

    # ----- Write results ----- #
    for i_seg in range(n_seg):
        hdu_ext=fits.BinTableHDU.from_columns([\
            fits.Column(name='FREQ', format='f4', array=fs_record),\
            fits.Column(name='FT',   format='c8', array=ftss[i_seg])])
        hdu_ext.header['MU']  =(mu           , 'Mean count rate')
        hdu_ext.header['DT']  =(dt_record    , 'Timing interval')
        hdu_ext.header['NBIN']=(n_data_record, 'Number of bin per segment')
        if i_seg==0:
            hdu_pri=fits.PrimaryHDU(data=None, header=None)
            hdus=fits.HDUList([hdu_pri, hdu_ext])
        else:
            hdus.append(hdu_ext)
    hdus.writeto(name_outfits, overwrite=True)

if __name__=='__main__':
    main()
