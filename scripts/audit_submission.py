"""ตรวจตารางและข้อมูลกราฟ HTML กับผลจาก kernel โดยไม่ fit โมเดลเพิ่ม."""
import base64,csv,hashlib,json,re,sys
from pathlib import Path
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import config
sys.stdout.reconfigure(encoding='utf-8')
records=[]
def check(label,ok,actual='',expected=''):
 records.append(dict(check=label,passed=bool(ok),actual=str(actual),expected=str(expected)))
 if not ok:print('FAIL',label,actual,expected)
def numeric(label,cells,expected):
 tokens=re.findall(r'[-+]?\d+(?:\.\d+)?',' '.join(c.get_text(' ',strip=True) for c in cells).replace(',','').replace('−','-'))
 actual=[float(t) for t in tokens]
 ok=len(tokens)==len(expected) and all(abs(a-e)<=0.50001*10**(-len(t.split('.')[1]) if '.' in t else 0) for a,e,t in zip(actual,expected,tokens))
 check(label,ok,actual,expected)
def main():
 r=json.loads((ROOT/'verification/results.json').read_text(encoding='utf-8')); t=r['tables']
 raw=pd.read_csv(config.RAW_CSV,encoding=config.RAW_ENCODING)
 df=pd.read_csv(config.DATA_CSV,encoding=config.RAW_ENCODING).rename(columns=config.COLUMN_MAP)
 check('raw dimensions',list(raw.shape)==[8760,14],list(raw.shape),[8760,14])
 check('raw no missing',raw.isna().sum().sum()==0)
 check('processed nine missing',df.isna().sum().sum()==9)
 check('input 18 features',len(r['features'])==18)
 for p in sorted((ROOT/'notebooks').glob('*.ipynb')):
  nb=json.loads(p.read_text(encoding='utf-8'));code=[c for c in nb['cells'] if c['cell_type']=='code']
  check(p.name+' sequence',[c['execution_count'] for c in code]==list(range(1,len(code)+1)))
  check(p.name+' no errors',not any(o.get('output_type')=='error' for c in code for o in c['outputs']))
 docs={str(p.relative_to(ROOT)):BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser') for p in [ROOT/'reports/report.html',*sorted((ROOT/'slides').glob('*.html'))]}
 full=t['baselines']+t['compare']
 resources=[[e['CV MAE'],e['± std'],e['fit ทั้ง train (s)'],e['latency / 1 แถว (ms)']] for e in t['clo4']]
 fs=[]
 for name in ['Linear Regression','kNN','Random Forest','HistGradientBoosting']:
  fs.append([v for method in ['Baseline','Filter F','Filter MI','Wrapper RFE','Embedded'] for e in t['fs_results'] if e['model']==name and e['method']==method for v in [e['CV MAE'],e['std']]])
 errors=sorted(t['season_errors'],key=lambda e:e['seasons'])+t['day_errors']+t['rain_errors']
 for filename,s in docs.items():
  for i,table in enumerate(s.find_all('table')):
   if not table.find('tr'):continue
   h=table.find('tr').get_text(' ',strip=True)
   rows=[tr.find_all('td') for tr in table.find_all('tr')[1:] if tr.find_all('td')]
   label=filename+' table '+str(i)
   if re.search(r'\bMSE\b',h) and 'RMSE' in h and ('train' in h or 'Baseline' in h):
    expected=full if len(rows)==7 else t['baselines']
    for j,(cells,e) in enumerate(zip(rows,expected)):
     vals=[e[k] for k in ['MAE','MAE_std','MSE','RMSE','R2']]
     if 'train' in h:vals+=[e['MAE_train']]+([e['gap (CV − train)']] if 'gap (CV − train)' in e else [])
     numeric(label+f' row {j}',cells[1:],vals)
   elif 'fit' in h and 'ms/แถว' in h:
    for j,(cells,e) in enumerate(zip(rows,resources)):numeric(label+f' row {j}',cells[-3:],e)
   elif 'Embedded' in h and 'MI' in h:
    for j,(cells,e) in enumerate(zip(rows,fs)):numeric(label+f' row {j}',cells[1:],e)
   elif 'ไม่มี' in h and '25' in h:
    for j,(cells,e) in enumerate(zip(rows,t['pca_table'])):numeric(label+f' row {j}',cells[1:],[e[k] for k in ['ไม่มี PCA','PCA 5','PCA 10','PCA 15','PCA 20','PCA 25']])
   elif 'วันที่' in h and 'error' in h and len(rows)==10:
    for j,(cells,e) in enumerate(zip(rows,t['worst'])):numeric(label+f' row {j}',[cells[k] for k in [1,2,3,4,6,7,8]],[e['hour'],e['temp_c'],e['humidity_pct'],e['rainfall_mm'],e['y'],round(e['pred']),round(e['error'])])
   elif 'ขอบเขต' in h and 'MAE' in h and len(rows)==3:
    for j,(cells,e) in enumerate(zip(rows,t['scope_sensitivity'])):numeric(label+f' row {j}',cells[1:],[e['n hours']]+([e['n days']] if 'วัน' in h else [])+[e['MAE'],e['RMSE']]+([e['R2']] if 'R²' in h else []))
   elif 'bias' in h and len(rows)==8:
    for j,(cells,e) in enumerate(zip(rows,errors)):numeric(label+f' row {j}',cells[1:],[e[k] for k in ['n','mean_y','MAE','bias','MAE / mean_y (%)']])
   elif 'fold' in h and 'mean' in h:
    for j,(cells,e) in enumerate(zip(rows,t['fold_table'])):numeric(label+f' row {j}',cells,[e[k] for k in ['fold','train วัน','val วัน','วันซ้ำ train-val','scaler mean temp_c','imputer median humidity']]+([e['y เฉลี่ยใน val']] if 'mean y' in h else []))
  for im in s.find_all('img'):
   src=im.get('src','')
   if src.startswith('data:'):check(filename+' embedded '+im.get('alt',''),hashlib.sha256(base64.b64decode(src.split(',')[1])).hexdigest() in r['sha256'].values())
   else:check(filename+' image '+src,(ROOT/Path(filename).parent/src).exists())
  check(filename+' no CDN fonts',not s.select('link[href^="https://fonts."]'))
  for old in ['จำนวนนับต่อเนื่อง','ผล test ครั้งเดียว']:check(filename+' obsolete '+old,old not in s.get_text())
 source=(ROOT/'slides/seoul-bike-presentation.html').read_text(encoding='utf-8')
 df['date']=pd.to_datetime(df['date'],format=config.DATE_FORMAT)
 dates=pd.to_datetime(pd.read_csv(config.TRAIN_DATES)['date']);op=df.loc[df.date.isin(dates)&df.functioning_day.eq('Yes')].copy()
 hist=json.loads(re.search(r'const HIST=\{counts:(\[.*?\])',source)[1]);check('JS histogram',hist==np.histogram(op.rented_bike_count,bins=30)[0].tolist())
 daytype=np.select([op.holiday.eq('Holiday'),op.date.dt.dayofweek.ge(5)],['holiday','weekend'],'weekday')
 hourly=op.assign(day_type=daytype).pivot_table(index='hour',columns='day_type',values='rented_bike_count',aggfunc='mean').round().astype(int)
 for key in ['weekday','weekend','holiday']:check('JS hourly '+key,json.loads(re.search(key+r':(\[.*?\])',source)[1])==hourly[key].tolist())
 arr=json.loads(re.search(r'const MODELS=(\[.*?\]);',source,re.S)[1]);check('JS model bars',[e[1] for e in arr]==[round(e['MAE'],3) for e in full])
 arr=json.loads(re.search(r'const SCEN=(\[.*?\]);',source,re.S)[1]);check('JS scenario predictions',[e[1] for e in arr]==[int(e['ทำนาย (คัน/ชม.)']) for e in t['scenarios']])
 arr=json.loads(re.search(r'const TEST_DAYS=(\[.*?\]);',source,re.S)[1]);testdays=pd.to_datetime(pd.read_csv(config.TEST_DATES)['date']);check('JS test calendar',arr==((testdays-df.date.min()).dt.days).tolist())
 arr=json.loads(re.search(r'const TEMP=(\[.*?\]);',source,re.S)[1]);means=op.groupby(pd.cut(op.temp_c,bins=range(-20,45,5)),observed=True).rented_bike_count.mean().round().astype(int).tolist();check('JS temperature bins',[e[1] for e in arr]==means)
 arr=json.loads(re.search(r'const RAIN=(\[.*?\]);',source,re.S)[1]);means=op.groupby(pd.cut(op.rainfall_mm,[-.1,0,1,5,40]),observed=True).rented_bike_count.mean().round().astype(int).tolist();check('JS rainfall bins',[e[1] for e in arr]==means)
 (ROOT/'verification/content-checks.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 with (ROOT/'verification/table-checks.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['check','passed','actual','expected']);w.writeheader();w.writerows(records)
 failures=sum(not e['passed'] for e in records);print(f'{len(records)} checks, {failures} failed')
 if failures:sys.exit(1)
if __name__=='__main__':main()
