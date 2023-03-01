#import oyaml as yaml
import yaml
import json
import datetime
import copy

def read_yaml(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

def write_yaml(path, content):
    with open(path, 'w') as f:
        yaml.dump(json.loads(str(content).replace("'", '"')),
                    f,
                    default_flow_style=False)
        
def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")

class PromComposer:

    compose_dir = "output"
    config_dict = {"prom_gateway" : "nano_pushgateway:9091"}
    compose_dict = {"services" : {},
                    "volumes" : {},
                    "networks" : {}}

    def __init__(self, runid = None):
         self.default_config(runid or f'run_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')

    def default_config(self, runid):
        self.config_dict.setdefault(
            "promexporter_enable",
            str2bool(self.config_dict.get("prom_enable", True)))
        
        self.config_dict.setdefault(
            "prom_gateway",
            str2bool(self.config_dict.get("prom_gateway", "nano_pushgateway:9091")))
        
        self.config_dict.setdefault("prom_runid", runid)


    def grafana_stack(self):
        promexporter_compose = read_yaml('./promexporter/docker-compose-grafana-stack.yml')
        for container in promexporter_compose["services"]:
            self.compose_dict["services"][
                container] = promexporter_compose["services"][container]
        for volume in promexporter_compose["volumes"]:
            self.compose_dict["volumes"][volume] = promexporter_compose[
                "volumes"][volume]
        
        for network in promexporter_compose["networks"]:
            self.compose_dict["networks"][network] = promexporter_compose[
                "networks"][network]
        self.write_docker_compose(f"./{self.compose_dir}/docker-compose-grafana-stack1.yml")
    
    def prom_exporters(self,nodes):    

        nano_prom_compose = read_yaml('./promexporter/docker-compose-prom-exporter.yml')
        for node in nodes:
            node_name = node.replace(":", "_")
            host_ip, node_rpc_port = node.split(":")            

            prom_gateway = self.config_dict.get("prom_gateway")
            prom_runid = self.config_dict.get("prom_runid")
            
            container = nano_prom_compose["services"]["default_exporter"]
            container_name = f'{node_name}_exporter'
            self.compose_dict["services"][container_name] = copy.deepcopy(
                container)
            self.compose_dict["services"][container_name][
                "container_name"] = container_name            

            self.compose_dict["services"][container_name]["command"] = f'--rpchost {host_ip} --rpc_port {node_rpc_port} --push_gateway {prom_gateway} --hostname {node_name} --runid {prom_runid} --interval 2'

            #This only works for dockerized nodes
            #self.compose_dict["services"][container_name]["pid"] = f'service:{node_name}'
        
        for network in nano_prom_compose["networks"]:
            self.compose_dict["networks"][network] = nano_prom_compose[
                "networks"][network]
        self.write_docker_compose(f"./{self.compose_dir}/docker-compose-prom-exporter1.yml")
    
    def write_docker_compose(self, path) -> None:
        write_yaml(path,self.compose_dict)