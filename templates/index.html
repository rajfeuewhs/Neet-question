<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Target720</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --pw-blue: #1b10b1; --pw-gradient: linear-gradient(135deg, #1b10b1 0%, #4a3aff 100%); }
        body { font-family: sans-serif; margin: 0; background-size: cover; background-attachment: fixed; }
        .page-section { display: none; min-height: 100vh; background: rgba(248, 250, 255, 0.88); }
        .active-page { display: block !important; }
        .container { max-width: 600px; margin: auto; padding: 15px; }
        /* Centered Logo */
        .branding { text-align: center; padding: 10px; background: white; border-radius: 0 0 20px 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 15px; }
        .branding img { max-width: 140px; height: auto; }
        .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .main-card { background: white; padding: 15px; border-radius: 15px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .rect-card { background: var(--pw-gradient); color: white; padding: 15px; border-radius: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
        .item-row { display: flex; justify-content: space-between; padding: 14px; background: white; margin: 8px 0; border-radius: 12px; font-weight: bold; border: 1px solid #eee; }
        .analysis-row { display: flex; justify-content: space-between; padding: 10px; margin: 5px 0; border-radius: 8px; font-size: 0.85rem; border-left: 4px solid #ccc; }
        .correct-row { border-color: #28a745; background: #f0fff4; } .wrong-row { border-color: #dc3545; background: #fff5f5; }
        .footer { position: fixed; bottom: 0; width: 100%; background: white; padding: 12px; display: flex; gap: 8px; box-sizing: border-box; border-top: 1px solid #eee; }
        .btn { flex: 1; padding: 12px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
        .opt { padding: 14px; border: 2px solid #edf2f7; margin: 8px 0; border-radius: 10px; background: #fff; }
        .opt.active { border-color: var(--pw-blue); background: #f0f2ff; }
    </style>
</head>
<body>

<div id="page-home" class="page-section active-page">
    <div class="branding" id="logo-div"><h2 style="color:var(--pw-blue);margin:0;">Target720</h2></div>
    <div class="container"><div class="main-grid" id="main-subs"></div><div id="custom-area" style="margin-top:20px;"><div id="custom-list"></div></div></div>
</div>

<div id="page-chapters" class="page-section"><div class="container"><div onclick="goBack()" style="cursor:pointer;margin-bottom:10px;"><i class="fas fa-arrow-left"></i> Back</div><h3 id="sub-t"></h3><div id="chap-list"></div></div></div>
<div id="page-dpps" class="page-section"><div class="container"><div onclick="goBack()" style="cursor:pointer;margin-bottom:10px;"><i class="fas fa-arrow-left"></i> Back</div><h3 id="chap-t"></h3><div id="dpp-list"></div></div></div>
<div id="page-test" class="page-section">
    <div style="background:var(--pw-gradient);color:white;padding:15px;display:flex;justify-content:space-between;"><span id="tn">Test</span><span id="timer">00:00</span></div>
    <div class="container"><h4 id="qi" style="color:var(--pw-blue);margin:0;">Q1</h4><div id="qt" style="font-size:1.1rem;margin:10px 0;"></div><div id="qimg"></div><div id="opts"></div></div>
    <div class="footer"><button class="btn" onclick="submitTest()" style="background:#eee;">SUBMIT</button><button class="btn" onclick="nextQ()" style="background:var(--pw-gradient);color:white;">NEXT</button></div>
</div>
<div id="page-res" class="page-section">
    <div class="container" style="text-align:center;">
        <h3>Analysis</h3><div style="max-width:180px;margin:auto;position:relative;"><canvas id="resChart"></canvas><div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"><b><span id="score">0</span></b><br><small>/ <span id="max">0</span></small></div></div>
        <div style="display:flex;justify-content:space-around;margin:15px 0;background:white;padding:10px;border-radius:10px;"><div style="color:green">Right: <b id="rc">0</b></div><div style="color:red">Wrong: <b id="wc">0</b></div></div>
        <div id="anal-list" style="text-align:left;margin-bottom:80px;"></div>
        <div class="footer"><button onclick="location.reload()" class="btn" style="background:var(--pw-gradient);color:white;">HOME</button></div>
    </div>
</div>

<script>
    let config={}, questions=[], cur=0, answers=[], curSub="", timeLeft=0, tInt, pageStack=['page-home'], bpc=0;

    window.onload = async () => {
        const bgR = await fetch('/get_bg_config?v='+Date.now()); const bgD = await bgR.json();
        if(bgD.bg_url) document.body.style.backgroundImage = `url('${bgD.bg_url}')`;
        if(bgD.logo_url) document.getElementById('logo-div').innerHTML = `<img src="${bgD.logo_url}">`;
        const res = await fetch('/get_config?v='+Date.now()); config = await res.json(); renderHome();
        history.pushState(null,'','');
        window.onpopstate = () => {
            if(pageStack.length>1) { goBack(); history.pushState(null,'',''); }
            else { bpc++; if(bpc==2) window.close(); else { alert("Press again to exit"); setTimeout(()=>bpc=0,2000); history.pushState(null,'',''); } }
        };
    };

    function renderHome() {
        const main = ['physics','chemistry','botany','zoology']; let mH='', cH='', hasC=false;
        for (let s in config) {
            if (main.includes(s)) {
                let icon = s=='physics'?'atom':s=='chemistry'?'flask':s=='botany'?'leaf':'dna';
                mH += `<div class="main-card" onclick="openSub('${s}')"><i class="fas fa-${icon}" style="font-size:1.5rem;color:var(--pw-blue)"></i><h5>${s.toUpperCase()}</h5></div>`;
            } else { hasC=true; cH += `<div class="rect-card" onclick="openSub('${s}')"><b>${s.toUpperCase()}</b><i class="fas fa-chevron-right"></i></div>`; }
        }
        document.getElementById('main-subs').innerHTML = mH;
        if(hasC) { document.getElementById('custom-area').style.display='block'; document.getElementById('custom-list').innerHTML=cH; }
    }

    function showP(id, push=true) {
        document.querySelectorAll('.page-section').forEach(p=>p.classList.remove('active-page'));
        document.getElementById(id).classList.add('active-page');
        if(push && pageStack[pageStack.length-1]!==id) pageStack.push(id);
    }
    function goBack() { if(pageStack.length>1) { pageStack.pop(); showP(pageStack[pageStack.length-1], false); } }

    function openSub(s) {
        curSub = s; const chaps = Object.keys(config[s]);
        if(chaps.length==1 && chaps[0]=="Direct_Tests") { openDPPs("Direct_Tests"); return; }
        document.getElementById('sub-t').innerText = s.toUpperCase(); let h='';
        for(let c in config[s]) h += `<div class="item-row" onclick="openDPPs('${c}')">${c=='Direct_Tests'?'Tests':c}</div>`;
        document.getElementById('chap-list').innerHTML = h; showP('page-chapters');
    }

    function openDPPs(c) {
        document.getElementById('chap-t').innerText = c=="Direct_Tests"?"Tests":c;
        const tests = config[curSub][c]; let h='';
        tests.forEach(t=> h += `<div class="item-row" onclick="startT('${t.file}','${t.name}')">${t.name} <i class="fas fa-play-circle" style="color:var(--pw-blue)"></i></div>`);
        document.getElementById('dpp-list').innerHTML = h; showP('page-dpps');
    }

    async function startT(p, n) {
        const r = await fetch(`/get_test/${p}?v=${Date.now()}`); questions = await r.json();
        answers = new Array(questions.length).fill(null); document.getElementById('tn').innerText=n;
        timeLeft = questions.length*60; if(tInt) clearInterval(tInt);
        tInt = setInterval(() => { timeLeft--; let m=Math.floor(timeLeft/60), s=timeLeft%60; document.getElementById('timer').innerText=`${m}:${s<10?'0':''}${s}`; if(timeLeft<=0) submitTest(); }, 1000);
        showP('page-test'); render(0);
    }

    function render(i) {
        cur = i; const q=questions[i]; document.getElementById('qi').innerText=`Q${i+1}`; document.getElementById('qt').innerText=q.q;
        document.getElementById('qimg').innerHTML=q.img?`<img src="${q.img}" style="width:100%;border-radius:10px;margin:10px 0;">`:"";
        let h=''; q.options.forEach((o,idx)=>h+=`<div class="opt ${answers[i]===idx?'active':''}" onclick="answers[${i}]=${idx};render(${i})">${o}</div>`);
        document.getElementById('opts').innerHTML=h;
    }

    function nextQ() { if(cur<questions.length-1) render(cur+1); }

    function submitTest() {
        clearInterval(tInt); let r=0, w=0, s=0, h='';
        questions.forEach((q,i)=>{
            let st=''; if(answers[i]===null){s++; st='skipped-row';} else if(answers[i]===q.correct_ans){r++; st='correct-row';} else {w++; st='wrong-row';}
            h += `<div class="analysis-row ${st}"><span>Q${i+1}: ${q.q.substring(0,25)}..</span><b>${st=='correct-row'?'+4':st=='wrong-row'?'-1':'0'}</b></div>`;
        });
        document.getElementById('score').innerText=(r*4)-w; document.getElementById('max').innerText=questions.length*4;
        document.getElementById('rc').innerText=r; document.getElementById('wc').innerText=w;
        document.getElementById('anal-list').innerHTML=h; showP('page-res');
        new Chart(document.getElementById('resChart'), { type:'doughnut', data:{ datasets:[{data:[r,w,s], backgroundColor:['#28a745','#dc3545','#ffc107']}]}, options:{cutout:'80%'} });
    }
</script>
</body>
</html>
