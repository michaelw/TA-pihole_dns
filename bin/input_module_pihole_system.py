# encoding = utf-8

import os
import sys
import time
import datetime
import json
import pihole_constants as const


def validate_input(helper, definition):
    # Simple validation
    pihole_host = definition.parameters.get('pihole_host')

    if len(pihole_host) == 0:
        raise ValueError('Pi-hole host cannot be empty.')
    else:
        pass


def collect_events(helper, ew):
    # Get Log Level
    log_level = helper.get_log_level()
    helper.set_log_level(log_level)
    helper.log_info(f'log_level="{log_level}"')

    # Get Pi-hole host
    pihole_host = helper.get_arg('pihole_host')

    # Get Interval
    interval = int(helper.get_arg('interval'))

    # Get Checkpoint
    key = 'pihole_api'
    current_time = int(time.time())
    check_time = current_time - interval

    if helper.get_check_point(key):
        old_state = int(helper.get_check_point(key)['checkpoint'])
        helper.log_info('msg="Checkpoint found"')
        helper.log_debug(
            f'msg="Checkpoint information", checkpoint="{old_state}", interval="{interval}"')

        if check_time < old_state:
            helper.log_info(
                'msg="Skipping because interval is too close to previous run", action="stopped"')
            sys.exit(0)
        else:
            helper.log_info('msg="Running scheduled Interval"')

    else:
        helper.log_info('msg="Checkpoint file not found"')

    new_state = {'checkpoint': f'{current_time}'}

    # Get Proxy
    proxy = helper.get_proxy()

    if proxy:
        if proxy["proxy_username"]:
            helper.log_info('msg="Proxy is configured with authenticaiton"')
            helper.log_debug(
                f'proxy_type="{proxy["proxy_type"]}", proxy_url="{proxy["proxy_url"]}", proxy_port="{proxy["proxy_port"]}", proxy_username="{proxy["proxy_username"]}"')
        else:
            helper.log_info('msg="Proxy is configured with no authentication"')
            helper.log_debug(
                f'proxy_type="{proxy["proxy_type"]}", proxy_url="{proxy["proxy_url"]}", proxy_port="{proxy["proxy_port"]}"')

    # URL
    url = f'http://{pihole_host}/{const.api_system}'
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json'
    }

    # Make Call
    try:
        helper.log_info('msg="starting request"')
        r = helper.send_http_request(
            url, 'get', headers=headers, use_proxy=True)
    except Exception as e:
        helper.log_error(
            'error_msg="Unable to complete request", action="failed"')
        helper.log_debug(f'error_msg="{e}"')
        sys.exit(1)

    if r.status_code == 200:
        helper.log_info('msg="request completed", action="success"')
        response = r.json()
        event = {}
        event['status'] = response['status']
        event['privacy_level'] = response['privacy_level']
        event['domains_on_blocklist'] = response['domains_being_blocked']
        event['gravity_updated'] = response['gravity_last_updated']['absolute']

        # Create Splunk Event
        splunk_event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(
        ), sourcetype=helper.get_sourcetype(), data=json.dumps(event))
        ew.write_event(splunk_event)

        # Checkpointer
        helper.save_check_point(key, new_state)
        helper.log_info(
            f'msg="Updating Checkpoint", checkpoint="{new_state["checkpoint"]}"')
    else:
        helper.log_error(
            'error_msg="Unable to retrieve information", action="failed"')
        helper.log_debug(f'status_code="{r.status_code}"')
        sys.exit(1)
