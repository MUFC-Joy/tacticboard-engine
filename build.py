import pathlib

APP = r"""
/* =========================================================
   对位引擎 v4.1
   L1 球员本体(players.js) · L2 体系(教练/阵型) · L3 比赛态
   ========================================================= */
'use strict';
var ALIAS={'维拉':'阿斯顿维拉','森林':'诺丁汉森林','纽卡':'纽卡斯尔','纽卡斯尔':'纽卡斯尔'};
function norm(c){return ALIAS[c]||c;}

var POOL={};
PLAYERS.forEach(function(p){ var c=norm(p.club); if(!c||c.indexOf('离开')>=0) return;
  (POOL[c]=POOL[c]||[]).push(p); });
var byName={}; PLAYERS.forEach(function(p){ byName[p.n]=p; });

var TEAMS=['曼联','曼城','阿森纳','利物浦','热刺','切尔西','阿斯顿维拉','纽卡斯尔',
           '诺丁汉森林','埃弗顿','水晶宫','布莱顿','布伦特福德','伯恩茅斯','富勒姆',
           '利兹联','桑德兰','考文垂','伊普斯维奇','赫尔城'];
var GROUPS=[{t:'BIG6',list:['曼城','阿森纳','利物浦','切尔西','热刺']},
            {t:'其余英超球队',list:['阿斯顿维拉','纽卡斯尔','布莱顿','富勒姆','布伦特福德','水晶宫','埃弗顿','诺丁汉森林']},
            {t:'升班马',list:['伯恩茅斯','利兹联','桑德兰','考文垂','伊普斯维奇','赫尔城']}];
var CARD={}; PL20.forEach(function(t){CARD[t.name]=t;});

/* ---------------- L2 体系层：换帅只改这里 ---------------- */
var FORM_SEL={};
var FORM_OVERRIDE={'曼联':'4-2-3-1','曼城':'4-2-3-1','阿森纳':'4-2-3-1','利物浦':'4-2-3-1','热刺':'4-2-3-1','切尔西':'3-4-2-1'};
var STYLE_FIX={
 '曼联':{press:2,control:3,direct:2,low:1},
 '曼城':{press:2,control:4,direct:1,low:0},
 '阿森纳':{press:3,control:3,direct:1,low:1},
 '利物浦':{press:4,control:2,direct:3,low:1},
 '热刺':{press:2,control:4,direct:1,low:1}
};
var PREFERRED={
 '曼联':{form:'4-2-3-1',xi:['拉门斯','达洛特','马奎尔','L.马丁内斯','多古','巴莱巴','蒂勒曼斯','姆贝乌莫','B费','库尼亚','谢什科']},
 '曼城':{form:'4-2-3-1',xi:['多纳鲁马','努内斯','鲁本·迪亚斯','格伊','格瓦迪奥尔','埃利奥特·安德森','恩佐','塞门约','谢尔基','恩迪亚耶','哈兰德']},
 '阿森纳':{form:'4-2-3-1',xi:['拉亚','本·怀特','孔萨','加布里埃尔','卡拉菲奥里','赖斯','刘易斯·斯凯利','萨卡','厄德高','措利斯','哈弗茨']},
 '利物浦':{form:'4-2-3-1',xi:['阿利松','阿劳霍','杰雷米·雅凯','范戴克','科尔克兹','麦卡利斯特','索博斯洛伊','维克托·穆尼奥斯','维尔茨','巴尔克拉','伊萨克']},
 '热刺':{form:'4-2-3-1',xi:['金斯基','范赫克','托辛·阿达拉比奥尤','范德文','罗伯逊','托纳利','阿奇·格雷','库杜斯','马特乌斯·费尔南德斯','马尔穆什','索兰克']},
 '切尔西':{form:'3-4-2-1',xi:['埃米·马丁内斯','阿奇姆蓬','马克桑斯·拉克鲁瓦','科尔威尔','内托','凯塞多','乔丹·亨德森','佩普·查瓦里亚','帕尔默','摩根·罗杰斯','若昂·佩德罗']}
};

var BASE_FORMS=['4-2-3-1','4-3-3','3-4-2-1','4-4-2','4-1-4-1','3-1-6'];
var FORMS={
 '4-2-3-1':[['GK',50,90],['RB',84,72],['CB',62,77],['CB',38,77],['LB',16,72],
            ['DM',62,55],['DM',38,55],['RW',84,34],['AM',50,38],['LW',16,34],['ST',50,14]],
 '4-3-3':[['GK',50,90],['RB',84,72],['CB',62,77],['CB',38,77],['LB',16,72],
          ['CM',70,54],['DM',50,58],['CM',30,54],['RW',82,30],['ST',50,14],['LW',18,30]],
 '3-4-2-1':[['GK',50,90],['CB',70,77],['CB',50,80],['CB',30,77],
            ['RWB',88,54],['CM',62,54],['CM',38,54],['LWB',12,54],
            ['AM',64,32],['AM',36,32],['ST',50,12]],
 '4-4-2':[['GK',50,90],['RB',84,74],['CB',62,78],['CB',38,78],['LB',16,74],
          ['RM',84,50],['CM',62,52],['CM',38,52],['LM',16,50],['ST',62,18],['ST',38,18]],
 '4-1-4-1':[['GK',50,90],['RB',84,74],['CB',62,78],['CB',38,78],['LB',16,74],
            ['DM',50,60],['RM',84,42],['CM',62,44],['CM',38,44],['LM',16,42],['ST',50,16]],
 '3-1-6':[['GK',50,90],['CB',70,78],['CB',50,81],['CB',30,78],['DM',50,60],
          ['LW',10,30],['AM',68,32],['AM',32,32],['RW',90,30],['ST',44,14],['ST',58,14]],
 '5-4-1':[['GK',50,91],['CB',70,75],['CB',50,75],['CB',30,75],
          ['RWB',88,72],['LWB',12,72],
          ['RM',80,54],['CM',60,55],['CM',40,55],['LM',20,54],
          ['ST',50,24]]
};
var POSS_FORMS={
 '3-1-6':[['GK',50,92],['CB',72,80],['CB',50,82],['CB',28,80],['DM',50,56],
          ['LW',10,26],['AM',68,28],['AM',32,28],['RW',90,26],['ST',44,12],['ST',58,12]],
 '4-2-3-1':[['GK',50,92],['RB',88,44],['CB',70,80],['CB',50,82],['LB',12,44],
            ['DM',62,60],['DM',38,60],['RW',80,26],['AM',50,34],['LW',20,26],['ST',50,12]],
 '4-3-3':[['GK',50,92],['RB',88,42],['CB',62,80],['CB',38,80],['LB',12,42],
          ['CM',70,52],['DM',50,62],['CM',30,52],['RW',80,24],['ST',50,12],['LW',20,24]],
 '3-4-2-1':[['GK',50,92],['CB',72,80],['CB',50,82],['CB',28,80],
            ['RWB',88,46],['CM',62,58],['CM',38,58],['LWB',12,46],
            ['AM',64,30],['AM',36,30],['ST',50,12]],
 '4-4-2':[['GK',50,92],['RB',86,50],['CB',62,80],['CB',38,80],['LB',14,50],
          ['RM',84,44],['CM',60,54],['CM',40,54],['LM',16,44],['ST',60,20],['ST',40,20]],
 '4-1-4-1':[['GK',50,92],['RB',88,44],['CB',62,80],['CB',38,80],['LB',12,44],
            ['DM',50,62],['RM',84,40],['CM',62,48],['CM',38,48],['LM',16,40],['ST',50,16]],
 '5-4-1':[['GK',50,92],['CB',70,76],['CB',50,76],['CB',30,76],
          ['RWB',88,50],['LWB',12,50],
          ['RM',80,30],['CM',60,54],['CM',40,54],['LM',20,30],
          ['ST',50,16]]
};
var ADJ={RB:['RWB','CB','RM','LB'],LB:['LWB','CB','LM','RB'],RWB:['RB','RM','RW'],LWB:['LB','LM','LW'],
  CB:['DM','RB','LB'],DM:['CM','CB'],CM:['DM','AM'],AM:['CM','RW','LW','ST'],
  RW:['LW','AM','RWB','RM'],LW:['RW','AM','LWB','LM'],ST:['AM','RW','LW'],RM:['RW','RB'],LM:['LW','LB','GK']};
var GRP={GK:'门',RB:'卫',CB:'卫',LB:'卫',RWB:'卫',LWB:'卫',DM:'中',CM:'中',AM:'中',RM:'中',LM:'中',RW:'锋',LW:'锋',ST:'锋'};

/* ---------------- L3 比赛态 ---------------- */
var S={home:'曼联',away:'曼城',minute:0,hs:0,as:0,
       lineup:{},status:{},events:[],lastDiff:null,snap:null,
       tactic:{},poss:{},subMark:{},weather:'dry'};
function taxOf(t){ return S.tactic[t]||'bal'; }
function possOn(t){ return !!S.poss[t]; }
function setTax(team,v){ S.tactic[team]=v; renderAll(); }
function setWeather(w){ S.weather=(w==='rain'?'rain':'dry'); renderAll(); renderSetup(); }
var KEEP={};
var SHAPES={'3-1-6':'atk','5-4-1':'def'};
function toggleShape(team,shape){
  var cur=formOf(team);
  if(cur===shape){
    var k=KEEP[team]||{};
    FORM_SEL[team]=k.form||(PREFERRED[team]?PREFERRED[team].form:'4-2-3-1');
    changeForm(team,FORM_SEL[team]);
    if(k.lineup) S.lineup[team]=k.lineup.slice();
    if(k.tactic) S.tactic[team]=k.tactic;
    delete KEEP[team];
    renderAll();
    return;
  }
  var base=KEEP[team];
  if(cur==='3-1-6'||cur==='5-4-1'){
    if(!base) base={form:(PREFERRED[team]?PREFERRED[team].form:'4-2-3-1')};
    FORM_SEL[team]=base.form;
    if(base.lineup) S.lineup[team]=base.lineup.slice();
    if(base.tactic) S.tactic[team]=base.tactic;
  }else{
    KEEP[team]={form:cur,lineup:(S.lineup[team]||[]).slice(),tactic:taxOf(team)};
  }
  changeForm(team,shape);
  if(shape==='5-4-1') S.poss[team]=false;
  if(SHAPES[shape]) S.tactic[team]=SHAPES[shape];
  renderAll();
}
function toggleDesperate(team){ toggleShape(team,'3-1-6'); }
function toggleLead(team){ toggleShape(team,'5-4-1'); }
function togglePoss(team){ S.poss[team]=!S.poss[team]; renderAll(); }

function formOf(name){
  if(FORM_SEL[name]) return FORM_SEL[name];
  if(FORM_OVERRIDE[name]) return FORM_OVERRIDE[name];
  var t=CARD[name]; if(!t) return '4-2-3-1';
  var m=(t.sys||'').match(/(\d(?:-\d){1,3})/); return m?m[1]:'4-2-3-1';
}
function coachOf(t){ var c=CARD[t]; return c?(c.mgr||'以官网为准'):'—'; }
function styleOf(name){
  if(STYLE_FIX[name]) return Object.assign({},STYLE_FIX[name]);
  var t=CARD[name]; if(!t) return {press:2,control:2,direct:2,low:1};
  var s=(t.sys||'')+(t.threat||'');
  return {press:/高压|压迫|逼抢|疯狗/.test(s)?3:2,
          control:/控球|围攻|渗透|推进/.test(s)?3:2,
          direct:/转换|反击|直接|长传/.test(s)?3:1,
          low:/低块|低位|摆好|挨打/.test(s)?3:1};
}

/* ---------------- 阵容 ---------------- */
function hurt(p){ return !!(p.status&&/伤|报销|停赛/.test(p.status)); }
function scoreFor(p,slot){
  var sc=0;
  if(p.pos.indexOf(slot)>=0){ sc+=10; if(p.pos[0]===slot) sc+=3; }
  else if(p.pos.some(function(x){return (ADJ[slot]||[]).indexOf(x)>=0;})) sc+=4;
  else if(p.pos.some(function(x){return GRP[x]===GRP[slot];})) sc+=1;
  else sc-=8;
  if(p.a) sc+=(p.a.sta||70)/25;
  return sc;
}
function autoLineup(team){
  var form=formOf(team), slots=FORMS[form]||FORMS['4-2-3-1'];
  var pref=PREFERRED[team];
  if(pref&&pref.form===form&&pref.xi.length===slots.length&&
     pref.xi.every(function(n){return byName[n]&&norm(byName[n].club)===team;})) return pref.xi.slice();
  var list=(POOL[team]||[]).filter(function(p){return !hurt(p);}).slice()
    .sort(function(a,b){return (b.a?1:0)-(a.a?1:0);});
  if(list.length<11) list=(POOL[team]||[]).slice();
  var used={},out=[];
  slots.forEach(function(sl){
    var best=null,bs=-99;
    list.forEach(function(p){ if(used[p.n])return; var sc=scoreFor(p,sl[0]);
      if(sc>bs){bs=sc;best=p;} });
    if(best&&bs>0){used[best.n]=1;out.push(best.n);} else out.push(null);
  });
  return out;
}
function changeForm(team,form){
  if(!FORMS[form]) return;
  FORM_SEL[team]=form;
  var slots=FORMS[form];
  var keep=(S.lineup[team]||[]).filter(Boolean).map(function(n){return byName[n];}).filter(Boolean);
  var all=(POOL[team]||[]).filter(function(p){return !hurt(p);});
  var used={},out=[];
  slots.forEach(function(sl){
    var kb=-99,keepBest=null;
    keep.forEach(function(p){ if(used[p.n])return; var sc=scoreFor(p,sl[0]);
      if(sc>kb){kb=sc;keepBest=p;} });
    var pb=-99,poolBest=null;
    all.forEach(function(p){ if(used[p.n])return; var sc=scoreFor(p,sl[0]);
      if(sc>pb){pb=sc;poolBest=p;} });
    var best=keepBest,bs=kb;
    if(poolBest&&pb>kb+1){best=poolBest;bs=pb;}
    if(best&&bs>0){used[best.n]=1;out.push(best.n);} else out.push(null);
  });
  S.lineup[team]=out;
  log('form',team,form);
  S.lastDiff=null;
  renderAll(); save();
}

/* ---------------- 指标 ---------------- */
var TG=function(p){return p.tags||[];};
function hasT(p,arr){ if(!p) return false; return arr.some(function(t){return TG(p).indexOf(t)>=0;}); }
function stOf(n){ return S.status[n]||'ok'; }
var STMOD={hot:{wing:1,mid:1,behind:1},ok:{},low:{wing:-1,mid:-1,behind:-1},
           inj:{air:-1,mid:-1},yellow:{def:-1,wing:-1},
           out:{def:-3,wing:-3,mid:-3,behind:-3,air:-3}};
function metrics(names){
  var m={wing:0,mid:0,behind:0,air:0,build:0,press:0,def:0};
  (names||[]).filter(Boolean).forEach(function(n){
    var p=byName[n]; if(!p) return;
    var mod=STMOD[stOf(n)]||{};
    if(hasT(p,['逆足内切','顺足下底'])) m.wing+=2+(mod.wing||0);
    if(hasT(p,['内锋','翼卫'])) m.wing+=1;
    if(hasT(p,['破坏型','B2B'])) m.mid+=2+(mod.mid||0);
    if(hasT(p,['组织8','拖后组织','节拍器','现代10','自由10','伪10'])) m.mid+=1+(mod.mid||0);
    if(hasT(p,['逼抢9','全能9','抢点型'])) m.behind+=1+(mod.behind||0);
    if(/爆点|速度|冲击|反击|突/.test(p.st||'')) m.behind+=1+(mod.behind||0);
    if(p.a&&p.a.air) m.air+=p.a.air/10+(mod.air||0);
    else if(hasT(p,['争顶型','支点'])) m.air+=7+(mod.air||0);
    if(hasT(p,['出球型','拖后组织','清球型','节拍器'])) m.build+=1;
    if(hasT(p,['破坏型','逼抢9','B2B'])) m.press+=1;
    var g0=(p.pos||[])[0];
    if(GRP[g0]==='卫'){ m.def+=1+(mod.def||0); if(hasT(p,['上抢型','对抗型','回追型','套边型'])) m.def+=1; }
  });
  return m;
}
function airOf(p){
  if(p.a&&p.a.air) return p.a.air/10;
  if(hasT(p,['争顶型'])) return 8.5;
  if(hasT(p,['支点'])) return 7.5;
  return 4;
}
function slotMap(lineup,form){
  var slots=FORMS[form]||FORMS['4-2-3-1'],o={};
  (lineup||[]).forEach(function(n,i){ if(n&&slots[i]) (o[slots[i][0]]=o[slots[i][0]]||[]).push(n); });
  return o;
}


/* ---------------- 术语词典（白话版） ---------------- */
var TERMS={
 '弧顶':{d:'禁区前面那条弧线的正中央。这里是远射最舒服的位置，也是后腰必须站住的地方——没人站，对面就能随便远射。',pos:'禁区正前方',ex:'曼联被远射打穿，基本都是弧顶没人。'},
 '肋部':{d:'中卫和边后卫之间那条竖着的缝。既不算边路也不算中路，是防守最难受的地方——两个人都会以为"这是他的"。',pos:'禁区两侧的斜向区域',ex:'边锋内切就是往肋部钻。'},
 '半空间':{d:'就是肋部，同一个东西的不同叫法。',pos:'同肋部',ex:'—'},
 '逆足':{d:'右脚球员踢左边、左脚球员踢右边。好处是内切射门顺脚，坏处是下底传中要用非惯用脚。',pos:'边路',ex:'姆贝乌莫左脚踢右路=逆足。'},
 '逆足内切':{d:'逆足球员拿球后往球场中间切，寻找射门角度。防守方最怕这个，因为你以为他会下底。',pos:'禁区角',ex:'萨拉赫、姆贝乌莫的招牌。'},
 '顺足下底':{d:'右脚球员在右路往底线走，然后用惯用脚传中。传统边锋打法。',pos:'底线附近',ex:'多库。'},
 '套边':{d:'边后卫从边锋的外侧绕过去插上，形成二打一。英文 overlap。',pos:'边线外侧',ex:'达洛特压上就是套边。'},
 '内收':{d:'边后卫不站边线，往中路站，变成中场人数优势。曼城、阿森纳最爱这么踢。',pos:'中场偏边',ex:'里科·刘易斯内收。'},
 '低位块':{d:'全队退到自家半场，排成两条横线，把中路堵死，让对手在外围倒脚。也叫"摆大巴"。',pos:'自家禁区前沿',ex:'诺丁汉森林的标准打法。'},
 '高位压迫':{d:'在对方半场就开始抢，不让对手舒服出球。费体力，但抢下来就是单刀。',pos:'对方禁区到中场',ex:'利物浦、布莱顿。'},
 '转换':{d:'抢断成功或丢球后那 3–5 秒。全队攻守角色瞬间对调，是一场比赛最容易进球也最容易丢球的时刻。',pos:'全场',ex:'"被打转换"= 你刚压上去，球丢了，身后一片空。'},
 '反抢':{d:'丢球后不退回防守，而是立刻在原地抢回来。克洛普、瓜迪奥拉都强调这个。',pos:'丢球点附近',ex:'—'},
 '第二落点':{d:'第一点头球或解围之后，球落到哪、谁抢到。这个比第一点更决定比赛。',pos:'禁区前沿、中场',ex:'"抢第二落点"= 混战里谁更凶。'},
 '支点':{d:'中锋背对球门拿球，用身体挡住后卫，把球做给队友。作用像墙。',pos:'中圈到禁区之间',ex:'谢什科就是支点型。'},
 '伪9':{d:'中锋不回禁区，反而回撤到中场拿球，把对方中卫引出来，给队友制造身后空间。',pos:'中场偏前',ex:'齐尔克泽、菲尔米诺。'},
 'B2B':{d:'box-to-box，两个禁区之间来回跑的中场。既能抢又能插上。',pos:'全场',ex:'巴莱巴、B费回撤时都算。'},
 '6号位':{d:'后腰。站在后卫线前面，负责拦截和出球。',pos:'中圈后方',ex:'巴莱巴。'},
 '8号位':{d:'中场，介于后腰和前腰之间，要能跑、能传、能插上。',pos:'中场',ex:'蒂勒曼斯、梅努。'},
 '10号位':{d:'前腰。负责最后一传和创造力。',pos:'对方禁区弧顶',ex:'B费。'},
 '3-2-5':{d:'有球进攻时的站位：3 个后卫 + 2 个后腰 + 5 个人压在前场。现代控球队的标准形状。',pos:'全场',ex:'曼联有球形态就是这个。'},
 '出球':{d:'从后场把球传出去，突破对方的第一道压迫。英文 build-up。',pos:'自家禁区到中场',ex:'出球被锁死，就只能开大脚。'},
 '制空':{d:'高空球的争顶能力。角球、任意球、长传都靠这个。',pos:'禁区',ex:'马奎尔制空 90。'},
 '定位球':{d:'角球、任意球、界外球这类"死球"机会。英超三成进球来自定位球。',pos:'全场',ex:'阿森纳是英超定位球第一。'},
 '弱侧':{d:'球不在的那一边。进攻时把球转到弱侧，往往能打对手一个措手不及。',pos:'球场的另一边',ex:'—'},
 '二点球':{d:'同"第二落点"。',pos:'—',ex:'—'},
 '双后腰':{d:'两个后腰并排站。防守更稳，但进攻人数会少一个。',pos:'中圈后方',ex:'4-2-3-1 的基础。'},
 '边翼卫':{d:'三中卫体系里负责整条边路的人，既要防守也要进攻，跑动量最大。',pos:'边线',ex:'多古、达洛特在三中卫里就是翼卫。'},
 '直塞':{d:'贴着地面、穿过防线缝隙的传球，直接给到身后的队友。',pos:'防线身后',ex:'B费的招牌。'},
 '对抗':{d:'身体接触时的强度。英超最看重这个。',pos:'全场',ex:'—'},
 '禁区六码区':{d:'门将前面那块小禁区，抢点最危险的位置。',pos:'球门前',ex:'—'}
};

/* ---------------- 分析 ---------------- */
var STMARK={hot:'🔥',low:'😑',inj:'🤕',yellow:'🟨',out:'⛔'};
function mk(n){ return STMARK[stOf(n)]||''; }
function statusLine(n){
  var s=stOf(n); var p=byName[n];
  if(!p||s==='ok') return '';
  if(s==='yellow') return `（${p.n} 已吃黄牌，防守动作会收）`;
  if(s==='inj') return `（${p.n} 带伤，覆盖面积下降）`;
  if(s==='low') return `（${p.n} 状态低迷）`;
  if(s==='hot') return `（${p.n} 状态火爆）`;
  return '';
}

function analyze(){
  var H=S.home,A=S.away,hf=formOf(H),af=formOf(A);
  var hl=S.lineup[H]||autoLineup(H), al=S.lineup[A]||autoLineup(A);
  var hp=slotMap(hl,hf), ap=slotMap(al,af);
  var hs=styleOf(H), as=styleOf(A);
  var hLow=Math.max(0,(hs.low||0)-1), hPress=Math.min(5,(hs.press||2)+1);
  var th=taxOf(H), ta=taxOf(A);
  var msgs=[];
  var wet=S.weather==='rain';
  msgs.push({area:'环境',lvl:wet?1:0,c:'infer',
    txt: wet?'雨战：湿滑、球速快，停球/传中容错下降；远射脱手、定位球第二点、长传冲吊的收益上升。':'晴：天气不额外修正，按当前阵型与对位判断。',
    p: wet?'雨天更容易出现脱手、二点和乱战，别只迷信地面配合。':'天气不是这场的主要变量。',
    ev: wet?'当前天气：雨。湿滑场地影响停球、传中、门将脱手和定位球第二点。':'当前天气：晴。'
  });

  /* 0 战术姿态 */
  var taxTxt=[],taxLvl=0;
  if(th!=='bal'){ taxTxt.push(th==='atk'
    ? `${H} 压出去：边后卫会站到中场线，中场投入 +1，但身后空间同步变大`
    : `${H} 收回来：防线压低、弧顶保护优先，但前场只剩反击点`); taxLvl=Math.max(taxLvl,1); }
  if(ta!=='bal'){ taxTxt.push(ta==='atk'
    ? `${A} 压出去：他们会把人数堆到你禁区前沿，你的出球点会被锁死`
    : `${A} 收回来：他们会让你控球，然后打你的转换`); taxLvl=Math.max(taxLvl,1); }
  if(possOn(H)) taxTxt.push(`${H} 切到有球形态：中卫拉开、边后卫内收，变成 3-2-5 出球 —— 这时候身后最危险`);
  if(possOn(A)) taxTxt.push(`${A} 切到有球形态：他们会用 3+2 的结构从后场起球`);
  if(taxTxt.length) msgs.push({area:'姿态',lvl:taxLvl,c:'infer',
    txt:taxTxt.join('；')+'。',
    ev:'姿态是「当时的战术选择」，不是能力值：同一套首发，压出去和收回来是两种风险。'});

  /* 0.5 搏命 */
  var hm=metrics(hl), am=metrics(al);
  var despH=formOf(H)==='3-1-6', despA=formOf(A)==='3-1-6';
  if(despH||despA){
    var who=despH?H:A;
    msgs.push({area:'搏命',lvl:2,c:'infer',
      txt:`${who} 切到 3-1-6：三中卫 + 单后腰 + 6 人压上。禁区里人多、二点球密集、定位球价值翻倍，但中场只剩一层——丢球后一次直塞就是单刀。`,
      ev:'这是「放弃中场换禁区人数」的选择，不是加强进攻，是换一种死法。'});
    if(despH){ hm.mid-=3; hm.def-=2; hm.wing+=2; hm.behind+=2; }
    if(despA){ am.mid-=3; am.def-=2; am.wing+=2; am.behind+=2; }
  }

  /* 1 形态 */
  if(hLow<=1&&(as.low||0)<=1){
    msgs.push({area:'形态',lvl:0,
      txt:`两队都不摆低位（${H} 主场：压迫 +1、低位 −1）→ 控球对攻，回合数多，中场对拼决定谁先崩。`,
      ev:`体系 ${H} ${CARD[H]?CARD[H].sys:''} ／ ${A} ${CARD[A]?CARD[A].sys:''}`});
  }else if(hLow<=1&&(as.low||0)>=2){
    msgs.push({area:'形态',lvl:1,
      txt:`${A} 会摆低位（${CARD[A]?CARD[A].sys:''}），${H} 主控 → 围攻 vs 一脚捅穿，阵地战不会轻松。`,
      ev:`低位倾向 ${H}=${hLow} ／ ${A}=${as.low}`});
  }else{
    var owner=(hs.control||2)>=(as.control||2)?H:A;
    msgs.push({area:'形态',lvl:0,
      txt:`${H} 主场会推到中场（不摆低位），球权重心在 ${owner} 脚下，另一队打转换更划算。`,
      ev:`控球权重 ${H}=${hs.control} ／ ${A}=${as.control}`});
  }

  /* 2 边路 */
  function flank(myTeam,myLu,myForm,opTeam,opLu,opForm){
    var out=[];
    [['RB','LW','右路'],['LB','RW','左路']].forEach(function(pr){
      var fbN=(slotMap(myLu,myForm)[pr[0]]||[])[0], wN=(slotMap(opLu,opForm)[pr[1]]||[])[0];
      var fb=fbN?byName[fbN]:null, w=wN?byName[wN]:null;
      if(!w) return;
      var wIn=hasT(w,['逆足内切']), wWd=hasT(w,['顺足下底']);
      var fbUp=!!(fb&&hasT(fb,['套边型','攻击型'])&&!hasT(w,['翼卫']));
      var hc=fb&&stOf(fb.n)==='yellow';
      if(fbUp&&(wIn||wWd)){
        out.push({lvl:2,area:pr[2],
          txt:`${pr[2]}是主战场：${myTeam} 的 ${fb.n} 要压上（套边型），${opTeam} 的 ${w.n} 正好${wIn?'内切吃内线':'下底拉外线'}——来回拉扯${hc?'，而且他刚吃牌不敢做动作':''}。`,
          ev:`${fb.n} tags=${TG(fb).join('/')} ｜ ${w.n} tags=${TG(w).join('/')} · ${w.foot}脚`});
      }else if(wIn){
        out.push({lvl:2,area:pr[2],
          txt:`${w.n} 内切型（${w.foot||'?'}脚踢${pr[1]}），往肋部钻${fb?'，'+fb.n+'（'+fb.foot+'脚）的内线最吃这套':''}${statusLine(fb?fb.n:'')}。`,
          ev:`${w.n} tags=${TG(w).join('/')}`});
      }else if(fbUp){
        out.push({lvl:2,area:pr[2],
          txt:`${myTeam} 的 ${fb.n} 是套边型，压上后${pr[2]}身后只剩中卫，${opTeam} 抢下球第一脚就找这里。`,
          ev:`${fb.n} tags=${TG(fb).join('/')} · st:${fb.st||''}`});
      }else if(wWd){
        out.push({lvl:1,area:pr[2],
          txt:`${w.n} 顺足下底，会把${pr[2]}的边后卫拉到外线，禁区里必须有人抢第二点。`,
          ev:`${w.n} tags=${TG(w).join('/')}`});
      }
    });
    return out.slice(0,2);
  }
  msgs=msgs.concat(flank(H,hl,hf,A,al,af));

  /* 3 中场 */
  var d=hm.mid-am.mid+(th==='atk'?1:th==='def'?-1:0)-(ta==='atk'?1:ta==='def'?-1:0);
  var mids=function(a){ return a.filter(function(n){ var p=n&&byName[n];
    return p&&(p.pos||[]).some(function(x){return x==='DM'||x==='CM'||x==='AM';}); }).join(' / '); };
  msgs.push({area:'中场',lvl:d<0?2:(d>0?1:0),
    txt:d===0?`中场结构打平（${hm.mid} vs ${am.mid}）：谁先输第二落点，谁就被迫退。`
      :d<0?`中场吃亏（${hm.mid} vs ${am.mid}）：${A} 组织/推进人手更厚，${H} 的双后腰会被拉着横移，弧顶会空。`
            :`中场占优（${hm.mid} vs ${am.mid}）：${H} 的中场配比更完整，能把节奏压住。`,
    ev:`${H}：${mids(hl)}\n${A}：${mids(al)}`});

  /* 4 两条锋线 */
  function lineVsCB(teamName,lu,form,oppName,oppLu,oppForm,label){
    var stN=(slotMap(lu,form).ST||[])[0]; if(!stN) return null;
    var st=byName[stN];
    var cbs=(slotMap(oppLu,oppForm).CB||[]).map(function(n){return byName[n];}).filter(Boolean);
    if(!cbs.length) return null;
    var pusher=cbs.filter(function(c){return hasT(c,['上抢型']);})[0];
    var deeps=cbs.filter(function(c){return hasT(c,['拖后型','回追型']);});
    var names=cbs.map(function(c){return c.n;}).join('+');
    if(hasT(st,['支点'])&&pusher)
      return {lvl:1,area:label,txt:`${st.n} 支点型 9 顶 ${names}：${pusher.n} 是上抢型，会被他背身做墙拉出来，第二落点很难抢${statusLine(st.n)}。`,
              ev:`${st.n} tags=${TG(st).join('/')} ｜ ${pusher.n} tags=${TG(pusher).join('/')}`};
    if(hasT(st,['支点'])&&deeps.length)
      return {lvl:0,area:label,txt:`对面中卫偏拖后（${deeps.map(function(c){return c.n;}).join('+')}）：${st.n} 的做墙压不进去，禁区里人多 → 破局点在外围远射和肋部后插上。`,
              ev:`${st.n} tags=${TG(st).join('/')}`};
    if(hasT(st,['抢点型','逼抢9']))
      return {lvl:1,area:label,txt:`${st.n} 是抢点/逼抢型 9，对 ${names}：他的价值在六码区和小禁区前沿，中卫必须贴身，别让他抢前点。`,
              ev:`${st.n} tags=${TG(st).join('/')}`};
    if(/速度|爆点|冲击|身后/.test(st.st||''))
      return {lvl:2,area:label,txt:`${st.n} 打身后（${st.st||''}），${names} 转身慢就是隐患 —— 防线别压太高。`,
              ev:`${st.n} st:${st.st||''}`};
    return null;
  }
  var l1=lineVsCB(H,hl,hf,A,al,af,'锋线'); if(l1) msgs.push(l1);
  var l2=lineVsCB(A,al,af,H,hl,hf,'对方锋线'); if(l2) msgs.push(l2);

  /* 5 制空 */
  function cbAir(lu,form){
    var cbs=(slotMap(lu,form).CB||[]).map(function(n){return byName[n];}).filter(Boolean);
    return cbs.length?cbs.reduce(function(a,c){return a+airOf(c);},0)/cbs.length:0;
  }
  var ha=cbAir(hl,hf), aa=cbAir(al,af);
  msgs.push({area:'定位球',lvl:ha>=aa?1:2,c:'fact',
    txt:`制空 ${ha.toFixed(1)} vs ${aa.toFixed(1)}（只比中卫组合，0–10）：${ha>=aa?H+' 的高点球是稳定得分点，'+A+' 防空降档。':A+' 的中卫争顶更硬，'+H+' 禁区第一落点会吃亏。'}`,
    ev:`中卫 ${(slotMap(hl,hf).CB||[]).join('+')} vs ${(slotMap(al,af).CB||[]).join('+')}`});
  var PLAIN={
   '形态':'这场球大概会怎么踢：谁控球、谁退守。',
   '右路':'这条边会被反复冲，因为两边的人都习惯往前跑，身后会空。',
   '左路':'这条边会被反复冲，因为两边的人都习惯往前跑，身后会空。',
   '中场':'中场人多的一方控场，人少的一方只能往回退。',
   '锋线':'你的中锋能不能顶住对方中卫，决定球能不能压进对方禁区。',
   '对方锋线':'对方中锋会不会把你的中卫拉出来打身后。',
   '定位球':'角球和任意球时，谁更能在空中赢球。',
   '姿态':'你选的踢法：压上去抢、正常踢、还是缩回来守。',
   '搏命':'全员压上、不要中场，赌一个进球——也赌不丢第二个球。'
  };
  var oppFull=(POOL[A]||[]).length;
  msgs.forEach(function(m){
    if(!m.p) m.p=PLAIN[m.area]||'';
    if(!m.c) m.c='infer';
    if(oppFull<11 && m.c==='infer' && m.area!=='环境') m.c='guess';
  });
  return {msgs:msgs,hm:hm,am:am,hl:hl,al:al};
}

/* ---------------- 可信度标签 ---------------- */
var CONF={fact:['确定','#23c55e'],infer:['推断','#f0b429'],guess:['待确认','#e2383f']};
function confTag(c){ var d=CONF[c]||CONF.infer;
  return '<span class="cf" style="color:'+d[1]+';border-color:'+d[1]+'55;background:'+d[1]+'1a">'+d[0]+'</span>'; }

/* ---------------- 术语 ---------------- */
var MIDSLOTS=['DM','CM','AM','RM','LM'];
function midCnt(t){ var m=slotMap(S.lineup[t]||[],formOf(t));
  return MIDSLOTS.reduce(function(n,k){return n+(m[k]||[]).length;},0); }
function midsOf(t){
  var f=formOf(t), m=slotMap(S.lineup[t]||[],f), out=[];
  MIDSLOTS.forEach(function(k){ if(m[k]) out=out.concat(m[k]); });
  return out.length?out.join('、'):'—';
}
function rbOf(t){ var m=slotMap(S.lineup[t]||[],formOf(t)); return (m.RB||m.RWB||[])[0]; }
function lwOf(t){ var m=slotMap(S.lineup[t]||[],formOf(t)); return (m.LW||m.LM||[])[0]; }
function termsCard(msgs){
  var all=msgs.map(function(m){return m.txt;}).join(' ');
  var hits=[];
  for(var k in TERMS){ if(all.indexOf(k)>=0) hits.push(k); }
  hits.sort(function(a,b){ return all.split(b).length-all.split(a).length; });
  hits=hits.slice(0,6);
  if(!hits.length) return '';
  return `<div class="ac l0"><div class="ah"><span class="tag">本场术语</span>
    <span class="lv">点开看白话</span></div>
    <div class="tchips">${hits.map(function(k){return `<button class="tchip" data-term="${esc(k)}">${esc(k)}</button>`;}).join('')}</div>
    <div class="ae">看懂这 ${hits.length} 个词，这一页就都能读了。全部术语在右上角「术语表」。</div></div>`;
}
function openTerm(name){
  var t=TERMS[name]; if(!t) return;
  $('#sheet').innerHTML=`<div class="sheetIn"><div class="sh"><b>${esc(name)}</b>
    <button class="x" onclick="closeSheet()">✕</button></div>
    <div class="at" style="margin:6px 0 10px">${esc(t.d)}</div>
    <div class="ae" style="border-top:1px dashed #ffffff14;margin-top:0">
      一般在哪：${esc(t.pos)}<br>举个例子：${esc(t.ex)}</div></div>`;
  $('#sheet').classList.add('on');
}
function openTermsAll(){
  var keys=Object.keys(TERMS).sort();
  $('#sheet').innerHTML=`<div class="sheetIn"><div class="sh"><b>术语表 · ${keys.length} 条</b>
    <button class="x" onclick="closeSheet()">✕</button></div><div class="plist">
    ${keys.map(function(k){return `<button class="pr" data-term="${esc(k)}">
      <span><b>${esc(k)}</b> <i class="mut">${esc(TERMS[k].d.slice(0,24))}…</i></span></button>`;}).join('')}
    </div></div>`;
  $('#sheet').classList.add('on');
}

/* ---------------- 比赛形势（比分 × 时间） ---------------- */
function benchOf(team){
  var lu=S.lineup[team]||[];
  return (POOL[team]||[]).filter(function(p){ return lu.indexOf(p.n)<0 && !hurt(p); });
}
function scoreCard(){
  var m=S.minute, d=S.hs-S.as;
  if(m<1&&d===0) return '';
  var lvl=0,txt='',hint='',benchTip='';
  if(d===0){
    if(m<45) txt=`上半场 ${S.hs}:${S.as} 僵局。最忌讳先变阵——谁先动结构，谁先露出空当。`;
    else if(m<75) txt=`${m}' 仍是 ${S.hs}:${S.as}。换人要换「类型」而不是换「人」：先解决被打穿的那条边，别动中场配比。`;
    else txt=`${m}' 还在平局，时间不多了：想要 3 分就得冒险压上，想稳 1 分就守住弧顶。二选一，别夹在中间。`;
    hint='平局时的换人应该有明确目的：加强压迫 / 加强控球 / 保住平局，只选一个。';
  }else if(d>0){
    if(m<60) txt=`领先 ${d} 球但时间还早，别急着收——收太早等于把球权交出去。先换体能，别动结构。`;
    else if(m<80) txt=`领先 ${d} 球、${m}'：开始做减法。换下一个前锋或一个自由人，上一个破坏型 6，把防线压到中场线以下。`;
    else { txt=`领先 ${d} 球、${m}'，该收了：能换的全换防守型，前场只留一个能反击的点。`; lvl=1; }
    hint='领先时要保住的是「弧顶」和「第二落点」，不是控球率。';
  }else{
    if(m<55) txt=`落后 ${-d} 球，先别慌——确认是不是被同一条边打了三次以上，那才是根因。`;
    else if(m<80){ txt=`落后 ${-d} 球、${m}'，该动了：换一个能打身后的，或把双后腰之一换成组织点，把进攻方向变直。`; lvl=1; }
    else { txt=`落后 ${-d} 球、${m}'，必须压：${formOf(S.home)==='3-1-6'?'已经是搏命形态了，那就只剩一件事——把球往禁区里砸。':'可以直接切「搏命 3-1-6」：三中卫 + 单后腰 + 6 人压上。'}`; lvl=2; }
    hint='落后时最值钱的是「身后威胁」，不是再堆一个组织手。';
    var bench=benchOf(S.home).filter(function(p){
      return /爆点|速度|冲击|身后|突/.test(p.st||'')||hasT(p,['逆足内切']);});
    if(bench.length) benchTip='替补席上有 '+bench.slice(0,3).map(function(p){return p.n;}).join('、')+' —— 这类才是落后时该上的。';
  }
  return `<div class="ac l${lvl}"><div class="ah"><span class="tag">比赛形势</span>
    <span class="lv">${m}' · ${S.home} ${S.hs}:${S.as} ${S.away}${confTag('infer')}</span></div>
    <div class="at">${txt}${benchTip?'<br><span class="mut">'+benchTip+'</span>':''}</div>
    <div class="pl"><b>人话：</b>现在这个比分和时间段，该攻还是该守。</div>
    <div class="ae">${hint}</div></div>`;
}

/* ---------------- 赛中复盘 ---------------- */
function phaseCard(r){
  if(!S.snap||S.minute<1) return '';
  var keys=[['wing','边路威胁'],['mid','中场控制'],['def','防线质量'],['behind','身后威胁'],['air','制空'],['build','出球质量']];
  var rows=keys.map(function(k){ return [k[1], r.hm[k[0]]-S.snap.h[k[0]], r.am[k[0]]-S.snap.a[k[0]] ]; })
    .filter(function(x){ return Math.abs(x[1])>=1||Math.abs(x[2])>=1; })
    .sort(function(a,b){ return Math.abs(b[1])+Math.abs(b[2])-(Math.abs(a[1])+Math.abs(a[2])); }).slice(0,3);
  var subs=S.events.filter(function(e){return e.type==='sub'&&e.min>0;}).length;
  var body=rows.length? rows.map(function(x){
        var hc=x[1]>0?'#23c55e':(x[1]<0?'#e2383f':'#93a0af');
      var ac=x[2]>0?'#23c55e':(x[2]<0?'#e2383f':'#93a0af');
      return `${x[0]} ${S.home} <b style="color:${hc}">${x[1]>0?'+':''}${x[1].toFixed(0)}</b> / ${S.away} <b style="color:${ac}">${x[2]>0?'+':''}${x[2].toFixed(0)}</b>`;
    }).join('　') : '结构没有明显变化';
  return `<div class="ac l1"><div class="ah"><span class="tag">${S.minute}' 复盘</span>
    <span class="lv">${subs} 次换人${confTag('fact')}</span></div>
    <div class="at">${body}</div>
    <div class="pl"><b>人话：</b>从开场到现在，球队这几项能力哪项变强了、哪项掉了。</div>
    <div class="ae">当前结构：边路 ${r.hm.wing} · 中场 ${r.hm.mid} · 防线 ${r.hm.def} · 制空 ${r.hm.air.toFixed(0)} · 出球 ${r.hm.build}<br>
      相对开球时的变化，正值=变强，负值=被削弱。</div></div>`;
}

function timelineCard(){
  if(!S.events.length) return '<div class="ac l0"><div class="ah"><span class="tag">比赛进程</span>'+
    '<span class="lv">空</span></div><div class="at">还没有换人记录。去「排阵」页点场上球员，换一个人、或标一个状态，'+
    '这里就会按分钟记下来。</div></div>';
  var items=S.events.slice().reverse().map(function(e){
    if(e.type==='sub') return `<div class="tl"><b>${e.min}'</b> ${esc(e.team)} <span class="mut">${esc(e.out)} → ${esc(e.in)}</span></div>`;
    return `<div class="tl"><b>${e.min}'</b> ${esc(e.team)} <span class="mut">${esc(e.who)} 标记 ${e.mark}</span></div>`;
  }).join('');
  return `<div class="sec">比赛进程</div><div class="tlc">${items}</div>`;
}

/* ---------------- 换人诊断 ---------------- */
function rolesOf(p){
  if(!p) return '—';
  var t=[];
  if(hasT(p,['逆足内切','顺足下底','内锋','翼卫'])) t.push('边路');
  if(hasT(p,['破坏型','B2B','组织8','拖后组织','节拍器','现代10','自由10','伪10'])) t.push('中场');
  if(hasT(p,['支点','抢点型','逼抢9','全能9','伪9'])) t.push('锋线');
  if(hasT(p,['套边型','上抢型','拖后型','回追型','左脚中卫','清球型'])) t.push('防线');
  if(hasT(p,['出球型','拖后组织'])) t.push('出球');
  return t.length?t.join('/'):'—';
}
function intentOf(p){
  if(!p) return [];
  var out=[], st=p.st||'';
  if(hasT(p,['支点'])) out.push('加高点：改打边路传中和定位球');
  if(hasT(p,['逆足内切','内锋'])||/内切/.test(st)) out.push('加内切一对一，吃对方边后卫的内线');
  if(/爆点|速度|冲击|身后|突|快马/.test(st)) out.push('加速度/身后：把进攻变直，不再磨阵地');
  if(hasT(p,['破坏型','B2B','逼抢9'])||/抢断|扫荡|绞杀|拦截/.test(st)) out.push('加强反抢：压缩对方出球时间，把比赛拉回中场');
  if(hasT(p,['组织8','拖后组织','节拍器','现代10'])||/组织|调度|节拍/.test(st)) out.push('加控球：降节奏，把球留在自己脚下');
  if(hasT(p,['套边型','翼卫'])) out.push('加边路宽度：拉开对方防线，给肋部腾空间');
  if(hasT(p,['抢点型'])) out.push('加禁区抢点：不再追求过程，直接冲六码区');
  if(hasT(p,['伪10','自由10'])||/盘带|魔术|创造力|最后一传|想象力/.test(st)) out.push('加一个能改变节奏的自由人：多一种"最后一传"的可能');
  if(hasT(p,['左脚中卫','拖后型','回追型','清球型','门线型'])) out.push('补防线：保平 / 守住领先');
  if(!out.length){
    var g=GRP[(p.pos||[])[0]];
    out.push(g==='锋'?'换一个进攻点：换的是「类型」，不是「体能」'
      :g==='中'?'调整中场配比：要么加控球，要么加拦截'
      :'补防线轮换，先把结构保住');
  }
  return out.slice(0,3);
}
function impactOf(inP,team){
  if(!inP) return '';
  var opp=team===S.home?S.away:S.home;
  var f=formOf(opp), m=slotMap(S.lineup[opp]||[],f);
  if(hasT(inP,['支点','抢点型'])) return `对面中卫（${(m.CB||[]).join('+')||'—'}）要开始把注意力放在第一落点，别被拉出来。`;
  if(hasT(inP,['逆足内切','内锋'])||/爆点|速度/.test(inP.st||'')) return `正对你的边后卫（${(m.LB||[]).concat(m.RB||[]).join('/')||'—'}）：他会吃一对一，需要有人协防内线。`;
  if(hasT(inP,['破坏型','B2B','逼抢9'])) return `你们的中场出球会被压：${(m.CM||[]).concat(m.DM||[]).join('/')||'—'} 接球前先看身后。`;
  if(hasT(inP,['组织8','拖后组织','节拍器'])) return '球权会更多地停在他脚下，逼抢要提上去，别让他抬头。';
  if(hasT(inP,['套边型','翼卫'])) return '边路会被拉开，肋部会空出来，注意后插上的人。';
  if(hasT(inP,['伪10','自由10'])||/盘带|魔术|最后一传/.test(inP.st||'')) return '他会在肋部接球，你们的中场和边后卫之间会出现空当，得有人盯着他的接球点。';
  var g=GRP[(inP.pos||[])[0]];
  return g==='锋'?'前场多了一个点，你们的后腰回撤要更深。'
    :g==='中'?'中场人数或类型变了，注意中路的第二落点。'
    :'他们开始收结构，进攻要更耐心，别急着传中。';
}
function subCard(){
  var d=S.lastDiff;
  if(!d||!d.out||!d.in) return '';
  var o=byName[d.out], i=byName[d.in];
  var intents=intentOf(i);
  var impact=impactOf(i,d.team);
  return `<div class="ac l1"><div class="ah"><span class="tag">换人诊断 · ${esc(d.team)}</span>
    <span class="lv">${S.minute}'${confTag('infer')}</span></div>
    <div class="at"><b style="color:#ffb4b7">↓ ${esc(d.out)}</b>（${rolesOf(o)}）
      → <b style="color:#8ef0b3">↑ ${esc(d.in)}</b>（${rolesOf(i)}）<br>
      <span class="mut">换下「${esc((o&&o.st)||'')}」，换上「${esc((i&&i.st)||'')}」</span></div>
    ${intents.length?`<div class="ae" style="border-top:0;color:#cdd7e1;padding-top:6px">
      <b>教练可能想：</b><br>${intents.map(function(x,k){return '&nbsp;'+(k+1)+'. '+x;}).join('<br>')}</div>`:''}
    ${impact?`<div class="ae"><b>对你的影响：</b>${esc(impact)}</div>`:''}
    <div class="pl"><b>人话：</b>教练换这个人，是想解决什么问题。</div>
  </div>`;
}

/* ---------------- 渲染 ---------------- */
function $(s){return document.querySelector(s);}
function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(m){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m];}); }

function postureSlots(slots,tax){
  if(tax!=='atk'&&tax!=='def') return slots;
  return slots.map(function(sl){
    if(sl[0]==='GK') return sl;
    var g=(sl[0]==='RWB'||sl[0]==='LWB')?'中':GRP[sl[0]];
    var dy=0;
    if(g==='卫') dy=(tax==='atk'?-7:0);
    else if(g==='中') dy=(tax==='atk'?-6:6);
    else if(g==='锋') dy=(tax==='atk'?-3:4);
    return [sl[0],sl[1],Math.max(8,Math.min(86,sl[2]+dy))];
  });
}
function fixGKSlot(team){
  var lu=S.lineup[team]; if(!lu||!lu.length) return;
  var p0=lu[0]?byName[lu[0]]:null;
  if(p0 && (p0.pos||[]).indexOf('GK')>=0) return;
  for(var i=1;i<lu.length;i++){
    var p=lu[i]?byName[lu[i]]:null;
    if(p && (p.pos||[]).indexOf('GK')>=0){
      lu[0]=p.n; lu[i]=p0?p0.n:null; return;
    }
  }
}
function renderPitch(which){
  var team=which==='h'?S.home:S.away;
  var form=formOf(team);
  var base=FORMS[form]||FORMS['4-2-3-1'];
  var slots=postureSlots(possOn(team)?(POSS_FORMS[form]||base):base,taxOf(team));
  if(which==='h') slots=slots.map(function(sl){return [sl[0],sl[1],100-sl[2]];});
  var lu=S.lineup[team]||autoLineup(team); S.lineup[team]=lu;
  fixGKSlot(team);
  var full=(POOL[team]||[]).length;
  var starters=lu.filter(Boolean).length;
  var subs=Math.max(0,full-starters);
  var tok='';
  slots.forEach(function(sl,i){
    var n=lu[i],p=n?byName[n]:null,st=n?stOf(n):'ok';
    var emo=STMARK[st]||'';
    var sub=(n&&S.subMark[n])?`<u class="sbm">↑${S.subMark[n]}'</u>`:'';
    tok+=`<div class="tk ${p?'':'empty'}" data-w="${which}" data-i="${i}" style="left:${sl[1]}%;top:${sl[2]}%">
      <b>${p?esc(p.n):sl[0]}</b><i>${sl[0]}</i>${emo?'<em>'+emo+'</em>':''}${sub}</div>`;
  });
  var chips=BASE_FORMS.map(function(f){
    return `<button class="fchip ${f===form?'on':''}" data-team="${esc(team)}" data-form="${f}">${f}</button>`;}).join('');
  var tx=taxOf(team);
  var taxRow=`<div class="frow tax">
    <span class="mut" style="font-size:10px;align-self:center">姿态</span>
    <button class="fchip ${tx==='atk'?'on':''}" data-tax="${esc(team)}" data-v="atk">压出去</button>
    <button class="fchip ${tx==='bal'?'on':''}" data-tax="${esc(team)}" data-v="bal">平衡</button>
    <button class="fchip ${tx==='def'?'on':''}" data-tax="${esc(team)}" data-v="def">收回来</button>
    <span class="sep2"></span>
    <button class="fchip ${possOn(team)?'on':''}" data-poss="${esc(team)}">${possOn(team)?'有球形态':'无球形态'}</button>
    <span class="fbrk"></span>
    <button class="fchip lead ${form==='5-4-1'?'on':''}" data-lead="${esc(team)}">守领先 5-4-1</button>
    <button class="fchip desperate ${form==='3-1-6'?'on':''}" data-desp="${esc(team)}">搏命 3-1-6</button>
  </div>`;
  return `<div class="pitchwrap">
    <div class="phead"><span class="dot" style="background:${which==='h'?'#e2383f':'#4ea1ff'}"></span>
      <b>${esc(team)}</b>
      <span class="mut">${esc(coachOf(team))} · ${full} 人库 · 首发 ${starters} · 替补 ${subs}${full<11?' <b style="color:#f0b429">数据不足</b>':''}</span>
      <button class="hbtn" style="margin-left:auto" data-coach="${esc(team)}">改教练</button></div>
    <div class="frow">${chips}</div>
    ${taxRow}
    ${which==='h'?'<div class="postureHint">姿态=整条线前压/回收；有球形态=出球结构</div>':''}
    <div class="pitch">${tok}</div>
    <div class="hint">点球员 → 换人 / 标状态</div></div>`;
}

function legendCard(){
  return '<div class="ac l0 legend"><div class="ah"><span class="tag">怎么读这一页</span></div>'+
   '<div class="at">每张卡右上角有个标记：'+confTag('fact')+' 来自球员库或官网；'+
   confTag('infer')+' 引擎按规则算的结论；'+confTag('guess')+' 数据不全或凭外部信息，我在猜。</div>'+
   '<div class="ae">先看标记再看结论。确定 ≠ 结论一定对，只是依据硬；推断 ≠ 结论一定错，只是没实证。</div></div>';
}
var HUDKEY='tb_hud_pref';
var HUD={size:(window.matchMedia&&window.matchMedia('(max-width:480px)').matches?'compact':'standard'),mode:'always'};
var HUD_TIMER=null;
function loadHudPref(){
  try{
    var d=JSON.parse(localStorage.getItem(HUDKEY)||'{}');
    if(d.size==='compact'||d.size==='standard'||d.size==='large') HUD.size=d.size;
    if(d.mode==='always'||d.mode==='semi'||d.mode==='auto') HUD.mode=d.mode;
  }catch(e){}
}
function saveHudPref(){
  try{ localStorage.setItem(HUDKEY,JSON.stringify({size:HUD.size,mode:HUD.mode})); }catch(e){}
}
function syncHudSpace(){
  var h=document.getElementById('hud'); if(!h) return;
  document.documentElement.style.setProperty('--hud-h',h.offsetHeight+'px');
}
function scheduleHudHide(){
  clearTimeout(HUD_TIMER);
  if(HUD.mode!=='auto') return;
  if(TAB!=='lineup'&&TAB!=='analysis') return;
  var p=document.getElementById('hudCfg'); if(p&&p.classList.contains('on')) return;
  HUD_TIMER=setTimeout(hideHud,5000);
}
function hideHud(){
  if(HUD.mode!=='auto'||(TAB!=='lineup'&&TAB!=='analysis')) return;
  var p=document.getElementById('hudCfg'); if(p&&p.classList.contains('on')) return;
  var h=document.getElementById('hud'); if(!h) return;
  h.classList.add('hud-hidden');
  var s=document.getElementById('hudShow'); if(s) s.classList.add('on');
  clearTimeout(HUD_TIMER);
}
function showHud(){
  var h=document.getElementById('hud'); if(h) h.classList.remove('hud-hidden');
  var s=document.getElementById('hudShow'); if(s) s.classList.remove('on');
  if(HUD.mode==='auto') scheduleHudHide();
}
function syncHudForTab(t){
  var h=document.getElementById('hud'), s=document.getElementById('hudShow'), p=document.getElementById('hudCfg');
  if(!h) return;
  if(t!=='lineup'&&t!=='analysis'){
    clearTimeout(HUD_TIMER);
    if(s) s.classList.remove('on');
    if(p) p.classList.remove('on');
    return;
  }
  if(HUD.mode==='auto'&&h.classList.contains('hud-hidden')){
    if(s) s.classList.add('on');
  }else{
    if(s) s.classList.remove('on');
    scheduleHudHide();
  }
}
function renderHudCfg(){
  var el=document.getElementById('hudCfg'); if(!el) return;
  var sizes=[['compact','紧凑'],['standard','标准'],['large','大']];
  var modes=[['always','常驻'],['semi','半透明'],['auto','自动收起']];
  el.innerHTML='<div class="hudcfg-h"><b>比分牌</b><button class="x" onclick="toggleHudCfg()">✕</button></div>'+
    '<div class="hudcfg-row"><span class="mut">大小</span>'+sizes.map(function(s){
      return '<button class="fchip '+(HUD.size===s[0]?'on':'')+'" onclick="setHudSize(\''+s[0]+'\')">'+s[1]+'</button>';
    }).join('')+'</div>'+
    '<div class="hudcfg-row"><span class="mut">出现</span>'+modes.map(function(m){
      return '<button class="fchip '+(HUD.mode===m[0]?'on':'')+'" onclick="setHudMode(\''+m[0]+'\')">'+m[1]+'</button>';
    }).join('')+'</div>'+
    (HUD.mode==='auto'?'<button class="tb" style="width:100%;margin-top:8px;padding:9px" onclick="collapseHudNow()">立即收起</button>':'')+
    '<div class="hudcfg-tip">偏好只存在本机；自动收起后点底部「比分」展开。</div>';
}
function applyHudPref(){
  var h=document.getElementById('hud'); if(!h) return;
  h.classList.remove('hud-compact','hud-standard','hud-large','hud-semi','hud-auto','hud-hidden');
  h.classList.add('hud-'+HUD.size);
  if(HUD.mode==='semi') h.classList.add('hud-semi');
  if(HUD.mode==='auto') h.classList.add('hud-auto');
  if(HUD.mode!=='auto'){
    clearTimeout(HUD_TIMER);
    var s=document.getElementById('hudShow'); if(s) s.classList.remove('on');
  }
  syncHudSpace();
  var p=document.getElementById('hudCfg'); if(p&&p.classList.contains('on')) renderHudCfg();
  if(HUD.mode==='auto') scheduleHudHide();
}
function toggleHudCfg(){
  var p=document.getElementById('hudCfg'); if(!p) return;
  var open=!p.classList.contains('on');
  if(open){ renderHudCfg(); p.classList.add('on'); clearTimeout(HUD_TIMER); showHud(); }
  else { p.classList.remove('on'); if(HUD.mode==='auto') scheduleHudHide(); }
}
function setHudSize(s){
  if(s!=='compact'&&s!=='standard'&&s!=='large') return;
  HUD.size=s; saveHudPref(); applyHudPref();
}
function setHudMode(m){
  if(m!=='always'&&m!=='semi'&&m!=='auto') return;
  HUD.mode=m; saveHudPref(); applyHudPref();
}
function collapseHudNow(){
  var p=document.getElementById('hudCfg'); if(p) p.classList.remove('on');
  hideHud();
}
function renderHUD(){
  $('#hud').innerHTML=`
    <div class="hRow">
      <span class="hTeam">${esc(S.home)}</span>
      <button class="mini goal" onclick="addGoal('h',-1)">−</button>
      <b class="sc" onclick="addGoal('h',1)">${S.hs}</b>
      <button class="mini goal" onclick="addGoal('h',1)">+</button>
      <span class="mut sc2">:</span>
      <button class="mini goal" onclick="addGoal('a',-1)">−</button>
      <b class="sc" onclick="addGoal('a',1)">${S.as}</b>
      <button class="mini goal" onclick="addGoal('a',1)">+</button>
      <span class="hTeam">${esc(S.away)}</span>
    </div>
    <div class="hRow">
      <button class="mini" onclick="addMin(-5)">−5'</button>
      <b class="mn">${S.minute}'</b>
      <button class="mini" onclick="addMin(5)">+5'</button>
      <span class="sep"></span>
      <button class="mini" onclick="setMin(0)">0'</button>
      <button class="mini" onclick="setMin(45)">45'</button>
      <button class="mini" onclick="setMin(60)">60'</button>
      <button class="mini" onclick="setMin(75)">75'</button>
      <button class="mini" onclick="setMin(90)">90'</button>
      <button class="mini warnb" onclick="resetMatch()">重置</button>
    </div>
    <button class="hcfg" onclick="toggleHudCfg()" aria-label="比分牌设置">⚙</button>`;
  syncHudSpace();
}

function renderAll(){
  $('#pitches').innerHTML=renderPitch('h')+renderPitch('a');
  renderSubStrip();
  var r=analyze();
  var cards=r.msgs.map(function(m){
    return `<div class="ac l${m.lvl}"><div class="ah"><span class="tag">${m.area}</span>
      <span class="lv">${['参考','注意','红灯'][m.lvl]}${confTag(m.c||'infer')}</span></div>
      <div class="at">${m.txt}</div>
      ${m.p?`<div class="pl"><b>人话：</b>${esc(m.p)}</div>`:''}
      <div class="ae">依据：${esc(m.ev).replace(/\n/g,'<br>')}</div></div>`;}).join('');
  var diff='';
  if(S.lastDiff){
    var after=metrics(S.lineup[S.lastDiff.team]||[]);
    var keys=[['wing','边路威胁'],['mid','中场控制'],['def','防线质量'],['behind','身后威胁'],['air','制空'],['build','出球质量']];
    var dl=keys.map(function(k){return [k[1], after[k[0]]-S.lastDiff.m[k[0]]];})
      .filter(function(x){return Math.abs(x[1])>=1;})
      .sort(function(a,b){return Math.abs(b[1])-Math.abs(a[1]);}).slice(0,3);
    if(dl.length) diff=`<div class="ac l1"><div class="ah"><span class="tag">刚换人</span><span class="lv">结构变化</span></div>
      <div class="at">${dl.map(function(x){return x[0]+' <b style="color:'+(x[1]>0?'#23c55e':'#e2383f')+'">'+(x[1]>0?'+':'')+x[1].toFixed(0)+'</b>';}).join(' · ')}</div>
      <div class="ae">结构差值，不是评分：问题搬家比分数涨落更重要。</div></div>`;
  }
  $('#analysis').innerHTML=`<div class="sec">对位 · ${esc(S.home)}（主）vs ${esc(S.away)}</div>`
    + legendCard() + coachNoteCard() + scoreCard() + phaseCard(r) + subCard() + timelineCard() + termsCard(r.msgs) + cards + diff;
  renderHUD();
  save();
}

function renderSubStrip(){
  var el=document.getElementById('substrip'); if(!el) return;
  var subs=S.events.filter(function(e){return e.type==='sub';});
  if(!subs.length){ el.innerHTML=''; return; }
  el.innerHTML='<div class="sec">换人记录</div><div class="tlc">'+subs.slice().reverse().map(function(e){
    return '<div class="tl"><b>'+e.min+"'</b> "+esc(e.team)+' <span class="mut">'+esc(e.out)+' → '+esc(e.in)+'</span></div>';
  }).join('')+'</div>';
}
function renderSetup(){
  var opp=S.home==='曼联'?S.away:S.home;
  var groups=GROUPS.map(function(g){ return `<details ${g.list.indexOf(opp)>=0?'open':''}>
    <summary>${g.t}</summary><div class="grid2">${g.list.map(function(t){
      return `<button class="tb ${opp===t?'on':''}" onclick="setTeam('a','${t}')">${t}</button>`;}).join('')}</div></details>`;}).join('');
  $('#setup').innerHTML=`<div class="row"><span class="mut">对手</span>
      <div class="fml">${esc(opp)} · ${esc(coachOf(opp))} · ${formOf(opp)} · ${(POOL[opp]||[]).length} 人库</div></div>
    ${groups}
    <div class="row"><span class="mut">比赛条件 · 天气</span>
      <button class="fchip wxchip ${S.weather==='dry'?'on':''}" onclick="setWeather('dry')">晴</button>
      <button class="fchip wxchip ${S.weather==='rain'?'on':''}" onclick="setWeather('rain')">雨</button></div>
    <div class="row" style="justify-content:space-between">
      <div><span class="mut">主场</span> <span class="fml">${esc(S.home)}</span>
        <span class="mut">（曼联${S.home==='曼联'?'主':'客'}场）</span></div>
      <button class="tb" style="padding:6px 10px" onclick="swapSides()">交换主客</button></div>`;
}

/* ---------------- 交互 ---------------- */
function openSheet(wi,idx){
  var team=wi==='h'?S.home:S.away, form=formOf(team), slots=FORMS[form];
  var slot=slots[idx][0];
  var lu=S.lineup[team]||autoLineup(team); S.lineup[team]=lu;
  var cur=lu[idx];
  var cands=(POOL[team]||[]).slice().sort(function(a,b){return scoreFor(b,slot)-scoreFor(a,slot);});
  var sts=[['hot','🔥'],['ok','🙂'],['low','😑'],['inj','🤕'],['yellow','🟨'],['out','⛔']];
  var h=`<div class="sheetIn"><div class="sh"><b>${esc(team)} · ${slot}</b>
    <button class="x" onclick="closeSheet()">✕</button></div>`;
  if(cur) h+=`<div class="strow"><span class="mut">状态</span>${sts.map(function(s){
      return `<button class="st ${stOf(cur)===s[0]?'on':''}" data-st="${s[0]}" data-n="${esc(cur)}">${s[1]}</button>`;}).join('')}</div>`;
  h+=`<div class="lov">选择球员（按位置分组，组内按适配度排序）</div><div class="plist">
      <button class="pr ${!cur?'on':''}" data-slotnull="1"><span>— 留空 —</span></button>`;
  var buckets={};
  cands.forEach(function(p){
    var g=GRP[(p.pos||[])[0]]||'';
    (buckets[g]=buckets[g]||[]).push(p);
  });
  [['门','门将'],['卫','后卫'],['中','中场'],['锋','前锋'],['','其他']].forEach(function(g){
    var arr=buckets[g[0]]||[];
    if(!arr.length) return;
    arr.sort(function(a,b){return scoreFor(b,slot)-scoreFor(a,slot);});
    h+=`<div class="lgrp">${g[1]} <em>${arr.length}</em></div>`;
    arr.forEach(function(p){
      var used=lu.filter(function(n,i){return n===p.n&&i!==idx;}).length>0;
      h+=`<button class="pr ${cur===p.n?'on':''} ${used?'used':''}" data-pick="${esc(p.n)}">
        <span><b>${esc(p.n)}</b> <i class="mut">${(p.pos||[]).join('/')} · ${esc(p.st||'')}</i></span>
        <em>${scoreFor(p,slot)>9?'✔':''}${used?' · 已在场(互换)':''}${hurt(p)?' ⛔':''}</em></button>`;
    });
  });
  h+=`</div></div>`;
  $('#sheet').innerHTML=h; $('#sheet').classList.add('on');
  $('#sheet').dataset.wi=wi; $('#sheet').dataset.idx=idx;
}
function closeSheet(){ $('#sheet').classList.remove('on'); $('#sheet').innerHTML=''; }
function setSlot(wi,idx,name){
  var team=wi==='h'?S.home:S.away;
  var lu=S.lineup[team]||autoLineup(team);
  var before=metrics(lu);
  var prev=lu[idx];
  var j=(name?lu.indexOf(name):-1);
  var isSwap=j>=0&&j!==idx;
  if(name){
    if(isSwap) lu[j]=prev;
    lu[idx]=name;
  } else lu[idx]=null;
  S.lineup[team]=lu;
  if(isSwap){
    S.lastDiff=null;
  }else if(S.minute===0){
    // 赛前调整：只改首发，不写换人事件、不生成换人诊断、不打 ↑0' 徽标
    S.lastDiff=null;
    log('edit',team,name||'空');
  }else if(name&&prev&&prev!==name){
    S.lastDiff={team:team,m:before,out:prev,in:name};
    log('sub',team,name,prev);
    S.subMark[name]=S.minute;
    if(prev&&S.subMark) delete S.subMark[prev];
  }else{
    S.lastDiff={team:team,m:before,out:(prev&&prev!==name?prev:null),in:(name&&prev!==name?name:null)};
    log('edit',team,name||'空');
  }
  closeSheet(); renderAll();
}
function setSt(name,k){
  S.status[name]=k;
  log('status',S.home==='曼联'?S.home:S.away,name,STMARK[k]||k);
  closeSheet(); renderAll();
}
function setTeam(which,t){
  if(S.home==='曼联') S.away=t; else S.home=t;
  S.lineup[t]=autoLineup(t); S.lastDiff=null; S.events=[];
  renderAll(); renderSetup();
}
function swapSides(){
  var t=S.home; S.home=S.away; S.away=t;
  if(!S.lineup[S.home]) S.lineup[S.home]=autoLineup(S.home);
  if(!S.lineup[S.away]) S.lineup[S.away]=autoLineup(S.away);
  S.snap={h:metrics(S.lineup[S.home]),a:metrics(S.lineup[S.away])};
  S.lastDiff=null; S.events=[];
  renderAll(); renderSetup();
}
function addGoal(side,d){
  if(side==='h') S.hs=Math.max(0,S.hs+d); else S.as=Math.max(0,S.as+d);
  renderAll();
  var arr=document.querySelectorAll('#hud .sc');
  var el=arr[side==='h'?0:1];
  if(el){ el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); }
}
function addMin(d){ setMin(S.minute+d); }
function setMin(m){
  S.minute=Math.max(0,Math.min(95,m)); renderAll();
  var el=document.querySelector('#hud .mn'); if(el){ el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); }
}
function resetMatch(){
  S.hs=0;S.as=0;S.minute=0;S.status={};S.events=[];S.lastDiff=null;S.weather='dry';
  S.lineup[S.home]=autoLineup(S.home); S.lineup[S.away]=autoLineup(S.away);
  S.snap={h:metrics(S.lineup[S.home]),a:metrics(S.lineup[S.away])};
  renderAll(); renderSetup();
}
function log(type,team,a,b){
  if(type!=='sub'&&type!=='status') return;
  S.events.push({type:type,min:S.minute,team:team,a:a,b:b,
    out:(type==='sub'?b:a), in:(type==='sub'?a:null), who:(type==='status'?a:null),
    mark:(type==='status'?b:'')});
  if(S.events.length>60) S.events.shift();
}
function cleanPreSubs(events){
  return (events||[]).filter(function(e){ return !(e.type==='sub' && (!e.min || e.min<=0)); });
}
function cleanSubMark(mark){
  var out={};
  Object.keys(mark||{}).forEach(function(n){ if(mark[n]>0) out[n]=mark[n]; });
  return out;
}

/* ---------------- 存储 ---------------- */
var KEY='tb_v41_state';
function save(){
  try{ localStorage.setItem(KEY,JSON.stringify({
    home:S.home,away:S.away,form:FORM_SEL,lineup:S.lineup,status:S.status,minute:S.minute,hs:S.hs,as:S.as,
    tactic:S.tactic,poss:S.poss,keep:KEEP,events:S.events,subMark:S.subMark,weather:S.weather
  })); }catch(e){}
}
function load(){
  try{
    var raw=localStorage.getItem(KEY); if(!raw) return false;
    var d=JSON.parse(raw);
    if(!d||!d.home||!d.away) return false;
    S.home=d.home;S.away=d.away;S.minute=d.minute||0;S.hs=d.hs||0;S.as=d.as||0;
    FORM_SEL=d.form||{}; S.status=d.status||{};
    S.tactic=d.tactic||{}; S.poss=d.poss||{};
    S.weather=d.weather==='rain'?'rain':'dry';
    S.events=cleanPreSubs(d.events||[]); S.subMark=cleanSubMark(d.subMark||{});
    if(d.keep){ for(var k in d.keep){ KEEP[k]=d.keep[k]; } }
    S.lineup=d.lineup||{};
    return true;
  }catch(e){ return false; }
}


/* ---------------- 页签 ---------------- */
var TAB='lineup';
function switchTab(t){
  TAB=t;
  ['lineup','analysis','learn','log'].forEach(function(k){
    var p=document.getElementById('pane-'+k); if(p) p.classList.toggle('on',k===t);
  });
  [].forEach.call(document.querySelectorAll('#tabs button'),function(b){
    b.classList.toggle('on',b.getAttribute('data-tab')===t);
  });
  document.getElementById('hud').style.display=(t==='lineup'||t==='analysis')?'':'none';
  syncHudForTab(t);
  if(t==='learn') renderLearn();
  if(t==='log') renderLog();
  window.scrollTo(0,0);
}

/* ---------------- 训练：3 题情境推演 ---------------- */
var DRILL={sig:'',round:0,idx:0,qs:[],picked:[]};
function drillLu(t){ return S.lineup[t]||autoLineup(t); }
function drillFull(t){
  var lu=drillLu(t)||[];
  return (POOL[t]||[]).length>=11 && lu.filter(Boolean).length>=11;
}
function drillPlayer(n){ return n?byName[n]:null; }
function drillSlot(t,slot,alt){
  var m=slotMap(drillLu(t),formOf(t));
  var a=m[slot]||[];
  if(a.length) return a[0];
  if(alt){ for(var i=0;i<alt.length;i++){ var b=m[alt[i]]||[]; if(b.length) return b[0]; } }
  return null;
}
function drillTags(n){
  var p=drillPlayer(n); return p?(p.tags||[]).join('/'):'—';
}
function drillFoot(n){
  var p=drillPlayer(n); return p&&p.foot?p.foot:'?';
}
function drillMidNames(t){
  var m=slotMap(drillLu(t),formOf(t)), out=[];
  ['DM','CM','AM'].forEach(function(k){ if(m[k]) out=out.concat(m[k]); });
  return out.filter(Boolean);
}
function drillOrgNames(names){
  return names.filter(function(n){
    var p=drillPlayer(n);
    return p&&hasT(p,['组织8','拖后组织','节拍器','现代10','自由10','伪10']);
  });
}
function drillRotate(q,seed){
  var r=((seed%3)+3)%3;
  if(!r) return q;
  q.opts=q.opts.slice(r).concat(q.opts.slice(0,r));
  q.ans=(q.ans-r+3)%3;
  return q;
}
function drillSig(){
  return JSON.stringify({h:S.home,a:S.away,hf:formOf(S.home),af:formOf(S.away),
    lu:S.lineup,tax:S.tactic,poss:S.poss,min:S.minute,hs:S.hs,as:S.as});
}
function drillFlankQs(){
  var out=[];
  function one(atk,def,side){
    var w=side==='R'?drillSlot(atk,'RW',['RM']):drillSlot(atk,'LW',['LM']);
    var fb=side==='R'?drillSlot(def,'LB',['LWB']):drillSlot(def,'RB',['RWB']);
    if(!w||!fb) return;
    var P=drillPlayer(w), F=drillPlayer(fb); if(!P||!F) return;
    var wIn=hasT(P,['逆足内切']), wWd=hasT(P,['顺足下底']);
    var fbUp=hasT(F,['套边型','攻击型'])&&!hasT(P,['翼卫']);
    if(!(wIn||wWd||fbUp)) return;
    var label=atk+(side==='R'?'右路':'左路');
    var q={kind:'flank',id:'flank-'+atk+'-'+side,type:'对位',conf:'infer'};
    if(fbUp&&(wIn||wWd)){
      q.scenario=label+'：'+w+'（'+drillTags(w)+'）对'+def+'的'+fb+'（'+drillTags(fb)+'）。';
      q.q='这条边最可能怎么发展？';
      q.opts=[
        '谁先压上谁吃亏，所以两人都会收着踢',
        w+'和'+fb+'都往前，来回拉扯，谁丢球谁身后空',
        '这条边只影响进攻，不会影响防守'
      ];
      q.ans=1;
      q.why='按引擎的边路规则：'+fb+'是套边型/翼卫，会压上；'+w+'是'+(wIn?'逆足内切':'顺足下底')+'。两个人都往前，身后就互相空——谁丢球谁被打身后。';
      q.ev=w+' tags='+drillTags(w)+' · '+drillFoot(w)+'脚 ｜ '+fb+' tags='+drillTags(fb)+' · '+drillFoot(fb)+'脚';
    } else if(wIn){
      q.scenario=label+'：'+w+'（'+drillTags(w)+'，'+drillFoot(w)+'脚）对'+fb+'（'+drillTags(fb)+'，'+drillFoot(fb)+'脚）。';
      q.q=w+'最舒服的进攻方式是什么？';
      q.opts=[
        '下底用非惯用脚传中',
        '往肋部内切，吃'+fb+'的内线',
        '回撤到后腰位置组织'
      ];
      q.ans=1;
      q.why=w+'是逆足内切：'+drillFoot(w)+'脚踢'+(side==='R'?'右路':'左路')+'，内切射门才是顺脚。'+fb+'是'+drillFoot(fb)+'脚，内线不是他的顺足侧——这是规则推断，不是说他一定防不住。';
      q.ev=w+' tags='+drillTags(w)+' · '+drillFoot(w)+'脚 ｜ '+fb+' tags='+drillTags(fb)+' · '+drillFoot(fb)+'脚';
    } else if(fbUp){
      q.scenario=label+'：'+fb+'（'+drillTags(fb)+'）会压上；'+w+'（'+drillTags(w)+'）就在这一侧。';
      q.q=fb+'压上后，最危险的空当在哪？';
      q.opts=['他身后的边路空当','对方中卫身后','本方禁区弧顶'];
      q.ans=0;
      q.why=fb+'是套边型/翼卫，压上后那条边只剩中卫补；对手抢下球第一脚就会找这里。';
      q.ev=fb+' tags='+drillTags(fb)+' ｜ '+w+' tags='+drillTags(w);
    } else if(wWd){
      q.scenario=label+'：'+w+'（'+drillTags(w)+'）对'+fb+'（'+drillTags(fb)+'）。';
      q.q=w+'下底传中时，禁区里最该抢什么？';
      q.opts=['第一点','第二落点','第一点顶到就行，第二点不重要'];
      q.ans=1;
      q.why=w+'顺足下底会把防线拉到外线，传中后的第二落点往往比第一点更决定比赛。';
      q.ev=w+' tags='+drillTags(w)+' ｜ '+fb+' tags='+drillTags(fb);
    }
    out.push(q);
  }
  one(S.home,S.away,'R');
  one(S.home,S.away,'L');
  one(S.away,S.home,'R');
  one(S.away,S.home,'L');
  return out;
}
function drillLineQs(){
  var out=[];
  function one(atk,def){
    var stN=drillSlot(atk,'ST'); if(!stN) return;
    var st=drillPlayer(stN); if(!st) return;
    var cbs=(slotMap(drillLu(def),formOf(def)).CB||[]).map(drillPlayer).filter(Boolean);
    if(!cbs.length) return;
    var pusher=cbs.filter(function(c){return hasT(c,['上抢型']);})[0];
    var deep=cbs.filter(function(c){return hasT(c,['拖后型','回追型']);})[0];
    var cbFull=cbs.map(function(c){return c.n+'（'+drillTags(c.n)+'）';}).join('+');
    var cbEv=cbs.map(function(c){return c.n+' tags='+drillTags(c.n);}).join(' ｜ ');
    var q={kind:'line',id:'line-'+atk+'-'+stN,type:'锋线',conf:'infer'};
    if(hasT(st,['支点'])&&pusher){
      q.scenario=atk+'锋线：'+stN+'（'+drillTags(stN)+'）对'+def+'中卫 '+cbFull+'。';
      q.q=def+'最怕哪一幕？';
      q.opts=[
        pusher.n+'被'+stN+'背身做墙拉出来，第二落点没人抢',
        stN+'回撤到后腰位置组织',
        stN+'拉到边路传中'
      ];
      q.ans=0;
      q.why='按引擎的锋线规则：支点型 9 遇到上抢中卫，会背身做墙把人拉出来，第二落点难抢。'+
        pusher.n+'是上抢型，身后需要有人兜底。';
      q.ev=stN+' tags='+drillTags(stN)+' ｜ '+cbEv;
    } else if(hasT(st,['支点'])&&deep){
      q.scenario=atk+'锋线：'+stN+'（'+drillTags(stN)+'）对'+def+'中卫 '+cbFull+'。';
      q.q='按引擎规则，'+atk+'更该往哪打？';
      q.opts=[
        '继续高球硬砸第一点',
        '外围远射 + 肋部后插上',
        '让'+stN+'拉到边路传中'
      ];
      q.ans=1;
      q.why='支点遇到拖后中卫，做墙压不进去；'+deep.n+'是拖后型，禁区里人多，破局点在外围远射和肋部后插上。';
      q.ev=stN+' tags='+drillTags(stN)+' ｜ '+cbEv;
    } else if(hasT(st,['抢点型','逼抢9'])){
      q.scenario=atk+'锋线：'+stN+'（'+drillTags(stN)+'）对'+def+'中卫 '+cbFull+'。';
      q.q=stN+'的价值最可能在哪个区域？';
      q.opts=['六码区/小禁区前沿','中场弧顶','边线附近'];
      q.ans=0;
      q.why=stN+'是抢点/逼抢型 9，价值在六码区和小禁区前沿；中卫必须贴身，别让他抢前点。';
      q.ev=stN+' tags='+drillTags(stN)+' ｜ '+def+' 中卫 '+cbEv;
    } else if(/速度|爆点|冲击|身后/.test(st.st||'')){
      q.scenario=atk+'锋线：'+stN+'（'+drillTags(stN)+'）打'+def+'中卫 '+cbFull+' 的身后。';
      q.q=def+'防线最怕什么？';
      q.opts=['防线压太高，身后被单刀','中锋回撤到后腰位置组织','中锋去边路传中'];
      q.ans=0;
      q.why=stN+'的特点是'+st.st+'；防线压太高，身后就是单刀。';
      q.ev=stN+' st:'+st.st+' ｜ '+def+' 中卫 '+cbEv;
    } else return;
    out.push(q);
  }
  one(S.home,S.away);
  one(S.away,S.home);
  return out;
}
function drillMidQ(){
  var hn=drillMidNames(S.home), an=drillMidNames(S.away);
  if(hn.length<2||an.length<2) return null;
  var hnOrg=drillOrgNames(hn), anOrg=drillOrgNames(an);
  var ho=hnOrg.length, ao=anOrg.length;
  var q={kind:'mid',id:'mid',type:'中场',conf:'infer'};
  q.scenario='中场中路槽位（DM/CM/AM）：'+S.home+' '+hn.length+' 人（'+hn.map(function(n){return n+'：'+drillTags(n);}).join('；')+'）；'+
    S.away+' '+an.length+' 人（'+an.map(function(n){return n+'：'+drillTags(n);}).join('；')+'）。';
  q.ev=S.home+'：'+hn.map(function(n){return n+'('+drillTags(n)+')';}).join(' / ')+'\n'+
       S.away+'：'+an.map(function(n){return n+'('+drillTags(n)+')';}).join(' / ');
  if(hn.length!==an.length){
    q.q='中场中路 '+hn.length+' vs '+an.length+'，人数多的一方最直接的好处是什么？';
    q.opts=['多一个接应点，传球线路更多','多一个人就一定控住，不用看类型','人数优势只影响防守，不影响出球'];
    q.ans=0;
    q.why='中场多一个人，就多一条接应线路；少人一方只能被动退。但人数多不等于一定控住——还要看类型和站位。';
  } else if(ao>ho){
    q.q='双方中场都是 '+hn.length+' 人。哪句话更准确？';
    q.opts=[
      S.home+'人数多，能稳控',
      '人数打平；'+S.away+'有 '+ao+' 人带组织标签，'+S.home+'只有 '+ho+' 人',
      '人数打平，所以两队中场完全一样'
    ];
    q.ans=1;
    q.why='人数打平，差别在类型：'+S.away+'的组织点是'+anOrg.join('、')+'，'+S.home+'是'+(hnOrg.length?hnOrg.join('、'):'没有明显的组织标签')+'。人数是事实，类型优势是推断。';
  } else if(ho>ao){
    q.q='双方中场都是 '+hn.length+' 人。哪句话更准确？';
    q.opts=[
      '人数打平；'+S.home+'有 '+ho+' 人带组织标签，'+S.away+'只有 '+ao+' 人',
      S.away+'人数多，能稳控',
      '人数打平，所以两队中场完全一样'
    ];
    q.ans=0;
    q.why='人数打平，差别在类型：'+S.home+'的组织点是'+hnOrg.join('、')+'，'+S.away+'是'+(anOrg.length?anOrg.join('、'):'没有明显的组织标签')+'。人数是事实，类型优势是推断。';
  } else {
    return null;
  }
  return q;
}
function drillPairQ(){
  var t=S.home, m=slotMap(drillLu(t),formOf(t));
  var names=(m.DM||[]).slice(0,2);
  if(names.length<2){
    var all=[];
    ['DM','CM'].forEach(function(k){ if(m[k]) all=all.concat(m[k]); });
    names=all.slice(0,2);
  }
  if(names.length<2) return null;
  var a=drillPlayer(names[0]), b=drillPlayer(names[1]); if(!a||!b) return null;
  function dest(p){ return hasT(p,['破坏型','B2B']); }
  function org(p){ return hasT(p,['组织8','拖后组织','节拍器','现代10']); }
  var ad=dest(a)&&!org(a), bd=dest(b)&&!org(b);
  var ao=org(a)&&!dest(a), bo=org(b)&&!dest(b);
  var destroyer=ad?a.n:(bd?b.n:null);
  var passer=ao?a.n:(bo?b.n:null);
  if(!destroyer||!passer) return null;
  var q={kind:'mid',id:'pair-'+t,type:'中场',conf:'fact'};
  q.scenario=t+' 的中场保护层：'+destroyer+'（'+drillTags(destroyer)+'）+ '+passer+'（'+drillTags(passer)+'）。';
  q.q='这对组合的分工更接近哪种？';
  q.opts=[
    destroyer+'负责扫荡，'+passer+'负责调度',
    '两人都只负责防守',
    '两人都只负责组织'
  ];
  q.ans=0;
  q.why=destroyer+'带破坏型/B2B标签，是扫荡和推进点；'+passer+'带组织标签，是出球和节奏点。一个抢、一个传，才是保护层的互补。';
  q.ev=destroyer+' tags='+drillTags(destroyer)+' ｜ '+passer+' tags='+drillTags(passer);
  return q;
}
function drillShapeQ(){
  var teams=[S.home,S.away];
  for(var ti=0;ti<teams.length;ti++){
    var t=teams[ti], f=formOf(t), base=FORMS[f], poss=POSS_FORMS[f];
    if(!base||!poss||possOn(t)) continue;
    var lu=drillLu(t), best=-1, idxs=[];
    for(var i=0;i<Math.min(base.length,poss.length);i++){
      var d=base[i][2]-poss[i][2];
      if(d>best){best=d;idxs=[i];}
      else if(d===best&&d>0){idxs.push(i);}
    }
    if(best<6||!idxs.length) continue;
    var names=idxs.map(function(i){return lu[i];});
    if(names.filter(Boolean).length!==idxs.length) continue;
    var slots=idxs.map(function(i){return base[i][0];});
    var line=slots.every(function(s){return s==='RB'||s==='LB'||s==='RWB'||s==='LWB';})?'边后卫/翼卫':
             slots.every(function(s){return s==='CB';})?'中卫':
             slots.every(function(s){return s==='DM'||s==='CM'||s==='AM'||s==='RM'||s==='LM';})?'中场':'前场';
    var wrong1=line==='中卫'?'两名边后卫压到中场线':'两名中卫压到中场线';
    var q={kind:'shape',id:'shape-'+t,type:'结构',conf:'fact'};
    q.scenario=t+' 当前是 '+f+'，姿态'+({atk:'压出去',bal:'平衡',def:'收回来'}[taxOf(t)]||'平衡')+'。点「有球形态」后：';
    q.q='谁的位置变化最大？';
    q.opts=[names.join('、')+'（'+line+'）位置明显前压',wrong1,'全队都压到对方禁区，不留后卫'];
    q.ans=0;
    q.why='按阵型坐标，'+f+' 切到有球形态时，'+line+'的纵向位移最大（'+best+' 个单位，向上）。'+
      (line==='边后卫/翼卫'?'边后卫压到中场线，和后腰并排，形成更稳的出球结构。':'这一线整体前压，给后场出球多一个接应点。')+
      '不同阵型的具体形状不完全一样。';
    q.ev='阵型坐标：'+slots.join('+')+' 的 y 从 '+base[idxs[0]][2]+' 到 '+poss[idxs[0]][2]+'（'+best+'）';
    return q;
  }
  return null;
}
function drillFormQ(){
  var t=S.home, f=formOf(t);
  if(!FORMS[f]) return null;
  var target=f==='3-1-6'?'4-2-3-1':'3-1-6';
  var base=FORMS[f], tg=FORMS[target];
  if(!base||!tg) return null;
  function holdSlots(slots){ return slots.filter(function(s){return s[0]==='DM'||s[0]==='CM';}); }
  function cbSlots(slots){ return slots.filter(function(s){return s[0]==='CB';}); }
  var bhs=holdSlots(base), ths=holdSlots(tg), bcs=cbSlots(base), tcs=cbSlots(tg);
  var bm=bhs.length, tm=ths.length, bc=bcs.length, tc=tcs.length;
  if(bm===tm) return null;
  var q={kind:'form',id:'form-'+t+'-'+target,type:'变阵',conf:'fact'};
  q.scenario=t+' 当前是 '+f+'。如果切到 '+(target==='3-1-6'?'搏命 3-1-6':target)+'：';
  q.q='中场保护层（DM/CM）会怎么变？';
  q.opts=[
    '从 '+bm+' 人变 '+tm+' 人'+(tm<bm?'，保护层变薄':'，保护层加厚'),
    '从 '+bm+' 人变 '+bm+' 人，完全不变',
    '从 '+bm+' 人变 0 人，中场彻底没人'
  ];
  q.ans=0;
  q.why='按阵型槽位：'+f+' 的保护层是 '+bm+' 人（'+bhs.map(function(s){return s[0];}).join('/')+'），'+
    target+' 是 '+tm+' 人（'+ths.map(function(s){return s[0];}).join('/')+'）；中卫从 '+bc+' 人变 '+tc+' 人。'+
    (tm<bm?'这就是搏命形态的代价：前场人数多了，保护层变薄，丢球后弧顶和身后更容易暴露。':'切回更稳的形态，保护层多一层。');
  q.ev='阵型槽位：'+f+' 保护层 '+bm+'（'+bhs.map(function(s){return s[0];}).join('/')+'）→ '+
    target+' 保护层 '+tm+'（'+ths.map(function(s){return s[0];}).join('/')+'）；中卫 '+bc+'→'+tc;
  return q;
}
function drillSubQs(){
  var out=[];
  var bench=benchOf(S.home)||[];
  if(bench.length<3) return out;
  var speed=bench.filter(function(p){return hasT(p,['逆足内切'])||/爆点|速度|冲击|身后|突/.test(p.st||'');});
  var control=bench.filter(function(p){return hasT(p,['组织8','拖后组织','节拍器','现代10']);});
  var height=bench.filter(function(p){return hasT(p,['支点','抢点型','争顶型']);});
  var defense=bench.filter(function(p){return hasT(p,['争顶型'])||(p.a&&p.a.air>=75);});
  speed.sort(function(a,b){
    function sc(p){ return (/速度|身后|爆点|冲击|快马/.test(p.st||'')?2:0)+(hasT(p,['逆足内切'])?1:0); }
    return sc(b)-sc(a);
  });
  height.sort(function(a,b){
    function sc(p){ return (p.pos.indexOf('ST')>=0?2:0)+(hasT(p,['支点'])?1:0); }
    return sc(b)-sc(a);
  });
  if(speed.length&&control.length&&height.length){
    var sp=speed[0], ct=control[0], ht=height[0];
    var q={kind:'sub',id:'sub-behind-'+S.home,type:'换人',conf:'infer'};
    q.scenario='赛前预案：如果'+S.home+'落后一球，替补席上有 '+sp.n+'、'+ct.n+'、'+ht.n+'。';
    q.q='谁最直接增加身后威胁？';
    q.opts=[
      sp.n+'（'+drillTags(sp.n)+'）',
      ct.n+'（'+drillTags(ct.n)+'）',
      ht.n+'（'+drillTags(ht.n)+'）'
    ];
    q.ans=0;
    q.why=sp.n+'有'+drillTags(sp.n)+'，更直接打身后；'+ct.n+'是加控球，'+ht.n+'是加高点——不是错，只是目标不同。落后时最值钱的是身后威胁。';
    q.ev=sp.n+' tags='+drillTags(sp.n)+' · st:'+(sp.st||'')+' ｜ '+ct.n+' tags='+drillTags(ct.n)+' ｜ '+ht.n+' tags='+drillTags(ht.n);
    out.push(q);
  }
  if(defense.length&&control.length&&speed.length){
    var df=defense[0], ct2=control[0], sp2=speed[0];
    var q2={kind:'sub',id:'sub-lead-'+S.home,type:'换人',conf:'infer'};
    q2.scenario='赛前预案：如果'+S.home+'领先一球，替补席上有 '+df.n+'、'+ct2.n+'、'+sp2.n+'。';
    q2.q='谁更直接补禁区高点和第二落点？';
    q2.opts=[
      df.n+'（'+drillTags(df.n)+'）',
      ct2.n+'（'+drillTags(ct2.n)+'）',
      sp2.n+'（'+drillTags(sp2.n)+'）'
    ];
    q2.ans=0;
    q2.why=df.n+'有'+drillTags(df.n)+'，更直接补高点和第二落点；'+ct2.n+'是控球，'+sp2.n+'是进攻——领先时先保住弧顶和第二落点。';
    q2.ev=df.n+' tags='+drillTags(df.n)+' ｜ '+ct2.n+' tags='+drillTags(ct2.n)+' ｜ '+sp2.n+' tags='+drillTags(sp2.n);
    out.push(q2);
  }
  return out;
}
function drillScoreQ(){
  if(S.minute<1) return null;
  var d=S.hs-S.as;
  var q={kind:'score',id:'score',type:'形势',conf:'infer'};
  q.scenario='现在 '+S.minute+'′，'+S.home+' '+S.hs+':'+S.as+' '+S.away+'。';
  if(d===0){
    q.q='最符合形势卡的做法是什么？';
    if(S.minute<45){
      q.opts=['先别变阵，谁先动结构谁先露空当','立刻改三中卫搏命','同时换三个前锋'];
      q.why='上半场僵局最忌讳先变阵；先看清对方从哪条边打，再动。';
    } else if(S.minute<75){
      q.opts=['换类型，先修被打穿的那条边，别动中场配比','先改三中卫','同时换三个前锋'];
      q.why='这个时间段换人要换「类型」而不是换「人」：先解决被打穿的那条边；别急着动中场配比。';
    } else {
      q.opts=['想要 3 分就冒险压上，想稳 1 分就守住弧顶，二选一','继续控球等点球','同时换三个进攻手'];
      q.why='时间不多了，不能夹在中间：要么压上赌 3 分，要么守住弧顶保 1 分。';
    }
  } else if(d>0){
    q.q='领先时最该保住什么？';
    q.opts=['弧顶和第二落点','控球率','再堆一个组织手'];
    q.why='领先时要保住的是弧顶和第二落点，不是控球率；适当收结构，换防守型。';
  } else {
    q.q='落后时最值钱的是什么？';
    q.opts=['身后威胁','再堆一个组织手','稳住平局'];
    q.why='落后时最值钱的是身后威胁，不是再堆一个组织手；把进攻变直。';
  }
  q.ans=0;
  q.ev='比赛形势卡规则：'+S.minute+'′ · '+S.hs+':'+S.as+'（比分 × 时间）';
  return q;
}
function drillSetQs(){
  var out=[];
  if(S.home!=='曼联') return out;
  var oppSt=drillSlot(S.away,'ST'), st=drillPlayer(oppSt);
  var hCBs=(slotMap(drillLu(S.home),formOf(S.home)).CB||[]).map(drillPlayer).filter(Boolean);
  if(st&&hasT(st,['支点','抢点型','争顶型'])&&hCBs.length>=2){
    var airs=hCBs.filter(function(p){return p.a&&p.a.air;}).sort(function(a,b){return (b.a.air||0)-(a.a.air||0);});
    if(airs.length>=2){
      var best=airs[0], weak=airs[airs.length-1];
      var fb=drillSlot(S.home,'RB',['RWB'])||drillSlot(S.home,'LB',['LWB']);
      if(fb&&best.n!==weak.n){
        var q={kind:'set',id:'set-def-'+S.away,type:'定位球',conf:'infer'};
        q.scenario='定位球预案：'+S.away+'角球，'+st.n+'（'+drillTags(st.n)+'）在禁区；'+S.home+'中卫 '+best.n+'（air '+best.a.air+'）+ '+weak.n+'（air '+weak.a.air+'）。边后卫 '+fb+' 守近门柱。';
        q.q=S.home+'最该让谁盯'+st.n+'？';
        q.opts=[best.n,weak.n,fb];
        q.ans=0;
        q.why=st.n+'是支点/抢点型，第一点必须有人顶；'+best.n+'的 air 示意值 '+best.a.air+' 高于 '+weak.n+' 的 '+weak.a.air+'，最该承担第一点。示意值不是真实数据，别当绝对。';
        q.ev='球员库示意值：'+best.n+' air '+best.a.air+' / '+weak.n+' air '+weak.a.air+'；'+st.n+' tags='+drillTags(st.n);
        out.push(q);
      }
    }
  }
  var mids=drillMidNames(S.home);
  var destroyer=mids.filter(function(n){var p=drillPlayer(n);return p&&hasT(p,['破坏型','B2B']);})[0];
  var passer=mids.filter(function(n){var p=drillPlayer(n);return p&&hasT(p,['组织8','拖后组织','节拍器','现代10']);})[0];
  var fwd=drillSlot(S.home,'ST');
  if(destroyer&&passer&&fwd){
    var q2={kind:'set',id:'set-second-'+S.home,type:'定位球',conf:'infer'};
    q2.scenario='定位球预案：'+S.home+'角球被解围，球落到禁区外。中场有 '+destroyer+'（'+drillTags(destroyer)+'）和 '+passer+'（'+drillTags(passer)+'）；前锋 '+fwd+' 还在禁区。';
    q2.q='第二落点最该谁抢？';
    q2.opts=[destroyer,passer,fwd];
    q2.ans=0;
    q2.why='第二落点更看谁更凶、谁站位更靠外；'+destroyer+'是破坏型/B2B，最适合扫第二点。'+passer+'更偏组织，不是第一选择。';
    q2.ev=destroyer+' tags='+drillTags(destroyer)+' ｜ '+passer+' tags='+drillTags(passer);
    out.push(q2);
  }
  return out;
}
function drillBuildQs(){
  var out=[];
  var t=S.home, m=slotMap(drillLu(t),formOf(t));
  var mids=[];
  ['DM','CM'].forEach(function(k){ if(m[k]) mids=mids.concat(m[k]); });
  mids=mids.filter(Boolean);
  var cbs=(m.CB||[]).filter(Boolean);
  var fbs=[];
  ['RB','LB','RWB','LWB'].forEach(function(k){ if(m[k]) fbs=fbs.concat(m[k]); });
  fbs=fbs.filter(Boolean);
  var am=(m.AM||[])[0], st=(m.ST||[])[0], rw=(m.RW||m.RM||[])[0], lw=(m.LW||m.LM||[])[0];
  if(mids.length>=1&&am&&st){
    var q={kind:'build',id:'build-first-'+t,type:'出球',conf:'infer'};
    q.scenario=t+' 有球形态：中卫拉开，边路球员压上。';
    q.q='谁站在中卫身前接第一脚？';
    q.opts=[
      mids.slice(0,2).join('/')+'（中场）',
      am+'（前腰）',
      st+'（中锋）'
    ];
    q.ans=0;
    q.why='有球形态下，中卫拉开、边路球员压上，后腰回撤到中卫身前接第一脚；前腰和中锋位置更高，不是第一接应点。';
    q.ev='阵型位置：'+mids.slice(0,2).join('/')+' 在 DM/CM；'+am+' 在 AM；'+st+' 在 ST';
    out.push(q);
  }
  if(cbs.length>=1&&mids.length>=1&&fbs.length>=1){
    var q2={kind:'build',id:'build-cover-'+t,type:'出球',conf:'infer'};
    q2.scenario=t+' 有球形态：'+fbs.slice(0,2).join('/')+' 压到中场线，身后留空。';
    q2.q='谁给他们身后兜底？';
    q2.opts=[
      cbs.slice(0,2).join('/')+'（中卫）',
      mids.slice(0,2).join('/')+'（中场）',
      (rw||lw)+'（边路）'
    ];
    q2.ans=0;
    q2.why='边后卫/翼卫压上后，身后只剩中卫补；后腰保护的是弧顶，边路球员在更前面，回追距离最长。';
    q2.ev='阵型位置：'+cbs.slice(0,2).join('/')+' 在 CB；'+mids.slice(0,2).join('/')+' 在 DM/CM；'+fbs.slice(0,2).join('/')+' 在边路';
    out.push(q2);
  }
  return out;
}
function buildDrills(){
  if(!drillFull(S.home)||!drillFull(S.away)) return [];
  var byKind={};
  function add(k,arr){ if(arr&&arr.length) byKind[k]=(byKind[k]||[]).concat(arr); }
  add('flank',drillFlankQs());
  add('line',drillLineQs());
  add('sub',drillSubQs());
  var pq=drillPairQ(); if(pq) add('mid',[pq]);
  var mq=drillMidQ(); if(mq) add('mid',[mq]);
  add('set',drillSetQs());
  var sq=drillShapeQ(); if(sq) add('shape',[sq]);
  add('build',drillBuildQs());
  var fq=drillFormQ(); if(fq) add('form',[fq]);
  var scq=drillScoreQ(); if(scq) add('score',[scq]);
  var kinds=['flank','line','sub','mid','set','shape','build','form','score'];
  var order=[];
  for(var i=0;i<kinds.length;i++){
    var k=kinds[(i+DRILL.round)%kinds.length];
    if(byKind[k]&&byKind[k].length) order.push(k);
  }
  if(DRILL.round===0&&byKind.score&&byKind.score.length){
    order=['score'].concat(order.filter(function(k){return k!=='score';}));
  }
  var out=[];
  for(var j=0;j<order.length&&out.length<3;j++){
    var arr=byKind[order[j]];
    var q=arr[(DRILL.round*2+j)%arr.length];
    if(out.indexOf(q)<0) out.push(q);
  }
  if(out.length<3){
    var all=[];
    kinds.forEach(function(k){ if(byKind[k]) all=all.concat(byKind[k]); });
    for(var t=0;t<all.length&&out.length<3;t++){
      var q2=all[(DRILL.round*2+t)%all.length];
      if(out.indexOf(q2)<0) out.push(q2);
    }
  }
  out=out.slice(0,3);
  for(var r=0;r<out.length;r++) drillRotate(out[r],DRILL.round+r*2+out[r].kind.length);
  return out;
}
function ensureDrills(){
  var sig=drillSig();
  if(sig!==DRILL.sig){
    DRILL.sig=sig; DRILL.round=0; DRILL.idx=0; DRILL.picked=[]; DRILL.qs=buildDrills();
  }
}
function drillAnswer(oi){
  if(DRILL.idx>=DRILL.qs.length) return;
  if(DRILL.picked[DRILL.idx]!==undefined) return;
  DRILL.picked[DRILL.idx]=oi;
  renderLearn();
  setTimeout(function(){
    var w=document.getElementById('drillWhy');
    if(w&&w.scrollIntoView) w.scrollIntoView({block:'nearest'});
  },0);
}
function drillNext(){
  if(DRILL.picked[DRILL.idx]===undefined) return;
  DRILL.idx++;
  renderLearn();
  window.scrollTo(0,0);
}
function drillRegroup(){
  DRILL.round++;
  DRILL.sig=drillSig();
  DRILL.idx=0; DRILL.picked=[]; DRILL.qs=buildDrills();
  renderLearn();
  window.scrollTo(0,0);
}
function quickRef(){
  return '<details class="dquick"><summary>速查 · 4 条</summary>'+
    '<div class="dqrow"><b>看球三件事</b><p>谁有球；中场谁人多；哪条边在冲。剩下的都是细节。</p></div>'+
    '<div class="dqrow"><b>阵型是起步姿势</b><p>4-2-3-1 只是开球站法。球一动，有球可能变 <button class="tchip" data-term="3-2-5">3-2-5</button>，无球可能变 4-4-2。</p></div>'+
    '<div class="dqrow"><b>6/8/10 + 肋部</b><p>6 后腰、8 能跑能传、10 最后一传；<button class="tchip" data-term="肋部">肋部</button>是中卫和边后卫之间的缝。</p></div>'+
    '<div class="dqrow"><b>换人三问</b><p>换体能、换类型、换结构——只看它解决了当时的哪个问题。</p></div>'+
    '<button class="dbtn" style="margin-top:9px" onclick="openTermsAll()">打开完整术语表</button>'+
    '</details>';
}
function renderLearn(){
  ensureDrills();
  var el=document.getElementById('learn'); if(!el) return;
  var total=DRILL.qs.length;
  var wx=S.weather==='rain'?'雨':'晴';
  var html='<div class="dhead"><div class="dstate">'+esc(S.home)+' <b>'+esc(formOf(S.home))+'</b> vs '+esc(S.away)+' <b>'+esc(formOf(S.away))+'</b></div>'+
    '<div class="dmeta">'+S.minute+'′ '+S.hs+':'+S.as+' · '+wx+' · '+(total?('本组 '+total+' 题'):'本场暂无题')+' · 题目随当前排阵/阵型/比分/时间变化</div>'+
    '<div class="dlegend">每题答完标可信度：'+confTag('fact')+' 直接来自库内字段；'+confTag('infer')+' 按规则推断。</div></div>';
  if(!total){
    html+='<div class="dempty">这场暂时出不了情境题：'+esc(S.home)+' '+(POOL[S.home]||[]).length+' 人 / '+esc(S.away)+' '+(POOL[S.away]||[]).length+' 人，至少一队名单不足 11 人或首发有缺位。先去「排阵」补人/换阵，或看下面的速查。</div>';
  } else if(DRILL.idx>=total){
    var ok=0; DRILL.picked.forEach(function(v,i){ if(v===DRILL.qs[i].ans) ok++; });
    html+='<div class="dsum"><div class="dsumh">本组完成</div><div class="dscore">'+total+' 题 · 对 '+ok+' · 错 '+(total-ok)+'</div>'+
      '<div class="dsub">答错不用背答案，重点看每题的「依据」。同场会轮换题型；改比分/时间/阵型/换人后会重新生成。</div>'+
      '<div class="dacts"><button class="dbtn primary" data-drill-regroup>再练一组</button><button class="dbtn" data-drill-goto>去排阵改情境</button></div></div>';
  } else {
    var q=DRILL.qs[DRILL.idx], chosen=DRILL.picked[DRILL.idx];
    var dots='';
    for(var i=0;i<total;i++){ dots+='<span class="'+(i<DRILL.idx?'done':i===DRILL.idx?'now':'')+'"></span>'; }
    html+='<div class="dprog"><span>第 '+(DRILL.idx+1)+'/'+total+' 题</span><span class="ldots">'+dots+'</span></div>';
    html+='<div class="dcard" id="drillCard"><div class="dtop"><span class="dtype">'+esc(q.type||'训练')+'</span></div><div class="dscenario">'+esc(q.scenario)+'</div><div class="dq">'+esc(q.q)+'</div>';
    html+=q.opts.map(function(o,oi){
      var cls='';
      if(chosen!==undefined){ if(oi===q.ans) cls=' ok'; else if(oi===chosen) cls=' no'; }
      return '<button class="dopt'+cls+'" data-drill-opt="'+oi+'"'+(chosen!==undefined?' aria-pressed="'+(oi===chosen)+'"':'')+'><b>'+String.fromCharCode(65+oi)+'</b><span>'+esc(o)+'</span></button>';
    }).join('');
    if(chosen!==undefined){
      var right=chosen===q.ans;
      html+='<div class="dwhy" id="drillWhy"><div class="dres '+(right?'ok':'no')+'">'+(right?'✔ 对了':'✘ 正确答案是 '+String.fromCharCode(65+q.ans))+'</div>'+
        '<div class="dwhytxt">'+esc(q.why)+'</div>'+
        '<div class="dev"><b>依据：</b>'+esc(q.ev).replace(/\n/g,'<br>')+'</div>'+
        '<div class="dcf">'+confTag(q.conf)+'</div></div>';
      html+='<button class="dbtn primary dnext" data-drill-next>'+(DRILL.idx+1<total?'下一题 →':'看结果 →')+'</button>';
    }
    html+='</div>';
  }
  html+=quickRef();
  el.innerHTML=html;
}

/* ---------------- 复盘日志 ---------------- */
var LOGKEY='tb_v4_logs';
var LOG_EDIT=-1;
function logs(){ try{ return JSON.parse(localStorage.getItem(LOGKEY)||'[]'); }catch(e){ return []; } }
function logTime(ts){
  var d=new Date(ts);
  return (d.getMonth()+1)+'/'+d.getDate()+' '+('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2);
}
function wxLabel(w){ return w==='rain'?'雨':w==='dry'?'晴':''; }
function saveLog(){
  var t=document.getElementById('logtxt');
  var v=(t&&t.value||'').trim(); if(!v) return;
  var arr=logs();
  if(LOG_EDIT>=0){
    if(!arr[LOG_EDIT]){ LOG_EDIT=-1; renderLog(); return; }
    arr[LOG_EDIT].txt=v;
    arr[LOG_EDIT].edited=Date.now();
    try{ localStorage.setItem(LOGKEY,JSON.stringify(arr)); }catch(e){}
    LOG_EDIT=-1;
    renderLog();
    return;
  }
  arr.unshift({ts:Date.now(),txt:v,home:S.home,away:S.away,hs:S.hs,as:S.as,min:S.minute,
    form:formOf(S.home),tax:taxOf(S.home),wx:S.weather});
  try{ localStorage.setItem(LOGKEY,JSON.stringify(arr.slice(0,60))); }catch(e){}
  renderLog();
}
function editLog(i){
  var arr=logs(); if(!arr[i]) return;
  LOG_EDIT=i;
  var t=document.getElementById('logtxt');
  if(t) t.value=arr[i].txt;
  renderLog();
  var t2=document.getElementById('logtxt');
  if(t2){ t2.value=arr[i].txt; t2.focus(); try{ t2.setSelectionRange(t2.value.length,t2.value.length); }catch(e){} }
}
function cancelEdit(){ LOG_EDIT=-1; renderLog(); }
function delLog(i){
  var arr=logs(); if(!arr[i]) return;
  if(LOG_EDIT>=0){
    if(i===LOG_EDIT) LOG_EDIT=-1;
    else if(i<LOG_EDIT) LOG_EDIT--;
  }
  arr.splice(i,1);
  try{ localStorage.setItem(LOGKEY,JSON.stringify(arr)); }catch(e){}
  renderLog();
}
function backupText(){
  return JSON.stringify({at:Date.now(),origin:location.origin,
    state:localStorage.getItem('tb_v41_state')||'',
    logs:localStorage.getItem('tb_v4_logs')||''},null,2);
}
function copyBackup(){
  var txt=backupText();
  if(navigator.clipboard&&window.isSecureContext){
    navigator.clipboard.writeText(txt).then(function(){ alert('已复制。粘到微信「文件传输助手」发给自己就行。'); },
      function(){ showBackup(txt); });
  }else{ showBackup(txt); }
}
function showBackup(txt){
  var ta=document.getElementById('bktext');
  if(!ta) return;
  ta.style.display='block'; ta.value=txt; ta.focus(); ta.select();
  try{ document.execCommand('copy'); }catch(e){}
  alert('已选中全部文本。长按选择「拷贝」，或直接按 Ctrl/⌘+C。');
}
function isObj(x){ return !!x && typeof x==='object' && Object.prototype.toString.call(x)==='[object Object]'; }
function isNum(x){ return typeof x==='number' && isFinite(x); }
function isInt(x){ return isNum(x) && Math.floor(x)===x; }
function isName(x){ return typeof x==='string' && x.length>0; }
function badBackup(msg){ throw new Error(msg); }
var STATUS_OK={hot:1,ok:1,low:1,inj:1,yellow:1,out:1};
var TAX_OK={atk:1,bal:1,def:1};
function validateBackupState(st){
  if(!isObj(st)) badBackup('state 不是对象');
  if(!isName(st.home)||!isName(st.away)) badBackup('state 缺少有效的 home/away');
  if(TEAMS.indexOf(st.home)<0||TEAMS.indexOf(st.away)<0) badBackup('state.home/away 不是已支持的球队');
  if(st.home===st.away) badBackup('state.home/away 不能是同一支球队');
  if(!isInt(st.minute)||st.minute<0||st.minute>95) badBackup('state.minute 必须是 0–95 的整数');
  if(!isInt(st.hs)||st.hs<0||!isInt(st.as)||st.as<0) badBackup('state.hs/as 必须是非负整数');
  if(st.weather!=null&&st.weather!=='dry'&&st.weather!=='rain') badBackup('state.weather 必须是 dry/rain');
  if(!isObj(st.form)) badBackup('state.form 必须是对象');
  Object.keys(st.form).forEach(function(t){
    if(typeof st.form[t]!=='string'||!FORMS[st.form[t]]) badBackup('state.form 里有未知阵型：'+st.form[t]);
  });
  if(!isObj(st.lineup)) badBackup('state.lineup 必须是对象');
  Object.keys(st.lineup).forEach(function(t){
    var lu=st.lineup[t];
    if(!Array.isArray(lu)||lu.length!==11) badBackup('state.lineup.'+t+' 必须是 11 人数组');
    lu.forEach(function(n){ if(n!==null&&!isName(n)) badBackup('state.lineup.'+t+' 有非法球员值'); });
  });
  if(!st.lineup[st.home]||!st.lineup[st.away]) badBackup('state.lineup 缺少主队或客队阵容');
  if(!isObj(st.status)) badBackup('state.status 必须是对象');
  Object.keys(st.status).forEach(function(n){
    if(!STATUS_OK[st.status[n]]) badBackup('state.status 有未知状态：'+st.status[n]);
  });
  if(!isObj(st.tactic)) badBackup('state.tactic 必须是对象');
  Object.keys(st.tactic).forEach(function(t){
    if(!TAX_OK[st.tactic[t]]) badBackup('state.tactic 有未知姿态：'+st.tactic[t]);
  });
  if(!isObj(st.poss)) badBackup('state.poss 必须是对象');
  Object.keys(st.poss).forEach(function(t){
    if(typeof st.poss[t]!=='boolean') badBackup('state.poss 必须是布尔值');
  });
  if(!Array.isArray(st.events)) badBackup('state.events 必须是数组');
  st.events.forEach(function(e){
    if(!isObj(e)) badBackup('state.events 里有非法记录');
    if(!isInt(e.min)||e.min<0||e.min>95) badBackup('state.events 的分钟不合法');
    if(e.type==='sub'){
      if(!isName(e.team)||!isName(e.out)||!isName(e.in)) badBackup('state.events 的换人记录不完整');
    }else if(e.type==='status'){
      if(!isName(e.team)||!isName(e.who)||typeof e.mark!=='string') badBackup('state.events 的状态记录不完整');
    }else badBackup('state.events 有未知类型：'+e.type);
  });
  if(!isObj(st.subMark)) badBackup('state.subMark 必须是对象');
  Object.keys(st.subMark).forEach(function(n){
    if(!isInt(st.subMark[n])||st.subMark[n]<0||st.subMark[n]>95) badBackup('state.subMark 的分钟不合法');
  });
  if(st.keep!=null){
    if(!isObj(st.keep)) badBackup('state.keep 必须是对象');
    Object.keys(st.keep).forEach(function(t){
      var k=st.keep[t];
      if(!isObj(k)) badBackup('state.keep.'+t+' 必须是对象');
      if(k.form!=null&&(typeof k.form!=='string'||!FORMS[k.form])) badBackup('state.keep.'+t+'.form 有未知阵型');
      if(k.lineup!=null){
        if(!Array.isArray(k.lineup)||k.lineup.length!==11) badBackup('state.keep.'+t+'.lineup 必须是 11 人数组');
        k.lineup.forEach(function(n){ if(n!==null&&!isName(n)) badBackup('state.keep.'+t+'.lineup 有非法球员值'); });
      }
      if(k.tactic!=null&&!TAX_OK[k.tactic]) badBackup('state.keep.'+t+'.tactic 有未知姿态');
    });
  }
}
function validateBackupLogs(arr){
  if(!Array.isArray(arr)) badBackup('logs 必须是数组');
  arr.forEach(function(x){
    if(!isObj(x)) badBackup('logs 里有非法记录');
    if(typeof x.txt!=='string') badBackup('logs 记录缺少文本');
    if(!isNum(x.ts)) badBackup('logs 记录缺少时间戳');
    if(x.wx!=null&&x.wx!=='dry'&&x.wx!=='rain') badBackup('logs.wx 类型不对');
    if(x.edited!=null&&!isNum(x.edited)) badBackup('logs.edited 类型不对');
    ['home','away','form'].forEach(function(k){
      if(x[k]!=null&&typeof x[k]!=='string') badBackup('logs.'+k+' 类型不对');
    });
    ['hs','as','min'].forEach(function(k){
      if(x[k]!=null&&!isNum(x[k])) badBackup('logs.'+k+' 类型不对');
    });
  });
}
function parseBackup(d){
  if(!isObj(d)) badBackup('备份最外层必须是 JSON 对象');
  var hasState=Object.prototype.hasOwnProperty.call(d,'state')&&d.state!=null&&d.state!=='';
  var hasLogs=Object.prototype.hasOwnProperty.call(d,'logs')&&d.logs!=null&&d.logs!=='';
  if(!hasState&&!hasLogs) badBackup('备份里没有可导入的 state 或 logs');
  var plan={state:null,stateText:null,logsText:null};
  if(hasState){
    if(typeof d.state!=='string') badBackup('state 必须是 JSON 字符串（现有备份格式）');
    var st;
    try{ st=JSON.parse(d.state); }catch(e){ badBackup('state 不是有效 JSON'); }
    validateBackupState(st);
    plan.state=st; plan.stateText=d.state;
  }
  if(hasLogs){
    if(typeof d.logs!=='string') badBackup('logs 必须是 JSON 字符串（现有备份格式）');
    var lg;
    try{ lg=JSON.parse(d.logs); }catch(e){ badBackup('logs 不是有效 JSON'); }
    validateBackupLogs(lg);
    plan.logsText=d.logs;
  }
  return plan;
}
function applyBackupState(st){
  S.home=st.home; S.away=st.away; S.minute=st.minute; S.hs=st.hs; S.as=st.as;
  FORM_SEL=st.form; S.status=st.status; S.tactic=st.tactic; S.poss=st.poss;
  S.weather=st.weather==='rain'?'rain':'dry';
  S.events=cleanPreSubs(st.events); S.subMark=cleanSubMark(st.subMark); S.lineup=st.lineup;
  Object.keys(KEEP).forEach(function(k){ delete KEEP[k]; });
  if(st.keep) Object.keys(st.keep).forEach(function(k){ KEEP[k]=st.keep[k]; });
  S.lastDiff=null;
  S.snap={h:metrics(S.lineup[S.home]||[]),a:metrics(S.lineup[S.away]||[])};
}
function applyBackup(d){
  var plan=parseBackup(d);
  var oldState=localStorage.getItem(KEY);
  var oldLogs=localStorage.getItem(LOGKEY);
  try{
    if(plan.stateText!=null) localStorage.setItem(KEY,plan.stateText);
    if(plan.logsText!=null) localStorage.setItem(LOGKEY,plan.logsText);
  }catch(e){
    try{ if(oldState===null) localStorage.removeItem(KEY); else localStorage.setItem(KEY,oldState); }catch(e2){}
    try{ if(oldLogs===null) localStorage.removeItem(LOGKEY); else localStorage.setItem(LOGKEY,oldLogs); }catch(e3){}
    badBackup('浏览器存储写入失败，已保持原数据');
  }
  if(plan.state) applyBackupState(plan.state);
}
function importFromText(){
  var ta=document.getElementById('bktext');
  var v=(ta&&ta.value||'').trim();
  if(!v){ alert('先把备份内容粘进下面那个框'); return; }
  var d;
  try{ d=JSON.parse(v); }catch(e){ alert('导入失败：这段内容不是有效的 JSON'); return; }
  try{ applyBackup(d); }catch(e){ alert('导入失败：'+e.message); return; }
  alert('导入成功，刷新后生效'); location.reload();
}
function exportData(){
  var data={at:Date.now(),origin:location.origin,
    state:localStorage.getItem('tb_v41_state')||'',
    logs:localStorage.getItem('tb_v4_logs')||''};
  var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  var a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='战术板备份-'+new Date().toISOString().slice(0,10)+'.json';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
}
function importData(f){
  if(!f) return;
  var r=new FileReader();
  r.onload=function(){
    var d;
    try{ d=JSON.parse(r.result); }catch(e){ alert('导入失败：文件不是有效的 JSON'); return; }
    try{ applyBackup(d); }catch(e){ alert('导入失败：'+e.message); return; }
    alert('导入成功，刷新后生效'); location.reload();
  };
  r.onerror=function(){ alert('文件读不出来，可能不是备份文件'); };
  r.readAsText(f);
}
function renderLog(){
  var arr=logs();
  var editing=(LOG_EDIT>=0&&arr[LOG_EDIT])?arr[LOG_EDIT]:null;
  if(!editing&&LOG_EDIT>=0) LOG_EDIT=-1;
  var old=document.getElementById('logtxt');
  var draft=old?old.value:null;
  var selStart=old?old.selectionStart:null;
  var selEnd=old?old.selectionEnd:null;
  var editVal=editing?(draft!=null?draft:editing.txt):'';
  var list=arr.length?arr.map(function(x,i){
    var tm=logTime(x.ts);
    var wx=wxLabel(x.wx);
    var ed=x.edited?'<span class="edtag">已编辑</span>':'';
    return '<div class="lg"><div class="lgx">'+
      '<button class="x edit" data-edit="'+i+'" aria-label="编辑">✎</button>'+
      '<button class="x del" data-del="'+i+'" aria-label="删除">✕</button></div>'+
      '<div class="m">'+tm+' · '+esc(x.home)+' '+esc(x.hs)+':'+esc(x.as)+' '+esc(x.away)+' · '+esc(x.min)+"' · "+esc(x.form)+(wx?' · '+wx:'')+(ed?' '+ed:'')+'</div>'+
      '<div class="c">'+esc(x.txt)+'</div></div>';
  }).join(''):'<div class="lesson"><p>还没有记录。看完一场球写一句判断，赛后回来对照——这是涨球商最快的办法。</p></div>';
  var editBar=editing?'<div class="editbar">正在编辑 '+logTime(editing.ts)+' 的记录；保存会覆盖文字，比分/时间/阵型不变</div>':'';
  var cancelBtn=editing?'<button class="tb" style="width:100%;margin-top:8px;padding:10px" onclick="cancelEdit()">取消编辑</button>':'';
  document.getElementById('log').innerHTML=
    '<div class="sec">复盘日志</div>'+
    '<div class="lesson"><h3>数据存在哪 · 会不会丢</h3>'+
    '<p><b>存在你这台设备的浏览器里</b>，不是存在我这边，也不是云端。对应的地址是 <b>'+location.origin+'</b>。</p>'+
    '<p>所以：<b>关掉网页、电脑重启，都还在</b>；但换一个地址打开（127.0.0.1 ↔ 局域网 IP ↔ 直接双击文件）就是另一份存储，互相看不见。</p>'+
    '<p>会丢的情况只有三种：清浏览器数据、无痕模式、换设备。</p>'+
    '<button class="hbtn2" onclick="copyBackup()">复制备份到剪贴板（手机推荐）</button>'+
    '<button class="tb" style="width:100%;margin-top:8px;padding:10px" onclick="exportData()">下载成 JSON 文件</button>'+
    '<div class="lov" style="margin-top:12px">恢复：把备份内容粘进下面的框，再点导入</div>'+
    '<textarea id="bktext" style="display:none;min-height:110px;font-size:11px"></textarea>'+
    '<button class="tb" style="width:100%;margin-top:8px;padding:10px" onclick="importFromText()">从这段内容导入</button>'+
    '<input type="file" id="impfile" accept=".json" style="display:none" onchange="importData(this.files[0])">'+
    '<button class="tb" style="width:100%;margin-top:8px;padding:10px" onclick="document.getElementById(\'impfile\').click()">从 JSON 文件恢复</button>'+
    '<div class="ae">手机上下载的 JSON 会落在「文件管理 → 下载」里；小米的路径是「文件管理 → 手机 → Download」。找不到就用上面的剪贴板方式。</div>'+
    '</div>'+
    '<div class="lesson"><h3>记一条判断</h3>'+
    '<p>不用写得好，写下来就行。会自动记录当前的对阵、比分、时间、阵型。</p>'+
    editBar+
    '<textarea id="logtxt" placeholder="例：我觉得曼联这场右路会被打穿，因为达洛特压上后身后没人补。">'+esc(editVal)+'</textarea>'+
    '<button class="hbtn2" onclick="saveLog()">'+(editing?'保存修改':'保存这条判断')+'</button>'+
    cancelBtn+
    '<div class="eg">'+S.home+' vs '+S.away+' · '+S.hs+':'+S.as+' · '+S.minute+"' · "+formOf(S.home)+'</div></div>'+
    '<div class="sec">历史（'+arr.length+'）</div>'+list;
  if(editing){
    var t2=document.getElementById('logtxt');
    if(t2){
      t2.focus();
      if(selStart!=null&&selEnd!=null){
        try{ t2.setSelectionRange(Math.min(selStart,t2.value.length),Math.min(selEnd,t2.value.length)); }catch(e){}
      }
    }
  }
}

/* ---------------- 教练卡（换帅） ---------------- */
var CE=null;
var PROFILE={};
var CFLAGS=[['fbin','边后卫内收','压上时变中场人数'],['single6','单后腰','只留一个 6 号'],
 ['highline','高位防线','防线压到中场'],['target9','支点中锋','中锋背身做墙'],
 ['gkbuild','门将出球','门将参与后场倒脚']];
function openCoach(team){
  var st=styleOf(team);
  var pf=PROFILE[team]||{};
  CE={team:team,press:st.press||2,control:st.control||2,direct:st.direct||2,low:st.low||1,
      form:formOf(team),flags:pf.flags||{}};
  drawCoach();
}
function drawCoach(){
  var rows=[['press','压迫强度','逼抢有多凶'],['control','控球意愿','想把球留在脚下'],
            ['direct','直接程度','一脚打身后的比例'],['low','低位倾向','愿不愿意退着踢']];
  var body=rows.map(function(r){
    var k=r[0],label=r[1],sub=r[2];
    var btns=[0,1,2,3].map(function(v){
      return '<button class="fchip '+(CE[k]===v?'on':'')+'" data-ce="'+k+'" data-v="'+v+'">'+v+'</button>';
    }).join('');
    return '<div class="row" style="justify-content:space-between;margin:8px 0"><div>'+
      '<div style="font-size:13px">'+label+' <span class="mut">'+sub+'</span></div></div>'+
      '<div style="display:flex;gap:4px">'+btns+'</div></div>';
  }).join('');
  var forms=BASE_FORMS.map(function(f){
    return '<button class="fchip '+(CE.form===f?'on':'')+'" data-cf="'+f+'">'+f+'</button>';
  }).join('');
  var flags=CFLAGS.map(function(f){
    return '<button class="fchip '+(CE.flags[f[0]]?'on':'')+'" data-cflag="'+f[0]+'">'+f[1]+'</button>';
  }).join('');
  var pf=PROFILE[CE.team]||{};
  $('#sheet').innerHTML='<div class="sheetIn"><div class="sh"><b>教练卡 · '+esc(CE.team)+'</b>'+
    '<button class="x" onclick="closeSheet()">✕</button></div>'+
    '<div class="lov">① 踢法四轴（给引擎用的方向，0=不要 3=极致）</div>'+body+
    '<div class="lov">② 结构特征（这些才是真正区分教练的东西）</div>'+
    '<div class="frow" style="margin:0;flex-wrap:wrap">'+flags+'</div>'+
    '<div class="lov">③ 阵型</div><div class="frow" style="margin:0">'+forms+'</div>'+
    '<div class="lov">④ 他的要求（人读的，写你自己的理解）</div>'+
    '<textarea id="ceText" placeholder="例：要求边后卫内收进中场，6 号位单后腰，丢球后 5 秒内反抢。">'+esc(pf.text||'')+'</textarea>'+
    '<div class="lov">⑤ 出处（写清楚你从哪知道的，别凭印象）</div>'+
    '<input id="ceSrc" style="width:100%;background:var(--card2);border:1px solid var(--line);border-radius:8px;color:var(--txt);padding:9px;font-size:12.5px;font-family:inherit" placeholder="例：官网公告 / The Athletic 长文 / 他在 X 队的公开采访" value="'+esc(pf.src||'')+'">'+
    '<button class="hbtn2" onclick="applyCoach()">应用并重排阵容</button>'+
    '<div class="ae" style="border:0;margin-top:8px">前三项给引擎算，④⑤给你自己和以后回看。出处空的卡片，页面上会标「未核实」。</div></div>';
  $('#sheet').classList.add('on');
}
function setCE(k,v){ if(CE){ CE[k]=v; drawCoach(); } }
function setCF(f){ if(CE){ CE.form=f; drawCoach(); } }
function applyCoach(){
  if(!CE) return;
  var t=CE.team;
  STYLE_FIX[t]={press:CE.press,control:CE.control,direct:CE.direct,low:CE.low};
  FORM_OVERRIDE[t]=CE.form;
  var before=(S.lineup[t]||[]).slice();
  FORM_SEL[t]=CE.form;
  var after=autoLineup(t);
  S.lineup[t]=after;
  var bset={},aset={};
  before.forEach(function(n){ if(n) bset[n]=1; });
  after.forEach(function(n){ if(n) aset[n]=1; });
  var inN=after.filter(function(n){ return n&&!bset[n]; });
  var outN=before.filter(function(n){ return n&&!aset[n]; });
  var tx=document.getElementById('ceText'), sr=document.getElementById('ceSrc');
  PROFILE[t]={text:(tx?tx.value.trim():''),src:(sr?sr.value.trim():''),flags:CE.flags};
  S.coachNote={team:t,form:CE.form,in:inN,out:outN,
    style:{press:CE.press,control:CE.control,direct:CE.direct,low:CE.low},
    text:PROFILE[t].text,src:PROFILE[t].src,flags:CE.flags};
  CE=null; closeSheet(); renderAll(); switchTab('analysis');
}
function coachNoteCard(){
  var c=S.coachNote; if(!c) return '';
  var st=c.style, tips=[];
  if(st.press>=3) tips.push('高位压迫：边锋和边后卫的跑动量要求暴涨，慢中卫会被暴露');
  if(st.control>=3) tips.push('控球为主：组织型中场升值，纯破坏型中场贬值');
  if(st.low>=2) tips.push('愿意退守：防守型中场和中卫升值，前锋变成反击支点');
  if(st.direct>=3) tips.push('直接打法：速度型前锋升值，控球型中场贬值');
  if(!tips.length) tips.push('这套体系比较均衡，阵容变化不会太大');
  return '<div class="ac l1"><div class="ah"><span class="tag">换帅影响 · '+esc(c.team)+'</span>'+
    '<span class="lv">'+c.form+confTag(c.src?'fact':'guess')+'</span></div>'+
    '<div class="at">'+
      (c.in.length?'新体系下首发变化：<b style="color:#8ef0b3">↑ '+esc(c.in.join('、'))+'</b><br>':'')+
      (c.out.length?'<b style="color:#ffb4b7">↓ '+esc(c.out.join('、'))+'</b>':'')+
      (c.in.length||c.out.length?'':'首发没有变化，说明这套人员对新体系是适配的。')+
    '</div>'+
    '<div class="pl"><b>人话：</b>换了教练，先动的是他的要求，不是球员的能力。</div>'+
    (c.flags&&Object.keys(c.flags).filter(function(k){return c.flags[k];}).length?
      '<div class="ae"><b>结构：</b>'+Object.keys(c.flags).filter(function(k){return c.flags[k];})
        .map(function(k){ var f=CFLAGS.filter(function(x){return x[0]===k;})[0]; return f?f[1]:k; }).join(' · ')+'</div>':'')+
    (c.text?'<div class="ae"><b>他的要求：</b>'+esc(c.text)+'</div>':'')+
    '<div class="ae"><b>出处：</b>'+(c.src?esc(c.src):'<span style="color:#f0b429">未核实——这张卡目前只是我的推测，别当权威用</span>')+'</div>'+
    '<div class="ae">'+tips.map(function(x){return '· '+esc(x);}).join('<br>')+'</div></div>';
}

/* ---------------- 事件委托 ---------------- */
document.addEventListener('click',function(e){
  var t=e.target;
  var tb=t.closest?t.closest('#tabs button'):null;
  if(tb){ switchTab(tb.getAttribute('data-tab')); return; }
  var dop=t.closest?t.closest('[data-drill-opt]'):null;
  if(dop){ drillAnswer(Number(dop.getAttribute('data-drill-opt'))); return; }
  var dnx=t.closest?t.closest('[data-drill-next]'):null;
  if(dnx){ drillNext(); return; }
  var drg=t.closest?t.closest('[data-drill-regroup]'):null;
  if(drg){ drillRegroup(); return; }
  var dgo=t.closest?t.closest('[data-drill-goto]'):null;
  if(dgo){ switchTab('lineup'); return; }
  var ed=t.closest?t.closest('[data-edit]'):null;
  if(ed){ editLog(Number(ed.getAttribute('data-edit'))); return; }
  var dl=t.closest?t.closest('[data-del]'):null;
  if(dl){ delLog(Number(dl.getAttribute('data-del'))); return; }
  var tx=t.closest?t.closest('[data-tax]'):null;
  if(tx){ setTax(tx.getAttribute('data-tax'),tx.getAttribute('data-v')); return; }
  var cb=t.closest?t.closest('[data-coach]'):null;
  if(cb){ openCoach(cb.getAttribute('data-coach')); return; }
  var cfl=t.closest?t.closest('[data-cflag]'):null;
  if(cfl){ var k=cfl.getAttribute('data-cflag'); CE.flags[k]=!CE.flags[k]; drawCoach(); return; }
  var ce=t.closest?t.closest('[data-ce]'):null;
  if(ce){ setCE(ce.getAttribute('data-ce'),Number(ce.getAttribute('data-v'))); return; }
  var cf=t.closest?t.closest('[data-cf]'):null;
  if(cf){ setCF(cf.getAttribute('data-cf')); return; }
  var tm=t.closest?t.closest('[data-term]'):null;
  if(tm){ openTerm(tm.getAttribute('data-term')); return; }
  var ld=t.closest?t.closest('[data-lead]'):null;
  if(ld){ toggleLead(ld.getAttribute('data-lead')); return; }
  var dp=t.closest?t.closest('[data-desp]'):null;
  if(dp){ toggleDesperate(dp.getAttribute('data-desp')); return; }
  var ps=t.closest?t.closest('[data-poss]'):null;
  if(ps){ togglePoss(ps.getAttribute('data-poss')); return; }
  var fc=t.closest?t.closest('.fchip[data-form]'):null;
  if(fc){ changeForm(fc.getAttribute('data-team'),fc.getAttribute('data-form')); return; }
  var tk=t.closest?t.closest('.tk'):null;
  if(tk){ openSheet(tk.getAttribute('data-w'),Number(tk.getAttribute('data-i'))); return; }
  var stb=t.closest?t.closest('.st'):null;
  if(stb){ setSt(stb.getAttribute('data-n'),stb.getAttribute('data-st')); return; }
  var pick=t.closest?t.closest('[data-pick]'):null;
  if(pick){ var sh=document.getElementById('sheet');
    setSlot(sh.dataset.wi,Number(sh.dataset.idx),pick.getAttribute('data-pick')); return; }
  var nul=t.closest?t.closest('[data-slotnull]'):null;
  if(nul){ var sh2=document.getElementById('sheet');
    setSlot(sh2.dataset.wi,Number(sh2.dataset.idx),null); return; }
  if(e.target.id==='sheet') closeSheet();
});

/* ---------------- 启动 ---------------- */
loadHudPref();
if(!load()){
  S.lineup[S.home]=autoLineup(S.home);
  S.lineup[S.away]=autoLineup(S.away);
}
if(!S.lineup[S.home]) S.lineup[S.home]=autoLineup(S.home);
if(!S.lineup[S.away]) S.lineup[S.away]=autoLineup(S.away);
S.snap={h:metrics(S.lineup[S.home]),a:metrics(S.lineup[S.away])};
renderSetup(); renderAll(); switchTab('lineup');
applyHudPref();
var _hudEl=document.getElementById('hud');
if(_hudEl){ _hudEl.addEventListener('pointerdown',function(){ if(HUD.mode==='auto') showHud(); }); }
window.addEventListener('resize',syncHudSpace);
window.setTeam=setTeam; window.swapSides=swapSides; window.setSlot=setSlot;
window.setSt=setSt; window.closeSheet=closeSheet; window.openSheet=openSheet;
window.changeForm=changeForm; window.addGoal=addGoal; window.addMin=addMin;
window.setMin=setMin; window.resetMatch=resetMatch;
window.setTax=setTax; window.togglePoss=togglePoss; window.toggleDesperate=toggleDesperate;
window.toggleLead=toggleLead;
window.openTerm=openTerm; window.openTermsAll=openTermsAll;
window.switchTab=switchTab; window.openCoach=openCoach; window.applyCoach=applyCoach;
window.setCE=setCE; window.setCF=setCF; window.saveLog=saveLog; window.delLog=delLog; window.renderLearn=renderLearn;
window.setWeather=setWeather; window.editLog=editLog; window.cancelEdit=cancelEdit;
window.toggleHudCfg=toggleHudCfg; window.setHudSize=setHudSize; window.setHudMode=setHudMode;
window.showHud=showHud; window.hideHud=hideHud; window.collapseHudNow=collapseHudNow;
"""

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0c1015">
<title>对位引擎 v4.2</title>
<style>
:root{--bg:#0c1015;--card:#151a21;--card2:#1b222c;--line:#2a323d;--txt:#e8eef5;--mut:#93a0af;
--red:#e2383f;--green:#23c55e;--amber:#f0b429;--blue:#4ea1ff;--pitchA:#0e4f2f;--pitchB:#0b3f25}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,BlinkMacSystemFont,"PingFang SC",Roboto,"Microsoft YaHei",sans-serif}
header{position:sticky;top:0;z-index:50;background:rgba(12,16,21,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding:10px 14px 8px}
h1{margin:0;font-size:16px;font-weight:800}h1 b{color:var(--red)}
.sub{font-size:11px;color:var(--mut);margin-top:2px}
main{max-width:760px;margin:0 auto;padding:10px 12px calc(var(--hud-h,104px) + 18px)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:10px}
.row{display:flex;align-items:center;gap:8px;margin:4px 0}
.mut{color:var(--mut);font-size:12px}
.fml{font-size:13px;font-weight:600}
details{margin:4px 0;border:1px solid var(--line);border-radius:10px;background:var(--card2)}
summary{padding:9px 12px;font-size:13px;cursor:pointer;color:var(--mut)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:0 8px 8px}
.tb{background:var(--card);border:1px solid var(--line);color:var(--txt);border-radius:8px;padding:9px 6px;font-size:13px;font-family:inherit}
.tb.on{border-color:var(--red);background:rgba(226,56,63,.14);font-weight:700}
.pitchwrap{margin-bottom:10px}
.phead{display:flex;align-items:center;gap:6px;font-size:13px;margin:2px 0 6px}
.phead .dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.postureHint{font-size:11px;color:#93a0af;text-align:left;margin:0 0 5px;padding:0 2px;line-height:1.4}
.frow{display:flex;gap:5px;overflow-x:auto;padding:2px 0 6px;max-width:420px;margin:0 auto;scrollbar-width:none}
.fchip{flex:0 0 auto;background:var(--card2);border:1px solid var(--line);color:var(--mut);border-radius:99px;padding:5px 9px;font-size:11px;font-family:inherit}
.fchip.on{border-color:var(--red);color:#fff;background:rgba(226,56,63,.16);font-weight:700}
.wxchip{padding:7px 12px;font-size:12px}
.frow.tax{justify-content:center;gap:4px;flex-wrap:wrap}
.fbrk{flex-basis:100%;height:0}
.fchip.desperate{border-color:rgba(226,56,63,.45);color:#ffb4b7}
.fchip.desperate.on{background:rgba(226,56,63,.28);border-color:var(--red);color:#fff}
.fchip.lead{border-color:rgba(78,161,255,.45);color:#a8d2ff}
.fchip.lead.on{background:rgba(78,161,255,.22);border-color:var(--blue);color:#fff}
.sep2{width:1px;height:14px;background:var(--line);margin:0 2px}
.cf{display:inline-block;font-size:10px;border:1px solid;border-radius:99px;padding:0 7px;margin-left:6px;vertical-align:1px}
.legend .at{font-size:12.5px}
.tchips{display:flex;flex-wrap:wrap;gap:6px;margin:2px 0}
.tchip{background:rgba(78,161,255,.14);border:1px solid rgba(78,161,255,.45);color:#a8d2ff;
border-radius:99px;padding:6px 12px;font-size:13px;font-family:inherit}
.tchip:active{transform:scale(.95)}
.pl{margin-top:6px;font-size:13px;color:#bfe3c9;background:rgba(35,197,94,.08);
border-left:2px solid rgba(35,197,94,.5);padding:6px 9px;border-radius:0 6px 6px 0;line-height:1.55}
.pl b{color:#8ef0b3}
.hbtn{background:rgba(78,161,255,.14);border:1px solid rgba(78,161,255,.4);color:#a8d2ff;
border-radius:99px;padding:3px 10px;font-size:11px;font-family:inherit;margin-left:6px}
.mini:active,.tb:active,.fchip:active,.pr:active{transform:scale(.93)}
.mn.pop,.sc.pop{animation:pop .38s ease-out}
@keyframes pop{0%{color:#fff;transform:scale(1.35)}60%{color:var(--amber);transform:scale(1.08)}100%{transform:scale(1)}}
.tk{transition:transform .12s}
.tk:active{transform:translate(-50%,-50%) scale(.9)}
.pitch{position:relative;width:100%;max-width:420px;aspect-ratio:.86;margin:0 auto;background:linear-gradient(180deg,var(--pitchA),var(--pitchB));border:1px solid #1d5c3a;border-radius:10px;overflow:hidden}
.pitch:before{content:"";position:absolute;left:0;right:0;top:50%;height:1px;background:rgba(255,255,255,.22)}
.tk{position:absolute;transform:translate(-50%,-50%);background:#c9202b;border:1.5px solid #fff3;border-radius:50%;width:54px;height:54px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:9px;line-height:1.1;text-align:center;box-shadow:0 2px 6px #0006}
.tk b{font-size:10px;font-weight:700;max-width:52px;overflow:hidden;white-space:nowrap}
.tk i{font-style:normal;opacity:.65;font-size:8px}
.tk em{position:absolute;top:-7px;right:-5px;font-style:normal;font-size:13px}
.tk .sbm{position:absolute;bottom:-8px;left:50%;transform:translateX(-50%);font-style:normal;
font-size:9px;background:#111a22;border:1px solid rgba(35,197,94,.6);color:#8ef0b3;
border-radius:99px;padding:1px 5px;white-space:nowrap}
.tk.empty{background:#ffffff10;border:1px dashed #ffffff45;color:#ffffff90}
.tk[data-w=a]{background:#1f6feb}
.hint{font-size:10.5px;color:#6b7887;text-align:center;margin-top:4px}
.sec{font-size:11px;letter-spacing:1.6px;color:var(--mut);margin:14px 0 6px;font-weight:700}
.ac{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--mut);border-radius:10px;padding:10px 11px;margin-bottom:8px}
.ac.l1{border-left-color:var(--amber)}
.ac.l2{border-left-color:var(--red);background:linear-gradient(180deg,rgba(226,56,63,.07),var(--card) 60%)}
.ah{display:flex;justify-content:space-between;font-size:11px;color:var(--mut);margin-bottom:4px}
.at{font-size:13.5px;line-height:1.6}
.ae{font-size:11px;color:#7d8a99;margin-top:6px;padding-top:6px;border-top:1px dashed #ffffff14;line-height:1.5}
.tlc{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 11px}
.tl{font-size:12px;color:var(--txt);padding:3px 0;border-bottom:1px dashed #ffffff10}
.tl:last-child{border-bottom:0}
.tl b{color:var(--amber);margin-right:6px}
#tabs{position:sticky;top:0;z-index:45;display:flex;gap:6px;padding:8px 12px;
background:rgba(12,16,21,.96);border-bottom:1px solid var(--line);max-width:760px;margin:0 auto}
#tabs button{flex:1;background:var(--card2);border:1px solid var(--line);color:var(--mut);
border-radius:9px;padding:8px 4px;font-size:13px;font-family:inherit}
#tabs button.on{background:rgba(226,56,63,.16);border-color:var(--red);color:#fff;font-weight:700}
.pane{display:none}
.pane.on{display:block}
html.embed header{display:none}
html.embed main{padding-top:6px}
.lesson{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin-bottom:12px}
.lesson h3{margin:0 0 8px;font-size:15px}
.lesson p{font-size:13.5px;line-height:1.7;margin:7px 0;color:#d3dce6}
.lesson p b{color:#fff}
.lesson .egline{margin:5px 0;font-size:12.5px;line-height:1.6}
.eg{background:rgba(78,161,255,.08);border-left:2px solid rgba(78,161,255,.5);
padding:8px 10px;border-radius:0 8px 8px 0;font-size:12.5px;color:#bcd8ff;margin:8px 0}
.qz{margin-top:10px;border-top:1px dashed #ffffff14;padding-top:10px}
.qz .qq{font-size:13px;margin-bottom:6px}
.qz .opt{display:block;width:100%;text-align:left;background:var(--card2);border:1px solid var(--line);
color:var(--txt);border-radius:8px;padding:8px 10px;font-size:12.5px;font-family:inherit;margin:5px 0}
.qz .opt.ok{border-color:var(--green);background:rgba(35,197,94,.12)}
.qz .opt.no{border-color:var(--red);background:rgba(226,56,63,.12)}
.qz .why{font-size:12px;color:var(--mut);margin-top:6px;line-height:1.6}
.dhead{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:10px}
.dstate{font-size:14px;line-height:1.5;overflow-wrap:anywhere}
.dstate b{color:#fff}
.dmeta{font-size:11px;color:var(--mut);margin-top:4px;line-height:1.55;overflow-wrap:anywhere}
.dlegend{font-size:11.5px;color:#8b98a7;line-height:1.6;margin-top:8px;border-top:1px dashed #ffffff14;padding-top:7px}
.dprog{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:var(--mut);margin:10px 2px 6px}
.ldots{display:flex;gap:5px;align-items:center}
.ldots span{width:7px;height:7px;border-radius:99px;background:#ffffff1f;display:block;transition:width .15s}
.ldots span.now{background:var(--red);width:18px}
.ldots span.done{background:var(--green)}
.dcard{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:13px;margin-bottom:10px}
.dtop{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.dtype{font-size:10px;letter-spacing:1.2px;color:#a8d2ff;background:rgba(78,161,255,.12);
border:1px solid rgba(78,161,255,.35);border-radius:99px;padding:2px 8px}
.dscenario{background:rgba(78,161,255,.08);border-left:2px solid rgba(78,161,255,.5);
border-radius:0 8px 8px 0;padding:8px 10px;font-size:12.5px;line-height:1.6;color:#bcd8ff;overflow-wrap:anywhere}
.dq{font-size:14px;line-height:1.6;margin:11px 0 8px;font-weight:700;overflow-wrap:anywhere}
.dopt{display:flex;gap:8px;align-items:flex-start;width:100%;text-align:left;background:var(--card2);
border:1px solid var(--line);color:var(--txt);border-radius:9px;padding:10px 11px;font-size:12.5px;
line-height:1.55;font-family:inherit;margin:6px 0;min-height:42px;overflow-wrap:anywhere}
.dopt b{color:var(--mut);font-size:11px;flex:0 0 14px;padding-top:2px}
.dopt span{flex:1}
.dopt.ok{border-color:var(--green);background:rgba(35,197,94,.12)}
.dopt.no{border-color:var(--red);background:rgba(226,56,63,.12)}
.dwhy{margin-top:10px;border-top:1px dashed #ffffff14;padding-top:9px}
.dres{font-size:12.5px;font-weight:700;margin-bottom:5px}
.dres.ok{color:#8ef0b3}
.dres.no{color:#ffb4b7}
.dwhytxt{font-size:12.5px;line-height:1.65;color:#d3dce6;overflow-wrap:anywhere}
.dev{font-size:11px;color:#7d8a99;line-height:1.55;margin-top:7px;overflow-wrap:anywhere}
.dev b{color:#9fb0c1}
.dcf{margin-top:6px;text-align:right}
.dbtn{background:var(--card2);border:1px solid var(--line);color:var(--txt);border-radius:9px;
padding:10px 12px;font-size:13px;font-family:inherit;min-height:42px}
.dbtn:active{transform:scale(.97)}
.dbtn.primary{background:rgba(226,56,63,.18);border-color:var(--red);color:#fff;font-weight:700}
.dnext{width:100%;margin-top:10px}
.dsum{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:10px;text-align:center}
.dsumh{font-size:12px;letter-spacing:1.4px;color:var(--mut);font-weight:700}
.dscore{font-size:22px;font-weight:800;margin:8px 0 4px}
.dsub{font-size:12px;color:var(--mut);line-height:1.6}
.dacts{display:flex;gap:8px;margin-top:12px}
.dacts .dbtn{flex:1}
.dempty{background:rgba(240,180,41,.08);border:1px solid rgba(240,180,41,.3);border-radius:12px;
padding:12px;font-size:12.5px;line-height:1.65;color:#e8cf9b;margin-bottom:10px}
.dquick{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:12px 0 20px}
.dquick summary{font-size:12.5px;color:#a8d2ff;font-weight:700;cursor:pointer}
.dqrow{margin-top:10px;border-top:1px dashed #ffffff10;padding-top:8px}
.dqrow b{font-size:12.5px}
.dqrow p{font-size:12px;line-height:1.65;color:#b9c6d3;margin:4px 0 0}
.dqrow .tchip{padding:2px 7px;font-size:11px;vertical-align:1px}
.lg{position:relative;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px;margin-bottom:8px}
.lg .m{font-size:11px;color:var(--mut);margin-bottom:4px;padding-right:62px}
.lg .c{font-size:13.5px;line-height:1.6;overflow-wrap:anywhere;word-break:break-word}
.lg .x{float:right;background:none;border:0;color:#6b7887;font-size:14px}
.lgx{position:absolute;top:6px;right:6px;display:flex;align-items:center;gap:6px}
.lgx .x{float:none;font-size:15px;line-height:1;padding:4px 5px;min-width:24px;min-height:24px;border-radius:5px}
.lgx .x.edit{color:#a8d2ff}
.lgx .x.del{color:#ffb4b7}
.edtag{display:inline-block;font-size:10px;border:1px solid rgba(78,161,255,.45);color:#a8d2ff;border-radius:99px;padding:0 6px;margin-left:4px;vertical-align:1px}
.editbar{background:rgba(78,161,255,.1);border:1px solid rgba(78,161,255,.35);border-left:3px solid var(--blue);border-radius:8px;padding:8px 10px;margin:8px 0;font-size:12px;line-height:1.5;color:#bcd8ff;overflow-wrap:anywhere}
textarea{width:100%;min-height:74px;background:var(--card2);border:1px solid var(--line);
border-radius:10px;color:var(--txt);padding:10px;font-size:13.5px;font-family:inherit;resize:vertical}
.hbtn2{background:linear-gradient(180deg,#e2383f,#a32228);border:0;color:#fff;border-radius:10px;
padding:10px 14px;font-size:13.5px;font-family:inherit;width:100%;margin-top:8px}
#hud{position:fixed;bottom:0;left:0;right:0;z-index:60;background:rgba(16,20,26,.97);border-top:1px solid var(--line);padding:4px 36px calc(5px + env(safe-area-inset-bottom)) 8px;transition:transform .22s ease,background .2s ease}
.hRow{display:flex;align-items:center;gap:5px;justify-content:center;margin:1px 0}
.hTeam{font-size:12px;color:var(--mut);max-width:22vw;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sc{font-size:17px;min-width:18px;text-align:center;cursor:pointer}
.goal{font-size:14px;padding:5px 9px;border-color:#3a4552}
.mn{font-size:13px;min-width:34px;text-align:center;color:var(--amber)}
.mini{background:var(--card2);border:1px solid var(--line);color:var(--txt);border-radius:6px;padding:4px 7px;font-size:11.5px;font-family:inherit;line-height:1}
.hcfg{position:absolute;right:6px;top:4px;z-index:2;width:30px;height:30px;padding:0;border-radius:8px;background:var(--card2);border:1px solid var(--line);color:var(--mut);font-size:16px;line-height:1;font-family:inherit}
.hcfg:active{transform:scale(.92)}
#hud.hud-compact{padding-top:2px;padding-bottom:calc(3px + env(safe-area-inset-bottom))}
.hud-compact .hRow{gap:3px;margin:0}
.hud-compact .mini{padding:2px 4px;font-size:10px}
.hud-compact .goal{font-size:12px;padding:3px 6px}
.hud-compact .sc{font-size:15px;min-width:16px}
.hud-compact .mn{font-size:12px;min-width:28px}
.hud-compact .hTeam{font-size:11px;max-width:20vw}
.hud-compact .hcfg{width:30px;height:30px;font-size:16px;top:2px}
#hud.hud-large{padding-top:6px;padding-bottom:calc(7px + env(safe-area-inset-bottom))}
.hud-large .hRow{gap:6px;margin:2px 0;flex-wrap:wrap}
.hud-large .mini{padding:6px 9px;font-size:13px}
.hud-large .goal{font-size:16px;padding:7px 10px}
.hud-large .sc{font-size:20px;min-width:20px}
.hud-large .mn{font-size:15px;min-width:38px}
.hud-large .hTeam{font-size:13px;max-width:22vw}
.hud-large .hcfg{width:32px;height:32px;font-size:17px;top:6px}
#hud.hud-semi{background:rgba(16,20,26,.72);backdrop-filter:blur(4px)}
#hud.hud-hidden{transform:translateY(110%)}
#hudShow{position:fixed;left:50%;bottom:calc(8px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:61;display:none;background:var(--card);border:1px solid var(--line);color:var(--txt);border-radius:99px;padding:9px 16px;font-size:12px;font-family:inherit;box-shadow:0 4px 12px #0006}
#hudShow.on{display:block}
#hudCfg{position:fixed;left:12px;right:12px;max-width:380px;margin:0 auto;bottom:calc(var(--hud-h,104px) + 10px);z-index:70;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;box-shadow:0 10px 28px #0009;display:none}
#hudCfg.on{display:block}
.hudcfg-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.hudcfg-h b{font-size:13px}
.hudcfg-h .x{background:none;border:0;color:var(--mut);font-size:20px;line-height:1;padding:6px 8px;min-width:34px;min-height:34px}
.hudcfg-row{display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin:7px 0}
.hudcfg-row .mut{min-width:34px;font-size:11px}
.hudcfg .fchip{padding:7px 12px;font-size:12px}
.hudcfg-tip{font-size:10.5px;color:var(--mut);line-height:1.45;margin-top:8px}
.warnb{border-color:rgba(226,56,63,.5);color:#ffb4b7}
.sep{width:1px;height:16px;background:var(--line);margin:0 3px}
#sheet{position:fixed;inset:0;z-index:100;background:#0009;display:none;align-items:flex-end}
#sheet.on{display:flex}
.sheetIn{background:var(--card);width:100%;max-height:78vh;overflow:auto;border-radius:16px 16px 0 0;padding:12px 12px calc(12px + env(safe-area-inset-bottom))}
.sh{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.sh .x{background:none;border:0;color:var(--mut);font-size:18px}
.strow{display:flex;align-items:center;gap:6px;margin:6px 0 10px;flex-wrap:wrap}
.st{background:var(--card2);border:1px solid var(--line);border-radius:8px;font-size:16px;width:42px;height:36px}
.st.on{border-color:var(--red);background:rgba(226,56,63,.15)}
.lov{font-size:11px;color:var(--mut);margin:8px 0 4px}
.lgrp{font-size:11px;font-weight:700;color:#c9d4df;padding:7px 2px 3px;margin-top:2px;border-bottom:1px dashed #ffffff10}
.lgrp em{font-style:normal;font-weight:400;color:var(--mut);font-size:10.5px;margin-left:2px}
.plist{display:flex;flex-direction:column;gap:5px}
.pr{display:flex;justify-content:space-between;align-items:center;gap:8px;background:var(--card2);border:1px solid var(--line);border-radius:9px;padding:9px 11px;color:var(--txt);font-family:inherit;text-align:left;font-size:13px}
.pr.on{border-color:var(--green)}
.pr.used{opacity:.55}
.pr em{font-style:normal;font-size:11px;color:var(--green);white-space:nowrap}
</style></head>
<body>
<script>
if(location.search.indexOf('embed=1')>=0){document.documentElement.className='embed';}
</script>
<header>
  <h1>对位引擎 <b>v4.2</b>
    <button class="hbtn" onclick="openTermsAll()">术语表</button>
    <span class="mut" style="font-weight:400;font-size:11px">19 队对位 · 换人诊断</span></h1>
  <div class="sub">L1 球员本体 · L2 教练体系（换帅只改这层）· L3 比赛态（比分/时间/状态/换人）</div>
</header>
<nav id="tabs">
  <button data-tab="lineup" class="on">排阵</button>
  <button data-tab="analysis">分析</button>
  <button data-tab="learn">训练</button>
  <button data-tab="log">复盘</button>
</nav>
<main>
  <section id="pane-lineup" class="pane on">
    <section id="setup" class="card"></section>
    <section id="pitches"></section>
    <section id="substrip"></section>
  </section>
  <section id="pane-analysis" class="pane">
    <section id="analysis"></section>
  </section>
  <section id="pane-learn" class="pane">
    <section id="learn"></section>
  </section>
  <section id="pane-log" class="pane">
    <section id="log"></section>
  </section>
</main>
<div id="hud"></div>
<div id="hudCfg"></div>
<div id="hudShow" class="hudshow" onclick="showHud()">比分 ▲</div>
<div id="sheet"></div>
<script>
/*__PLAYERS__*/
/*__DATA__*/
/*__APP__*/
</script>
</body></html>
"""

base=pathlib.Path('src')
players=(base/'players.js').read_text(encoding='utf-8')
data=(base/'data.js').read_text(encoding='utf-8')
for n,s in (('players',players),('data',data)):
    assert '</script' not in s.lower(), n

out=HTML.replace('/*__PLAYERS__*/',players).replace('/*__DATA__*/',data).replace('/*__APP__*/',APP)
p=pathlib.Path('index.html')
p.write_text(out,encoding='utf-8')
print('wrote',p,round(p.stat().st_size/1024,1),'KB')
