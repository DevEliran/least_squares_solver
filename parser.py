import argparse
from solver import solve_ls

parser = argparse.ArgumentParser()
required = parser.add_argument_group('required arguments')
required.add_argument('-ls','--ls_path', help="Full path for a csv file containing the coordinates", required=True)
required.add_argument('-d','--degree', help="The desired polynomial estimation degree", required=True)
parser.add_argument("-w", "--weighted", help ="Solve Weighted LS", action="store_true")
parser.add_argument("-r", "--regulized", help ="Solve regulized LS", action="store_true")
parser.add_argument("-pw", "--path_weighted", help = "Full path for weights specification", action="store")
args=parser.parse_args()

if str(args.ls_path).split('.')[-1] != 'csv':
    print('Please upload a csv file')
if args.weighted and args.path_weighted == None or str(args.path_weighted).split('.')[-1] != 'csv':
    print('Please upload a csv file containing the weights')

solve_ls(args.ls_path, args.weighted, args.regulized, args.path_weighted, args.degree)
