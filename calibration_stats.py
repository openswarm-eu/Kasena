"""
Utility script for calibration of the devices.
"""


import sys
import numpy as np
import matplotlib.pyplot as plt
import warnings
import datetime

warnings.filterwarnings("ignore")


def get_cropped_dataset(filename, N):
    """
    Returns a dataset which contains N samples per device.
    """
    dataset = {}
    with open(f"{filename}") as f:
        lines = f.readlines()[1:]
        for line in lines:
            mac, timestamp, temp = line.strip().split(",")
            dt_format = "%Y-%m-%d %H:%M:%S.%f"
            timestamp = datetime.datetime.strptime(timestamp, dt_format)
            temp = float(temp)

            if mac not in dataset:
                dataset[mac] = {
                    "samples": [],
                    "timestamps": [],
                    "mean": 0.0,
                    "median": 0.0,
                    "stddev": 0.0,
                    "samples_size": 0
                }

            if N < 0 or len(dataset[mac]["samples"]) < N:
                dataset[mac]["samples"].append(temp)
                dataset[mac]["timestamps"].append(timestamp)

    # if N < 0 is provided then we take the min_samples_len as its value
    if N < 0:
        for key in dataset.keys():
            samples_len = len(dataset[key]["samples"])
            if samples_len > N:
                N = samples_len

        for key in dataset.keys():
            dataset[key]["samples"] = dataset[key]["samples"][:N]

    all_data = []
    for key in dataset.keys():
        # filling the device_data dict with its stats.
        device_data = dataset[key]
        device_data["mean"] = np.mean(device_data["samples"])
        device_data["median"] = np.median(device_data["samples"])
        device_data["stddev"] = np.std(device_data["samples"])
        device_data["samples_size"] = N

        # adding the samples to the all_data array
        all_data += device_data["samples"]

    return dataset, N, all_data


def get_device_name(mac):
    """
    Utility function: takes a device's mac address and returns
    the last 3 bytes in the same format as it's physical label.
    """
    name_as_arr = [b.upper() for b in mac.split("-")[5:]]
    name = ""
    for byte_str in name_as_arr:
        name += byte_str
    return name


def plot_stats(dataset, N, all_data):
    """
    Plots both a histogram with temperature counts and a 
    line plot with the average temperature measured for each
    sensor. 
    """
    plot_data = []
    for key in dataset.keys():
        device_data = dataset[key]
        plot_data.append((get_device_name(key), device_data["mean"]))

    plot_data.sort(key=lambda x: x[0])
    figure, axs = plt.subplots(2, 1)
    figure.tight_layout(pad=3.0)

    axs[0].hist(all_data, bins=10, edgecolor="black")
    axs[0].set_title("Temperature Measurements Distribution")
    axs[0].set_xlabel("Temperature (°C)")
    axs[0].set_ylabel("Count")
    n_nodes = len(dataset.keys())
    n_samples = len(all_data)
    p_per_n = N
    mean = np.mean(all_data)
    median = np.median(all_data)
    stddev = np.std(all_data)
    stats_str = """
        num nodes: {n_nodes}
        num samples: {n_samples}
        packets per node: {p_per_n}
        mean: {mean:.2f}
        median: {median:.2f}
        stddev: {stddev:.2f}
    """.format(n_nodes=n_nodes,
               n_samples=n_samples,
               p_per_n=p_per_n,
               mean=mean,
               median=median,
               stddev=stddev)
    axs[0].text(0,
                0.3,
                stats_str,
                horizontalalignment='left',
                transform=axs[0].transAxes)

    device_names = [name for name, _ in plot_data]
    means = [mean for _, mean in plot_data]
    axs[1].set_xticklabels(device_names, rotation=90)
    axs[1].plot(device_names, means, color="orange")
    axs[1].scatter(device_names,
                   means,
                   color="orange",
                   edgecolors="black",
                   zorder=3)
    axs[1].set_title("Mean Temperature per Device")
    axs[1].set_xlabel("Device")
    axs[1].set_ylabel("Mean Temperature")
    plt.show()

    return device_names, means


def plot_comparison(device_names, in_avg_temp, out_avg_temp, gt_in, gt_out):
    """
    Plots both scenarios data: average temperature measured
    by each device and ground truth.
    """
    _, ax = plt.subplots()
    ax.set_xticklabels(device_names, rotation=90)
    ax.plot(device_names, in_avg_temp, color="mediumaquamarine", zorder=1)
    ax.plot(device_names, [gt_in] * len(device_names),
            color="seagreen",
            zorder=1,
            label=f"CO2 temp in: {gt_in}°C")
    ax.scatter(device_names,
               in_avg_temp,
               color="mediumaquamarine",
               edgecolors="black",
               zorder=2)

    ax.plot(device_names, out_avg_temp, color="cornflowerblue", zorder=3)
    ax.plot(device_names, [gt_out] * len(device_names),
            color="mediumblue",
            zorder=1,
            label=f"CO2 temp out: {gt_out}°C")
    ax.scatter(device_names,
               out_avg_temp,
               color="cornflowerblue",
               edgecolors="black",
               zorder=4)
    ax.set_title("Calibration Measurements")
    ax.set_xlabel("Device")
    ax.set_ylabel("Mean Temperature")
    ax.legend()

    plt.show()


def generate_output_csv(dataset, gt, filename):
    """
    For each device in the dataset, it takes the mean temperature
    measured and calculates its offset from the ground truth. The results
    are saved in a .csv file.
    """
    with open(f"{filename}", "w+") as f:
        f.write(
            "MAC Address,Average Temperature Measured (°C),Ground Truth (°C),Offset with Ground Truth (°C)\n"
        )
        for mac in dataset:
            name = get_device_name(mac)
            offset = gt - dataset[mac]["mean"]
            f.write("{name},{mean:.2f},{gt:.2f},{offset:.2f}\n".format(
                name=name, mean=dataset[mac]["mean"], gt=gt, offset=offset))


def main(inside_csv, outside_csv, gt_in, gt_out, N):
    dataset_in, in_N, in_raw_data = get_cropped_dataset(inside_csv, N)
    dataset_out, out_N, out_raw_data = get_cropped_dataset(outside_csv, N)

    device_names_in, in_avg_temp = plot_stats(dataset_in, in_N, in_raw_data)
    device_names_out, out_avg_temp = plot_stats(dataset_out, out_N,
                                                out_raw_data)

    assert device_names_in == device_names_out
    plot_comparison(device_names_in, in_avg_temp, out_avg_temp, gt_in, gt_out)

    generate_output_csv(dataset_in, gt_in, f"results_in_office.csv")
    generate_output_csv(dataset_out, gt_out, f"results_out_office.csv")

    for name in dataset_in:
        print(get_device_name(name))

if __name__ == "__main__":
    inside_csv, outside_csv, gt_in, gt_out, N = sys.argv[1:]
    main(inside_csv, outside_csv, float(gt_in), float(gt_out), int(N))
