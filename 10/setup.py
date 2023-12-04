from setuptools import setup, Extension


def main():
    setup(name="cjson",
          ext_modules=[
              Extension('cjson', ['cjson.c'])]
          )


if __name__ == "__main__":
    main()
