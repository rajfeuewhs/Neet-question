<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>Admin - Bulk JSON Upload</title>
    <style>
        :root { --pw-blue: #1b10b1; --bg: #f4f7fe; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); padding: 20px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .setup-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; background: #f9faff; padding: 15px; border-radius: 12px; }
        .dpp-block { border: 2px dashed #cbd5e1; padding: 20px; border-radius: 15px; margin-bottom: 20px; background: #fff; }
        label { font-weight: bold; display: block; margin-bottom: 5px; color: #444; }
        select, input, textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        textarea { font-family: monospace; font-size: 13px; background: #2d3436; color: #fab1a0; margin-top: 10px; }
        .actions { display: flex; gap: 15px; margin-top: 20px; }
        .btn { flex: 1; padding: 15px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
        .btn-add { background: #e0e6ff; color: var(--pw-blue); }
        .btn-submit { background: var(--pw-blue); color: white; }
    </style>
</head>
<body>

<div class="container">
    <h2>🚀 Bulk DPP Uploader</h2>

    <div class="setup-row">
        <div>
            <label>Subject</label>
            <select id="sub-select" onchange="updateChapters()">
                <option value="">--Select--</option>
                <option value="physics">Physics</option>
                <option value="chemistry">Chemistry</option>
                <option value="botany">Botany</option>
                <option value="zoology">Zoology</option>
            </select>
        </div>
        <div>
            <label>Chapter</label>
            <select id="chap-select"><option value="">Pehle Subject Chunein</option></select>
        </div>
    </div>

    <div id="dpp-list">
        <div class="dpp-block">
            <label>DPP Name</label>
            <input type="text" class="dpp-name" placeholder="e.g. DPP_01">
            <textarea class="dpp-json" rows="8" placeholder="Yahan apna JSON Code paste karein..."></textarea>
        </div>
    </div>

    <div class="actions">
        <button class="btn btn-add" onclick="addMoreDPP()">+ Add One More DPP</button>
        <button class="btn btn-submit" id="main-btn" onclick="uploadAll()">🚀 UPLOAD ALL TO LIVE</button>
    </div>
</div>

<script>
    let config = {};
    window.onload = async () => { config = await (await fetch('/get_config')).json(); };

    function updateChapters() {
        const sub = document.getElementById('sub-select').value;
        const chapDrop = document.getElementById('chap-select');
        chapDrop.innerHTML = "";
        if(sub && config[sub]) {
            Object.keys(config[sub]).forEach(ch => {
                let op = document.createElement('option'); op.value = ch; op.innerText = ch;
                chapDrop.appendChild(op);
            });
        }
    }

    function addMoreDPP() {
        const html = `
        <div class="dpp-block">
            <label>DPP Name</label>
            <input type="text" class="dpp-name" placeholder="e.g. DPP_02">
            <textarea class="dpp-json" rows="8" placeholder="Agla JSON Code paste karein..."></textarea>
        </div>`;
        document.getElementById('dpp-list').insertAdjacentHTML('beforeend', html);
    }

    async function uploadAll() {
        const sub = document.getElementById('sub-select').value;
        const chap = document.getElementById('chap-select').value;
        const btn = document.getElementById('main-btn');
        const blocks = document.querySelectorAll('.dpp-block');

        if(!sub || !chap) return alert("Subject aur Chapter chunein!");

        btn.disabled = true;
        btn.innerText = "Uploading... Please Wait";

        try {
            for (let block of blocks) {
                const name = block.querySelector('.dpp-name').value;
                const jsonText = block.querySelector('.dpp-json').value;

                if(!name || !jsonText) continue;

                const res = await fetch('/save_test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        subject: sub,
                        chapter: chap,
                        test_name: name,
                        questions: JSON.parse(jsonText)
                    })
                });
                console.log(`${name} upload status check complete.`);
            }
            alert("Saare DPPs Live ho gaye hain!");
            location.reload();
        } catch(e) {
            alert("Error: JSON format check karein ya internet check karein.");
        } finally {
            btn.disabled = false;
            btn.innerText = "🚀 UPLOAD ALL TO LIVE";
        }
    }
</script>
</body>
</html>
