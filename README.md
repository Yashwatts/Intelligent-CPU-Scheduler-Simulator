# Real-Time CPU Scheduler Simulator

This project is a Real-Time CPU Scheduler Simulator built using **Streamlit**. It allows users to simulate various CPU scheduling algorithms, visualize live execution with Gantt charts, and analyze scheduling metrics interactively. The simulator is designed as an educational tool to understand CPU scheduling behavior in operating systems.

## 🚀 Features

- ✅ **Algorithm Selection**  
  - Choose from seven scheduling algorithms:  
    - First-Come, First-Served (FCFS)  
    - Shortest Job First (SJF, Non-Preemptive)  
    - Shortest Job First (SJF, Preemptive)  
    - Priority (Non-Preemptive)  
    - Priority (Preemptive)  
    - Round Robin  
  - Simulates scheduling based on the selected algorithm's logic.

- ✅ **FCFS Scheduling Simulation**  
  - Sorts processes based on arrival time.  
  - Executes processes in the order of their arrival.  
  - Computes **Completion Time**, **Turnaround Time**, and **Waiting Time**.

- ✅ **SJF Scheduling (Non-Preemptive)**  
  - Selects the process with the shortest burst time among arrived processes.  
  - Executes the selected process to completion before choosing the next.  
  - Computes **Completion Time**, **Turnaround Time**, and **Waiting Time**.

- ✅ **SJF Scheduling (Preemptive)**  
  - Preempts the current process if a new process with a shorter remaining burst time arrives.  
  - Uses a user-defined time quantum for execution slices.  
  - Computes **Completion Time**, **Turnaround Time**, and **Waiting Time**.

- ✅ **Priority Scheduling (Non-Preemptive)** )
  - Selects the process with the highest priority (lowest priority number) among arrived processes.  
  - Executes the selected process to completion.  
  - Computes **Completion Time**, **Turnaround Time**, and **Waiting Time**.

- ✅ **Priority Scheduling (Preemptive)**  
  - Preempts the current process if a new process with higher priority arrives.  
  - Uses a user-defined time quantum for execution slices.  
  - Computes **Completion Time**, **Turnaround Time**, and **Waiting Time**.

- ✅ **Round Robin Scheduling**  
  - Allocates CPU in time slices using a user-defined time quantum.  
  - Manages a dynamic ready queue to ensure fair execution.  
  - Handles process arrivals dynamically.  
  - Computes **Completion Time**, **Turnaround Time**, and **Waiting Time**.

- ✅ **Live Execution Order**  
  - Displays the currently executing process with real-time status updates.  
  - Shows progressive execution with a **progress bar** for each algorithm.  

- ✅ **Gantt Chart Visualization**  
  - Graphical representation of process execution order using Matplotlib and Seaborn.  
  - Color-coded processes for clear visualization of scheduling behavior.  
  - Supports distinct coloring for Foreground and Background processes in Multilevel Queue.

- ✅ **Scheduling Metrics and Export**  
  - Displays a detailed table with **Process ID**, **Arrival Time**, **Burst Time**, **Priority** (if applicable), **Queue Type** (for Multilevel Queue), **Completion Time**, **Turnaround Time**, and **Waiting Time**.  
  - Computes average **Waiting Time** and **Turnaround Time**.  
  - Allows downloading the scheduling table as a **CSV file**.

## 📌 How to Run

### Step 1: Install Dependencies
Make sure you have **Python** installed. Then, install the required packages:

```sh
pip install streamlit pandas matplotlib seaborn
```
### Step 2: Save the code in a file named project.py and run the following command:
```sh
streamlit run project.py
```
