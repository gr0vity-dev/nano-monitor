# nano-monitor

Simple python wrapper around [pwojcik/nano-prom-exporter](https://github.com/pwojcikdev/nano-prom-exporter) to<br>
monitor all the stats of your [nano-node](https://github.com/nanocurrency/nano-node) with a few simple commands

Based on [pwojcikdev/nano-prom-grafana-stack](https://github.com/pwojcikdev/nano-prom-grafana-stack)

## How to use ?

- Setup and start grafana dashboard, prometheus and the pushgateway <br>
`./monitor setup` 

- Start monitoring one or more nano-nodes. The RPC port must be accessible<br>
`./monitor start --node host:rpc_port_1 -- node host:rpc_port_2`

- Stop monitoring <br>
`./monitor stop` #Stops all prom-exporters <br>
`./monitor stop --node host:rpc_port_1` #Only stops monitoring for specific nodes

- Stop & Remove all containers (including grafana stack)<br>
`./monior down`

