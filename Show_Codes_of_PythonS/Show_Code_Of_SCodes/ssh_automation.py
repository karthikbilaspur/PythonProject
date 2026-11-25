import argparse
import os

SSH_TEMPLATE = """
HOST {name}
    HostName {hostname}
    User {user}
    Port {port}
"""


def args_to_obj(args):
    return SSH_TEMPLATE.format(**vars(args))

def add_to_conf(conf: str, obj: str):
    conf = os.path.expanduser(conf)
    # Check if the host already exists in the config
    with open(conf, 'r') as f:
        if obj.strip() in f.read():
            print(f"Host '{vars(args)['name']}' already exists in the config.")
            return
    # Append the new host to the config
    with open(conf, 'a') as f:
        f.write(obj)
    print(f"Host '{vars(args)['name']}' added to the config.")


def remove_from_conf(conf: str, name: str):
    conf = os.path.expanduser(conf)
    # Read the config and remove the host
    with open(conf, 'r') as f:
        lines = f.readlines()
    with open(conf, 'w') as f:
        host_found = False
        for line in lines:
            if line.strip().startswith('HOST') and line.strip().lower() == f'host {name.lower()}':
                host_found = True
            elif host_found and line.strip().startswith('HOST'):
                host_found = False
                f.write(line)
            elif not host_found:
                f.write(line)
    if host_found:
        print(f"Host '{name}' removed from the config.")
    else:
        print(f"Host '{name}' not found in the config.")


def list_hosts(conf: str):
    conf = os.path.expanduser(conf)
    try:
        with open(conf, 'r') as f:
            hosts = [line.strip().split()[1] for line in f if line.strip().startswith('HOST')]
            print("Configured Hosts:")
            for host in hosts:
                print(host)
    except FileNotFoundError:
        print("No config file found.")


def main():
    parser = argparse.ArgumentParser(
        prog="Manages ssh hosts in the ssh config file.")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help="Add a new ssh host.")
    add_parser.add_argument('name', help="Name of the Host to add to the config.")
    add_parser.add_argument('hostname', help="Hostname/IP address of the host.")
    add_parser.add_argument('--user', default='root',
                            help="The user to connect with. Defaults to root.")
    add_parser.add_argument('--port', default=22, type=int,
                            help="The port to connect to. Defaults to 22.")
    add_parser.add_argument('--conf', default='~/.ssh/config',
                            help="The path to the ssh config file. Defaults to ~/.ssh/config.")

    remove_parser = subparsers.add_parser('remove', help="Remove an ssh host.")
    remove_parser.add_argument('name', help="Name of the Host to remove from the config.")
    remove_parser.add_argument('--conf', default='~/.ssh/config',
                              help="The path to the ssh config file. Defaults to ~/.ssh/config.")

    list_parser = subparsers.add_parser('list', help="List all ssh hosts.")
    list_parser.add_argument('--conf', default='~/.ssh/config',
                             help="The path to the ssh config file. Defaults to ~/.ssh/config.")

    args = parser.parse_args()
    if args.command == 'add':
        obj = args_to_obj(args)
        add_to_conf(args.conf, obj)
    elif args.command == 'remove':
        remove_from_conf(args.conf, args.name)
    elif args.command == 'list':
        list_hosts(args.conf)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()