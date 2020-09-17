import yaml
import argparse


def write_metaconfigs(input, samplesize):
    targets = [ 0, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 700, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
    #targets = [1000]
    #beta_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1]
    beta_values = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1]
    #beta_values = [1]
    for tar in targets:
        for beta in beta_values:
            parameters = {'num_genes': 15000,
                    'num_snps': 1,
                    'num_nullsnps': 0,
                    'sample_size': samplesize,
                    'allele_freq': 0.5,
                    'num_targets': [tar],
                    'identity': True,
                    'iterations': 100,
		    'beta': 'sd',
                    'beta_sd': [beta],
                    'beta_value': 'NA',
                    'rep': 1,
                    'sig_threshold': 0.05}
            value = str(beta).replace(".","")
            filename = f'{input}/numTarget_{tar}/Beta_{value}/metaconfig.yaml'
            #filename = f'/storage/cynthiawu/trans_eQTL/Scripts/Test_nullsnps/simulate_eqtls_only/FastMultivariate/Single_eqtl/SampleSize100/SingleParameter/numTarget_{tar}/Beta_{value}/metaconfig.yaml'
            with open(filename, 'w') as file:
                documents = yaml.dump(parameters, file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input folder with folders of targets and beta values")
    parser.add_argument("-s", "--samplesize", type=int, default=0, help="Sample size")
    params = parser.parse_args()

    write_metaconfigs(input=params.input,
          samplesize=params.samplesize)


if __name__ == "__main__":
    main()