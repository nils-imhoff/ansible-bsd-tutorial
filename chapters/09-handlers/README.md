# Exercise 10 - Handlers in Action

Extend your playbook with handlers to restart services when configuration changes.

## Details

In this exercise, you'll learn about Ansible handlers - special tasks that only run when notified by other tasks. This is particularly useful for restarting services after configuration changes.

## Preparation

For these exercises, you work from the main directory of the repository.

You'll extend the previous exercise by adding configuration file management and handlers.

## Tasks

### Task 1: Create nginx configuration templates

Create different nginx configuration templates for each BSD variant that include:
- Different document roots
- Basic security settings
- Custom error pages

### Task 2: Add handler tasks

Create handlers that restart nginx when configuration files change.

### Task 3: Add configuration deployment

Deploy the nginx configuration files and notify handlers when they change.

### Task 4: Test handler functionality

Modify the configuration and run the playbook to see handlers in action.

## Key Concepts

- **Handlers**: Special tasks that run only when notified
- **notify**: Keyword used to trigger handlers
- **changed_when**: Control when a task reports changes
- **Template**: Use Jinja2 templates for dynamic configuration

## Execution

```bash
# First run - should trigger handlers
ansible-playbook exercises/10-handlers/webserver-handlers.yml

# Second run - should not trigger handlers (no changes)
ansible-playbook exercises/10-handlers/webserver-handlers.yml

# Modify a template and run again - should trigger handlers
ansible-playbook exercises/10-handlers/webserver-handlers.yml
```

## Expected Result

- Configuration files deployed to each BSD system
- Services restarted only when configuration changes
- No unnecessary service restarts on subsequent runs

## Learning Objectives

- Understand when and why to use handlers
- Learn the notify mechanism
- Practice with Jinja2 templates
- Manage configuration files across different systems
