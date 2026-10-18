/* Regression: navigate the real deck from the cover, through every slide type. */
const {chromium}=require('playwright');
const path=require('path'),fs=require('fs'),{pathToFileURL}=require('url');
const out=path.resolve(__dirname,'../outputs');
const manifest=JSON.parse(fs.readFileSync(path.join(out,'lecture-manifest.json'),'utf8'));
const target=process.env.DECK_URL||pathToFileURL(path.join(out,'ml-architecture-lecture.html')).href;
const check=(ok,message)=>{if(!ok)throw new Error(message)};
(async()=>{
 const browser=await chromium.launch({...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{}),args:['--no-sandbox','--disable-dev-shm-usage']});
 const errors=[],passed=[];
 try{
  const page=await browser.newPage({viewport:{width:1280,height:720}});page.on('pageerror',e=>errors.push(e.message));
  await page.goto(target);await page.evaluate(()=>document.fonts.ready);
  await page.keyboard.press('Home');await page.keyboard.press('ArrowRight');
  check(await page.evaluate(()=>deck.current)===1,'Right arrow must leave the cover');
  await page.keyboard.press('ArrowRight');check(await page.evaluate(()=>deck.current)===2,'Right arrow must leave the text-only agenda');
  passed.push('Cover and text-only agenda advance with arrows');
  await page.keyboard.press('ArrowLeft');check(await page.evaluate(()=>deck.current)===1,'Left from first build returns to agenda');
  await page.keyboard.press('Home');await page.keyboard.press('ArrowLeft');check(await page.evaluate(()=>deck.current)===0,'First slide boundary');
  // Traverse using only real keyboard presses; do not jump to each diagram.
  for(let i=0;i<manifest.length-1;i++){
   const current=manifest[i];
   for(let step=0;step<current.steps;step++)await page.keyboard.press('ArrowRight');
   await page.keyboard.press('ArrowRight');check(await page.evaluate(()=>deck.current)===i+1,'Forward transition after slide '+(i+1));
  }
  await page.keyboard.press('ArrowRight');check(await page.evaluate(()=>deck.current)===manifest.length-1,'Final slide boundary');
  passed.push('Forward through all '+manifest.length+' slides, including every diagram and table');
  for(let i=manifest.length-1;i>0;i--){
   for(let step=0;step<manifest[i].steps;step++)await page.keyboard.press('ArrowLeft');
   await page.keyboard.press('ArrowLeft');check(await page.evaluate(()=>deck.current)===i-1,'Backward transition from slide '+(i+1));
   const figure=page.locator('.slide.active [data-motion-root]');if(manifest[i-1].steps)check(await figure.getAttribute('data-step-current')===String(manifest[i-1].steps),'Previous diagram must arrive complete');
  }
  passed.push('Backward through all slides, arriving at complete previous diagrams');
  await page.keyboard.press('PageDown');await page.keyboard.press('PageDown');
  const root=page.locator('.slide.active [data-motion-root]');await page.evaluate(()=>{const f=document.querySelector('.slide.active figure');f.tabIndex=0;f.focus();});
  await page.keyboard.press('ArrowRight');check(await root.getAttribute('data-step-current')==='1','Focused diagram receives exactly one forward build');
  await page.keyboard.press('ArrowLeft');check(await root.getAttribute('data-step-current')==='0','Focused diagram receives exactly one reverse build');
  passed.push('Focused diagram does not consume arrows twice');
  await page.keyboard.press('g');await page.locator('[data-jump="1"]').click();await page.keyboard.press('ArrowRight');check(await page.evaluate(()=>deck.current)===2,'Navigation after contents selection');
  await page.keyboard.press('e');const field=page.locator('.slide.active h1[data-edit]');await field.focus();await page.keyboard.press('ArrowRight');check(await page.evaluate(()=>deck.current)===2,'Editing text must not navigate');await page.keyboard.press('Escape');
  passed.push('Contents selection restores navigation; text editing keeps caret keys');
  await page.emulateMedia({reducedMotion:'reduce'});await page.keyboard.press('Home');for(let i=1;i<manifest.length;i++){await page.keyboard.press('ArrowRight');check(await page.evaluate(()=>deck.current)===i,'Reduced-motion navigation');}
  await page.goto(target+'?motion=static');for(let i=1;i<manifest.length;i++){await page.keyboard.press('ArrowRight');check(await page.evaluate(()=>deck.current)===i,'Static navigation');}
  passed.push('Reduced-motion and static modes navigate directly');check(!errors.length,'Browser errors: '+errors.join('; '));
  const report={passed,errors,slides:manifest.length};fs.writeFileSync(path.join(out,'navigation-verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e.message);process.exitCode=1});
