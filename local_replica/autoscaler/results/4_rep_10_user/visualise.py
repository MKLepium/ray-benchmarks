import pandas as pd
import matplotlib.pyplot as plt

def plot_performance_data(csv_file):
    # Load the CSV file
    data = pd.read_csv(csv_file)
    
    # Convert timestamp to a readable format (if it's in UNIX epoch time)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')


    
    # Set timestamp as index
    data.set_index('Timestamp', inplace=True)
    
    # Plotting Total Requests per Second
    plt.figure(figsize=(14, 7))
    plt.subplot(3, 1, 1)
    plt.plot(data.index, data['Requests/s'], label='Requests per second', color='blue')
    plt.title('Total Requests per Second', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Requests/s', fontsize=14)
    plt.grid(True)
    
    # Plotting Response Times
    plt.subplot(3, 1, 2)
    percentiles = ['95%']
    for percentile in percentiles:
        if percentile in data.columns:
            plt.plot(data.index, data[percentile], label=f'{percentile} percentile')
    if 'Total Average Response Time' in data.columns:
        plt.plot(data.index, data['Total Average Response Time'], label='Total Average Response Time', linestyle='--')

    plt.title('Response Times', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Response Time (ms)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True)
    
    # Plotting Number of Users
    plt.subplot(3, 1, 3)
    plt.plot(data.index, data['User Count'], label='Number of Users', color='green')
    plt.title('Number of Users', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('User Count', fontsize=14)
    plt.grid(True)
    
    # Display the plots
    plt.tight_layout()
    plt.savefig('performance_data.png')

# Usage
plot_performance_data('results_stats_history.csv')