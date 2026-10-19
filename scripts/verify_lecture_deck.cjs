/* Full browser verification for the topic-led lecture and its aligned guide. */
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const root=path.resolve(__dirname,'..'),out=path.join(root,'outputs'),pre=path.join(root,'previews/lecture-full');fs.mkdirSync(pre,{recursive:true});
const manifest=JSON.parse(fs.readFileSync(path.join(out,'lecture-manifest.json'),'utf8'));
const url=pathToFileURL(path.join(out,'ml-architecture-lecture.html')).href;
const assert=(v,msg)=>{if(!v)throw new Error(msg)};
(async()=>{
 const browser=await chromium.launch({...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{}),args:['--no-sandbox','--disable-dev-shm-usage']});
 const report={slides:[],errors:[],checks:[]};
 try{
  const ctx=await browser.newContext({viewport:{width:1280,height:720}});await ctx.route(/^https?:/,r=>r.abort());
  const p=await ctx.newPage();p.on('pageerror',e=>report.errors.push(String(e)));
  await p.goto(url+'?motion=static');await p.evaluate(()=>document.fonts.ready);
  for(let i=0;i<manifest.length;i++){
   await p.evaluate(n=>deck.show(n),i);
   const result=await p.locator('.slide.active').evaluate(s=>{
    const issues=[],stage=s.getBoundingClientRect(),bounds=e=>e.getBoundingClientRect(),overlap=(a,b)=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>1&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>1;
    const regions=[...s.querySelectorAll('.masthead,.heading,.body-grid,.example,footer,.cover-side,.cover-speakers')];
    for(const e of regions){const b=bounds(e);if(b.left<stage.left-1||b.right>stage.right+1||b.top<stage.top-1||b.bottom>stage.bottom+1)issues.push('Outside stage: '+e.className);}
    for(let j=0;j<regions.length;j++)for(let k=j+1;k<regions.length;k++)if(overlap(bounds(regions[j]),bounds(regions[k])))issues.push('Region overlap: '+regions[j].className+' / '+regions[k].className);
    const aside=s.querySelector('.explanation');if(aside){const ab=bounds(aside);for(const e of aside.children){const b=bounds(e);if(b.bottom>ab.bottom+1)issues.push('Presenter text outside aside: '+e.textContent);}}
    const example=s.querySelector('.example');if(example){const eb=bounds(example);for(const e of example.children){const b=bounds(e);if(b.top<eb.top-1||b.bottom>eb.bottom+1)issues.push('Example text overflow');}}
    const table=s.querySelector('.lecture-table table'),column=s.querySelector('.diagram-column');if(table){const t=bounds(table),c=bounds(column);if(t.right>c.right+1||t.bottom>c.bottom+1)issues.push('Table overflow');}
    const nodes=[...s.querySelectorAll('[data-node]')];for(const n of nodes){const r=n.querySelector('rect').getBBox();for(const t of n.querySelectorAll('text')){const b=t.getBBox();if(b.x<r.x+5||b.x+b.width>r.x+r.width-5||b.y<r.y+4||b.y+b.height>r.y+r.height-4)issues.push('Node text overflow: '+t.textContent);}}
    const svg=s.querySelector('svg');if(svg){const v=svg.viewBox.baseVal,texts=[...svg.querySelectorAll('text')];for(const t of texts){const b=t.getBBox();if(b.x<0||b.y<0||b.x+b.width>v.width||b.y+b.height>v.height)issues.push('SVG bounds: '+t.textContent);}
     for(let j=0;j<texts.length;j++)for(let k=j+1;k<texts.length;k++)if(overlap(bounds(texts[j]),bounds(texts[k])))issues.push('SVG label overlap: '+texts[j].textContent+' / '+texts[k].textContent);
     for(const e of svg.querySelectorAll('path.edge')){const len=e.getTotalLength(),first=e.getPointAtLength(0),last=e.getPointAtLength(len);for(const n of nodes){const b=n.querySelector('rect').getBBox(),at=p=>p.x>=b.x-2&&p.x<=b.x+b.width+2&&p.y>=b.y-2&&p.y<=b.y+b.height+2;if(at(first)||at(last))continue;for(let d=4;d<len-4;d+=4){const pt=e.getPointAtLength(d);if(pt.x>b.x+2&&pt.x<b.x+b.width-2&&pt.y>b.y+2&&pt.y<b.y+b.height-2){issues.push('Connector crosses unrelated node: '+n.getAttribute('data-node'));break;}}}}
    }
    const heading=s.querySelector('.heading');if(heading&&heading.scrollWidth>heading.clientWidth+2)issues.push('Heading width overflow');
    return {title:s.querySelector('h1').textContent,presenter:s.querySelector('.speaker')?.textContent||'All presenters',bullets:s.querySelectorAll('li').length,issues};
   });
   report.slides.push({number:i+1,...result});await p.screenshot({path:path.join(pre,`slide-${String(i+1).padStart(2,'0')}.png`)});
  }
  await p.setViewportSize({width:390,height:844});const mobile=await p.locator('#deckStage').boundingBox();console.error('MOBILE_BBOX',JSON.stringify(mobile),'ratio',mobile.width/mobile.height,'target',16/9);assert(Math.abs(mobile.width/mobile.height-16/9)<.005&&mobile.x>=-.5&&mobile.x+mobile.width<=390.5,'Phone stage fit');await p.screenshot({path:path.join(pre,'phone.png')});report.checks.push('Fixed 16:9 desktop and phone stage');
  await p.setViewportSize({width:1920,height:1080});await p.pdf({path:path.join(out,'ml-architecture-lecture.pdf'),printBackground:true,preferCSSPageSize:true});
  const live=await ctx.newPage();live.on('pageerror',e=>report.errors.push(String(e)));await live.goto(url);await live.evaluate(()=>document.fonts.ready);
  for(const m of manifest.filter(x=>x.steps)){
   await live.evaluate(n=>deck.show(n),m.number-1);const f=live.locator('.slide.active [data-motion-root]');assert(await f.getAttribute('data-step-current')==='0','Build start '+m.number);
   await live.keyboard.press('ArrowRight');assert(await f.getAttribute('data-step-current')==='1','Forward '+m.number);await live.keyboard.press('ArrowLeft');assert(await f.getAttribute('data-step-current')==='0','Reverse '+m.number);
   for(let step=0;step<m.steps;step++)await live.keyboard.press('ArrowRight');assert(await f.getAttribute('data-step-current')===String(m.steps),'Complete '+m.number);
  }
  assert(await live.locator('[data-motion-controls]:visible').count()===0,'Playback UI hidden');await live.keyboard.press('Home');await live.keyboard.press('PageDown');assert(await live.evaluate(()=>deck.current)===1,'Direct slide navigation');
  await live.keyboard.press('g');assert(await live.locator('#contents').isVisible(),'Contents keyboard');await live.locator('[data-jump="17"]').click();assert(await live.evaluate(()=>deck.current)===17,'Contents jump');
  await live.keyboard.press('e');assert(await live.locator('body').getAttribute('class')==='editing','Editing');
  const editable=live.locator('.slide.active h1[data-edit]'),editableId=await editable.getAttribute('id'),original=await editable.textContent();await editable.fill('Local review edit');
  assert(await live.evaluate(id=>JSON.parse(localStorage.getItem('ml-architecture-lecture-v2'))[id],editableId)==='Local review edit','Local edit persisted');
  await editable.fill(original);await live.keyboard.press('Escape');await live.evaluate(()=>localStorage.removeItem('ml-architecture-lecture-v2'));
  await live.emulateMedia({reducedMotion:'reduce'});assert(await live.locator('[data-motion-item]').evaluateAll(es=>es.every(e=>getComputedStyle(e).opacity==='1')),'Reduced motion');
  report.checks.push('Reversible arrow builds on all diagram slides; direct navigation; contents; editing; no visible playback UI; offline fonts; reduced motion');
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:1280,height:720}}),np=await nojs.newPage();await np.goto(url);assert(await np.locator('[data-motion-item]').evaluateAll(es=>es.every(e=>getComputedStyle(e).opacity==='1')),'Complete no-JS figures');await nojs.close();report.checks.push('Complete no-JavaScript figures');
  const gp=await ctx.newPage();await gp.goto(pathToFileURL(path.join(out,'lecture-presenter-guide.html')).href);await gp.evaluate(()=>document.fonts.ready);report.guideHeadings=await gp.locator('h2').allTextContents();
  assert(report.guideHeadings.filter(h=>/^\d+\./.test(h)).length===manifest.length,'Guide numbering');
  await gp.pdf({path:path.join(out,'lecture-presenter-guide.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:9px;width:100%;padding:0 18mm;color:#666;display:flex;justify-content:space-between"><span>ML Architecture · Presenter Guide</span><span class="pageNumber"></span></div>'});
  fs.writeFileSync(path.join(out,'lecture-verification.json'),JSON.stringify(report,null,2));const issues=report.slides.flatMap(s=>s.issues.map(issue=>({slide:s.number,issue})));console.log(JSON.stringify({slides:manifest.length,issues,errors:report.errors,checks:report.checks},null,2));
  assert(!issues.length&&!report.errors.length,'Geometry or runtime errors');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
