import ruamel
import ruamel.yaml
import fire
from functools import reduce

available_kinds = ["Deployment", "DaemonSet"]


class WorkloadConvertorCmd(object):
    def validate_available_kind(self, kind=""):
        if kind in available_kinds:
            return True
        return False

    def convert(self, from_file="", from_kind="", to_kind="", to_file=""):
        if not self.validate_available_kind(
            from_kind
        ) or not self.validate_available_kind(to_kind):
            print(f"Error: from_kind and to_kind can be in {available_kinds}")
            exit(9)

        if from_file == "" or to_file == "":
            print("Error: from_file or to_file is not defined")
            exit(9)

        w = WorkloadConvertor()
        w.load(from_file)

        if from_kind == "Deployment" and to_kind == "DaemonSet":
            w.convert_deployment_to_daemonset()
        else:
            print(f"Error: Convert from {from_kind} to {to_kind} is not available")
            exit(1)

        w.save(to_file)


class WorkloadConvertor(object):
    inputData = {}
    outputData = {}
    yaml = ruamel.yaml.YAML()

    def load(self, filename):
        with open(filename) as stream:
            self.inputData = self.yaml.load(stream)

    def save(self, filename):
        with open(filename, "w") as stream:
            self.yaml.dump(self.outputData, stream=stream)

    def convert_matadata(self):
        self.outputData["metadata"] = {}
        self.outputData["metadata"]["annotations"] = self.inputData["metadata"][
            "annotations"
        ]
        self.outputData["metadata"]["labels"] = self.inputData["metadata"]["labels"]
        self.outputData["metadata"]["name"] = self.inputData["metadata"]["name"]
        self.outputData["metadata"]["namespace"] = self.inputData["metadata"][
            "namespace"
        ]

    def convert_podSpec(self):
        self.outputData["spec"] = {}
        self.outputData["spec"]["selector"] = self.inputData["spec"]["selector"]
        self.outputData["spec"]["template"] = self.inputData["spec"]["template"]

    def remove_creationTimestamp(self):
        if dict_get(self.outputData, "metadata.creationTimestamp"):
            del self.outputData["metadata"]["creationTimestamp"]

        if dict_get(self.outputData, "spec.template.metadata.creationTimestamp"):
            del self.outputData["spec"]["template"]["metadata"]["creationTimestamp"]

    def convert_deployment_to_daemonset(self):
        deploy = self.inputData
        ds = self.outputData

        # DaemonSet Kind
        ds["apiVersion"] = "apps/v1"
        ds["kind"] = "DaemonSet"

        # metadata & podSpec
        self.convert_matadata()
        self.convert_podSpec()

        # DaemonSet Strategy
        if dict_get(deploy, "spec.updateStrategy.type") == "RollingUpdate":
            ds["spec"]["updateStrategy"] = {}
            ds["spec"]["updateStrategy"]["type"] = deploy["spec"]["strategy"]["type"]
            ds["spec"]["updateStrategy"]["rollingUpdate"] = {}
            ds["spec"]["updateStrategy"]["rollingUpdate"]["maxUnavailable"] = deploy[
                "spec"
            ]["strategy"]["rollingUpdate"]["maxUnavailable"]

        if dict_get(deploy, "spec.minReadySeconds"):
            ds["spec"]["minReadySeconds"] = deploy["spec"]["minReadySeconds"]

        # fixup
        self.remove_creationTimestamp()


def dict_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


if __name__ == "__main__":
    fire.Fire(WorkloadConvertorCmd)
