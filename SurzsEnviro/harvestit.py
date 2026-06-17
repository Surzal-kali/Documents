import subprocess
import sys

def harvester_scan(domain:str, output_file:str, search_engine:str="all", args:str=""):
    command = [
        "theHarvester",
        "-d", domain,
        "-b", search_engine,
        "-f", output_file
    ]
    if args:
        command.extend(args.split())
    try: # handle potential errors when running the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Scan completed successfully. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running harvester: {e.stderr}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python harvestit.py <domain> <output_file> [search_engine] [additional_args]")
        sys.exit(1)
    
    domain = sys.argv[1]
    output_file = sys.argv[2]
    search_engine = sys.argv[3] if len(sys.argv) > 3 else "all"
    additional_args = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
    
    harvester_scan(domain, output_file, search_engine, additional_args)