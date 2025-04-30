import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import seaborn as sns
import io

sns.set(style="whitegrid")

def fcfs_real_time(processes):
    processes.sort(key=lambda x: x[1])
    n = len(processes)
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    start_time = 0
    gantt = []

    st.write("### Live Execution Order (FCFS)")
    progress_bar = st.progress(0)
    for i in range(n):
        if processes[i][1] > start_time:
            start_time = processes[i][1]
        gantt.append((processes[i][0], start_time, processes[i][2]))
        completion_time[i] = start_time + processes[i][2]
        turnaround_time[i] = completion_time[i] - processes[i][1]
        waiting_time[i] = turnaround_time[i] - processes[i][2]
        with st.empty():
            st.write(f"Executing {processes[i][0]}... ⏳")
            time.sleep(processes[i][2] / 2)
            st.write(f"Completed {processes[i][0]} ✅")
        start_time = completion_time[i]
        progress_bar.progress((i + 1) / n)

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return processes, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time, gantt

def sjf_non_preemptive(processes):
    n = len(processes)
    completed = [False] * n
    start_time = 0
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    result = []
    gantt = []

    st.write("### Live Execution Order (SJF Non-Preemptive)")
    progress_bar = st.progress(0)
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
        gantt.append((processes[idx][0], start_time, processes[idx][2]))
        completion_time[idx] = start_time + processes[idx][2]
        turnaround_time[idx] = completion_time[idx] - processes[idx][1]
        waiting_time[idx] = turnaround_time[idx] - processes[idx][2]
        completed[idx] = True
        result.append(processes[idx])
        with st.empty():
            st.write(f"Executing {processes[idx][0]}... ⏳")
            time.sleep(processes[idx][2] / 2)
            st.write(f"Completed {processes[idx][0]} ✅")
        start_time = completion_time[idx]
        progress_bar.progress(len(result) / n)

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return result, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time, gantt

def sjf_preemptive(processes, quantum):
    n = len(processes)
    remaining_bt = [p[2] for p in processes]
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    start_time = 0
    completed = 0
    gantt = []
    current_pid = None
    current_start = 0

    st.write("### Live Execution Order (SJF Preemptive)")
    progress_bar = st.progress(0)
    while completed < n:
        min_bt = float('inf')
        idx = -1
        for i in range(n):
            if processes[i][1] <= start_time and remaining_bt[i] > 0 and remaining_bt[i] < min_bt:
                min_bt = remaining_bt[i]
                idx = i
        if idx == -1:
            start_time += 1
            continue
        if current_pid != processes[idx][0]:
            if current_pid is not None:
                gantt.append((current_pid, current_start, start_time - current_start))
            current_pid = processes[idx][0]
            current_start = start_time
        exec_time = min(quantum, remaining_bt[idx])
        remaining_bt[idx] -= exec_time
        with st.empty():
            st.write(f"Executing {processes[idx][0]} for {exec_time} unit(s)... ⏳")
            time.sleep(0.5)
        if remaining_bt[idx] == 0:
            completion_time[idx] = start_time + exec_time
            turnaround_time[idx] = completion_time[idx] - processes[idx][1]
            waiting_time[idx] = turnaround_time[idx] - processes[idx][2]
            completed += 1
            gantt.append((current_pid, current_start, start_time + exec_time - current_start))
            current_pid = None
            progress_bar.progress(completed / n)
        start_time += exec_time

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return processes, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time, gantt

def priority_non_preemptive(processes):
    n = len(processes)
    completed = [False] * n
    start_time = 0
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    result = []
    gantt = []

    st.write("### Live Execution Order (Priority Non-Preemptive)")
    progress_bar = st.progress(0)
    for _ in range(n):
        idx = -1
        min_priority = float('inf')
        for i in range(n):
            if not completed[i] and processes[i][1] <= start_time and processes[i][3] < min_priority:
                idx = i
                min_priority = processes[i][3]
        if idx == -1:
            start_time += 1
            continue
        gantt.append((processes[idx][0], start_time, processes[idx][2]))
        completion_time[idx] = start_time + processes[idx][2]
        turnaround_time[idx] = completion_time[idx] - processes[idx][1]
        waiting_time[idx] = turnaround_time[idx] - processes[idx][2]
        completed[idx] = True
        result.append(processes[idx])
        with st.empty():
            st.write(f"Executing {processes[idx][0]}... ⏳")
            time.sleep(processes[idx][2] / 2)
            st.write(f"Completed {processes[idx][0]} ✅")
        start_time = completion_time[idx]
        progress_bar.progress(len(result) / n)

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return result, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time, gantt

def priority_preemptive(processes, quantum):
    n = len(processes)
    remaining_bt = [p[2] for p in processes]
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    start_time = 0
    completed = 0
    gantt = []
    current_pid = None
    current_start = 0

    st.write("### Live Execution Order (Priority Preemptive)")
    progress_bar = st.progress(0)
    while completed < n:
        min_priority = float('inf')
        idx = -1
        for i in range(n):
            if processes[i][1] <= start_time and remaining_bt[i] > 0 and processes[i][3] < min_priority:
                min_priority = processes[i][3]
                idx = i
        if idx == -1:
            start_time += 1
            continue
        if current_pid != processes[idx][0]:
            if current_pid is not None:
                gantt.append((current_pid, current_start, start_time - current_start))
            current_pid = processes[idx][0]
            current_start = start_time
        exec_time = min(quantum, remaining_bt[idx])
        remaining_bt[idx] -= exec_time
        with st.empty():
            st.write(f"Executing {processes[idx][0]} for {exec_time} unit(s)... ⏳")
            time.sleep(0.5)
        if remaining_bt[idx] == 0:
            completion_time[idx] = start_time + exec_time
            turnaround_time[idx] = completion_time[idx] - processes[idx][1]
            waiting_time[idx] = turnaround_time[idx] - processes[idx][2]
            completed += 1
            gantt.append((current_pid, current_start, start_time + exec_time - current_start))
            current_pid = None
            progress_bar.progress(completed / n)
        start_time += exec_time

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return processes, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time, gantt

def round_robin_real_time(processes, quantum):
    n = len(processes)
    arrival = [p[1] for p in processes]
    burst = [p[2] for p in processes]
    remaining_bt = burst.copy()
    completion_time = [0] * n
    waiting_time = [0] * n
    turnaround_time = [0] * n
    start_time = 0
    ready_queue = []
    gantt = []
    arrived = [False] * n
    current_start = 0
    current_pid = None

    st.write("### Live Execution Order (Round Robin)")
    progress_bar = st.progress(0)
    while True:
        for i in range(n):
            if arrival[i] <= start_time and not arrived[i]:
                ready_queue.append(i)
                arrived[i] = True

        if not ready_queue:
            if all(bt == 0 for bt in remaining_bt):
                if current_pid is not None:
                    gantt.append((current_pid, current_start, start_time - current_start))
                break
            start_time += 1
            continue

        idx = ready_queue.pop(0)
        if current_pid != processes[idx][0]:
            if current_pid is not None:
                gantt.append((current_pid, current_start, start_time - current_start))
            current_pid = processes[idx][0]
            current_start = start_time

        exec_time = min(quantum, remaining_bt[idx])
        with st.empty():
            st.write(f"Executing {processes[idx][0]} for {exec_time} unit(s)... ⏳")
            time.sleep(exec_time / 2)
            st.write(f"Completed {processes[idx][0]} slice ✅")
        remaining_bt[idx] -= exec_time
        start_time += exec_time

        for i in range(n):
            if arrival[i] <= start_time and not arrived[i]:
                ready_queue.append(i)
                arrived[i] = True

        if remaining_bt[idx] > 0:
            ready_queue.append(idx)
        else:
            completion_time[idx] = start_time
            turnaround_time[idx] = completion_time[idx] - arrival[idx]
            waiting_time[idx] = turnaround_time[idx] - burst[idx]
            gantt.append((current_pid, current_start, start_time - current_start))
            current_pid = None
            progress_bar.progress(sum(1 for bt in remaining_bt if bt == 0) / n)

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return processes, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time, gantt

def plot_gantt_chart(gantt, title, algo_choice):
    fig, ax = plt.subplots(figsize=(10, 2))
    unique_pids = list(set([p[0] for p in gantt]))
    colors = sns.color_palette("hls", len(unique_pids))
    color_map = {pid: colors[i] for i, pid in enumerate(unique_pids)}
    
    for i, (pid, start, duration) in enumerate(gantt):
        ax.barh(0, duration, left=start, color=color_map[pid], edgecolor='black')
        ax.text(start + duration / 2, 0, pid, ha='center', va='center', color='white', fontsize=10, weight='bold')
    ax.set_xlabel("Time (ms)")
    ax.set_yticks([])
    ax.set_title(title)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    return fig

st.title("Real-Time CPU Scheduler Simulator")
st.markdown("Simulate various CPU scheduling algorithms with real-time execution and Gantt chart visualization.")

algo_choice = st.selectbox("Choose Scheduling Algorithm", [
    "FCFS", "SJF (Non-Preemptive)", "SJF (Preemptive)", 
    "Priority (Non-Preemptive)", "Priority (Preemptive)", 
    "Round Robin"
])

n = st.number_input("Number of Processes", min_value=1, max_value=10, step=1)
processes = []

st.subheader("Enter Process Details")
for i in range(n):
    st.markdown(f"**Process {i+1}**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pid = st.text_input(f"Process ID", f"P{i+1}", key=f"pid_{i}")
    with col2:
        arrival_time = st.number_input(f"Arrival Time", min_value=0, step=1, key=f"arrival_{i}")
    with col3:
        burst_time = st.number_input(f"Burst Time", min_value=1, step=1, key=f"burst_{i}")
    with col4:
        priority = st.number_input(f"Priority", min_value=1, step=1, key=f"priority_{i}") if algo_choice.startswith("Priority") else 1
    processes.append([pid, arrival_time, burst_time, priority])

quantum = None
if algo_choice in ["SJF (Preemptive)", "Priority (Preemptive)", "Round Robin"]:
    quantum = st.number_input(f"Time Quantum (for {algo_choice})", min_value=1, step=1, value=2)

if st.button("Simulate"):
    if not processes or any(p[2] <= 0 for p in processes):
        st.error("Please provide valid process details (Burst Time > 0).")
    elif algo_choice in ["SJF (Preemptive)", "Priority (Preemptive)", "Round Robin"] and quantum is None:
        st.error(f"Please specify a time quantum for {algo_choice}.")
    else:
        if algo_choice == "FCFS":
            sim_func = fcfs_real_time
            args = (processes,)
        elif algo_choice == "SJF (Non-Preemptive)":
            sim_func = sjf_non_preemptive
            args = (processes,)
        elif algo_choice == "SJF (Preemptive)":
            sim_func = sjf_preemptive
            args = (processes, quantum)
        elif algo_choice == "Priority (Non-Preemptive)":
            sim_func = priority_non_preemptive
            args = (processes,)
        elif algo_choice == "Priority (Preemptive)":
            sim_func = priority_preemptive
            args = (processes, quantum)
        else:  # Round Robin
            sim_func = round_robin_real_time
            args = (processes, quantum)

        processes_sorted, ct, tat, wt, avg_wt, avg_tat, gantt = sim_func(*args)

        st.subheader("Scheduling Results")
        df = pd.DataFrame(processes_sorted, columns=["Process ID", "Arrival Time", "Burst Time", "Priority"])
        df["Completion Time"] = ct
        df["Turnaround Time"] = tat
        df["Waiting Time"] = wt

        st.markdown("#### Scheduling Table")
        st.dataframe(df)

        st.markdown(f"**Average Waiting Time:** {avg_wt:.2f} ms")
        st.markdown(f"**Average Turnaround Time:** {avg_tat:.2f} ms")

        csv = df.to_csv(index=False)
        st.download_button("Download Scheduling Table", csv, "scheduling_table.csv", "text/csv")

        st.markdown("#### Gantt Chart")
        fig = plot_gantt_chart(gantt, f"{algo_choice} Gantt Chart", algo_choice)
        st.pyplot(fig)
