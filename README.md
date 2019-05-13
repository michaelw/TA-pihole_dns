# TA-pihole_dns
Splunk Add-on for the Pihole DNS server

## Sourcetype
```
pihole
```

## Where to Install
Splunk platform Instance type | Supported | Required | Actions required/ Comments
----------------------------- | --------- | -------- | --------------------------
Search Heads | Yes | Yes | Install this add-on to all search heads
Indexers | Yes | Conditional | Not required if heavy forwarders are used to collect data.
Heavy Forwarders | Yes | Conditional | Not required.

\* **This add-on must be installed on either the HF or Indexers.**

## Input Requirements
Set the sourcetype to `pihole` in the inputs.conf file on the forwarder.

i.e.

```
# Sample inputs.conf

[monitor:///var/log/pihole.log]
disabled = 0
sourcetype = pihole
```

## Pihole Logging Recommendations
Set `log-queries=extra` in the pihole dnsmasq.conf file. This is normally located in /etc/dnsmasq.d/01-pihole.conf but it may vary depending on your distribution.
