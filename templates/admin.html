<!DOCTYPE html>
<html>
<head>
    <title>Clean Admin Panel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f4f7fe; }
        .box { background: white; padding: 20px; border-radius: 12px; max-width: 600px; margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .tabs { display: flex; gap: 5px; margin-bottom: 20px; }
        .tab-btn { flex: 1; padding: 10px; cursor: pointer; border: none; border-radius: 5px; background: #ddd; font-weight: bold; }
        .tab-btn.active { background: #1b10b1; color: white; }
        
        /* Dropdown Styles */
        .collapsible { background: #1b10b1; color: white; cursor: pointer; padding: 12px; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; margin-top: 10px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
        .content { display: none; padding: 0 18px; background-color: white; border-left: 2px solid #1b10b1; margin-bottom: 10px; }
        .chap-box { background: #f0f2ff; padding: 10px; margin: 5px 0; border-radius: 5px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
        .test-box { padding: 8px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; }
        .del-btn { background: #ff4d4d; color: white; border: none; padding: 4px 8px; border-radius: 3px; cursor: pointer; font-size: 0.7rem; }
    </style>
</head>
<body>
    <div class="box">
        <div class="tabs">
            <button class="tab-btn active" id="btn-up" onclick="showTab('upload')">UPLOAD</button>
            <button class="tab-btn" id="btn-mn" onclick="showTab('manage')">MANAGE</button>
        </div>

        <div id="upload-sec">
            <h3>Upload New Test</h3>
            <input type="text" id="chap" placeholder="Chapter Name">
            <input type="text" id="tname" placeholder="Test Name">
            <textarea id="jsondata" rows="5" placeholder="JSON here..."></textarea>
            <button style="width:100%; padding:10px; background:#1b10b1; color:white; border:none; margin-top:10px;" onclick="upload()">PUBLISH</button>
        </div>

        <div id="manage-sec" style="display:none;">
            <h3>🛠️ Manage Data (Click to Expand)</h3>
            <div id="manage-tree">Loading...</div>
        </div>
    </div>

    <script>
        function showTab(t) {
            document.getElementById('upload-sec').style.display = t=='upload'?'block':'none';
            document.getElementById('manage-sec').style.display = t=='manage'?'block':'none';
            if(t=='manage') loadTree();
        }

        async function loadTree() {
            const res = await fetch('/get_config?t=' + Date.now());
            const config = await res.json();
            let h = '';

            for (let s in config) {
                h += `
                <button class="collapsible" onclick="toggleDisplay('sub-${s}')">
                    <span>📁 ${s.toUpperCase()}</span>
                    <span onclick="event.stopPropagation(); handleDelete({subject:'${s}', target:'subject'})" style="background:red; padding:2px 6px; font-size:10px; border-radius:3px;">DEL SUBJECT</span>
                </button>
                <div id="sub-${s}" class="content">`;
                
                for (let c in config[s]) {
                    h += `
                    <div class="chap-box" onclick="toggleDisplay('chap-${s}-${c.replace(/ /g,'_')}')">
                        <span>📖 ${c}</span>
                        <button class="del-btn" style="background:orange;" onclick="event.stopPropagation(); handleDelete({subject:'${s}', chapter:'${c}', target:'chapter'})">Del Chap</button>
                    </div>
                    <div id="chap-${s}-${c.replace(/ /g,'_')}" class="content" style="padding-left:20px; border-left:1px dashed #ccc;">`;
                    
                    config[s][c].forEach(t => {
                        h += `
                        <div class="test-box">
                            <span>📄 ${t.name}</span>
                            <button class="del-btn" onclick="handleDelete({subject:'${s}', chapter:'${c}', test_name:'${t.name}', target:'test'})">Delete DPP</button>
                        </div>`;
                    });
                    h += `</div>`;
                }
                h += `</div>`;
            }
            document.getElementById('manage-tree').innerHTML = h || "No Data Found";
        }

        function toggleDisplay(id) {
            let el = document.getElementById(id);
            el.style.display = (el.style.display === "block") ? "none" : "block";
        }

        async function handleDelete(params) {
            if(!confirm("Are you sure?")) return;
            const res = await fetch('/delete_item', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(params)
            });
            const r = await res.json();
            if(r.success) loadTree(); 
        }

        // Add upload function here...
    </script>
</body>
</html>
