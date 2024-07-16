# HTTP Load Testing and Benchmarking Library

## Goal:
To build an HTML load tester that measures multiple factors on a specified URL using concurrent workers.

## Language:
Python 3.9.12

## Dependencies:
requests
psutil

## Metrics:
Latency Statistics (min, max, avg, std deviation)
Error Rates
Resource Monitoring (CPU and memory usage)
Throughput

## Features:
HTTP methods (GET, POST)
Dynamic workload simulation using different queries per second (qps)

## Docker set-up:
Python: 3.9.12
Port: 8000
Command: python load_tester.py <url> [--max-qps <value>] [--duration <seconds>] [--workers <count>] [--method <http-method>]

## Testing:
./test_load_tester.sh

## Usage:
docker build -t load_tester .
python load_tester.py <url> [--max-qps <value>] [--duration <seconds>] [--workers <count>] [--method <http-method>]
