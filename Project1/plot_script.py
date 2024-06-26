import pandas as pd
import matplotlib.pyplot as plt

# Load the data from a CSV file
data = pd.read_csv("output.csv")
data = data.to_numpy()

# System specifications
page_size = 4096  # Page size in bytes
address_size = 8  # Address size in bytes for a 64-bit system
l1_size = 32 * 1024  # L1 cache size in bytes (32 KiB)
l2_size = 256 * 1024  # L2 cache size in bytes (256 KiB)
l3_size = 9 * 1024 * 1024  # L3 cache size in bytes (9 MiB)


# Calculate the page table eviction threshold
# This is derived from the formula:
# Threshold ≈ 1/2 * (Page Size / Address Size) * L3 Cache Size
ratio = page_size / address_size
page_table_eviction_threshold = 0.5 * ratio * l3_size  # calculate the threshold in bytes

# Plotting the latency data
plt.plot(data[:, 0], data[:, 1], label="Random access")
plt.plot(data[:, 0], data[:, 2], label="Sequential access")

# Setting the scale to logarithmic for x axe
plt.xscale('log')
plt.yscale('log')

# Adding vertical lines for cache sizes and the eviction threshold
plt.axvline(x=l1_size, label=f"L1 ({int(l1_size/1024)} KiB per core)", color='red')
plt.axvline(x=l2_size, label=f"L2 ({int(l2_size/1024)} KiB per core)", color='green')
plt.axvline(x=l3_size, label=f"L3 ({int(l3_size/1024/1024)} MiB shared)", color='brown')
plt.axvline(x=page_table_eviction_threshold, label=f"Page Table Eviction Threshold ({int(page_table_eviction_threshold/1024/1024)} MiB)", color='purple')

# Adding a legend
plt.legend()

# Adding titles and labels
plt.title("Memory Latency as a Function of Array Size \n"
          "on Intel(R) Core(TM) i5-8500 CPU @ 3.00GHz")
plt.ylabel("Latency (ns, log scale)")
plt.xlabel("Array Size (bytes, log scale)")

# Displaying the plot
plt.show()