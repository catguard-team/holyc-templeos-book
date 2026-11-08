from pathlib import Path
import json,re,html,sys,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'manuscript'))
import markdown
from content import PAGES
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'book'
SOURCES=json.loads((BASE/'evidence/sources.json').read_text(encoding='utf-8'))
CSS=''
for role in ('body','bold','title','pixel','window','code'):
 file='IBMPlexMono-Regular.ttf' if role in ('code','pixel') else 'NotoSansKR-Variable.ttf'
 CSS+='@font-face{font-family:"'+role+'";src:url("../assets/fonts/'+file+'");font-style:normal;font-weight:100 900;}\n'
CSS+='''
@page{size:A4;margin:21mm 20mm 21mm 25mm;
 @top-left{content:"HOLYC / TEMPLEOS";font:7pt "pixel";color:#6b657c;}
 @top-right{content:string(running);font:7pt "body";color:#6b657c;}
 @bottom-left{content:"읽기 · 만들기 · 나누기";font:7.5pt "body";color:#756b61;}
 @bottom-right{content:counter(page);font:11pt "pixel";color:#303357;}
}
@page:left{margin-left:20mm;margin-right:25mm;}
@page cover{margin:0;@top-left{content:none;}@top-right{content:none;}@bottom-left{content:none;}@bottom-right{content:none;}}
*{box-sizing:border-box;}body{margin:0;color:#242a40;font:10.5pt/1.77 "body";}
p{margin:0 0 3.3mm;orphans:2;widows:2;word-break:keep-all;overflow-wrap:anywhere;}
h1{font:900 32pt/1.35 "title";margin:4mm 0 10mm;letter-spacing:-.25pt;bookmark-level:2;}
h1 span{display:block;}h2{font:14pt/1.4 "bold";margin:5mm 0 3mm;}
strong,b{font-family:"bold";font-weight:700;}
.sheet{break-before:page;min-height:253mm;position:relative;padding-bottom:13mm;}
.kicker{font:9pt "pixel";letter-spacing:.4pt;color:#886d35;border-top:2pt solid #b79b5f;padding-top:3mm;string-set:running content();}
.rule{height:1px;background:#dfd9cf;margin:6mm 0;}
.refs{position:static;margin-top:6mm;border-top:.5pt solid #dad4cc;padding-top:2mm;font:7pt/1.4 "body";color:#716c7d;}
.refs a{color:inherit;}
a{color:#514a7d;text-decoration:none;overflow-wrap:anywhere;}
code{font:8.7pt/1.55 "code","body";background:#f0eef4;}
pre{font:8.7pt/13.5pt "code";white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f1f6;margin:0 0 4mm;padding:3mm 4mm;border-left:2pt solid #a99ad2;tab-size:2;}
pre code{font:inherit;background:none;}
.codebox{break-inside:avoid;margin:4mm 0;}
.codelabel{font:8pt "pixel";background:#303357;color:#fffdf8;padding:2mm 4mm;}
.codepath{font:7pt/1.4 "body";background:#eae5f1;padding:1.5mm 4mm;color:#625b77;}
code:not(pre code){padding:0 .5mm;}
table{width:100%;border-collapse:collapse;table-layout:fixed;margin:4mm 0 6mm;font:9pt/1.6 "body";}
thead{display:table-header-group;}th{background:#f3ebdc;font-family:"bold";font-weight:700;}
th,td{padding:2.4mm 2.8mm;text-align:left;vertical-align:top;border-bottom:.5pt solid #d9d3cd;word-break:keep-all;overflow-wrap:anywhere;}
tr{break-inside:avoid;}
ul,ol{padding-left:6mm;margin:3mm 0 5mm;}li{margin-bottom:2mm;}
blockquote{margin:7mm 0;padding:4mm 5mm;background:#f1edf8;border-left:2pt solid #9e8bc6;font:11pt/1.8 "body";}
blockquote p:last-child{margin:0;}
.front h1{font-size:36pt;margin:12mm 0;}.front p{line-height:1.9;}
.part{padding-top:8mm;background:#fffdf8;}.part h1{font-size:42pt;margin:7mm 0 7mm;bookmark-level:1;}.part p{font-size:12pt;line-height:1.85;max-width:150mm;}.part .roman{font:58pt "pixel";color:#ac9bcb;margin-top:8mm;}.part .arch{width:50mm;height:75mm;position:static;margin:6mm 0 0 auto;}
.cover{page:cover;width:210mm;height:297mm;position:relative;background:#fffdf8;padding:22mm 25mm;color:#303357;}
.cover .band{position:absolute;right:0;top:0;width:77mm;height:297mm;background:#f0e6d6;}
.cover .arch{position:absolute;width:95mm;height:154mm;right:7mm;top:111mm;}
.cover .top{position:relative;font:9pt "pixel";border-bottom:.8pt solid #8e794e;padding-bottom:5mm;letter-spacing:.6pt;}
.cover .eyebrow{position:relative;margin-top:16mm;font:12pt "bold";}
.cover h1{position:relative;font:900 53pt/1.22 "title";letter-spacing:-1pt;margin:8mm 0 8mm;bookmark-level:1;}
.cover .sub{position:relative;font:17pt/1.65 "bold";margin-top:6mm;}
.cover .holy{position:relative;font:12pt "pixel";letter-spacing:1pt;margin-top:6mm;}
.cover .bottom{position:absolute;bottom:22mm;left:25mm;right:25mm;border-top:.8pt solid #8e794e;padding-top:5mm;font:10pt/1.8 "body";}
.cover .seal{position:absolute;right:14mm;top:44mm;font:9pt/1.5 "window";color:#715b32;border:1pt solid #b59c67;padding:4mm;text-align:center;background:#fff8e9;}
.tocrow{display:flex;gap:4mm;padding:3mm 0;border-bottom:.5pt solid #ded7cf;font:10pt/1.6 "body";}
.tocrow:after{content:target-counter(attr(href),page);margin-left:auto;font:11pt "pixel";color:#8d713d;}
.tocrow span{font-family:"pixel";color:#8d713d;min-width:13mm;}
.source{margin-bottom:5mm;padding-bottom:3mm;border-bottom:.5pt solid #ddd5ca;}
.source b{font-size:10pt;}.source p{font-size:8pt;line-height:1.6;margin:1mm 0;}.source a{font:7pt/1.5 "body";word-break:break-all;}
.diagram{display:flex;gap:3mm;margin:7mm 0 4mm;}.diagram div{flex:1;padding:4mm 3mm;background:#f3ebdc;border-top:2pt solid #b79b5f;font:10pt/1.65 "bold";}.diagram small{display:block;font:8.5pt/1.6 "body";margin-top:2mm;}
.closing{padding-top:10mm;}.closing p{line-height:2;}
'''

def arch():
 return '''<svg viewBox="0 0 260 390" xmlns="http://www.w3.org/2000/svg"><path d="M26 375V162C26 75 130 20 130 20S234 75 234 162V375Z" fill="#d9d0e9" stroke="#a58a50" stroke-width="2"/><path d="M43 375V164C43 91 130 41 130 41S217 91 217 164V375Z" fill="#fffaf0" stroke="#a58a50" stroke-width="1.2"/><path d="M58 373V170C58 106 130 61 130 61S202 106 202 170V373Z" fill="#ebe4f4"/><path d="M130 64V373M58 230H202M61 170H199" stroke="#a58a50" stroke-width="2"/><path d="M123 125H137V212H123ZM101 151H159V165H101Z" fill="#b59b61"/><path d="M75 373V278H185V373" fill="#f6dfca"/><path d="M97 373V290H163V373" fill="#303357"/><path d="M130 290V373" stroke="#b59b61" stroke-width="2"/><path d="M12 376H248M5 386H255" stroke="#a58a50" stroke-width="2"/></svg>'''

CSS+="""
.figure{margin:7mm 0;padding:6mm;background:#faf7f0;border:.7pt solid #d2c3a2;break-inside:avoid;}
.figure .caption{font:8pt/1.6 "body";color:#70677a;margin-top:4mm;}
.memoryrow{display:flex;align-items:center;gap:5mm;margin:5mm 0;}
.memoryrow div{width:43mm;border:1pt solid #b49b65;padding:5mm;background:#eee8f5;font:11pt "code";}
.memoryrow b{font:12pt "bold";display:block;margin-bottom:3mm;}
.bitrow{display:flex;gap:2mm;margin:3mm 0 5mm;align-items:center;}
.bitrow em{width:35mm;font:9pt "body";font-style:normal;}
.bit{width:10mm;text-align:center;border:.7pt solid #b49b65;background:#e7e2eb;padding:3mm 0;font:10pt "code";}
.bit.on{background:#e7c972;}
"""
def figure(key):
 if key=='address':
  return '<div class="figure"><div class="memoryrow"><div><b>address</b>&amp;lamp</div><span>가리킨다 →</span><div><b>lamp</b>3</div></div><p style="font-family:code">*address = 7;</p><div class="memoryrow"><div><b>address</b>&amp;lamp</div><span>가리킨다 →</span><div><b>lamp</b>7</div></div><div class="caption">위치 관계는 같고, 가리킨 자리의 값이 바뀝니다.</div></div>'
 if key=='coordinates':
  return '<div class="figure"><svg viewBox="-25 -20 300 220" style="width:100%;height:103mm" xmlns="http://www.w3.org/2000/svg"><path d="M0 180V0H250M245 -4L250 0L245 4M-4 175L0 180L4 175" fill="none" stroke="#303357" stroke-width="1.2"/><path d="M40 0V170M140 0V170M190 0V170M0 60H230M0 90H230M0 120H230M0 150H230" fill="none" stroke="#ddd4c4" stroke-width=".5"/><rect x="40" y="60" width="100" height="60" fill="#aca6d9" stroke="#454a78"/><circle cx="190" cy="90" r="30" fill="none" stroke="#b56051" stroke-width="2"/><path d="M40 150H220" stroke="#5c8a6b" stroke-width="2"/><circle cx="40" cy="60" r="2.5" fill="#303357"/><circle cx="190" cy="90" r="2.5" fill="#b56051"/><text x="40" y="53" style="font-family:code;font-size:8px">(40,60)</text><text x="158" y="83" style="font-family:code;font-size:8px">(190,90)</text><text x="72" y="94" style="font-family:code;font-size:8px">100 x 60</text><text x="7" y="-5" style="font-family:code;font-size:8px">(0,0)</text><text x="252" y="3" style="font-family:code;font-size:10px">x</text><text x="-3" y="194" style="font-family:code;font-size:10px">y</text><text x="75" y="164" style="font-family:code;font-size:8px">y = 150</text></svg></div>'
 if key=='bits':
  out='<div class="figure">'
  for label,state in [('시작 / 0',0),('1 누름 / 1',1),('3 누름 / 5',5),('1 누름 / 4',4)]:
   out+='<div class="bitrow"><em>'+label+'</em>'+''.join('<div class="bit'+(' on' if state&(1<<i) else '')+'">'+str(i+1)+'</div>' for i in range(7))+'</div>'
  return out+'<div class="caption">금색은 켜진 등불, 연회색은 꺼진 등불입니다.</div></div>'
 raise ValueError(key)

includes=[]
def code_expand(match):
 file=match.group(1);start=int(match.group(2) or 1);end=int(match.group(3)) if match.group(3) else None
 raw=(BASE/'examples'/file).read_text(encoding='utf-8');lines=raw.splitlines(keepends=True);code=''.join(lines[start-1:end]);includes.append({'file':file,'start':start,'end':end or len(lines),'sha256':hashlib.sha256(code.encode()).hexdigest(),'text':code})
 label=file+(' / 이어지는 전체 코드' if start>1 else '')
 return '\n\n<div class="codebox"><div class="codelabel">'+html.escape(label)+'</div><div class="codepath">TempleOS · 작업 폴더 / '+html.escape(file)+'</div><pre><code>'+html.escape(code)+'</code></pre></div>\n\n'

def md(txt):
 txt=re.sub(r'\{\{FIGURE:([a-z]+)\}\}',lambda m:figure(m.group(1)),txt)
 txt=re.sub(r'\{\{CODE:([A-Z0-9.]+)(?::(\d+):([0-9]*))?\}\}',code_expand,txt)
 return markdown.markdown(txt,extensions=['markdown.extensions.tables','markdown.extensions.fenced_code','markdown.extensions.sane_lists'])

pages=[]
cover='<section class="cover"><div class="band"></div><div class="top">A SMALL OFFERING / KOREAN LEARNING EDITION</div><div class="eyebrow">Terry A. Davis의 뜻을 읽고, 직접 만드는</div><h1>작은 성전을<br>짓는 코드</h1><div class="sub">HolyC · TempleOS<br>처음 배우는 강의 책</div><div class="holy">READ · MAKE · SHARE</div><div class="arch">'+arch()+'</div><div class="bottom"><b>단순하게 이해하고, 정성껏 만들기</b><br>첫 문장에서 그림과 소리, 일곱 등불 프로젝트까지<br><span>한국어 학습판 · 2026년 11월</span></div></section>'
body=cover
# TOC references the first page for every numbered lesson.
chapter_starts=[];seen=set()
for i,p in enumerate(PAGES):
 if re.match(r'^\d',p['ch']) and p['ch'][:2] not in seen:
  seen.add(p['ch'][:2]);chapter_starts.append((i,p))
for idx,p in enumerate(PAGES):
 if idx==3:
  for half in (chapter_starts[:10],chapter_starts[10:]):
   body+='<section class="sheet toc"><div class="kicker">CONTENTS / 차례</div><h1>배움의 순서</h1>'
   for j,q in half:body+='<a class="tocrow" href="#p%d"><span>%s</span>%s</a>'%(j,q['ch'][:2],html.escape(q['ch'].split(' · ')[1]+' / '+q['title'].replace('\n',' ')))
   if half is not chapter_starts[:10]: pass
   body+='<p style="margin-top:9mm;font-size:9pt">각 강의의 설명을 읽고 전체 예제를 실행합니다.<br>부록에는 문제 해설·수업안·근거 자료를 모았습니다.</p></section>'
 kind=p['kind'];text=md(p['text']);refs=' · '.join('<a href="#src%s">%s</a>'%(s,s) for s in re.findall(r'S\d+',p['refs']))
 title=''.join('<span>'+html.escape(t)+'</span>' for t in p['title'].split('\n'))
 body+='<section class="sheet '+kind+'" id="p'+str(idx)+'"><div class="kicker">'+html.escape(p['ch'])+'</div>'
 if kind=='part':body+='<div class="roman">'+p['ch']+'</div>'
 body+='<h1>'+title+'</h1>'+text
 if kind=='part':body+='<div class="arch">'+arch()+'</div>'
 if p['title']=='상태와 그림을\n나누기':body+='<div class="diagram"><div>입력<small>키를 읽는다</small></div><div>상태<small>값을 바꾼다</small></div><div>그림<small>현재 값을 그린다</small></div></div>'
 if kind not in ('part',):body+='<div class="refs">근거 '+refs+' · 자세한 출처는 책 뒤의 자료 목록</div>'
 body+='</section>'
for start in range(0,len(SOURCES),5):
 body+='<section class="sheet"><div class="kicker">SOURCES / 조사 자료</div><h1>자료와 근거 '+str(start//5+1)+'</h1>'
 if start==0:body+='<p style="font-size:8.5pt">열람일 2026-11-08. Terry의 문서는 원저자 자료의 보존본이며, 보존 사이트 운영자를 원저자로 표기하지 않았습니다. 소스의 고정 커밋과 파일 해시는 연구 기록에 있습니다.</p>'
 for s in SOURCES[start:start+5]:body+='<div class="source" id="src%s"><b>%s · %s</b><p>%s</p><p>%s</p><a href="%s">%s</a></div>'%(s['id'],s['id'],html.escape(s['title']),html.escape(s['author']),html.escape(s['note']),html.escape(s['url']),html.escape(s['url']))
 body+='</section>'
body+='''<section class="sheet"><div class="kicker">EDITION / 판권과 제작 정보</div><h1>이 책에 대하여</h1><p><b>작은 성전을 짓는 코드</b><br>HolyC · TempleOS 처음 배우는 강의 책<br>한국어 학습판 · 2026년 11월 8일</p><p>원 운영체제·언어·기술 문서: Terry A. Davis<br>제작 요청: 박성모<br>본 학습판의 한국어 설명과 실습 예제는 새로 작성했습니다. 원저자의 공식 교재나 저자 승인판으로 표시하지 않습니다.</p><p>원본 TempleOS 자료의 public domain 안내는 공식 보존 사이트를 따릅니다. 후속 프로젝트와 외부 문서의 이용 조건은 각 원출처를 따릅니다. 이 책의 실습 파일은 학습하고 수정할 수 있도록 함께 제공합니다.</p><p>이 HTML판은 함께 보관한 Noto Sans KR와 IBM Plex Mono 공개 서체를 사용합니다. 원래 디자인의 PDF·INDD·IDML도 별도로 제공합니다. 새로운 원고·예제·디자인에는 CC0 1.0을 적용하며 외부 자료와 서체는 각각의 이용 조건을 따릅니다.</p><p>본 학습판의 코드 실행·지면·원본 대조 결과는 함께 제공하는 검증 기록에서 확인할 수 있습니다. 사용자가 확인한 환경과 제작 중 확인한 환경을 구분해 기록합니다.</p><div class="diagram"><div>읽기<small>원문과 코드를 이해하기</small></div><div>만들기<small>한 가지를 바꿔 확인하기</small></div><div>나누기<small>다음 사람이 읽을 수 있게</small></div></div></section>'''
htmltext='<!doctype html><html lang="ko"><meta charset="UTF-8"><title>작은 성전을 짓는 코드 - HolyC · TempleOS</title><style>'+CSS+'</style><body>'+body+'</body></html>'
CSS+='@media screen{body{max-width:210mm;margin:0 auto;background:#e7e4df}.sheet{background:white;padding:21mm 20mm 21mm 25mm;margin:12px 0;min-height:297mm}.cover{margin:12px 0}.tocrow:after{content:none}}'
htmltext='<!doctype html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>작은 성전을 짓는 코드</title><style>'+CSS+'</style></head><body>'+body+'</body></html>'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'index.html').write_text(htmltext,encoding='utf-8')
(BASE/'manuscript/pages.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(BASE/'evidence/html-code-inclusions.json').write_text(json.dumps(includes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'html':str(OUT/'index.html'),'content_pages':len(PAGES),'code_blocks':len(includes),'source_entries':len(SOURCES)},ensure_ascii=False))
