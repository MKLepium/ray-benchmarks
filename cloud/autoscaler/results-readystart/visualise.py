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
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Requests/s'], label='Requests per second', color='blue')
    plt.title('Total Requests per Second')
    plt.xlabel('Time')
    plt.ylabel('Requests/s')
    plt.grid(True)
    
    # Plotting Response Times
    plt.subplot(2, 1, 2)
    percentiles = ['95%']
    for percentile in percentiles:
        if percentile in data.columns:
            plt.plot(data.index, data[percentile], label=f'{percentile} percentile')
    if 'Total Average Response Time' in data.columns:
        plt.plot(data.index, data['Total Average Response Time'], label='Total Average Response Time', linestyle='--')

    plt.title('Response Times')
    plt.xlabel('Time')
    plt.ylabel('Response Time (ms)')
    plt.legend()
    plt.grid(True)

    # Display the plots
    plt.tight_layout()
    plt.savefig('performance_data.png')

# Usage
plot_performance_data('results_stats_history.csv')