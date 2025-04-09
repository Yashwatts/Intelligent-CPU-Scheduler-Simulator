# Real-Time CPU Scheduler Simulator (FCFS)

This project is a Real-Time CPU Scheduler Simulator built using Streamlit. It allows users to simulate First-Come, First-Served (FCFS) and Shortest Job First (SJF - Non-Preemptive) scheduling algorithms, visualize live execution, and analyze scheduling metrics interactively.

## 🚀 Features

- ✅ **Algorithm Selection**  
  - Choose between FCFS and SJF (Non-Preemptive).
  - Simulates scheduling based on selected algorithm logic.

- ✅ **FCFS Scheduling Simulation**  
  - Sorts processes based on arrival time.  
  - Simulates execution in real-time with live updates.  
  - Computes **Completion Time, Turnaround Time, and Waiting Time**.
  
- ✅ **SJF Scheduling (Non-Preemptive)**  
  - Selects the process with the shortest burst time among arrived processes.  
  - Dynamically chooses next job based on shortest execution time.
  - Computes **Completion Time, Turnaround Time, and Waiting Time**.  

- ✅ **Live Execution Order**  
  - Displays which process is currently executing.  
  - Shows **progressive execution** with **real-time status updates**.  

- ✅ **Gantt Chart Visualization**  
  - Graphical representation of process execution order.  
  - Helps in understanding scheduling behavior.  

- ✅ **Create a Real OS Process**  
  - Simulates an actual **operating system process** running for 3 seconds.  

---

## 📌 How to Run

### Step 1: Install Dependencies
Make sure you have **Python** installed. Then, install the required packages:

```sh
pip install streamlit pandas matplotlib
```

### Step 2: Run the Streamlit App

```sh
streamlit run app.py
