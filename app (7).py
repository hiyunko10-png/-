import streamlit as st
import json, html, copy

st.set_page_config(page_title="문 너머",page_icon="🌒",layout="centered")
VERSION=1
ENDINGS={
"return":("새벽의 귀환","이렌이 문턱을 넘는다. 낯선 하늘의 비는 멎었다. 창에 비친 너의 그림자는 두 개지만, 적어도 둘 다 너를 따라 움직인다."),
"seal":("닫힌 문","너는 연결을 끊었다. 모두가 살아남지는 못했다. 다음 날 휴대폰에서 앱이 사라졌다. 다만 새벽마다 없는 알림의 진동이 느껴진다."),
"exchange":("대신 남은 사람","이렌은 현실로 돌아갔다. 너는 검은 역의 새 안내자가 된다. 첫 메시지를 적는다. ‘이 메시지가 보이면 답장하지 마세요.’"),
"echo":("너의 목소리","문밖의 것은 네 이름으로 대답한다. 너의 가족에게, 너의 친구에게. 네가 마지막으로 보낸 메시지에 읽음 표시가 뜬다."),
"warden":("관리자의 자리","너는 문을 닫지 않고 열쇠를 바꾼다. 이제 누구를 통과시킬지 네가 결정한다. 첫 구조 요청은 너의 목소리로 도착한다."),
"lost":("읽지 않은 메시지","모든 연결이 끊긴다. 창밖에서 아침 햇살이 들어온다. 시계는 01:13을 가리킨다. 너는 같은 아침을 몇 번째 맞는지 기억하지 못한다."),
"escape":("관측 밖으로","휴대폰을 두고 계단을 내려간다. 매 층마다 같은 우산이 놓여 있다. 마지막 문은 바깥으로 열린다. 멀리서 이렌의 목소리가 들리지만 돌아보지 않는다.")}

def fresh():
 return dict(version=VERSION,turn=0,stage=0,trust=0,danger=0,clues=[],flags=[],ending=None,room="이렌",log=[dict(who="시스템",text="01:13 · 이름 없는 연결이 열렸습니다.",room="이렌"),dict(who="이렌",text="답장하지 말라는 문장은 자동으로 붙어요. 저는 이렌이에요. 당신 방에도 비가 오나요?",room="이렌")])

def say(who,text,room=None):
 s=st.session_state.game;s['log'].append(dict(who=who,text=text,room=room or s['room']))

def flag(x):
 s=st.session_state.game
 if x not in s['flags']:s['flags'].append(x)

def clue(x):
 s=st.session_state.game
 if x not in s['clues']:s['clues'].append(x)

def finish(key):
 s=st.session_state.game;s['ending']=key
 say("시스템",f"연결 종료 · {ENDINGS[key][0]}")
 if key not in st.session_state.collection:st.session_state.collection.append(key)

def perform(action,label=None):
 s=st.session_state.game
 if s['ending']:return
 say("나",label or action);s['turn']+=1
 f=s['flags']
 if action=='identity':
  s['trust']+=1;flag('asked');say('이렌','나는 검은 역의 기록원이었어요. 사라진 승객 명부에서 당신 이름을 봤어요. 당신은 아직 오지 않은 승객이에요.')
 elif action=='proof':
  clue('역 시계: 01:13');say('이렌','[사진 설명] 물에 잠긴 승강장. 시계는 01:13. 내 손목의 붉은 끈이 물에 비쳐 있어요. 사진 위에 ‘문은 초대받은 이름만 통과시킨다’는 글씨가 보여요.')
 elif action=='room':
  clue('거울 속 문장: 이름 대신 기억');say('시스템','거울에 김이 서린다. 손으로 닦자 ‘이름 대신 기억을 건네라’는 문장이 남는다. 뒤를 돌아보면 방문은 닫혀 있다.')
 elif action=='window':
  clue('그림자는 초대를 흉내 낸다');s['danger']+=1;say('시스템','창밖의 네 그림자가 먼저 고개를 든다. 입 모양은 분명하다. ‘들어와도 돼?’ 바닥의 물은 창문 쪽이 아니라 휴대폰에서 흘러나온다.')
 elif action=='lie':
  flag('lied');s['trust']-=1;s['danger']+=1;say('이렌','문을 열었다고요? …아니에요. 여기 문은 아직 잠겨 있어요. 당신 말고 누가 답장하고 있나요?')
 elif action=='name':
  flag('named');s['danger']+=2;say('시스템','이름을 전송하자 복도에서 네 이름을 부르는 소리가 난다. 목소리는 네 것과 같다.')
 elif action=='memory':
  flag('memory');s['trust']+=1;say('이렌','당신이 적은 기억을 열쇠에 새겼어요. 이름은 보내지 마세요. 문밖의 것은 기억을 만들 수 없지만 들은 이름은 훔칠 수 있어요.')
 elif action=='verify':
  if '역 시계: 01:13' in s['clues']:
   flag('verified');s['trust']+=1;clue('진짜 이렌: 붉은 끈');say('이렌','내 손목에는 붉은 끈이 있어요. 사진에서도 보였죠? 기록관 계정은 이미 비어 있어요. 그 계정이 무엇을 말하든 믿지 마세요.')
  else:say('이렌','먼저 내 사진을 확인해요. 말로만 증명할 수는 없으니까요.')
 elif action=='block':
  flag('blocked');s['trust']-=1;s['room']='기록관';say('기록관','이렌의 연결을 차단했군요. 현명합니다. 문을 열면 현실로 돌아가게 해드리겠습니다. 이름을 먼저 알려주세요.')
 elif action=='unblock':
  flag('unblocked');s['room']='이렌';say('이렌','다시 연결됐네요. 아직 늦지 않았어요. 누군가 당신에게 이름을 요구했나요?')
 elif action=='archive':
  clue('문 봉쇄 절차');s['danger']+=1;say('기록관','비상 절차: 거울을 가린 뒤 휴대폰의 연결을 끊으십시오. 열쇠를 바꾸려면 이름이 아닌 기억, 그리고 두 세계의 증인이 필요합니다. [마지막 줄은 삭제되었습니다]','기록관')
 elif action=='wait':
  s['danger']+=1;say('시스템','메시지를 보내지 않았다. 문 아래로 젖은 승차권이 밀려 들어온다. 목적지에는 네 방 주소가 적혀 있다.')
 elif action=='cover':
  flag('covered');s['danger']=max(0,s['danger']-1);say('시스템','거울을 천으로 덮었다. 문밖에서 두드리는 소리가 한 번 멈춘다. 휴대폰에서는 여전히 빗물이 떨어진다.')
 elif action=='open':
  if 'named' in f:finish('echo')
  elif 'memory' in f and 'verified' in f and s['trust']>=2 and 'blocked' not in f or ('memory' in f and 'verified' in f and 'unblocked' in f and s['trust']>=2):finish('return')
  else:finish('lost')
 elif action=='seal':
  if '문 봉쇄 절차' in s['clues'] and 'covered' in f:finish('seal')
  else:s['danger']+=2;say('시스템','연결 종료 버튼이 회색으로 변한다. 화면에 ‘반사면이 아직 열려 있습니다’라는 문장이 뜬다. 봉쇄 절차를 알아내야 한다.')
 elif action=='exchange':
  if 'memory' in f:finish('exchange')
  else:say('이렌','대가는 이름이 아니라 기억이에요. 먼저 기억을 하나 건네야 길이 열려요.')
 elif action=='warden':
  if 'memory' in f and 'verified' in f and '문 봉쇄 절차' in s['clues']:finish('warden')
  else:s['danger']+=1;say('시스템','열쇠가 바뀌지 않는다. 화면에 세 개의 빈칸이 보인다. 기억 / 두 세계의 증인 / 봉쇄 기록.')
 elif action=='escape':
  if 'named' in f:finish('echo')
  elif 'covered' in f:finish('escape')
  else:s['danger']+=2;say('시스템','현관문을 열자 똑같은 네 방이 나온다. 열린 반사면을 먼저 가려야 길을 찾을 수 있을 것 같다.')
 if not s['ending']:
  if s['turn']>=3 and s['stage']==0:
   s['stage']=1;say('시스템','새 대화방: 기록관. 문밖에서 세 번의 노크 소리가 난다.','기록관')
  if s['turn']>=6 and s['stage']==1:
   s['stage']=2;say('이렌','문이 곧 열려요. 날 데려가도, 길을 봉쇄해도 돼요. 당신이 대신 넘어오는 방법도 있지만… 그건 부탁할 수 없어요.','이렌')
  if s['danger']>=7:finish('echo' if 'named' in f else 'lost')
  elif s['turn']>=16:finish('lost')

ACTIONS={
'identity':'정체와 목적을 묻는다','proof':'사진으로 증명해 달라고 한다','room':'현실의 방과 거울을 조사한다','window':'창밖을 확인한다','lie':'문을 열었다고 거짓말한다','name':'내 이름을 알려준다','memory':'소중한 기억을 열쇠로 건넨다','verify':'사진과 손목의 표식을 대조한다','block':'이렌을 차단한다','unblock':'이렌과 다시 연결한다','archive':'기록관에서 봉쇄 기록을 찾는다','wait':'답장하지 않고 기다린다','cover':'거울을 천으로 가린다','open':'이렌을 초대하며 문을 연다','seal':'연결을 봉쇄한다','exchange':'내가 대신 넘어간다','warden':'문의 관리자가 된다','escape':'휴대폰을 두고 집 밖으로 나간다'}
RULES=[('거짓말','lie'),('차단 해제','unblock'),('다시 연결','unblock'),('차단','block'),('관리자','warden'),('대신','exchange'),('봉쇄','seal'),('끊','seal'),('가리','cover'),('가린','cover'),('덮','cover'),('사진','proof'),('표식','verify'),('대조','verify'),('검증','verify'),('기록','archive'),('기억','memory'),('이름','name'),('창문','window'),('창밖','window'),('거울','room'),('조사','room'),('정체','identity'),('누구','identity'),('기다','wait'),('나간','escape'),('탈출','escape'),('열','open')]
def parse(text):
 for keyword,act in RULES:
  if keyword in text:return act
 return None

def validate(data):
 if not isinstance(data,dict) or data.get('version')!=VERSION:raise ValueError('지원하지 않는 저장 형식입니다.')
 if set(data)!=set(fresh()):raise ValueError('저장 항목이 올바르지 않습니다.')
 for k in ['turn','stage','trust','danger']:
  if type(data[k]) is not int or not -100<=data[k]<=100:raise ValueError('상태 값 오류')
 if data['room'] not in ['이렌','기록관'] or data['ending'] not in [None,*ENDINGS]:raise ValueError('대화방 또는 엔딩 오류')
 for k in ['clues','flags']:
  if not isinstance(data[k],list) or len(data[k])>100 or any(not isinstance(x,str) or len(x)>300 for x in data[k]):raise ValueError('목록 오류')
 if not isinstance(data['log'],list) or len(data['log'])>500:raise ValueError('대화 기록 오류')
 for m in data['log']:
  if not isinstance(m,dict) or set(m)!=set(['who','text','room']) or any(not isinstance(v,str) or len(v)>4000 for v in m.values()):raise ValueError('메시지 오류')
 return data

if 'game' not in st.session_state:st.session_state.game=fresh()
if 'collection' not in st.session_state:st.session_state.collection=[]
s=st.session_state.game
st.markdown("""<style>
.stApp{background:#0c1019;color:#edf1f7} [data-testid="stSidebar"]{background:#141b29} .head{padding:22px;background:#1b2536;border-radius:20px;border:1px solid #344057;margin-bottom:16px}.tag{color:#f6d875;font-size:12px;letter-spacing:3px}.head h1{font-size:32px;margin:4px 0}.sub{color:#bac7d9;font-size:13px}.row{display:flex;margin:14px 0;flex-direction:column;align-items:flex-start}.row.mine{align-items:flex-end}.sender{font-size:12px;color:#b7c6dc;margin:0 8px 5px}.bubble{background:#243248;color:#f1f5fa;padding:13px 17px;border-radius:4px 17px 17px 17px;max-width:88%;line-height:1.7;white-space:pre-wrap;overflow-wrap:anywhere}.mine .bubble{background:#f4d56e;color:#20242d;border-radius:17px 4px 17px 17px}.system{text-align:center;color:#aebdd1;font-size:12px;padding:14px 8px}.stButton>button{border-radius:12px;min-height:44px} .stCaption{color:#b7c6dc}
</style>""",unsafe_allow_html=True)
with st.sidebar:
 st.title('🌒 문 너머')
 st.caption('선택을 기억하는 판타지 스릴러')
 room=st.radio('대화방',['이렌','기록관'] if s['stage'] else ['이렌'],index=(1 if s['room']=='기록관' and s['stage'] else 0))
 s['room']=room
 st.metric('문이 닫히기까지',f"{max(0,16-s['turn'])} 행동")
 st.progress(min(s['danger']/7,1),text='침입 위험')
 st.caption('실시간 타이머가 아닙니다. 확정한 행동만 시간을 소모합니다.')
 with st.expander('수집한 단서',expanded=True):
  for x in s['clues']:st.write('• '+x)
  if not s['clues']:st.caption('아직 발견한 단서가 없습니다.')
 st.download_button('진행 저장',json.dumps(s,ensure_ascii=False,indent=2),'door_save.json','application/json')
 upload=st.file_uploader('저장 불러오기',type=['json'])
 if st.button('선택한 저장 적용',disabled=upload is None):
  try:
   if upload.size>200000:raise ValueError('저장 파일이 너무 큽니다.')
   loaded=validate(json.loads(upload.getvalue()));st.session_state.game=loaded
   if loaded['ending'] and loaded['ending'] not in st.session_state.collection:st.session_state.collection.append(loaded['ending'])
   st.rerun()
  except (ValueError,TypeError,KeyError) as e:st.error(f'불러올 수 없습니다: {e}')
 with st.expander('새 게임'):
  confirm=st.checkbox('현재 진행을 초기화합니다')
  if st.button('처음부터',disabled=not confirm):st.session_state.game=fresh();st.rerun()
 st.caption(f"이번 세션에서 발견한 엔딩 {len(st.session_state.collection)} / {len(ENDINGS)}")
 with st.expander('플레이 안내'):
  st.write('API 없이 작동하는 규칙 기반 게임입니다. 자유 입력은 키워드로 행동에 매핑됩니다. 인식되지 않는 행동은 진행하지 않습니다. 대화방 전환과 저장은 시간을 소모하지 않습니다. 엔딩 수집 목록은 현재 접속 동안만 유지됩니다.')
st.markdown(f'<div class="head"><div class="tag">CROSSWORLD MESSENGER</div><h1>문 너머</h1><div class="sub">{html.escape(s["room"])} · 연결 불안정 · 현실과의 시차 00:00</div></div>',unsafe_allow_html=True)
st.caption('⚠ 긴장·실종·정체성 침해를 다루는 허구의 이야기입니다. 점프 스케어와 자동 재생 음향은 없습니다.')
for m in s['log']:
 if m['room']!=s['room']:continue
 text=html.escape(m['text']);who=html.escape(m['who'])
 if m['who']=='시스템':st.markdown(f'<div class="system">{text}</div>',unsafe_allow_html=True)
 else:
  cls='row mine' if m['who']=='나' else 'row'
  st.markdown(f'<div class="{cls}"><div class="sender">{who}</div><div class="bubble">{text}</div></div>',unsafe_allow_html=True)
if s['ending']:
 title,desc=ENDINGS[s['ending']];st.divider();st.subheader('ENDING · '+title);st.write(desc)
 st.caption('다른 결말을 찾으려면 초기화하거나 이전 저장을 불러오세요. 단서 확인, 기억 전달, 이름 공개 여부가 결과를 바꿉니다.')
else:
 st.divider()
 group=st.radio('행동 종류',['대화','현실 조사','결단'],horizontal=True)
 groups={'대화':['identity','proof','verify','memory','name','lie','block','unblock','archive'],'현실 조사':['room','window','cover','wait'],'결단':['open','seal','exchange','warden','escape']}
 cols=st.columns(2)
 for i,key in enumerate(groups[group]):
  with cols[i%2]:
   if st.button(ACTIONS[key],key=key,use_container_width=True):perform(key,ACTIONS[key]);st.rerun()
 text=st.chat_input('자유 행동 입력 · 예: 거울을 가린다 / 사진을 요구한다')
 if text:
  if len(text)>500:st.warning('500자 이내로 입력해 주세요.')
  else:
   act=parse(text)
   if act:st.session_state.pending=(act,text)
   else:st.info('아직 지원하지 않는 행동입니다. 위 행동 버튼을 선택하거나 사진·거울·기억·봉쇄 같은 키워드로 입력해 주세요. 시간은 흐르지 않았습니다.')
 if 'pending' in st.session_state:
  act,raw=st.session_state.pending
  st.info('해석한 행동: '+ACTIONS[act])
  a,b=st.columns(2)
  if a.button('이 행동 실행'):
   del st.session_state.pending;perform(act,raw);st.rerun()
  if b.button('취소'):
   del st.session_state.pending;st.rerun()
