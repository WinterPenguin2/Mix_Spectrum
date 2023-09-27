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
        element["files"].append(os.path.join(file,"eval.log"))

    algorithm_data.append(element)

# Create the plot
plt.figure(figsize=(10, 6))

for algo_info in algorithm_data:
    algo = algo_info["algorithm"]
    for log_file in algo_info["files"]:
        with open(log_file, 'r') as file:
            data = [eval(line) for line in file]
            for d in data:
                df = pd.DataFrame(data=[[algo, d["step"], d["episode_reward"],d["episode_reward_color_easy"],
                                         d["episode_reward_color_hard"],d["episode_reward_video_easy"],d["episode_reward_video_hard"]]],
                                  columns=["Algorithm", "Step", "Episode Reward","Color Easy"
    ,"Color Hard","Video Easy","Video Hard"])
                combined_data = pd.concat([combined_data, df])


eval_csv = pd.DataFrame(columns=["Algorithm","Color Easy","bound",
                                 "Color Hard","bound","Video Easy","bound","Video Hard","bound"])

for algo in algo_lst:
    # A 알고리즘의 Step 5000인 행들을 필터링합니다.
    filtered_df = combined_data[(combined_data['Algorithm'] == algo) & (combined_data['Step'] == 500000)]
    print(filtered_df)
    # Episode Reward 열의 값들을 추출합니다.
    color_easy = filtered_df['Color Easy']
    color_hard = filtered_df['Color Hard']
    video_easy = filtered_df['Video Easy']
    video_hard = filtered_df['Video Hard']
    # 평균값을 계산합니다.
    average_color_easy = np.mean(color_easy)
    average_color_hard = np.mean(color_hard)
    average_video_easy = np.mean(video_easy)
    average_video_hard = np.mean(video_hard)
    data=[algo,int(average_color_easy),int(np.std(color_easy)),
          int(average_color_hard),int(np.std(color_hard)),
          int(average_video_easy),int(np.std(video_easy)),
          int(average_video_hard),int(np.std(video_hard))]
    df = pd.DataFrame(data=[data],
                      columns=["Algorithm","Color Easy","bound",
                                 "Color Hard","bound","Video Easy","bound","Video Hard","bound"])
    eval_csv = pd.concat([eval_csv, df])

    everything=pd.concat([filtered_df['Color Easy'],filtered_df['Color Hard'],filtered_df['Video Easy'],filtered_df['Video Hard']])
eval_csv.to_csv("eval_{}.csv".format(args.environment))
