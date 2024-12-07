import time
import json
import statistics
import requests
import argparse
from pathlib import Path
import platform
import psutil
import sys

def get_system_info():
    """
    Gather system information for benchmark context
    """
    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "total_memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
        "available_memory": f"{psutil.virtual_memory().available / (1024**3):.2f} GB"
    }

def run_benchmark(prompt, num_runs=5):
    """
    Run benchmark tests for Ollama model inference
    """
    times = []
    tokens = []
    
    for i in range(num_runs):
        print(f"Running test {i+1}/{num_runs}")
        
        start_time = time.time()
        
        # Make request to Ollama API
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "qwen2.5-coder:latest",  # Change this to your model
                "prompt": prompt,
                "stream": False
            }
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            
            # Calculate metrics
            elapsed = end_time - start_time
            times.append(elapsed)
            tokens.append(len(response_text.split()))
        else:
            print(f"Error on run {i+1}: {response.status_code}")
            continue

    # Calculate statistics
    stats = {
        "average_time": statistics.mean(times),
        "std_dev_time": statistics.stdev(times) if len(times) > 1 else 0,
        "min_time": min(times),
        "max_time": max(times),
        "average_tokens": statistics.mean(tokens),
        "tokens_per_second": statistics.mean(tokens) / statistics.mean(times)
    }
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='Benchmark Ollama model performance')
    parser.add_argument('--runs', type=int, default=5, help='Number of test runs')
    parser.add_argument('--output', type=str, help='Output file for results')
    parser.add_argument('--model', type=str, default='llama2', help='Model to benchmark')
    args = parser.parse_args()

    # Test prompts of varying complexity
    prompts = [
        "What is 2+2?",  # Simple
        "Write a paragraph about machine learning.",  # Medium
        "Write a detailed analysis of the economic impacts of artificial intelligence on society.",  # Complex
    ]
    
    # Create results directory if it doesn't exist
    results_dir = Path('benchmark_results')
    results_dir.mkdir(exist_ok=True)
    
    # Get system information
    system_info = get_system_info()
    
    results = {
        "system_info": system_info,
        "model": args.model,
        "prompts": {}
    }
    
    for i, prompt in enumerate(prompts):
        print(f"\nRunning benchmark with prompt {i+1}")
        stats = run_benchmark(prompt, args.runs)
        results["prompts"][f"prompt_{i+1}"] = {
            "prompt": prompt,
            "stats": stats
        }
    
    # Print results
    print("\nBenchmark Results:")
    print(json.dumps(results, indent=2))
    
    # Save to file if specified
    if args.output:
        output_path = results_dir / args.output
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()