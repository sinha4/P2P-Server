# Technical Documentation: Core P2P Decentralized File Sharing Network

## 1. Project Abstract
Before the integration of the Synchronized Watch Party module, the baseline software functioned as a fully decentralized, peer-to-peer (P2P) file distribution network. Engineered in Go (Golang), the system eschews the traditional centralized client-server architecture in favor of a distributed mesh protocol where all connected "Localhost" nodes act simultaneously as both clients and servers (uploaders and seeders).

## 2. Core Architecture & Modules

### 2.1 File Chunking & Cryptographic Integrity
To ensure optimal network bandwidth utilization and resilience against data corruption, files are never transmitted in their entirety. 
- **File Slicing**: Upon upload, the backend `file/chunking.go` algorithm slices the payload into immutable 1MB fragments.
- **SHA-256 Hashing**: Each chunk is independently passed through a cryptographic SHA-256 hashing function. The resulting hash acts as a unique signature, ensuring that any intercepted or corrupted data during P2P transit is immediately flagged and discarded by the downloading peer.

### 2.2 Decentralized Transport Layer
The network communication relies on an abstract `Transport` interface mapped over standard HTTP sockets.
- The `http_transport.go` daemon facilitates the transmission of raw byte payloads (file chunks) across the nodes.
- Because it operates strictly on stateless HTTP 200/206 protocol paradigms, it cleanly manages network drops and concurrent requests without the overhead of maintaining prolonged TCP streams for standard file transfers.

### 2.3 Concurrent Downloading Engine (Swarm Fetching)
The crux of the data retrieval mechanism—found in `peer/downloader.go`—mimics BitTorrent swarm logic:
- **Goroutine Parallelism**: When a viewer initiates a file retrieval, the Downloader spins up mathematical Goroutines proportional to the available network nodes.
- **Round-Robin Chunk Selection**: The algorithm analyzes identical files hosted across Peer A, Peer B, etc., and requests `Chunk 0` from Peer A while simultaneously requesting `Chunk 1` from Peer B. This drastically accelerates retrieval speeds as network saturation is divided horizontally across the mesh.

### 2.4 User Authentication & Security
To prevent unauthorized network intrusion, a dedicated `auth.go` module gates access to the P2P swarm.
- **Bcrypt Encryption**: All local user credentials are encrypted via Bcrypt hashing algorithms before database storage.
- **Network-Level Passwords**: A unified `--network-password` argument ensures that rogue nodes cannot forcefully inject themselves into the private localhost swarm during bootstrapping.
- **Session Tokens**: Active UI access requires valid authentication cookies mapping to the `SessionManager` struct.

### 2.5 Hacker Terminal User Interface (UI)
The frontend application was specifically engineered to emulate a high-tech "Matrix" aesthetic. 
The CSS securely incorporates monospace terminal fonts, glowing green accents, glassmorphic suppression, and strict zero-clutter dashboarding designed explicitly to visualize network data natively on the `home.html`, `upload.html`, and `download.html` pages.
