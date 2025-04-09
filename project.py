import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import os
import subprocess

# FCFS Scheduling
def fcfs_real_time(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    n = len(processes)

    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    start_time = 0

    st.write("### Live Execution Order (FCFS)")

    for i in range(n):
        if processes[i][1] > start_time:
            start_time = processes[i][1]

        completion_time[i] = start_time + processes[i][2]
        turnaround_time[i] = completion_time[i] - processes[i][1]
        waiting_time[i] = turnaround_time[i] - processes[i][2]

        with st.empty():
            st.write(f"Executing {processes[i][0]}... ⏳")
            time.sleep(processes[i][2])
            st.write(f"Completed {processes[i][0]} ✅")

        start_time = completion_time[i]

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    return processes, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time


# SJF Non-Preemptive Scheduling
def sjf_real_time(processes):
    n = len(processes)
    completed = [False] * n
    start_time = 0

    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    result = []

    st.write("### Live Execution Order (SJF)")

    for _ in range(n):
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if not completed[i] and processes[i][1] <= start_time and processes[i][2] < min_burst:
                idx = i
                min_burst = processes[i][2]

        if idx == -1:
            start_time += 1
            continue

        completion_time[idx] = start_time + processes[idx][2]
        turnaround_time[idx] = completion_time[idx] - processes[idx][1]
        waiting_time[idx] = turnaround_time[idx] - processes[idx][2]
        completed[idx] = True
        result.append(processes[idx])

        with st.empty():
            st.write(f"Executing {processes[idx][0]}... ⏳")
            time.sleep(processes[idx][2])
            st.write(f"Completed {processes[idx][0]} ✅")

        start_time = completion_time[idx]

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    return result, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time


def create_os_process():
    if os.name == "posix":
        pid = os.fork()
        if pid == 0:
            os.execlp("sleep", "sleep", "3")
    else:
        subprocess.Popen(["timeout", "/T", "3"], shell=True)


# Streamlit UI
st.title("Real-Time CPU Scheduler Simulator")

algo_choice = st.selectbox("Choose Scheduling Algorithm", ["FCFS", "SJF (Non-Preemptive)"])

n = st.number_input("Enter number of processes", min_value=1, step=1)

processes = []
for i in range(n):
    pid = st.text_input(f"Process {i+1} ID", f"P{i+1}")
    arrival_time = st.number_input(f"Arrival Time for {pid}", min_value=0, step=1, key=f"arrival_{i}")
    burst_time = st.number_input(f"Burst Time for {pid}", min_value=1, step=1, key=f"burst_{i}")
    processes.append([pid, arrival_time, burst_time])

if st.button("Simulate"):
    if algo_choice == "FCFS":
        sim_func = fcfs_real_time
    else:
        sim_func = sjf_real_time

    processes_sorted, ct, tat, wt, avg_wt, avg_tat = sim_func(processes)

    df = pd.DataFrame(processes_sorted, columns=["Process ID", "Arrival Time", "Burst Time"])
    df["Completion Time"] = ct
    df["Turnaround Time"] = tat
    df["Waiting Time"] = wt

    st.write("### Scheduling Table")
    st.dataframe(df)

    st.write(f"**Average Waiting Time:** {avg_wt:.2f} ms")
    st.write(f"**Average Turnaround Time:** {avg_tat:.2f} ms")

    # Gantt Chart
    fig, ax = plt.subplots()
    start_time = 0
    for i in range(len(processes_sorted)):
        ax.barh(1, processes_sorted[i][2], left=start_time, label=processes_sorted[i][0])
        start_time += processes_sorted[i][2]

    ax.set_xlabel("Time")
    ax.set_ylabel("Process Execution")
    ax.legend()
    st.pyplot(fig)

if st.button("Create OS Process"):
    create_os_process()
    st.success("Real OS process started! (Runs for 3 seconds)")
