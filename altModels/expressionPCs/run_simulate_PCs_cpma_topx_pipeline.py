import subprocess
import argparse


def sim_cpmax_pipeline(input_folder, scripts_folder, topx, samplesize):
    #targets = [ 0, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 700, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
    #targets = [ 0, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400]
    #targets = [5, 10, 15, 30]
    #targets = [80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 700, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
    #targets = [0, 20, 40]
    #beta_values = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1]
    #beta_values = [0, 0.1, 1]
    #targets = [ 1, 5, 10, 15, 20, 30, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 700, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
    #targets = [ 1, 10, 15, 20, 30, 40, 60, 80, 150, 200, 250, 300, 350, 400, 450, 500, 700, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 11000, 12000, 13000, 14000, 15000]
    targets = [10000]
    #targets = [ 100, 1000, 10000]
    #targets = [0, 5, 10, 15, 20, 30, 40, 60, 80, 100, 200, 300, 400, 700, 1000, 5000, 10000, 15000]
    #targets = [5, 100, 1010000]
    #beta_values = [0, 0.01, 0.05, 0.1, 1]
    beta_values = [0.1]

    '''
    metaconfig_cmd = f'python {scripts_folder}/Simulator/write_metaconfig.py -i {input_folder} -s {samplesize}'.split(' ')
    #subprocess.call(metaconfig_cmd)
    print('Finished writing metaconfig files')

    print('Starting generating config files')
    #configen_cmd = []
    for tar in targets:
        configen_cmd = []
        for beta in beta_values:
            value = str(beta).replace(".","")
            configen_cmd.append(f'python {scripts_folder}/Simulator/config_generator_specific.py -c {input_folder}/numTarget_{tar}/Beta_{value}/metaconfig.yaml -i 100 -o {input_folder}/numTarget_{tar}/Beta_{value}'.split(' '))
        configen_procs = [ subprocess.Popen(i) for i in configen_cmd]
        #print(configen_procs)
        for p in configen_procs:
            #print(p)
            p.wait()
    print('Finished generating config files')

    print('Starting simulations')
    for tar in targets:
        simulate_cmd = []
        for beta in beta_values:
            value = str(beta).replace(".","")
            simulate_cmd.append(f'python {scripts_folder}/Simulator/simulate_expression_givenoise.py -c {input_folder}/numTarget_{tar}/Beta_{value}/metaconfig.yaml -i 100 -o {input_folder}/numTarget_{tar}/Beta_{value}'.split(' '))
        simulate_procs = [ subprocess.Popen(i) for i in simulate_cmd]
        for p in simulate_procs:
            p.wait()
    print('Finished simulating files')

    '''
    
    print('Starting computing PCA')
    
    for tar in targets:
        pca_cmd = []
        for beta in beta_values:
            value = str(beta).replace(".","")
            pca_cmd.append(f'python {scripts_folder}/expressionPCs/get_expressionPCs.py -f {input_folder}/numTarget_{tar}/Beta_{value} -i 1'.split(' '))
        pca_procs = [ subprocess.Popen(i) for i in pca_cmd]
        for p in pca_procs:
            p.wait()
    print('Finished computing PCA') 
    
     
    print('Starting running cpma pipeline')
    
    for tar in targets:
        cpma_cmd = []
        for beta in beta_values:
            value = str(beta).replace(".","")
            cpma_cmd.append(f'python {scripts_folder}/CPMA/run_cpmax_PCs_pipeline_sim.py -f {input_folder}/numTarget_{tar}/Beta_{value} -x {topx} -p {scripts_folder} -i 1'.split(' '))
        cpma_procs = [ subprocess.Popen(i) for i in cpma_cmd]
        for p in cpma_procs:
            p.wait()
    print('Finished calculating cpma') 
    

    #method = 2 for expression pcs cpmax, method = 1 for cpmax
    print('Starting comparing to chi distribution')
    for tar in targets:
        chidist_cmd = []
        for beta in beta_values:
            value = str(beta).replace(".","")
            chidist_cmd.append(f'python {scripts_folder}/Simulator/compute_pvalue_chidist.py -i {input_folder}/numTarget_{tar}/Beta_{value} -m 2 -x {topx} -t 1 -n 1'.split(' '))
        chidist_procs = [ subprocess.Popen(i) for i in chidist_cmd]
        for p in chidist_procs:
            p.wait()
    print('Finished comparing to chi distribution')
    ''' 
    # method = 2 for expression pcs cpmax, method = 8 for cpmax with null snps
    print('Starting to calculate power')
    for tar in targets:
        power_cmd = []
        for beta in beta_values:
            value = str(beta).replace(".","")
            power_cmd.append(f'python {scripts_folder}/Simulator/calculate_power_singleqtl_cpma.py -c {input_folder}/numTarget_{tar}/Beta_{value}/metaconfig.yaml -m 2 -x {topx} -f {input_folder}/numTarget_{tar}/Beta_{value} -i 100'.split(' '))
        power_procs = [ subprocess.Popen(i) for i in power_cmd]
        for p in power_procs:
            p.wait()
    print('Finished calculating power')
    '''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder", required=True, help="Input folder with num_target and Beta folders")
    parser.add_argument('-p', '--scripts_folder', type=str, help='Input folder with scripts')
    parser.add_argument("-x", "--topx", default=0.1, type=float, help="Top x percent of genes to be used for cpma calculation")
    parser.add_argument("-s", "--samplesize", type=int, default=0, help="Sample size")
    params = parser.parse_args()

    sim_cpmax_pipeline(input_folder=params.input_folder,
          scripts_folder=params.scripts_folder,
          topx=params.topx,
          samplesize=params.samplesize)


if __name__ == "__main__":
    main()
