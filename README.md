# TA-pihole_dns
Splunk Add-on for the Pihole DNS server

```
Version: 1.2.1
```

## Sourcetype
```
pihole
```

## Where to Install
Splunk platform Instance type | Supported | Required | Actions required/ Comments
----------------------------- | --------- | -------- | --------------------------
Search Heads | Yes | Yes | Install this add-on to all search heads
Indexers | Yes | Conditional | Not required if heavy forwarders are used to collect data.
Heavy Forwarders | Yes | Conditional | Only needed if data first passes through a HF before the indexer tier.


## Input Requirements
Set the sourcetype to `pihole` in the inputs.conf file on the forwarder.

i.e.

```
# Sample inputs.conf

[monitor:///var/log/pihole.log]
disabled = 0
sourcetype = pihole
```

## Pihole Logging Requirements
Set `log-queries=extra` in the pihole dnsmasq.conf file. Pi-hole recommends to make any changes to a new configuration file to avoid changes to be overridden during an update.
