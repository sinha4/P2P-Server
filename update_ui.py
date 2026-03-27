import re

hacker_style = """    <style>
        :root {
            --primary: #00FF41;
            --secondary: #008F11;
            --accent: #00FFCC;
            --background: #0D0D0D;
            --soft-accent: #008F11;
            --text-dark: #00FF41;
            --page-bg: #000000;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Courier New', Consolas, monospace;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: var(--page-bg);
            background-image: linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
            background-size: 20px 20px;
            color: var(--text-dark);
            -webkit-font-smoothing: antialiased;
        }

        /* User Top Bar */
        .user-bar {
            position: fixed; top: 0; left: 0; right: 0;
            display: flex; align-items: center; justify-content: flex-end;
            padding: 0.6rem 1.5rem;
            background: rgba(13,13,13,0.9); border-bottom: 1px solid var(--primary);
            z-index: 100; gap: 0.75rem; box-shadow: 0 2px 8px rgba(0,255,65,0.1);
        }
        .user-bar .user-name { font-weight: bold; color: var(--primary); font-size: 0.9rem; }
        .user-bar .user-avatar { 
            width: 32px; height: 32px; border-radius: 2px;
            background: var(--background); border: 1px solid var(--primary);
            display: flex; align-items: center; justify-content: center;
            color: var(--primary); font-weight: bold; font-size: 0.85rem;
        }
        .user-bar .logout-btn {
            background: var(--background); color: var(--primary); border: 1px solid var(--primary);
            padding: 0.4rem 1rem; font-family: inherit; font-size: 0.8rem;
            font-weight: bold; border-radius: 2px; cursor: pointer; text-transform: uppercase;
        }
        .user-bar .logout-btn:hover { background: var(--primary); color: var(--page-bg); }

        .container {
            text-align: center;
            padding: 3.5rem 3rem;
            background: rgba(13, 13, 13, 0.85); border-radius: 2px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.15); border: 1px solid var(--primary);
            max-width: 800px; width: 90%; backdrop-filter: blur(4px); margin: auto;
        }

        h1 { font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: bold; color: var(--primary); letter-spacing: 0.05em; text-shadow: 0 0 10px rgba(0, 255, 65, 0.5); text-transform: uppercase; }
        .subtitle { color: var(--secondary); font-size: 1.15rem; font-weight: normal; margin-bottom: 3rem; opacity: 0.9; }

        .cards { display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap; }
        .card { background: var(--background); border: 1px solid var(--secondary); border-radius: 2px; padding: 2.5rem 2rem; width: 260px; text-decoration: none; color: var(--text-dark); transition: all 0.2s ease-in-out; cursor: pointer; box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.05); display: flex; flex-direction: column; align-items: center; position: relative; }
        .card:hover { box-shadow: 0 0 20px rgba(0, 255, 65, 0.2), inset 0 0 15px rgba(0, 255, 65, 0.1); border-color: var(--primary); transform: translateY(-4px); }
        .card-icon { display: inline-flex; align-items: center; justify-content: center; width: 72px; height: 72px; background: var(--page-bg); color: var(--primary); border: 1px solid var(--secondary); border-radius: 2px; margin-bottom: 1.25rem; transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .card:hover .card-icon { transform: scale(1.05); box-shadow: 0 0 15px rgba(0, 255, 65, 0.3); border-color: var(--primary); }
        .icon-svg { width: 36px; height: 36px; stroke-width: 2; stroke: currentColor; fill: none; stroke-linecap: square; stroke-linejoin: miter; }
        .card h2 { font-size: 1.3rem; margin-bottom: 0.75rem; font-weight: bold; color: var(--primary); text-transform: uppercase; }
        .card p { font-size: 0.95rem; color: var(--secondary); opacity: 1; line-height: 1.5; }

        .peer-info { margin-top: 3.5rem; font-size: 0.9rem; color: var(--primary); background: rgba(0, 143, 17, 0.1); border: 1px dashed var(--secondary); padding: 0.75rem 1.5rem; border-radius: 2px; font-weight: bold; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 0.8; box-shadow: 0 0 0 rgba(0, 255, 65, 0); } 50% { opacity: 1; box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); } 100% { opacity: 0.8; box-shadow: 0 0 0 rgba(0, 255, 65, 0); } }

        /* Upload Specific */
        nav a { color: var(--secondary); text-decoration: none; font-weight: bold; font-size: 0.95rem; transition: color 0.2s; }
        nav a:hover { color: var(--primary); text-shadow: 0 0 8px rgba(0,255,65,0.5); }
        .form-group { background: var(--background); border: 1px dashed var(--secondary); border-radius: 2px; padding: 2rem; margin-bottom: 1.5rem; transition: all 0.2s; }
        .form-group:hover { border-color: var(--primary); background: rgba(0, 255, 65, 0.05); }
        label { margin-bottom: 1rem; font-weight: bold; color: var(--primary); font-size: 1rem; text-transform: uppercase; }
        input[type="file"] { display: none; }
        .file-custom { background: var(--background); border: 1px solid var(--primary); padding: 0.75rem 1.5rem; border-radius: 2px; color: var(--primary); font-weight: bold; cursor: pointer; text-transform: uppercase; transition: all 0.2s; }
        .file-custom:hover { background: var(--primary); color: var(--page-bg); box-shadow: 0 0 10px rgba(0,255,65,0.5); }
        .file-name-display { margin-top: 1rem; font-size: 0.95rem; color: var(--secondary); word-break: break-all; }
        button[type="submit"], .btn-refresh, .download-btn { background: var(--background); color: var(--primary); border: 1px solid var(--primary); padding: 1rem; font-size: 1.1rem; font-weight: bold; font-family: inherit; border-radius: 2px; cursor: pointer; text-transform: uppercase; transition: all 0.2s; width: 100%; display: block; }
        .btn-refresh, .download-btn { padding: 0.75rem 1.5rem; font-size: 0.95rem; width: auto; margin: 0 auto 1.5rem auto; }
        .download-btn { margin: 0; padding: 0.6rem 1.2rem; }
        button[type="submit"]:hover, .btn-refresh:hover, .download-btn:hover { background: rgba(0,255,65,0.1); box-shadow: 0 0 15px rgba(0,255,65,0.3); transform: translateY(-1px); }
        .download-btn:hover { background: var(--primary); color: var(--page-bg); }

        #status { margin-top: 1.5rem; padding: 1rem; border-radius: 2px; font-weight: bold; text-align: center; display: none; }
        .status-loading { display: block!important; background: rgba(0,143,17,0.1); color: var(--accent); border: 1px solid var(--secondary); }
        .status-success { display: block!important; background: rgba(0,255,65,0.1); color: var(--primary); border: 1px solid var(--primary); }
        .status-error { display: block!important; background: rgba(255,0,0,0.1); color: #ff3333; border: 1px solid #ff3333; }

        /* Download Specific */
        .file-card { background: var(--background); border: 1px solid var(--secondary); padding: 1.5rem; margin-bottom: 1rem; border-radius: 2px; display: flex; justify-content: space-between; align-items: center; transition: all 0.2s;}
        .file-card:hover { border-color: var(--primary); background: rgba(0,255,65,0.05); transform: translateX(4px); box-shadow: -4px 0 0 var(--primary), 0 0 10px rgba(0,255,65,0.1); }
        .file-info strong { color: var(--primary); font-size: 1.15rem; display: block; margin-bottom: 0.25rem; font-weight: bold; }
        .file-info small { color: var(--secondary); font-size: 0.9rem; }
        
        #chunkDetails { margin-top: 2rem; background: rgba(0,0,0,0.5); border: 1px dashed var(--secondary); border-radius: 2px; padding: 1.5rem; display: none; }
        #chunkDetails.visible { display: block; }
        .dashboard-main-title { color: var(--primary); margin-bottom: 1.5rem; font-size: 1.25rem; border-bottom: 1px solid var(--secondary); padding-bottom: 0.75rem; text-transform: uppercase; }
        .dashboard-section-title { color: var(--secondary); margin-bottom: 0.75rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: bold; }
        .peers-summary { margin-bottom: 1.5rem; }
        .peer-badge { display: inline-flex; padding: 0.25rem 0.6rem; border-radius: 2px; font-size: 0.8rem; font-weight: bold; margin-right: 0.5rem; margin-bottom: 0.5rem; border: 1px solid currentColor; background: rgba(0,0,0,0.5); align-items: center;}
        .chunk-grid { display: flex; flex-wrap: wrap; gap: 2px; margin-top: 0.8rem; }
        .chunk-cell { width: 28px; height: 28px; border-radius: 0; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: bold; border: 1px solid rgba(0,0,0,0.5); position: relative; cursor: default; }
        .chunk-cell:hover { z-index: 2; border-color: white; box-shadow: 0 0 8px currentColor; transform: scale(1.1); }
        
        #loadBarInner { height: 16px; border: 1px solid var(--secondary); display: flex; background: var(--background); margin-top: 0.5rem; margin-bottom: 2rem; overflow: hidden; }
        .load-bar-segment { height: 100%; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: bold; border-right: 1px solid rgba(0,0,0,0.3); transition: width 0.5s ease-out; }
        .load-bar-segment:last-child { border-right: none; }
    </style>"""

for fn in ["/Users/shambhavi/Desktop/P2P-Server/web/home.html", "/Users/shambhavi/Desktop/P2P-Server/web/upload.html", "/Users/shambhavi/Desktop/P2P-Server/web/download.html"]:
    with open(fn, "r") as f:
        content = f.read()
    content = re.sub(r'<style>.*?</style>', hacker_style, content, flags=re.DOTALL)
    
    if fn.endswith("download.html"):
        content = re.sub(r"const PEER_COLORS = \[.*?\];", "const PEER_COLORS = ['#00FF41', '#00FFCC', '#FF00FF', '#FFFF00', '#00BFFF', '#FF4500', '#32CD32', '#1E90FF'];", content, flags=re.DOTALL)
        content = re.sub(r"const tColor = \(peerColorMap.*?white';", "const tColor = 'var(--page-bg)';", content)
        content = re.sub(r"seg\.style\.color = \(peerColorMap.*?white';", "seg.style.color = 'var(--page-bg)';", content)
        content = re.sub(r"cell\.style\.color = \(peerColorMap.*?white';", "cell.style.color = 'var(--page-bg)';", content)
        
    with open(fn, "w") as f:
        f.write(content)
print("done")
