import sys

def main():
    if len(sys.argv) > 1:
        name = sys.argv[1]
        print(f"Hello, {name} from obritabot!")
    else:
        print("Hello from obritabot!")


if __name__ == "__main__":
    main()
