from tsgeneration import *
import sys
from sys import argv

def main():
    # ----- Main ----- #
    name_outfits=argv[1]
    dt          =float(argv[2])
    n_bin       =int(argv[3])
    n_seg       =int(argv[4])
    mu          =float(argv[5])
    sigma       =float(argv[6])
    df          =float(argv[7])

    gene=TSGeneration()
    gene.set_par(\
        dt=dt,\
        n_bin=n_bin,\
        n_seg=n_seg,\
        name_outfile=name_outfits)
    gene.set_property()
    # Print information on time series
    gene.print_info()

    # Define the power spectrum
    f_c=0 # Zero-centered Lorentzian
    psds=lorentz(f=gene.fs, mu=mu, sigma=sigma, f_c=f_c, df=df)
    gene.set_psd(psd=psds)
    # Simulate time series having zero mean
    gene.simulate_data()
    # Add average value to the time series
    gene.add_average(mu=mu)
    # Output time series
    gene.write_data()

def lorentz(f, mu, sigma, f_c, df):
    var=sigma**2
    # Normalization is always appropriate: \int _0 ^{\infty} df P(f) = (\sigma/\mu)^2 (fractional variance) 
    # (Ingram & Motta, 2019)
    l=(((sigma/mu)**2)/((np.pi/2.)+np.arctan(f_c/df)))*(df/( ((f-f_c)**2) + (df**2) )) 
    return l

if __name__=='__main__':
    main()
