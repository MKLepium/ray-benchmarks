import matplotlib.pyplot as plt


files = [
    'ray_serve_local_call_times.txt',
    'ray_serve_api_call_times.txt',
    'ray_actor_call_times.txt',
    'local_call_times.txt',
]

labels = [
    'Ray Serve Local Call',
    'Ray Serve API Call',
    'Ray Actor Call',
    'Local Call'
]

# Dictionary to store times
times = {}

# Read times from files
for file, label in zip(files, labels):
    try:
        with open(file, 'r') as f:
            times[label] = [float(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"Error: The file {file} does not exist.")
    except ValueError:
        print(f"Error: Data in {file} could not be converted to float.")

# Plotting
plt.figure(figsize=(10, 6))
for label in labels:
    if label in times:
        plt.plot(times[label], label=label)

plt.xlabel('Iteration')
plt.ylabel('Time (s)')
plt.title('Time taken for 1000 iterations across different setups')
plt.legend()
plt.savefig('comparison_times.png')  # Save the figure to file

# write out the average times, standard deviation and confidence intervals

with open("comparison_times_summary.txt", "w") as f:
    for label in labels:
        if label in times:
            average_time = sum(times[label]) / len(times[label])
            standard_deviation = (sum([(time - average_time) ** 2 for time in times[label]]) / len(times[label])) ** 0.5
            # cut off after 3 decimal places
            average_time = str(average_time)[:str(average_time).index('.') + 5]
            standard_deviation = str(standard_deviation)[:str(standard_deviation).index('.') + 5]
            f.write(f"{label}\n")
            f.write(f"Average time: {average_time}s\n")
            f.write(f"Standard deviation: {standard_deviation}\n\n")
        else:
            f.write(f"{label} does not have data\n\n")
