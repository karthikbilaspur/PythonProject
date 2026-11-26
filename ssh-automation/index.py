import argparse, os, re
SSH_TEMPLATE="\nHost {name}\n    HostName {hostname}\n    User {user}\n    Port {port}\n"
HOST_RE=re.compile(r"^\s*Host\s+(.+)$", re.IGNORECASE)
def _resolve(conf: str) -> str:
    p=os.path.expanduser(conf); os.makedirs(os.path.dirname(p) or ".", exist_ok=True); return p
def _blocks(path: str) -> list[list[str]]:
    if not os.path.exists(path): return []
    lines=open(path,encoding="utf-8",errors="ignore").readlines()
    blocks: list[list[str]] = []
    cur: list[str] = []
    for ln in lines:
        if HOST_RE.match(ln) and cur: blocks.append(cur); cur=[ln]
        else: cur.append(ln)
    if cur: blocks.append(cur)
    return blocks
def _names(b: list[str]) -> list[str]:
    n: list[str] = []
    for ln in b:
        m=HOST_RE.match(ln)
        if m: n.extend(m.group(1).split())
    return n
def add_to_conf(conf: str, name: str, hostname: str, user: str = "root", port: int = 22) -> None:
    path=_resolve(conf)
    for b in _blocks(path):
        if name.lower() in [x.lower() for x in _names(b)]: print(f"Host '{name}' already exists. Skipping."); return
    open(path,"a",encoding="utf-8").write(SSH_TEMPLATE.format(name=name,hostname=hostname,user=user,port=port))
    print(f"Host '{name}' added to {conf}.")
def remove_from_conf(conf: str, name: str) -> None:
    path=_resolve(conf)
    if not os.path.exists(path): print("No config file found."); return
    blocks=_blocks(path); kept=[b for b in blocks if name.lower() not in [x.lower() for x in _names(b)]]
    if len(kept)==len(blocks): print(f"Host '{name}' not found."); return
    with open(path,"w",encoding="utf-8") as f:
        for b in kept: f.writelines(b)
    print(f"Host '{name}' removed.")
def list_hosts(conf: str) -> None:
    path=os.path.expanduser(conf)
    if not os.path.exists(path): print("No config file found."); return
    found: list[str] = []
    for b in _blocks(path): found.extend(_names(b))
    print("Configured Hosts:" if found else "No hosts configured.")
    for h in found: print(f"  {h}")
def main():
    p=argparse.ArgumentParser(prog="ssh-automation",description="Manage SSH hosts in ~/.ssh/config")
    sub=p.add_subparsers(dest="command",required=True)
    a=sub.add_parser("add"); a.add_argument("name"); a.add_argument("hostname"); a.add_argument("--user",default="root"); a.add_argument("--port",default=22,type=int); a.add_argument("--conf",default="~/.ssh/config")
    r=sub.add_parser("remove"); r.add_argument("name"); r.add_argument("--conf",default="~/.ssh/config")
    l=sub.add_parser("list"); l.add_argument("--conf",default="~/.ssh/config")
    args=p.parse_args()
    if args.command=="add": add_to_conf(args.conf,args.name,args.hostname,args.user,args.port)
    elif args.command=="remove": remove_from_conf(args.conf,args.name)
    else: list_hosts(args.conf)
if __name__=="__main__": main()
