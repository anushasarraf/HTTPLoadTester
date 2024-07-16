#!/bin/sh

# Ensure load_tester.py is executable
chmod +x load_tester.py

# Execute the load tester script with provided arguments
python load_tester.py "$@"
