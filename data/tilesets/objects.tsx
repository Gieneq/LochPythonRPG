<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="objects" tilewidth="20" tileheight="20" tilecount="225" columns="15">
 <image source="objects.png" width="300" height="300"/>
 <tile id="0">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="3" width="20" height="14"/>
  </objectgroup>
 </tile>
 <tile id="1">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="20"/>
  </objectgroup>
 </tile>
 <tile id="2">
  <properties>
   <property name="use" type="bool" value="false"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="3" width="20" height="14"/>
  </objectgroup>
 </tile>
 <tile id="3">
  <properties>
   <property name="use" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="4">
  <properties>
   <property name="use" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="3" width="20" height="14"/>
  </objectgroup>
 </tile>
 <tile id="5">
  <properties>
   <property name="use" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="10">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="3" width="20" height="14"/>
  </objectgroup>
 </tile>
 <tile id="11">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="3" width="20" height="14"/>
  </objectgroup>
 </tile>
 <tile id="12">
  <properties>
   <property name="use" type="bool" value="false"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" x="1" y="1" width="18" height="13"/>
  </objectgroup>
 </tile>
 <tile id="13">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="16"/>
  </objectgroup>
 </tile>
 <tile id="14">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="20" height="16"/>
  </objectgroup>
 </tile>
 <tile id="15">
  <animation>
   <frame tileid="15" duration="1000"/>
   <frame tileid="16" duration="1000"/>
   <frame tileid="17" duration="1000"/>
   <frame tileid="18" duration="1000"/>
  </animation>
 </tile>
 <tile id="19">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="3" width="20" height="14"/>
  </objectgroup>
 </tile>
 <tile id="30">
  <properties>
   <property name="light" type="int" value="8"/>
   <property name="light_color" type="color" value=""/>
   <property name="particles" value="flame"/>
   <property name="source_x" type="int" value="10"/>
   <property name="source_y" type="int" value="10"/>
  </properties>
  <objectgroup draworder="index" id="2">
   <object id="1" x="1" y="6" width="18" height="13"/>
  </objectgroup>
  <animation>
   <frame tileid="30" duration="100"/>
   <frame tileid="31" duration="100"/>
   <frame tileid="32" duration="100"/>
   <frame tileid="33" duration="100"/>
  </animation>
 </tile>
 <tile id="34">
  <properties>
   <property name="light" type="int" value="0"/>
   <property name="light_color" type="color" value=""/>
   <property name="particles" value="flame"/>
   <property name="source_x" type="int" value="10"/>
   <property name="source_y" type="int" value="10"/>
  </properties>
 </tile>
</tileset>
