const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {simulate}=require('../domain.js');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
test('partial final redemption conserves book assets',()=>{
 const r=simulate(.25,.1,.2);assert.equal(r.length,3);near(r[2].paid,5);near(r[2].assets,68.75);
 near(r.reduce((s,x)=>s+x.loss,0),6.25);
});
test('exhaustion preserves the unmet claim',()=>{const r=simulate(1,.1,.5);near(r.at(-1).assets,0);near(r.at(-1).pending,50);});
test('zero requests and no haircut edge cases',()=>{assert.deepEqual(simulate(0,.1,.15),[]);near(simulate(.3,.1,0).at(-1).assets,70);});
test('invalid assumptions fail instead of looping',()=>{for(const args of [[.3,0,.15],[.3,.1,1],[-1,.1,.2],[NaN,.1,.2],[.3,Infinity,.2]])assert.throws(()=>simulate(...args),RangeError);});
test('accounting identity holds across slider domain',()=>{
 for(let request=0;request<=100;request+=5)for(let gate=1;gate<=25;gate+=3)for(let haircut=0;haircut<=75;haircut+=5){
  const rows=simulate(request/100,gate/100,haircut/100);let paid=0,loss=0;
  for(const r of rows){paid+=r.paid;loss+=r.loss;near(r.assets+paid+loss,100);near(r.pending+paid,request);assert.ok(r.paid<=gate+1e-9);assert.ok(r.assets>=0&&r.pending>=0);}
  assert.ok(rows.length<=100);
 }
});
test('browser and Python default scenarios agree',()=>{
 const fixture=JSON.parse(fs.readFileSync(path.join(__dirname,'../public/research.json'))).liquidity;
 const actual=simulate(.3,.1,.15);assert.equal(actual.length,fixture.length);
 actual.forEach((r,i)=>{near(r.assets,fixture[i].remaining_assets);near(r.pending,fixture[i].withdrawals_left);near(r.paid,fixture[i].redemption_paid);near(r.loss,fixture[i].haircut_loss);});
});
test('static distribution has all local assets and no remote runtime dependencies',()=>{
 const dist=path.join(__dirname,'../../dist');const html=fs.readFileSync(path.join(dist,'index.html'),'utf8');
 for(const m of html.matchAll(/(?:src|href)="([^"]+)"/g)){const v=m[1];if(v.startsWith('#')||v.startsWith('data:')||v.startsWith('https:'))continue;assert.ok(fs.existsSync(path.join(dist,v)),`Missing ${v}`);}
 assert.ok(!/<script[^>]*src="https?:/.test(html));
 const data=JSON.parse(fs.readFileSync(path.join(dist,'research.json')));
 assert.equal(data.credit.train_rows+data.credit.test_rows,data.credit.rows);
 assert.ok(data.credit.models.every(m=>m.roc.every(p=>p.x>=0&&p.x<=1&&p.y>=0&&p.y<=1)));
 assert.ok(!('loans' in data.credit));
});
