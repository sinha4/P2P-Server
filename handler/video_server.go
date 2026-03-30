package handler

import (
	"bytes"
	"fmt"
	"net/http"
	"p2p/peer"
	"time"
)

// VideoStreamHandler serves a file from the peer's chunk storage directly
// as an HTTP video stream, supporting standard Byte-Range requests native to HTML5 video.
func VideoStreamHandler(p *peer.Peer) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		fileName := r.URL.Query().Get("name")
		if fileName == "" {
			http.Error(w, "Missing 'name' parameter", http.StatusBadRequest)
			return
		}

		p.Mu.Lock()
		meta, exists := p.SharedFiles[fileName]
		p.Mu.Unlock()

		if !exists {
			http.Error(w, "File not found on this host", http.StatusNotFound)
			return
		}

		// Reassemble the file in memory to create a ReadSeeker for http.ServeContent
		// (For very large files, a custom `io.ReadSeeker` over the chunk map is better,
		// but memory reconstruction works perfectly for this P2P prototype).
		var fileBuffer bytes.Buffer
		
		p.Mu.Lock()
		for _, chunkMeta := range meta.Chunks {
			hashStr := fmt.Sprintf("%x", chunkMeta.Hash)
			chunkData, ok := p.ChunkDataStorage[hashStr]
			if !ok {
				p.Mu.Unlock()
				http.Error(w, fmt.Sprintf("Missing chunk %d", chunkMeta.Index), http.StatusInternalServerError)
				return
			}
			fileBuffer.Write(chunkData)
		}
		p.Mu.Unlock()

		reader := bytes.NewReader(fileBuffer.Bytes())

		// ServeContent handles Range requests, Content-Length, and Accept-Ranges automatically.
		w.Header().Set("Content-Type", "video/mp4")
		http.ServeContent(w, r, fileName, time.Now(), reader)
	}
}
