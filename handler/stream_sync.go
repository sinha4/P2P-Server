package handler

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"p2p/peer"
	"p2p/registry"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Allow all for local P2P
	},
}

// StreamEvent represents a watch party event
type StreamEvent struct {
	Action   string  `json:"action"` // "start", "end", "play", "pause", "sync"
	FileName string  `json:"file_name"`
	HostURL  string  `json:"host_url,omitempty"` // e.g. "http://localhost:8080"
	Time     float64 `json:"time,omitempty"`
}

// Global Hub for frontend WebSockets
var (
	wsClients = make(map[*websocket.Conn]bool)
	wsMutex   sync.Mutex
)

// StreamSyncWSHandler handles the frontend browser connecting to listen for stream events.
func StreamSyncWSHandler(p *peer.Peer) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Printf("[%s] WS Upgrade error: %v", p.PeerID, err)
			return
		}

		wsMutex.Lock()
		wsClients[conn] = true
		wsMutex.Unlock()

		defer func() {
			wsMutex.Lock()
			delete(wsClients, conn)
			wsMutex.Unlock()
			conn.Close()
		}()

		selfAddr := fmt.Sprintf("localhost:%d", p.Port)

		// Keep connection alive, listen for frontend events (if host)
		for {
			_, msg, err := conn.ReadMessage()
			if err != nil {
				break
			}
			// Frontend sent an event (Host triggered action)
			var event StreamEvent
			if err := json.Unmarshal(msg, &event); err == nil {
				log.Printf("[%s] Broadcasting Local Stream Event: %s", p.PeerID, event.Action)
				// Broadcast this event to all P2P peers
				BroadcastP2PStreamEvent(event, selfAddr)
				// Re-broadcast to self (other tabs)
				broadcastLocalWS(event)
			}
		}
	}
}

// broadcastLocalWS pushes an event to all connected browser tabs locally
func broadcastLocalWS(event StreamEvent) {
	wsMutex.Lock()
	defer wsMutex.Unlock()
	for client := range wsClients {
		err := client.WriteJSON(event)
		if err != nil {
			client.Close()
			delete(wsClients, client)
		}
	}
}

// StreamEventP2PHandler receives events from other Peers and pushes to local WS
func StreamEventP2PHandler(p *peer.Peer) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		var event StreamEvent
		if err := json.NewDecoder(r.Body).Decode(&event); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		log.Printf("[%s] Received P2P Stream Event: %s for %s", p.PeerID, event.Action, event.FileName)

		// Push to local browsers
		broadcastLocalWS(event)

		w.WriteHeader(http.StatusOK)
	}
}

// BroadcastP2PStreamEvent sends a StreamEvent to all known peers in the registry
func BroadcastP2PStreamEvent(event StreamEvent, selfAddr string) {
	peers := registry.GetPeers()
	payload, _ := json.Marshal(event)

	client := &http.Client{Timeout: 5 * time.Second}

	for _, peerAddr := range peers {
		if peerAddr == selfAddr {
			continue // skip self
		}
		// Attempt to send to each peer
		url := fmt.Sprintf("http://%s/api/p2p/stream/event", peerAddr)
		go func(peerURL string) {
			resp, err := client.Post(peerURL, "application/json", bytes.NewReader(payload))
			if err == nil {
				resp.Body.Close()
			}
		}(url)
	}
}
