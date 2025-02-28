import subprocess
import time
import csv
import threading

# Количество параллельных процессов для тестирования
process_counts = [200]

results = []

def run_test():
    """Запускает один процесс с тестами и возвращает время выполнения"""
    start_time = time.time()
    print("test started")
    subprocess.run(
        ['python', '-m', 'pytest', 'test_win.py'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Test completed in {elapsed_time:.2f} seconds")
    return elapsed_time

def run_tests_in_threads(num_threads):
    threads = []
    results = []

    def worker():
        result = run_test()
        if result is not None:
            results.append(result)

    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

for processes in process_counts:
    execution_times = []
    print(f"Testing with {processes} processes...")
    future_results = run_tests_in_threads(processes)
    if future_results:
        avg_time = sum(future_results) / len(future_results)
        execution_times.append(avg_time)

    if execution_times:
        final_avg_time = sum(execution_times) / len(execution_times)
        results.append((processes, final_avg_time))
        print(f"✅ Processes: {processes}, Avg time: {final_avg_time:.2f} sec")

# Сохранение результатов в CSV
csv_file = "test_results.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Processes", "Avg_Response_Time"])
    writer.writerows(results)

print(f"\n📁 Results saved to {csv_file}")
