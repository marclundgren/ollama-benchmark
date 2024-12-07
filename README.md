# Ollama Benchmark Tool

This tool helps benchmark Ollama model performance across different systems.

## Setup

1. Make sure you have Python 3.8+ installed
2. Run the setup script:
   ```bash
   ./setup.sh
   ```

## Usage

1. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

2. Install the requirements

   ```bash
   pip install -r requirements.txt
   ```

3. Run the benchmark:

   ```bash
   python benchmark.py --runs 10 --output results.json --model llama2
   ```

   Options:

   - `--runs`: Number of test runs (default: 5)
   - `--output`: Output file name for results
   - `--model`: Model to benchmark (default: llama2)

4. To deactivate the virtual environment when done:
   ```bash
   deactivate
   ```

## Results

Results are saved in the `benchmark_results` directory with system information and performance metrics.
EOL
