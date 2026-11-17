import { chromium } from '/home/nmaldaner/projetos/inemaccbot/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const dir='/home/nmaldaner/projetos/output/solar-noaa-serie/media';
const b=await chromium.launch({headless:true,args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1920,height:1080}});
for (const f of fs.readdirSync(dir).filter(x=>x.endsWith('.svg'))){
 await p.goto('file://'+dir+'/'+f);await p.locator('svg').screenshot({path:dir+'/'+f.replace('.svg','.png')});
}
await b.close();console.log('Diagramas PNG renderizados nos dois formatos.');
