#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
Ansible custom module for managing BSD services
Author: Nils Imhoff
Description: A custom module to start, stop, restart, and check status of BSD services
"""

from ansible.module_utils.basic import AnsibleModule
import subprocess
import os


def run_command(module, command):
    """Execute a shell command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return {
            'rc': result.returncode,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip()
        }
    except subprocess.CalledProcessError as e:
        module.fail_json(
            msg=f"Command failed: {command}",
            rc=e.returncode,
            stdout=e.stdout,
            stderr=e.stderr
        )


def get_service_status(module, service_name):
    """Check if a service is running"""
    # Check if service exists
    exists_cmd = f"rcctl ls all | grep -q '^{service_name}$'"
    exists_result = run_command(module, exists_cmd)
    service_exists = exists_result['rc'] == 0
    
    if not service_exists:
        return {
            'exists': False,
            'enabled': False,
            'running': False,
            'status_output': f"Service {service_name} does not exist"
        }
    
    # Check if service is enabled
    enabled_cmd = f"rcctl ls on | grep -q '^{service_name}$'"
    enabled_result = run_command(module, enabled_cmd)
    enabled = enabled_result['rc'] == 0
    
    # Check if service is running
    status_cmd = f"rcctl check {service_name}"
    status_result = run_command(module, status_cmd)
    running = status_result['rc'] == 0
    
    return {
        'exists': True,
        'enabled': enabled,
        'running': running,
        'status_output': status_result['stdout']
    }


def main():
    """Main function"""
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', choices=['started', 'stopped', 'restarted', 'enabled', 'disabled'], required=True),
            enabled=dict(type='bool', default=None)
        ),
        supports_check_mode=True
    )
    
    service_name = module.params['name']
    state = module.params['state']
    enabled = module.params['enabled']
    
    # Get current status
    current_status = get_service_status(module, service_name)
    
    changed = False
    result = {
        'name': service_name,
        'state': state,
        'changed': changed,
        'current_status': current_status
    }
    
    # Determine what actions to take
    if state == 'started':
        if not current_status['running']:
            if not module.check_mode:
                run_command(module, f"rcctl start {service_name}")
            changed = True
            result['msg'] = f"Service {service_name} started"
        else:
            result['msg'] = f"Service {service_name} is already running"
    
    elif state == 'stopped':
        if current_status['running']:
            if not module.check_mode:
                run_command(module, f"rcctl stop {service_name}")
            changed = True
            result['msg'] = f"Service {service_name} stopped"
        else:
            result['msg'] = f"Service {service_name} is already stopped"
    
    elif state == 'restarted':
        if not module.check_mode:
            run_command(module, f"rcctl restart {service_name}")
        changed = True
        result['msg'] = f"Service {service_name} restarted"
    
    elif state == 'enabled':
        if not current_status['enabled']:
            if not module.check_mode:
                run_command(module, f"rcctl enable {service_name}")
            changed = True
            result['msg'] = f"Service {service_name} enabled"
        else:
            result['msg'] = f"Service {service_name} is already enabled"
    
    elif state == 'disabled':
        if current_status['enabled']:
            if not module.check_mode:
                run_command(module, f"rcctl disable {service_name}")
            changed = True
            result['msg'] = f"Service {service_name} disabled"
        else:
            result['msg'] = f"Service {service_name} is already disabled"
    
    # Handle enabled parameter
    if enabled is not None:
        if enabled and not current_status['enabled']:
            if not module.check_mode:
                run_command(module, f"rcctl enable {service_name}")
            changed = True
            result['msg'] = f"Service {service_name} enabled"
        elif not enabled and current_status['enabled']:
            if not module.check_mode:
                run_command(module, f"rcctl disable {service_name}")
            changed = True
            result['msg'] = f"Service {service_name} disabled"
    
    result['changed'] = changed
    
    # Get final status
    final_status = get_service_status(module, service_name)
    result['final_status'] = final_status
    
    module.exit_json(**result)


if __name__ == '__main__':
    main()
