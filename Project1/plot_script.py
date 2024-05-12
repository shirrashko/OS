import pandas as pd
import matplotlib.pyplot as plt

# Load the data from a CSV file
data = pd.read_csv(r"/Users/srashkovits/PycharmProjects/Lightricks/pythonProject/output.csv")
data = data.to_numpy()

# Define the cache sizes (assuming these values are in bytes and per core)
l1_size = 32 * 1024  # 32 KiB for L1 cache
l2_size = 1 * 1024 * 1024  # 1 MiB for L2 cache
l3_size = 9 * 1024 * 1024  # 9 MiB for L3 cache

# Plotting the latency data
plt.plot(data[:, 0], data[:, 1], label="Random access")
plt.plot(data[:, 0], data[:, 2], label="Sequential access")

# Setting the scale to logarithmic for both axes
plt.xscale('log')

# Adding vertical lines for cache sizes
plt.axvline(x=l1_size, label=f"L1 ({l1_size/1024} KiB)", c='red', linestyle=':')
plt.axvline(x=l2_size, label=f"L2 ({l2_size/1024/1024} MiB)", c='green', linestyle=':')
plt.axvline(x=l3_size, label=f"L3 ({l3_size/1024/1024} MiB)", c='brown', linestyle=':')

# Adding a legend
plt.legend()

# Adding titles and labels
plt.title("Memory Latency as a Function of Array Size on \n"
          "Intel(R) Core(TM) i5-8500 CPU @ 3.00GHz")
plt.ylabel("Latency (ns)")
plt.xlabel("Array Size (bytes, log scale)")

# Displaying the plot
plt.show()
