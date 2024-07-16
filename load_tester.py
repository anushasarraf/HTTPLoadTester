# Installing all dependencies

import argparse
import requests
import time
import threading
import statistics
import psutil
from queue import Queue, Empty

class LoadTester:
    def __init__(self, url, max_qps, duration, workers, method='GET'):
        """
        Initialize the LoadTester object with parameters for the load test.

        Args:
        - url (str): URL to test.
        - max_qps (int): Maximum queries per second.
        - duration (int): Test duration in seconds.
        - workers (int): Number of concurrent workers.
        - method (str): HTTP method to use (default: 'GET').
        """
        self.url = url
        self.max_qps = max_qps
        self.duration = duration
        self.workers = workers
        self.method = method.upper()

        self.latencies = []
        self.errors = 0
        self.request_queue = Queue()
        self.stop_event = threading.Event()

    def worker(self):
        """
        Worker function that sends HTTP requests and records latencies.
        """
        while not self.stop_event.is_set():
            try:
                self.request_queue.get(timeout=1)
                start_time = time.time()
                try:
                    if self.method == 'GET':
                        response = requests.get(self.url)
                    elif self.method == 'POST':
                        response = requests.post(self.url, data={'key': 'value'})
                    # Add more HTTP methods as needed (PUT, DELETE, etc.)
                    else:
                        print(f"Unsupported HTTP method: {self.method}")
                        continue
                    
                    latency = time.time() - start_time
                    self.latencies.append(latency)
                    if response.status_code != 200:
                        self.errors += 1
                except requests.RequestException as e:
                    print(f"Request failed: {e}")
                    self.errors += 1
                finally:
                    self.request_queue.task_done()
            except Empty:
                continue

    def adjust_workload(self, current_time):
        """
        Simulates workload adjustments over time.
        
        Args:
        - current_time (float): Current time elapsed since the start of the test.

        Returns:
        - int: Adjusted queries per second (QPS).
        """

        # Example workload simulation: Varying QPS over time
        if current_time < self.duration / 3:
            return int(self.max_qps * 0.5)
        elif current_time < 2 * self.duration / 3:
            return self.max_qps
        else:
            return int(self.max_qps * 0.75)

    def monitor_resources(self):
        """
        Monitors CPU and memory usage during the load test.
        """
        while not self.stop_event.wait(timeout=1):
            # Monitor CPU and memory usage
            cpu_percent = psutil.cpu_percent(interval=None)
            memory_percent = psutil.virtual_memory().percent
            print(f"CPU Usage: {cpu_percent}% | Memory Usage: {memory_percent}%")
    
    def run(self):
        """
        Executes the load test, coordinating workers, resource monitoring, and reporting.
        """
        print(f"Starting load test with {self.method} requests")
        threads = []
        
        # Start resource monitoring thread
        resource_thread = threading.Thread(target=self.monitor_resources)
        resource_thread.daemon = True
        resource_thread.start()
        
        # Start worker threads
        for _ in range(self.workers):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            threads.append(thread)
            thread.start()

        start_time = time.time()
        while time.time() - start_time < self.duration:
            current_qps = self.adjust_workload(time.time() - start_time)
            print(f"Current QPS: {current_qps}")
            for _ in range(current_qps):
                self.request_queue.put(None)
            time.sleep(1.0)
        
        self.request_queue.join()
        self.stop_event.set()

        for thread in threads:
            thread.join()

        resource_thread.join()

        self.report()

    def report(self):
        """
        Generates and prints a report summarizing the load test results.
        """
        print("Generating report")
        total_requests = len(self.latencies) + self.errors
        successful_requests = len(self.latencies)
        failed_requests = self.errors

        if self.latencies:
            avg_latency = statistics.mean(self.latencies)
            min_latency = min(self.latencies)
            max_latency = max(self.latencies)
            stddev_latency = statistics.stdev(self.latencies)
        else:
            avg_latency = min_latency = max_latency = stddev_latency = 0

        throughput = successful_requests / self.duration

        print(f"Total requests: {total_requests}")
        print(f"Successful requests: {successful_requests}")
        print(f"Failed requests: {failed_requests}")
        print(f"Error rate: {failed_requests / total_requests * 100:.2f}%")
        print(f"Average latency: {avg_latency:.4f} seconds")
        print(f"Minimum latency: {min_latency:.4f} seconds")
        print(f"Maximum latency: {max_latency:.4f} seconds")
        print(f"Standard deviation of latency: {stddev_latency:.4f} seconds")
        print(f"Throughput: {throughput:.2f} requests/second")

def main():
    parser = argparse.ArgumentParser(description="HTTP Load Testing Tool")
    parser.add_argument("url", type=str, help="URL to test")
    parser.add_argument("--max-qps", type=int, default=10, help="Maximum queries per second")
    parser.add_argument("--duration", type=int, default=30, help="Test duration in seconds")
    parser.add_argument("--workers", type=int, default=1, help="Number of concurrent workers")
    parser.add_argument("--method", type=str, default='GET', help="HTTP method to use (GET, POST, etc.)")
    
    args = parser.parse_args()

    load_tester = LoadTester(args.url, args.max_qps, args.duration, args.workers, args.method)
    load_tester.run()

if __name__ == "__main__":
    main()
