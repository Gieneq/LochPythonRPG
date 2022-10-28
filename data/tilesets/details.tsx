<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="details" tilewidth="20" tileheight="20" tilecount="225" columns="15">
 <image source="details.png" width="300" height="300"/>
 <tile id="0">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="4"/>
   <object id="2" x="0" y="0" width="4" height="20"/>
  </objectgroup>
 </tile>
 <tile id="1">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="4"/>
  </objectgroup>
 </tile>
 <tile id="2">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="4"/>
   <object id="2" x="16" y="0" width="4" height="20"/>
  </objectgroup>
 </tile>
 <tile id="11">
  <animation>
   <frame tileid="11" duration="1000"/>
   <frame tileid="12" duration="1000"/>
  </animation>
 </tile>
 <tile id="13">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="20"/>
  </objectgroup>
 </tile>
 <tile id="15">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="4" height="20"/>
  </objectgroup>
 </tile>
 <tile id="17">
  <objectgroup draworder="index" id="2">
   <object id="1" x="16" y="0" width="4" height="20"/>
  </objectgroup>
 </tile>
 <tile id="23">
  <animation>
   <frame tileid="23" duration="1000"/>
   <frame tileid="24" duration="1000"/>
  </animation>
 </tile>
 <tile id="25">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="4" height="4"/>
  </objectgroup>
 </tile>
 <tile id="26">
  <objectgroup draworder="index" id="2">
   <object id="1" x="16" y="0" width="4" height="4"/>
  </objectgroup>
 </tile>
 <tile id="27">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="16" width="4" height="4"/>
  </objectgroup>
 </tile>
 <tile id="28">
  <objectgroup draworder="index" id="2">
   <object id="1" x="16" y="16" width="4" height="4"/>
  </objectgroup>
 </tile>
 <tile id="30">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="16" width="20" height="4"/>
   <object id="2" x="0" y="0" width="4" height="20"/>
  </objectgroup>
 </tile>
 <tile id="31">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="16" width="20" height="4"/>
  </objectgroup>
 </tile>
 <tile id="32">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="16" width="20" height="4"/>
   <object id="2" x="16" y="0" width="4" height="20"/>
  </objectgroup>
 </tile>
 <tile id="40">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="13"/>
  </objectgroup>
 </tile>
 <tile id="41">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="15"/>
  </objectgroup>
  <animation>
   <frame tileid="41" duration="1000"/>
   <frame tileid="42" duration="1000"/>
   <frame tileid="43" duration="1000"/>
   <frame tileid="44" duration="1000"/>
  </animation>
 </tile>
 <tile id="46">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="4" height="4"/>
   <object id="2" x="16" y="16" width="4" height="4"/>
  </objectgroup>
 </tile>
 <tile id="47">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="16" width="4" height="4"/>
   <object id="2" x="16" y="0" width="4" height="4"/>
  </objectgroup>
 </tile>
 <wangsets>
  <wangset name="Bridges" type="corner" tile="-1">
   <wangcolor name="Bridge" color="#ffd230" tile="-1" probability="1"/>
   <wangtile tileid="0" wangid="0,1,0,0,0,1,0,1"/>
   <wangtile tileid="1" wangid="0,1,0,0,0,0,0,1"/>
   <wangtile tileid="2" wangid="0,1,0,1,0,0,0,1"/>
   <wangtile tileid="15" wangid="0,0,0,0,0,1,0,1"/>
   <wangtile tileid="17" wangid="0,1,0,1,0,0,0,0"/>
   <wangtile tileid="25" wangid="0,0,0,0,0,0,0,1"/>
   <wangtile tileid="26" wangid="0,1,0,0,0,0,0,0"/>
   <wangtile tileid="27" wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="28" wangid="0,0,0,1,0,0,0,0"/>
   <wangtile tileid="30" wangid="0,0,0,1,0,1,0,1"/>
   <wangtile tileid="31" wangid="0,0,0,1,0,1,0,0"/>
   <wangtile tileid="32" wangid="0,1,0,1,0,1,0,0"/>
   <wangtile tileid="45" wangid="0,1,0,1,0,1,0,1"/>
   <wangtile tileid="46" wangid="0,0,0,1,0,0,0,1"/>
   <wangtile tileid="47" wangid="0,1,0,0,0,1,0,0"/>
  </wangset>
  <wangset name="Carpets" type="corner" tile="-1">
   <wangcolor name="" color="#ff0000" tile="-1" probability="1"/>
   <wangtile tileid="19" wangid="0,1,0,1,0,0,0,1"/>
   <wangtile tileid="20" wangid="0,1,0,1,0,1,0,0"/>
   <wangtile tileid="21" wangid="0,1,0,0,0,1,0,1"/>
   <wangtile tileid="22" wangid="0,0,0,1,0,1,0,1"/>
   <wangtile tileid="34" wangid="0,0,0,1,0,0,0,0"/>
   <wangtile tileid="35" wangid="0,0,0,1,0,1,0,0"/>
   <wangtile tileid="36" wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="37" wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="38" wangid="0,0,0,0,0,0,0,1"/>
   <wangtile tileid="49" wangid="0,1,0,1,0,0,0,0"/>
   <wangtile tileid="50" wangid="0,1,0,1,0,1,0,1"/>
   <wangtile tileid="51" wangid="0,0,0,0,0,1,0,1"/>
   <wangtile tileid="52" wangid="0,0,0,0,0,0,0,1"/>
   <wangtile tileid="53" wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="64" wangid="0,1,0,0,0,0,0,0"/>
   <wangtile tileid="65" wangid="0,1,0,0,0,0,0,1"/>
   <wangtile tileid="66" wangid="0,0,0,0,0,0,0,1"/>
  </wangset>
 </wangsets>
</tileset>
