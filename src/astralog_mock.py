import os
import sys
import time
import argparse
import json

class AstraLogHPC:
    """
    Mock Engine for AstraLog-HPC (Standard Track).
    Simulates semantic analysis of telemetry data.
    """
    def __init__(self, rules_path, input_path, output_dir):
        self.rules_path = rules_path
        self.input_path = input_path
        self.output_dir = output_dir
        self.is_initialized = False

    def initialize(self):
        print(f"[*] Initializing engine with rules: {self.rules_path}")
        if not os.path.exists(self.rules_path):
            raise FileNotFoundError(f"Rules file not found at {self.rules_path}")
        
        time.sleep(0.5)
        self.is_initialized = True
        return True

    def run_analysis(self):
        if not self.is_initialized:
            print("[!] Error: Engine not initialized")
            return False

        print(f"[*] Starting semantic analysis on: {self.input_path}")
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input telemetry file not found at {self.input_path}")

        print("[*] Processing timestamps...")
        time.sleep(1.5)

        os.makedirs(self.output_dir, exist_ok=True)

        valid_path = os.path.join(self.output_dir, "valid_data.csv")
        alarms_path = os.path.join(self.output_dir, "alarms.log")

        try:
            with open(valid_path, "w") as f:
                f.write("2025-11-15T12:00:00Z;NOMINAL;TEMP-01:25.5|PRES-01:101.3|VOLT-MAIN:24.1\n")
            
            with open(alarms_path, "w") as f:
                f.write("2025-11-15T12:00:05Z;R1;MEDIUM;TEMP-01;51.2\n")
                f.write("2025-11-15T12:00:05Z;R4;HIGH;TEMP-01,PRES-01;51.2,98.0\n")
            
            print(f"[+] Analysis successful. Results saved to {self.output_dir}")
            return True
        except Exception as e:
            print(f"[!] Critical I/O Error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="AstraLog-HPC Mock Semantic Analyzer")
    
    parser.add_argument("--rules", required=True, help="Path to rules.json")
    parser.add_argument("--input", required=True, help="Path to telemetry_cleaned.csv")
    parser.add_argument("--output", required=True, help="Directory to save logs")
    
    args = parser.parse_args()

    print("--- AstraLog-HPC | Mission Control Mock ---")
    
    try:
        engine = AstraLogHPC(args.rules, args.input, args.output)
        
        if engine.initialize():
            if engine.run_analysis():
                print("--- Process Finished Successfully ---")
                sys.exit(0)
            else:
                print("--- Process Failed during Analysis ---")
                sys.exit(1)
                
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()