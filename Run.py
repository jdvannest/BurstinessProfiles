import os,argparse,pickle

parser = argparse.ArgumentParser(description='Run collection of burstiness profiles for all simulations, or a specific one')
parser.add_argument("-n","--numproc",type=int,default=1,help='The number of processes to use (default=1)')
parser.add_argument("-s","--simulation",choices=['cptmarvel','elektra','storm','rogue','h148','h229','h242','h329'])
args = parser.parse_args()

try:
    config = pickle.load(open('Code/Config.pickle','rb'))
except:
    print('No config files found. Creating new ones...')
    os.system('python Code/Config.py')
    os.system('mv Config.pickle Code/')
    os.system('mv SimulationInfo.pickle Code/')
    config = pickle.load(open('Code/Config.pickle','rb'))

if args.simulation in ['cptmarvel','elektra','storm','rogue','h148','h229','h242','h329']:
    os.system(f'{config["python_path"]} Code/BurstinessCalculation.py -s {args.simulation} -n {args.numproc}')
else:
    for sim in ['cptmarvel','elektra','storm','rogue']:#,'h148','h229','h242','h329']:
        os.system(f'{config["python_path"]} Code/BurstinessCalculation.py -s {sim} -n {args.numproc}')