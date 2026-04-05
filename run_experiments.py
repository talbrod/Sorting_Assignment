import time
import random
import statistics
import argparse
import matplotlib.pyplot as plt
import sys


# --- Part A: The Full Quintet ---

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped: break
    return arr


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]);
            i += 1
        else:
            result.append(right[j]);
            j += 1
    result.extend(left[i:]);
    result.extend(right[j:])
    return result


def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# --- Part C: Noise Logic (5% and 20%) ---

def add_noise(arr, percent):
    n = len(arr)
    num_swaps = int(n * (percent / 100))
    for _ in range(num_swaps):
        idx1, idx2 = random.randint(0, n - 1), random.randint(0, n - 1)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr


# --- Core Experiment Runner ---

def run_experiment(algo_ids, sizes, exp_type, repetitions):
    algo_map = {1: ("Bubble Sort", bubble_sort), 2: ("Selection Sort", selection_sort),
                3: ("Insertion Sort", insertion_sort), 4: ("Merge Sort", merge_sort),
                5: ("Quick Sort", quick_sort)}

    results = {aid: {"mean": [], "std": []} for aid in algo_ids if aid in algo_map}

    # Define noise and descriptions based on Part D requirements
    if exp_type == 1:
        noise_percent, desc = 5, "Nearly Sorted (5% Noise)"
    elif exp_type == 2:
        noise_percent, desc = 20, "Nearly Sorted (20% Noise)"
    else:
        noise_percent, desc = 0, "Random Arrays"

    print(f"\n--- Running Experiment: {desc} ---")
    for size in sizes:
        print(f"  Processing size: {size}...")
        for aid in algo_ids:
            if aid not in algo_map: continue
            times = []
            for _ in range(repetitions):
                if exp_type == 0:
                    arr = [random.randint(0, 100000) for _ in range(size)]
                else:
                    # Starts with Sorted Array for Part C/D
                    arr = sorted([random.randint(0, 100000) for _ in range(size)])
                    arr = add_noise(arr, noise_percent)

                start = time.perf_counter()
                algo_map[aid][1](arr.copy())
                end = time.perf_counter()
                times.append(end - start)

            results[aid]["mean"].append(statistics.mean(times))
            results[aid]["std"].append(statistics.stdev(times) if repetitions > 1 else 0)

    # Plotting
    plt.figure(figsize=(10, 6))
    for aid in algo_ids:
        if aid in algo_map:
            plt.errorbar(sizes, results[aid]["mean"], yerr=results[aid]["std"],
                         label=algo_map[aid][0], capsize=5, marker='o')

    plt.xlabel("Size (n)");
    plt.ylabel("Time (seconds)")
    plt.title(desc)
    plt.legend();
    plt.grid(True)

    # Standard naming for assignment submission
    filename = "result1.png" if exp_type == 0 else "result2.png"
    plt.savefig(filename)
    print(f"Successfully saved plot as {filename}")
    plt.show()


# --- Main Logic ---

def main():
    parser = argparse.ArgumentParser(description="Sorting Assignment")
    parser.add_argument("-a", nargs="+", type=int, help="Algorithm IDs (1-5)")
    parser.add_argument("-s", nargs="+", type=int, help="Array sizes")
    parser.add_argument("-e", type=int, default=0, help="0:Random, 1:5% Noise, 2:20% Noise")
    parser.add_argument("-r", type=int, default=10, help="Repetitions")
    args = parser.parse_args()

    # If flags are used in terminal, run and quit immediately
    if args.a and args.s:
        run_experiment(args.a, args.s, args.e, args.r)
        return

    # --- AUTO-RUN FOR ASSIGNMENT ---
    print("Executing standard assignment experiments...")
    # Part B
    run_experiment([1, 4, 5], [100, 500, 1000, 2500, 5000], 0, 10)
    # Part C (Defaults to 20% noise per your previous request)
    run_experiment([1, 4, 5], [100, 500, 1000, 2500, 5000], 2, 10)

    # --- INTERACTIVE PART D MODE ---
    print("\n" + "=" * 50)
    print("Welcome to the PART D Lounge!")
    print("Run custom experiments without restarting the script.")
    print("Usage: ID1 ID2 | Size1 Size2 | ExpType(0-2) | Reps")
    print("Example: 1 2 3 | 100 500 1000 | 1 | 5")

    while True:
        try:
            line = input("\nEnter custom parameters (or 'Q' to quit): ").strip()
            if line.upper() == 'Q': break

            sections = line.split('|')
            ids = [int(x) for x in sections[0].split()]
            sizes = [int(x) for x in sections[1].split()]
            etype = int(sections[2].strip())
            reps = int(sections[3].strip())

            run_experiment(ids, sizes, etype, reps)
        except Exception as err:
            print(f"That didn't quite abide, man: {err}")
            print("Format: IDs | Sizes | ExpType | Reps")


if __name__ == "__main__":
    main()