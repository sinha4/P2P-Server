# Technical Documentation: Synchronized Watch Party via P2P

## 1. Feature Abstract
The overarching goal of the **Synchronized Watch Party** module is to evolve the application from a standardized File Storage system into a dynamic, real-time collaboration environment. Rather than requiring users to wait for a full file payload download before media playback, this feature permits an Uploader (Host) to concurrently broadcast video playback events to all participating P2P nodes while directly proxying the underlying MP4 file byte-range streams across the network.

## 2. Core Methodologies
This feature leverages three principal web methodologies integrated cohesively over the Go backend:
*   **WebSockets (Gorilla Websocket)**: Maintains an active, full-duplex TCP pipeline between the server and the frontend client for pushing zero-latency event payloads (Start/End Stream triggers).
*   **P2P HTTP Event Routing**: The backend acts as an intermediary broadcast hub, passing physical host triggers sequentially across the known node network.
*   **Native HTTP 206 Partial Content (Range Streams)**: The `video_server.go` mechanism securely reassembles binary chunks from active memory block stores and pipes them securely to the frontend HTML5 `<video>` player, thus mitigating extensive disk swapping.

## 3. Implementation Workflow

### Step 1: Initializing the Session
When the Uploader (Host) selects the "Watch Party" action on a viable `.mp4` module, the frontend UI sends an upstream WebSocket packet encompassing the file UUID/Hash and a localized `host_url`.

### Step 2: Network Broadcast & Synchronization
The Host's local Go daemon parses the WebSocket payload and invokes physical HTTP POST broadcasts to all neighboring Localhosts configured inside the `registry.go` instance tracker.

```go
BroadcastP2PStreamEvent(event StreamEvent, selfAddr string)
```
Simultaneously, the receiving Remote Daemons bounce this payload downward to their active Viewer frontend contexts.

### Step 3: Uninterrupted Media Pipeline
Receiving the synchronous WebSocket payload dynamically initializes a hidden DOM Modal (`#videoModal`) atop the executing Viewer screens. The inner HTML5 `<video>` source is strictly mapped to dynamically request bytes from the Host's `/api/stream/video?name=` endpoint. 
Owing to Go's `http.ServeContent` native functionality, byte constraints and dynamic scrubbing queries (HTTP 206) are seamlessly honored in standard O(1) processing paradigms.

### Step 4: Stream Authority & Termination
Only the initial Host node retains DOM accessibility to the **"End Watch Party"** UI subcomponent. Triggering termination cascades an upstream `action: end` WebSocket packet that forcibly halts playback and aggressively closes the viewing modals of all active nodes across the mesh network.
