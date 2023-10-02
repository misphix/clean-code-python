from sys import argv

from args.args import Args

if __name__ == "__main__":
    arg = Args("l", argv[1:])
    logging = arg.get_boolean("l")
    print(f"logging: {logging}")
