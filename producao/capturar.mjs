import { chromium } from '/home/nmaldaner/projetos/inemaccbot/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const dir='/home/nmaldaner/projetos/output/solar-noaa-serie/media';fs.mkdirSync(dir,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
for (const [nome,url] of [
 ['dashboard','https://www.spaceweather.gov/communities/space-weather-enthusiasts-dashboard'],
 ['fenomenos-noaa','https://www.spaceweather.gov/phenomena'],
 ['escala-noaa','https://www.spaceweather.gov/noaa-scales-explanation'],
 ['erupcoes-pt','https://www.spaceweatherlive.com/pt/atividade-solar/erupcoes-solares.html'],
]) {
 await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
 await page.waitForTimeout(8000);
 await page.screenshot({path:`${dir}/${nome}-inteiro.png`,fullPage:true});
 const heading=page.locator('h1').first();
 if(await heading.count()) await heading.scrollIntoViewIfNeeded();
 await page.screenshot({path:`${dir}/${nome}.png`});
 fs.writeFileSync(`${dir}/${nome}.txt`,await page.locator('body').innerText());
 console.log(nome,page.url());
}
await browser.close();
