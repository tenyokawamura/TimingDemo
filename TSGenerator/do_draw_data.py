import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ptick
import numpy as np 
import astropy.io.fits as fits
from sys import argv

def main():
    # ----- Main ----- #
    name_infits=argv[1]
    name_outpdf=argv[2]
    out_pdf=PdfPages(name_outpdf)

    # ----- Plot ----- #
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['figure.subplot.bottom']=0.15
    plt.rcParams['figure.subplot.left']=0.15
    fig=plt.figure(figsize=(9, 6))
    ax=fig.add_subplot(1, 1, 1)

    hdus=fits.open(name_infits)
    ts  =hdus[1].data['TIME']
    data=hdus[1].data['DATA']
    hdus.close()

    ax.plot(ts,\
            data,\
            color='black',\
            marker='None',\
            markersize=2.0,\
            linestyle='solid',\
            linewidth=2.0)

    #ax.set_xlim(2.*10**(-3), 8.*10**(1))
    #ax.set_xlim(0.1, 10)
    #ax.set_xticks(np.linspace(0, 20, 21))
    #ax.set_xticks(np.linspace(0, 20, 41), minor=True)
    #ax.set_ylim(ys_pl[0], ys_pl[1])
    #ax.set_yticks(np.linspace(-1200, 1200, 13))
    #ax.set_yticks(np.linspace(-1200, 1200, 25), minor=True)
    ax.set_xlabel('Time (s)', fontsize=24)
    ax.set_ylabel('Data', fontsize=24)
    #ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    #ax.ticklabel_format(style='sci',axis='x',scilimits=(0,0))
    #ax.xaxis.offsetText.set_fontsize(16)
    #ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    #ax.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
    #ax.yaxis.offsetText.set_fontsize(16)
    ax.spines['top'].set_linewidth(2.0)
    ax.spines['left'].set_linewidth(2.0)
    ax.spines['bottom'].set_linewidth(2.0)
    ax.spines['right'].set_linewidth(2.0)
    #ax.legend(bbox_to_anchor=(0, 0),\
    #          loc='lower left',\
    #          borderaxespad=1.,\
    #          fancybox=0,\
    #          edgecolor='black',\
    #          fontsize=16).get_frame().set_linewidth(1.2)
    ax.tick_params(which='major',\
                   direction="in",\
                   length=12,\
                   width=2.0,\
                   labelsize=22,\
                   pad=8.0,\
                   top=True,\
                   bottom=True,\
                   right=True,\
                   left=True)
    ax.tick_params(which='minor',\
                   direction="in",\
                   length=6,\
                   width=2.0,\
                   labelsize=22,\
                   pad=8.0,\
                   top=True,\
                   bottom=True,\
                   right=True,\
                   left=True)
    #ax.set_title('Cutoff frequency: {0:.2g} Hz'.format(df), fontsize=20)
    out_pdf.savefig()
    plt.close()
    out_pdf.close()

if __name__=='__main__':
    main()
