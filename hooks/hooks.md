# Hooks

This is the location for cpenv module event hooks. Hooks are simple python modules are executed before and after an event occurs in cpenv. Each python module should include a run method that accepts 1 argument module

## Available Hooks

|       hook       |                                                               description                                                                |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| pre_activate.py  | Executed before a module is activated. This is the best place to perform additional setup like copying files or executing shell scripts. |
| post_activate.py | Executed after a module is activated.                                                                                                    |
| pre_remove.py    | Executed before a module is removed from a local repo.                                                                                   |
| post_remove.py   | Executed after a module is removed from a local repo.                                                                                    |

## Example Hook

pre_activate.py

```
def run(module):
    print(f'Hello from {module.name}/hooks/pre_activate.py')
```
