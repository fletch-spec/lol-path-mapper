import argparse
import python_modules as py

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="League of Legends replay map renderer")
    parser.add_argument("--restore", help="Restore defaults and wipe cache", action="store_true")
    args = parser.parse_args()

    system = py.System(args)
    system.start()