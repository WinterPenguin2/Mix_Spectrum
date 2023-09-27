import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import argparse
import numpy as np


parser = argparse.ArgumentParser()

# environment
parser.add_argument('--environment')
parser.add_argument('--group1_address')
parser.add_argument('--group1_name')
parser.add_argument('--group2_address')
parser.add_argument('--group2_name')
parser.add_argument('--group3_address')
parser.add_argument('--group3_name')
parser.add_argument('--group4_address')
parser.add_argument('--group4_name')
parser.add_argument('--group5_address')
parser.add_argument('--group5_name')
parser.add_argument('--group6_address')
parser.add_argument('--group6_name')
parser.add_argument('--group7_address')
parser.add_argument('--group7_name')
args = parser.parse_args()


combined_data = pd.DataFrame(columns=["Algorithm", "Step", "Episode Reward","Color Easy"
    ,"Color Hard","Video Easy","Video Hard"])
algorithm_data=[]

group_1=args.group1_address.split(",")
group_2=args.group2_address.split(",")
group_3=args.group3_address.split(",")
group_4=args.group4_address.split(",")
group_5=args.group5_address.split(",")
group_6=args.group6_address.split(",")
group_7=args.group7_address.split(",")


group_1=[os.path.join("./logs",args.environment,"sac",g) for g in group_1]
group_2=[os.path.join("./logs",args.environment,"sac_aug",g) for g in group_2]
group_3=[os.path.join("./logs",args.environment,"sac_aug",g) for g in group_3]
group_4=[os.path.join("./logs",args.environment,"sac_aug",g) for g in group_4]
group_5=[os.path.join("./logs",args.environment,"sac_aug",g) for g in group_5]
group_6=[os.path.join("./logs",args.environment,"sac_aug",g) for g in group_6]
group_7=[os.path.join("./logs",args.environment,"sac_aug",g) for g in group_7]

group1_name=args.group1_name
group2_name=args.group2_name
group3_name=args.group3_name
group4_name=args.group4_name
group5_name=args.group5_name
group6_name=args.group6_name
group7_name=args.group7_name

algo_lst=[group1_name,group2_name,group3_name,group4_name,group5_name,group6_name,group7_name]
algo_path_lst=[group_1,group_2,group_3,group_4,group_5,group_6,group_7]

for algo,algo_path in zip(algo_lst,algo_path_lst):
    element={}
    element["environment"]=args.environment
    element["algorithm"]=algo
    element["files"]=[]

    for file in algo_path:
        element["files"].append(os.path.join(file,"train.log"))

    algorithm_data.append(element)

# Create the plot
plt.figure(figsize=(10, 6))

for algo_info in algorithm_data:
    algo = algo_info["algorithm"]
    for log_file in algo_info["files"]:
        with open(log_file, 'r') as file:
            data = [eval(line) for line in file]
            for d in data:
                df = pd.DataFrame(data=[[algo, d["step"], d["episode_reward"]]],
                                  columns=["Algorithm", "Step", "Episode Reward"])
                combined_data = pd.concat([combined_data, df])

combined_data=combined_data.iloc[::50]
# Plot data using Seaborn
sns.set(style="darkgrid")
plt.figure(figsize=(10, 6))
sns.lineplot(x="Step", y="Episode Reward", hue="Algorithm", data=combined_data)

plt.xlabel('Step')
plt.ylabel('Episode Reward')
plt.title(args.environment)
plt.savefig("{}.png".format(args.environment))

