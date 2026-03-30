# Watch Party P2P Architecture

Here are two versions of the Watch Party architecture diagram.
You can copy the Mermaid code block into any Markdown viewer or Notion, or you can use the Plain Text version anywhere.

## 1. Mermaid Diagram (Colorful)

```mermaid
sequenceDiagram
    autonumber
    
    %% Define Hacker Colors
    classDef host fill:#008F11,stroke:#00FF41,stroke-width:2px,color:#fff
    classDef network fill:#1A1A1A,stroke:#5D7B3D,stroke-width:2px,color:#00FF41
    classDef viewer fill:#052B33,stroke:#00FFCC,stroke-width:2px,color:#00FFCC

    participant Uploader as 🎬 Uploader (Host)
    participant Network as 🖥️ P2P Network (All Nodes)
    participant Viewers as 🍿 Viewer Browsers

    class Uploader host
    class Network network
    class Viewers viewer

    %% The Flow
    Uploader->>Network: Click "Start Watch Party"
    
    rect rgb(0, 30, 0)
        Note over Network, Viewers: 🚀 The Broadcast Sync
        Network->>Viewers: "Wake Up! Start playing video X!"
    end

    rect rgb(0, 20, 40)
        Note over Network, Viewers: 🎥 Live Video Streaming
        Viewers-->>Network: Auto-connect to Host's IP
        Network-->>Viewers: Streams the .mp4 file chunks live
    end
    
    Note over Uploader, Viewers: 🛑 Ending the Stream
    Uploader->>Network: Click "End Watch Party"
    Network->>Viewers: "Party Over!" (Auto-closes their screens)
```

---

## 2. Plain Text Diagram (ASCII)

```text
 +-----------------------+                   +-------------------------+
 |                       |                   |                         |
 |  🎬 HOST (Uploader)   |                   |   🖥️ P2P NETWORK      |
 |                       |                   |   (Backend Go Servers)  |
 +-----------+-----------+                   +------------+------------+
             |                                            |
             | 1. Clicks "Start Watch Party"              |
             |------------------------------------------->|
             |   (Sends WebSocket 'start' event)          |
             |                                            |
             |                                            | 2. Broadcasts Sync Event
             |                                            +----------------------------------+
             |                                            |   (HTTP POST /api/p2p/event)     |
                                                          |                                  v
                                            +-------------+-------------+
                                            |                           |
                                            |  🍿 VIEWER BROWSERS        |
                                            |  (Other Localhosts)       |
                                            +-------------+-------------+
                                                          |
                                                          | 3. Auto-opens Video Player
                                                          |    (Receives WS 'start' event)
                                                          |
             <============================================| 4. Fetch streams .mp4 chunks live 
               (Native HTTP 206 Range Requests to Host)   |    
             |                                            |
             | 5. Host clicks "End Party"                 |
             |------------------------------------------->|
             |   (Sends WebSocket 'end' event)            |
             |                                            | 6. Broadcasts End Event
             |                                            +--------------------------------->
                                                          |   (Auto-closes all Viewer screens)
```
