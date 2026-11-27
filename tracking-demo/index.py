"""
Safe Package Tracker - no scraping, no fake User-Agent, no ToS violation.

How it works:
- You add a package with a carrier + tracking number.
- It builds the OFFICIAL carrier tracking URL (you click it, carrier shows status).
- You log status updates yourself (or paste them from the carrier email/SMS).
- Everything is stored in packages.json locally. No Amazon, no Crunchyroll,
  no copyrighted content is copied.

Carriers supported: Amazon (via order page link), USPS, UPS, FedEx, DHL,
India Post, Delhivery, Blue Dart, DTDC, Ecom Express, + Custom.

Run:  python safe_package_tracker.py
"""
import json
import os
import webbrowser
from dataclasses import dataclass, field, asdict
from datetime import datetime

FILE = "packages.json"

CARRIERS = {
    "1": ("USPS", "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1={id}"),
    "2": ("UPS", "https://www.ups.com/track?tracknum={id}"),
    "3": ("FedEx", "https://www.fedex.com/fedextrack/?trknbr={id}"),
    "4": ("DHL", "https://www.dhl.com/en/express/tracking.html?AWB={id}"),
    "5": ("India Post", "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx"),
    "6": ("Delhivery", "https://www.delhivery.com/track/package/{id}"),
    "7": ("Blue Dart", "https://www.bluedart.com/tracking?trackingID={id}"),
    "8": ("DTDC", "https://www.dtdc.in/tracking/tracking_results.asp"),
    "9": ("Ecom Express", "https://ecomexpress.in/tracking/?awb_field={id}"),
    "10": ("Amazon Order", "https://www.amazon.in/gp/your-account/order-history"),
    "11": ("Custom / Other", "{id}"),
}

STATUSES = ["Ordered", "Shipped", "In Transit", "Out for Delivery", "Delivered", "Delayed", "Returned"]


@dataclass
class Event:
    status: str
    note: str = ""
    at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))


@dataclass
class Package:
    tracking_id: str
    carrier: str
    item_name: str
    expected_date: str = ""
    events: list[Event] = field(default_factory=list[Event])

    @property
    def current_status(self) -> str:
        return self.events[-1].status if self.events else "Ordered"

    @property
    def tracking_url(self) -> str:
        for _, (name, template) in CARRIERS.items():
            if name == self.carrier:
                return template.format(id=self.tracking_id)
        return self.tracking_id

    def days_since_order(self) -> int:
        if not self.events:
            return 0
        try:
            first = datetime.strptime(self.events[0].at, "%Y-%m-%d %H:%M")
            return (datetime.now() - first).days
        except ValueError:
            return 0


class SafeTracker:
    def __init__(self, filename: str = FILE):
        self.filename = filename
        self.packages: dict[str, Package] = self._load()

    def _load(self) -> dict[str, Package]:
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Warning: packages.json was corrupt, starting fresh.")
            return {}
        out: dict[str, Package] = {}
        for tid, p in raw.items():
            out[tid] = Package(
                tracking_id=p["tracking_id"],
                carrier=p["carrier"],
                item_name=p["item_name"],
                expected_date=p.get("expected_date", ""),
                events=[Event(**e) for e in p.get("events", [])],
            )
        return out

    def _save(self):
        data = {tid: asdict(p) for tid, p in self.packages.items()}
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_package(self):
        print("\n--- Add Package ---")
        for k, (name, _) in CARRIERS.items():
            print(f"{k}. {name}")
        choice = input("Carrier number: ").strip()
        carrier = CARRIERS.get(choice, ("Custom / Other", "{id}"))[0]
        tid = input("Tracking ID / Order ID: ").strip()
        if not tid:
            print("Tracking ID is required.")
            return
        if tid in self.packages:
            print("That tracking ID already exists.")
            return
        name = input("Item name: ").strip() or "Untitled package"
        expected = input("Expected delivery date (YYYY-MM-DD, optional): ").strip()
        pkg = Package(tracking_id=tid, carrier=carrier, item_name=name, expected_date=expected)
        pkg.events.append(Event(status="Ordered", note="Added to tracker"))
        self.packages[tid] = pkg
        self._save()
        print(f"Added: {name} [{carrier} {tid}]")

    def update_status(self):
        tid = input("Tracking ID to update: ").strip()
        pkg = self.packages.get(tid)
        if not pkg:
            print("Not found.")
            return
        print("Statuses:", ", ".join(STATUSES))
        status = input("New status: ").strip()
        if status not in STATUSES:
            print("Pick one of the listed statuses.")
            return
        note = input("Note (optional, e.g. 'Left Bengaluru hub'): ").strip()
        pkg.events.append(Event(status=status, note=note))
        self._save()
        print(f"Updated {pkg.item_name} -> {status}")

    def view_all(self):
        if not self.packages:
            print("\nNo packages yet.")
            return
        print(f"\n{'Item':<25} {'Carrier':<15} {'Status':<18} {'Days':<5} Expected")
        print("-" * 80)
        for p in self.packages.values():
            print(f"{p.item_name[:24]:<25} {p.carrier[:14]:<15} {p.current_status:<18} {p.days_since_order():<5} {p.expected_date}")
        print("\nTip: open a package's official tracking page from the detail view.")

    def view_one(self):
        tid = input("Tracking ID: ").strip()
        pkg = self.packages.get(tid)
        if not pkg:
            print("Not found.")
            return
        print(f"\n{pkg.item_name}")
        print(f"Carrier: {pkg.carrier} | ID: {pkg.tracking_id}")
        print(f"Current: {pkg.current_status} | Expected: {pkg.expected_date or '—'}")
        print(f"Official tracking link: {pkg.tracking_url}")
        print("\nTimeline:")
        for e in pkg.events:
            print(f"  {e.at} - {e.status}" + (f" - {e.note}" if e.note else ""))
        if input("\nOpen official tracking page in browser? (y/n): ").lower() == "y":
            webbrowser.open(pkg.tracking_url)

    def delete_package(self):
        tid = input("Tracking ID to delete: ").strip()
        if tid in self.packages:
            del self.packages[tid]
            self._save()
            print("Deleted.")
        else:
            print("Not found.")

    def summary(self):
        total = len(self.packages)
        delivered = sum(1 for p in self.packages.values() if p.current_status == "Delivered")
        in_transit = sum(1 for p in self.packages.values() if p.current_status in ("Shipped", "In Transit", "Out for Delivery"))
        print(f"\nTotal: {total} | Delivered: {delivered} | In transit: {in_transit} | Other: {total - delivered - in_transit}")


def main():
    tracker = SafeTracker()
    while True:
        print("\n=== Safe Package Tracker ===")
        print("1. Add package")
        print("2. Update status")
        print("3. View all packages")
        print("4. View one package + open carrier page")
        print("5. Delete package")
        print("6. Summary")
        print("7. Quit")
        choice = input("Choice: ").strip()
        if choice == "1":
            tracker.add_package()
        elif choice == "2":
            tracker.update_status()
        elif choice == "3":
            tracker.view_all()
        elif choice == "4":
            tracker.view_one()
        elif choice == "5":
            tracker.delete_package()
        elif choice == "6":
            tracker.summary()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
