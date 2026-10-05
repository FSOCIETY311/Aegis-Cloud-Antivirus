# 🛡️ Aegis Cloud Antivirus v2.5

An advanced, lightweight **Cloud-Assisted Antivirus Engine** developed as a cybersecurity research project. Built with Python and integrated with global Threat Intelligence feeds, it delivers real-time malware detection and secure file containment without high system resource overhead.

## 🚀 Key Features

* **Cloud-Assisted Detection:** Dynamically queries the **MalwareBazaar (abuse.ch)** API to fetch the latest 1,000 active malware signatures discovered globally within the last 24 hours.
* **Hybrid Database Architecture:** Features a local fallback signature database to maintain protection even in offline or air-gapped environments.
* **Cryptographic File Auditing:** Instantly calculates unique **MD5 file hashes** to verify system integrity against known malicious payloads.
* **Automated Quarantine Subsystem:** Safely isolates flagged files by revoking execution permissions, appending a `.locked` extension, and moving objects to a secure directory (`C:\Antivirus_Quarantine`).
* **Sleek Modern GUI:** Built entirely using native Python GUI libraries, eliminating external terminal reliance and ensuring compatibility across modern desktop systems.

## 🔬 Research & Empirical Testing

During the development phase, the detection engine was strictly tested under secure conditions using simulated and real-world targets:
1. **Mock Malware Deployment:** Verified signature parsing and hashing speed using standardized text payloads (`EICAR` strings).
2. **Threat Intelligence Simulation:** Successfully mapped, detected, and quarantined a suspicious game installation package (`setup.exe`) sourced via qBittorrent, cross-verifying its signature against **VirusTotal** telemetry data.

*Note: All tests were handled without execution to ensure 100% security of the host environment.*

## 💻 Tech Stack
* **Language:** Python 3.x
* **Core Libraries:** `hashlib`, `shutil`, `urllib.request`, `threading`
* **User Interface:** `tkinter`
