import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import seaborn as sns
import io

# Set Seaborn style for better visuals
sns.set(style="whitegrid")

# FCFS Scheduling
def fcfs_real_time(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
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
            time.sleep(processes[i][2] / 2)  # Reduced sleep for demo
            st.write(f"Completed {processes[i][0]} ✅")
        start_time = completion_time[i]
        progress_bar.progress((i + 1) / n)

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return processes, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time, gantt

# SJF Non-Preemptive Scheduling
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

# SJF Preemptive Scheduling (SRTF with Time Quantum)
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

# Priority Non-Preemptive Scheduling
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

# Priority Preemptive Scheduling (with Time Quantum)
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

# Round Robin Scheduling
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

# Multilevel Queue Scheduling
def multilevel_queue_real_time(processes, quantum):
    n = len(processes)
    foreground = [p for p in processes if p[4] == "Foreground"]
    background = [p for p in processes if p[4] == "Background"]
    
    completion_time = [0] * n
    turnaround_time = [0] * n
    waiting_time = [0] * n
    start_time = 0
    gantt = []
    completed = [False] * n
    result = []
    
    process_map = {p[0]: i for i, p in enumerate(processes)}
    
    st.write("### Live Execution Order (Multilevel Queue)")
    progress_bar = st.progress(0)
    
    fg_queue = []
    fg_arrived = [False] * len(foreground)
    fg_remaining_bt = [p[2] for p in foreground]
    fg_idx_map = {p[0]: i for i, p in enumerate(foreground)}
    
    bg_sorted = sorted(background, key=lambda x: x[1])
    
    while sum(completed) < n:
        for i, p in enumerate(foreground):
            if p[1] <= start_time and not fg_arrived[i]:
                fg_queue.append(i)
                fg_arrived[i] = True
        
        if fg_queue:
            idx = fg_queue.pop(0)
            p = foreground[idx]
            exec_time = min(quantum, fg_remaining_bt[idx])
            gantt.append((p[0], start_time, exec_time))
            with st.empty():
                st.write(f"Executing {p[0]} (Foreground, RR) for {exec_time} unit(s)... ⏳")
                time.sleep(exec_time / 2)
                st.write(f"Completed {p[0]} slice ✅")
            fg_remaining_bt[idx] -= exec_time
            start_time += exec_time
            
            for i, p in enumerate(foreground):
                if p[1] <= start_time and not fg_arrived[i]:
                    fg_queue.append(i)
                    fg_arrived[i] = True
            
            if fg_remaining_bt[idx] > 0:
                fg_queue.append(idx)
            else:
                orig_idx = process_map[p[0]]
                completion_time[orig_idx] = start_time
                turnaround_time[orig_idx] = completion_time[orig_idx] - p[1]
                waiting_time[orig_idx] = turnaround_time[orig_idx] - p[2]
                completed[orig_idx] = True
                result.append(p)
                progress_bar.progress(sum(completed) / n)
        
        elif bg_sorted:
            p = bg_sorted[0]
            if p[1] <= start_time:
                gantt.append((p[0], start_time, p[2]))
                with st.empty():
                    st.write(f"Executing {p[0]} (Background, FCFS)... ⏳")
                    time.sleep(p[2] / 2)
                    st.write(f"Completed {p[0]} ✅")
                orig_idx = process_map[p[0]]
                completion_time[orig_idx] = start_time + p[2]
                turnaround_time[orig_idx] = completion_time[orig_idx] - p[1]
                waiting_time[orig_idx] = turnaround_time[orig_idx] - p[2]
                completed[orig_idx] = True
                result.append(p)
                bg_sorted.pop(0)
                start_time += p[2]
                progress_bar.progress(sum(completed) / n)
            else:
                start_time += 1
        else:
            start_time += 1

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return processes, completion_time, turnaround_time, waiting_time, avg_waiting_time, avg_turnaround_time, gantt

# Plot Gantt Chart
def plot_gantt_chart(gantt, title, algo_choice):
    fig, ax = plt.subplots(figsize=(10, 2))
    unique_pids = list(set([p[0] for p in gantt]))
    colors = sns.color_palette("hls", len(unique_pids))
    color_map = {pid: colors[i] for i, pid in enumerate(unique_pids)}
    
    if algo_choice == "Multilevel Queue":
        color_map = {}
        for pid, _, _ in gantt:
            if pid in [p[0] for p in processes if p[4] == "Foreground"]:
                color_map[pid] = sns.color_palette("hls", 2)[0]
            else:
                color_map[pid] = sns.color_palette("hls", 2)[1]
    
    for i, (pid, start, duration) in enumerate(gantt):
        ax.barh(0, duration, left=start, color=color_map[pid], edgecolor='black')
        ax.text(start + duration / 2, 0, pid, ha='center', va='center', color='white', fontsize=10, weight='bold')
    ax.set_xlabel("Time (ms)")
    ax.set_yticks([])
    ax.set_title(title)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    return fig

# Streamlit UI
st.title("Real-Time CPU Scheduler Simulator")
st.markdown("Simulate various CPU scheduling algorithms with real-time execution and Gantt chart visualization.")

# Algorithm selection
algo_choice = st.selectbox("Choose Scheduling Algorithm", [
    "FCFS", "SJF (Non-Preemptive)", "SJF (Preemptive)", 
    "Priority (Non-Preemptive)", "Priority (Preemptive)", 
    "Round Robin", "Multilevel Queue"
])

# Process input
n = st.number_input("Number of Processes", min_value=1, max_value=10, step=1)
processes = []

st.subheader("Enter Process Details")
for i in range(n):
    st.markdown(f"**Process {i+1}**")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pid = st.text_input(f"Process ID", f"P{i+1}", key=f"pid_{i}")
    with col2:
        arrival_time = st.number_input(f"Arrival Time", min_value=0, step=1, key=f"arrival_{i}")
    with col3:
        burst_time = st.number_input(f"Burst Time", min_value=1, step=1, key=f"burst_{i}")
    with col4:
        priority = st.number_input(f"Priority", min_value=1, step=1, key=f"priority_{i}") if algo_choice.startswith("Priority") else 1
    with col5:
        queue_type = st.selectbox(f"Queue Type", ["Foreground", "Background"], key=f"queue_{i}") if algo_choice == "Multilevel Queue" else "N/A"
    processes.append([pid, arrival_time, burst_time, priority, queue_type])

# Time quantum input
quantum = None
if algo_choice in ["SJF (Preemptive)", "Priority (Preemptive)", "Round Robin", "Multilevel Queue"]:
    quantum = st.number_input(f"Time Quantum (for {algo_choice})", min_value=1, step=1, value=2)

# Simulate button
if st.button("Simulate"):
    if not processes or any(p[2] <= 0 for p in processes):
        st.error("Please provide valid process details (Burst Time > 0).")
    elif algo_choice in ["SJF (Preemptive)", "Priority (Preemptive)", "Round Robin", "Multilevel Queue"] and quantum is None:
        st.error(f"Please specify a time quantum for {algo_choice}.")
    elif algo_choice == "Multilevel Queue" and not any(p[4] in ["Foreground", "Background"] for p in processes):
        st.error("Please assign valid queue types (Foreground or Background).")
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
        elif algo_choice == "Round Robin":
            sim_func = round_robin_real_time
            args = (processes, quantum)
        else:  # Multilevel Queue
            sim_func = multilevel_queue_real_time
            args = (processes, quantum)

        processes_sorted, ct, tat, wt, avg_wt, avg_tat, gantt = sim_func(*args)

        # Display results
        st.subheader("Scheduling Results")
        df = pd.DataFrame(processes_sorted, columns=["Process ID", "Arrival Time", "Burst Time", "Priority", "Queue Type"])
        df["Completion Time"] = ct
        df["Turnaround Time"] = tat
        df["Waiting Time"] = wt

        st.markdown("#### Scheduling Table")
        st.dataframe(df)  # Removed .style.highlight_max to remove green background

        st.markdown(f"**Average Waiting Time:** {avg_wt:.2f} ms")
        st.markdown(f"**Average Turnaround Time:** {avg_tat:.2f} ms")

        # Queue summary for Multilevel Queue
        if algo_choice == "Multilevel Queue":
            fg_count = sum(1 for p in processes if p[4] == "Foreground")
            bg_count = sum(1 for p in processes if p[4] == "Background")
            st.markdown(f"**Queue Summary:** {fg_count} Foreground (RR), {bg_count} Background (FCFS)")

        # Downloadable CSV
        csv = df.to_csv(index=False)
        st.download_button("Download Scheduling Table", csv, "scheduling_table.csv", "text/csv")

        # Gantt Chart
        st.markdown("#### Gantt Chart")
        fig = plot_gantt_chart(gantt, f"{algo_choice} Gantt Chart", algo_choice)
        st.pyplot(fig)
