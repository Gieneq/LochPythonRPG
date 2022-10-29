<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="particles" tilewidth="2" tileheight="2" tilecount="900" columns="30">
 <image source="particles.png" width="60" height="60"/>
 <tile id="0" class="particle">
  <properties>
   <property name="behaviour" value="flame"/>
  </properties>
  <animation>
   <frame tileid="0" duration="100"/>
   <frame tileid="1" duration="100"/>
   <frame tileid="2" duration="100"/>
   <frame tileid="3" duration="100"/>
   <frame tileid="4" duration="100"/>
   <frame tileid="5" duration="100"/>
   <frame tileid="6" duration="100"/>
   <frame tileid="7" duration="100"/>
  </animation>
 </tile>
 <tile id="1" class="particle"/>
 <tile id="2" class="particle"/>
 <tile id="3" class="particle"/>
 <tile id="4" class="particle"/>
 <tile id="5" class="particle"/>
 <tile id="6" class="particle"/>
 <tile id="7" class="particle"/>
 <tile id="30" class="particle">
  <properties>
   <property name="behaviour" value="leaf"/>
  </properties>
  <animation>
   <frame tileid="30" duration="500"/>
   <frame tileid="31" duration="500"/>
   <frame tileid="32" duration="500"/>
   <frame tileid="33" duration="500"/>
  </animation>
 </tile>
 <tile id="31" class="particle"/>
 <tile id="32" class="particle"/>
 <tile id="33" class="particle"/>
</tileset>
