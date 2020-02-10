from os.path import dirname, abspath, join

this_dir = dirname(abspath(__file__))
stuff_dir = join(this_dir, "stuff")


def get_sample(path):
    with open(join(stuff_dir, path), "r") as f:
        return f.read()
