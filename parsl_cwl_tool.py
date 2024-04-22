"""Module to represent a command line tool for CWLApp."""

import sys

import parsl
import yaml
from parsl.configs.local_threads import config

from cwl import CWLApp

parsl.load(config)


class ParslCWLTool:
    """Class to represent a command line tool for CWLApp."""

    def __init__(self, *args):
        if not args[1].endswith(".cwl"):
            raise ValueError(f"Invalid CWL file: {args[1]}")

        self.cwl_app = CWLApp(args[1])
        self.app_future = self.run(args)

    def run(self, args: list[str]):
        cwl_inputs_outputs = {}

        if len(args) == 3 and args[2].endswith(".yml"):
            with open(args[2], "r") as f:
                cwl_inputs_outputs = yaml.safe_load(f)

        else:
            for arg in args[2:]:
                key, value = arg.split("=")
                cwl_inputs_outputs[key.lstrip("--")] = (
                    value if not (value.startswith("[") and value.endswith("]")) else eval(value)
                )

        app_future = self.cwl_app(**cwl_inputs_outputs)
        return app_future

    def result(self):
        try:
            self.app_future.result()

            if self.app_future.stdout:
                print("STDOUT:")
                with open(self.app_future.stdout, "r") as f:
                    print(f.read())

        except:
            if self.app_future.stderr:
                print("STDERR:")
                with open(self.app_future.stderr, "r") as f:
                    print(f.read())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Invalid arguments")

    args = sys.argv
    parsl_cwl_tool = ParslCWLTool(*args)
    parsl_cwl_tool.result()
