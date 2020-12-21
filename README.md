# TA-pihole_dns - Add-on for Pi-hole DNS Server

![GitHub](https://img.shields.io/github/license/zachchristensen28/TA-pihole_dns)

Info | Description
------|----------
Version | 1.2.7 - See on [Splunkbase](https://splunkbase.splunk.com/app/4505/)
Vendor Product Version | [Pi-hole v5.2.x](https://pi-hole.net/)
Add-on has a web UI | Yes, this Add-on contains a configuration page for the Modular Input.

The TA-pihole_dns Add-on allows Splunk data administrators to map the Pi-Hole DNS events to the [CIM](https://docs.splunk.com/Splexicon:CommonInformationModel) enabling the data to be used with other Splunk Apps, such as Enterprise Security.

## Release Notes

```TEXT
Version 1.2.7

New:
- Added Modular Input for pulling select data from the HTTP API.
```

## Navigation

- [Pihole Logging Requirements](#pihole-logging-requirements)
- [Where to Install](#where-to-install)
- [Input Requirements](#input-requirements)
- [Modular Input Setup](#setup-modular-input)
- [Sourcetypes](#sourcetypes)
- [Installation Walkthrough](#installation-walkthrough)

## Pihole Logging Requirements

\* ***Failing to perform the following will cause this add-on to not extract fields properly***

Set `log-queries=extra` in the pihole dnsmasq configuration file. Pi-hole recommends to make any changes to a new configuration file to avoid changes to be overridden during an update.

1. Create a new file: `/etc/dnsmasq.d/02-pihole-splunk.conf`.
1. Add `log-queries=extra` to the file. save and close the file
1. Restart pi-hole with `pihole restartdns`

## Where to Install

Splunk platform Instance type | Supported | Required | Actions required/ Comments
----------------------------- | --------- | -------- | --------------------------
Search Heads | Yes | Yes | Install this add-on to all search heads.
Indexers | Yes | Conditional | Not required if heavy forwarders are used to collect data. Required if using Universal or Light Forwarders.
Heavy Forwarders | Yes | Conditional | Required, if HFs are used to collect this data source.
Universal Forwarders | Yes | Not required | The add-on includes an inputs.conf that is disabled by default. This can be used to create an input on the forwarder if enabled.

\* For more information, see Splunk's [documentation](https://docs.splunk.com/Documentation/AddOns/released/Overview/Installingadd-ons) on installing Add-ons.

## Input Requirements

Set the sourcetype to `pihole` in the inputs.conf file on the forwarder.

\* ***See [Installation Walkthrough](#Installation-Walkthrough) for more information***

## Setup Modular Input

This modular input interacts with the Pi-hole server's http API. This is currently an unsupported method, however, pi-hole has stated that they have plans to build out the API in the upcoming releases.

1. Open the Pi-hole Add-on in Splunk Web and click "Create New Input"
2. Fill out the following information:
    - Unique name
    - Interval in seconds to run on (default 1 hour)
    - Select the appropriate index
    - Enter the IP or FQDN of the Pi-hole server
3. Click add to Save

Search for your data in the index you selected with the sourcetype of `pihole:system`.

### Troubleshooting

If data does not appear within a few moments, there may be a connection issue. Perform the following to begin troubleshooting:

1. Enable `DEBUG` logging. Navigate to the configuration page and click the "Logging" Tab. Change Log Level to `DEBUG`.
2. search the internal index with the sourcetype of `tapiholedns:log` for issues.

```TEXT
index=_internal sourcetype=tapiholedns:log
```

## Sourcetypes

Below are a list of sourcetypes which this Add-on uses. The `pihole:dhcp` sourcetype will automatically be transformed when the `pihole` sourcetype is set in the inputs configuration.

Source type | Description | CIM Data Models
----------- | ----------- | ---------------
`pihole` | Pi-hole DNS events | [Network Resolution](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkResolutionDNS)
`pihole:dhcp` | Pi-hole DHCP events | [Network Sessions](https://docs.splunk.com/Documentation/CIM/latest/User/NetworkSessions)
`pihole:ftl` | Pi-hole FTL events | None
`pihole:system` | Pi-hole API data | None

## Installation Walkthrough

### Splunk Universal Forwarder Configuration

Download the latest [Splunk Universal Forwarder (UF)](https://www.splunk.com/en_us/download/universal-forwarder.html) appropriate for your server. _This UF should be installed on the same server as the Pi-Hole server_.

Install the UF according to [Splunk Docs](https://docs.splunk.com/Documentation/Forwarder/latest/Forwarder/Installtheuniversalforwardersoftware).

Once installed the configurations can be made. The following is a sample inputs.conf that can be pushed using a deployment server or configured on the UF itself.

```SHELL
# inputs.conf
[monitor:///var/log/pihole.log]
disabled = 0
sourcetype = pihole
# optionally specify an index, if configured.
#index = dns

[monitor:///var/log/pihole-FTL.log]
disabled = 0
sourcetype = pihole:ftl
# optionally specify an index, if configured.
#index = dns
```

Push the configuration to the forwarder, if using a deployment server, or restart the UF if configuring on the UF itself.

## Bugs/Feature Requests

Please open an issue or submit feature requests at [github.com](https://github.com/ZachChristensen28/TA-pihole_dns)
