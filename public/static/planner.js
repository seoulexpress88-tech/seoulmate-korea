// Seoulmate trip planner. Pure client-side: builds a day-by-day plan from the place list below.
// window.SEOULMATE_GUIDES (injected by build.py) maps city id -> [{title,url}] so days can link to guides.
(function(){
const CITIES=[["seoul","Seoul","서울"],["busan","Busan","부산"],["jeju","Jeju","제주"],["gyeongju","Gyeongju","경주"],["jeonju","Jeonju","전주"],
["incheon","Incheon","인천"],["suwon","Suwon","수원"],["gapyeong","Gapyeong & Nami","가평"],["gangneung","Gangneung","강릉"],["sokcho","Sokcho & Seoraksan","속초"],
["andong","Andong","안동"],["daegu","Daegu","대구"],["yeosu","Yeosu","여수"],["tongyeong","Tongyeong","통영"]];
const CATS=[["food","Food"],["local","Local life"],["culture","Culture"],["history","History"],["kpop","K-pop"],["sports","Sports"],["nature","Nature"],["night","Nightlife"]];
const SLOTS=[["am","Morning","9–12"],["pm","Afternoon","13–17"],["eve","Evening","18–22"],["late","Late","22+"]];
const MOVES={"seoul>busan":"KTX, about 2h 40m","busan>seoul":"KTX, about 2h 40m","seoul>jeju":"Flight from Gimpo, about 1h 10m","busan>jeju":"Flight from Gimhae, about 1h","jeju>seoul":"Flight to Gimpo, about 1h 10m","jeju>busan":"Flight to Gimhae, about 1h","seoul>gyeongju":"KTX to Singyeongju, about 2h 10m","busan>gyeongju":"Train or bus, about 1h","gyeongju>busan":"Train or bus, about 1h","gyeongju>seoul":"KTX, about 2h 10m","seoul>jeonju":"KTX, about 1h 40m","jeonju>seoul":"KTX, about 1h 40m",
"seoul>incheon":"Subway Line 1 or AREX, about 1h","seoul>suwon":"Subway Line 1 or bus, about 1h","seoul>gapyeong":"ITX-Cheongchun train, about 1h",
"seoul>gangneung":"KTX from Seoul Station, about 2h","seoul>sokcho":"Express bus, about 2h 30m","seoul>andong":"KTX-Eum from Cheongnyangni, about 2h",
"seoul>daegu":"KTX, about 1h 50m","seoul>yeosu":"KTX to Yeosu-Expo, about 3h","seoul>tongyeong":"Express bus, about 4h",
"busan>daegu":"KTX, about 50m","busan>tongyeong":"Intercity bus, about 1h 40m","busan>yeosu":"Intercity bus, about 3h",
"daegu>gyeongju":"Train or bus, about 1h","andong>gyeongju":"Train or bus, about 1h 30m","andong>daegu":"Train or bus, about 1h 30m",
"gangneung>sokcho":"Intercity bus, about 1h","gapyeong>gangneung":"KTX, about 1h 20m","jeonju>yeosu":"KTX, about 1h 20m","suwon>busan":"KTX, about 2h 20m"};
const moveText=(a,b)=>MOVES[a+">"+b]||MOVES[b+">"+a]||"train or bus, check KTX and express bus times";
// [id, city, category, slot, name, korean name, practical tip]
const P=[
["gbg","seoul","history","am","Gyeongbokgung Palace","경복궁","Arrive at opening for the gatekeeper ceremony. Visitors wearing hanbok enter free."],
["cdg","seoul","history","am","Changdeokgung Secret Garden","창덕궁 후원","The garden is guided-tour only and sells out. Book online a few days ahead."],
["bch","seoul","culture","am","Bukchon Hanok Village","북촌 한옥마을","People live here and visiting hours are limited. Go in the morning and keep quiet."],
["jgs","seoul","culture","am","Jogyesa Temple","조계사","Free to enter, right downtown. Pair it with a tea house in nearby Insadong."],
["bhs","seoul","nature","am","Bukhansan Baegundae hike","북한산 백운대","Steep near the top with fixed ropes. Bring gloves, water and good shoes."],
["gjm","seoul","food","pm","Gwangjang Market","광장시장","Try bindaetteok and mayak gimbap. Some stalls prefer cash."],
["mwm","seoul","local","pm","Mangwon Market & Han River","망원시장","A neighborhood market Seoulites actually use. Walk 10 minutes to the river after."],
["isd","seoul","local","pm","Ikseon-dong hanok alleys","익선동","Small cafés inside old hanok. Weekdays are far less crowded."],
["nmk","seoul","history","pm","National Museum of Korea","국립중앙박물관","Permanent exhibits are free. Don't miss the Room of Quiet Contemplation."],
["lee","seoul","culture","pm","Leeum Museum of Art","리움미술관","Celadon and Joseon art next to contemporary works. Reserve a time slot online."],
["hkr","seoul","kpop","pm","HiKR Ground","하이커 그라운드","Free Hallyu exhibits and photo zones by Cheonggyecheon. About an hour is enough."],
["kdc","seoul","kpop","pm","K-pop dance class, Hongdae","홍대 K-pop 댄스 클래스","Beginner classes teach one chorus in about 90 minutes. Book a day ahead."],
["ksr","seoul","kpop","pm","K-Star Road, Cheongdam","K스타로드","Bear statues for each group along the street. Combine with Garosu-gil."],
["hdb","seoul","kpop","eve","Hongdae street busking","홍대 버스킹 거리","Dance crews cover new releases most evenings. Weekends are busiest."],
["eul","seoul","night","eve","Euljiro nogari alley","을지로 노가리 골목","Outdoor stools, cheap draft beer and dried pollack. Best in warm months."],
["nst","seoul","nature","eve","Namsan Seoul Tower at dusk","남산서울타워","Walk the trail from Myeongdong instead of queuing for the cable car."],
["hrc","seoul","local","eve","Han River chimaek picnic","한강 치맥","Fried chicken delivers to the riverside parks. Yeouido and Banpo are easiest."],
["gje","seoul","food","eve","Gwangjang night stalls","광장시장 야시장","Yukhoe (beef tartare) alley is on the east side. Stalls close around 10–11pm."],
["sgb","seoul","night","late","Itaewon & Haebangchon bars","이태원·해방촌","Rooftop bars with Namsan views and an international crowd."],
["gcv","busan","culture","am","Gamcheon Culture Village","감천문화마을","Buy the stamp map at the info center. Lanes are steep, so wear sneakers."],
["jgl","busan","food","am","Jagalchi Fish Market","자갈치시장","Pick seafood on the ground floor and have it cooked upstairs for a table fee."],
["hdy","busan","history","am","Haedong Yonggungsa Temple","해동용궁사","A seaside temple on the rocks. Arrive early to avoid tour buses."],
["bbp","busan","nature","pm","Haeundae Blueline Park sky capsule","해운대 블루라인파크","Capsules sell out on weekends. Reserve a time slot in advance."],
["jpc","busan","local","pm","Jeonpo café street","전포카페거리","Old workshop buildings turned cafés, popular with locals in their 20s."],
["bms","busan","history","pm","Beomeosa Temple","범어사","A mountain temple reachable by subway plus a short bus ride."],
["gal","busan","night","eve","Gwangalli Beach drone show","광안리 드론쇼","Drone shows run on Saturday evenings. Check the schedule before you go."],
["bpk","busan","food","eve","Bupyeong Kkangtong night market","부평깡통시장","Fish cakes, hotteok and dumplings in one covered street."],
["sio","jeju","nature","am","Seongsan Ilchulbong sunrise","성산일출봉","About 25 minutes to the crater rim. Check sunrise time the night before."],
["hls","jeju","nature","am","Hallasan Yeongsil trail","한라산 영실코스","The summit trails need online booking. Yeongsil does not and is very scenic."],
["hny","jeju","culture","pm","Haenyeo diver performance","해녀 공연","Jeju's women free-divers, a UNESCO-listed tradition. Shows depend on weather."],
["wjr","jeju","local","pm","Woljeongri beach cafés","월정리","Turquoise water and sea-view windows. Easiest with a rental car."],
["p43","jeju","history","pm","Jeju 4.3 Peace Park","제주4·3평화공원","Heavy but important modern history. Allow about two hours."],
["bpg","jeju","food","eve","Black pork street","흑돼지거리","Thick-cut Jeju black pork grilled at the table. Dip it in melchijeot sauce."],
["dmm","jeju","food","eve","Dongmun night market","동문야시장","Abalone gimbap and tangerine snacks. Stalls open in the early evening."],
["bgs","gyeongju","history","am","Bulguksa Temple","불국사","UNESCO-listed and now free to enter. Add Seokguram Grotto if you have time."],
["drw","gyeongju","history","pm","Daereungwon tomb park","대릉원","Grassy Silla royal tombs in the middle of town. Lovely in autumn."],
["hrd","gyeongju","local","pm","Hwangridan-gil","황리단길","Hanok cafés and small shops. Try Gyeongju bread while it's warm."],
["dgw","gyeongju","culture","eve","Donggung Palace & Wolji Pond","동궁과 월지","Best after dark when the pavilions reflect on the pond."],
["gcf","gyeongju","food","eve","Gyochon Village dinner","교촌마을","A restored traditional village next to Woljeonggyo Bridge."],
["jhv","jeonju","culture","am","Jeonju Hanok Village","전주 한옥마을","About 700 hanok in one area. Consider a night in a hanok guesthouse."],
["gkj","jeonju","history","pm","Gyeonggijeon Shrine","경기전","Bamboo grove and the royal portrait of King Taejo, founder of Joseon."],
["jbb","jeonju","food","pm","Jeonju bibimbap lunch","전주비빔밥","Order the brass-bowl version, the local classic."],
["nbm","jeonju","food","eve","Nambu night market","남부시장 야시장","Runs on Friday and Saturday evenings only."],
["mkg","jeonju","night","eve","Makgeolli alley","막걸리 골목","Order a kettle of makgeolli and side dishes arrive with each round."],
["icp","incheon","history","am","Incheon Open Port area","인천 개항장","Late-1800s Japanese and Western-style buildings from when Incheon first opened to foreign trade."],
["icc","incheon","food","pm","Incheon Chinatown","인천 차이나타운","Korean jajangmyeon was born here. Have a bowl, then walk the Fairy Tale Village next door."],
["ics","incheon","nature","eve","Songdo Central Park","송도 센트럴파크","Water taxis and a futuristic skyline. Best around sunset."],
["icw","incheon","local","eve","Wolmido seaside promenade","월미도","Seafood restaurants, small rides and harbor views. An easy evening near the airport."],
["swh","suwon","history","am","Suwon Hwaseong Fortress","수원 화성","UNESCO-listed walls about 5.7 km around. Walk a section and try traditional archery at Yeonmudae."],
["swp","suwon","culture","pm","Hwaseong Haenggung Palace","화성행궁","The king's temporary palace. Weekend martial arts shows run in front of the gate."],
["swl","suwon","local","pm","Haenggung-dong café streets","행리단길","Small cafés and shops inside the fortress walls, popular with young locals."],
["swg","suwon","food","eve","Suwon galbi","수원 왕갈비","Suwon is known for extra-large marinated beef ribs grilled at the table."],
["swn","suwon","nature","eve","Banghwasuryujeong at night","방화수류정 야경","The pavilion and fortress walls are lit after dark. Locals picnic on the lawn."],
["gpn","gapyeong","nature","am","Nami Island","남이섬","A short ferry from Gapyeong Wharf. Famous for its tree-lined paths from Winter Sonata."],
["gpr","gapyeong","local","am","Gangchon Rail Park","강촌레일파크","Pedal a rail bike along an old railway line through the valley. Book ahead on weekends."],
["gpp","gapyeong","culture","pm","Petite France & Italian Village","쁘띠프랑스·이탈리아마을","Colorful theme village used as a K-drama set. Good for photos."],
["gpg","gapyeong","nature","eve","Garden of Morning Calm","아침고요수목원","A large garden by day; in winter it hosts a lighting festival after dark."],
["gpd","gapyeong","food","eve","Dakgalbi dinner","닭갈비","Spicy stir-fried chicken cooked at your table, the region's signature dish. Add rice at the end."],
["gnc","gangneung","food","am","Chodang sundubu village","초당 순두부마을","Silky tofu made with seawater. Many restaurants open early for breakfast."],
["gnb","gangneung","nature","am","Gyeongpo Beach & Lake","경포해변·경포호","A wide beach next to a calm lake with a flat walking and cycling path."],
["gna","gangneung","local","pm","Anmok Coffee Street","안목 커피거리","Seaside cafés with ocean views. Gangneung calls itself Korea's coffee city."],
["gnh","gangneung","history","pm","Ojukheon House","오죽헌","Birthplace of scholar Yi I and his mother Shin Saimdang, both pictured on Korean banknotes."],
["gnk","gangneung","kpop","pm","Jumunjin breakwater & BTS bus stop","주문진 방사제·BTS 버스정류장","The Goblin drama breakwater and, nearby at Hyangho Beach, the bus stop from a BTS album cover."],
["gnm","gangneung","food","eve","Gangneung Jungang Market","강릉 중앙시장","Try squid sundae and crispy dakgangjeong chicken to go."],
["skr","sokcho","nature","am","Seoraksan National Park","설악산 국립공원","Take the cable car to Gwongeumseong, or hike to Ulsanbawi rock (about 4 hours round trip)."],
["sks","sokcho","history","pm","Sinheungsa Temple","신흥사","At the park entrance, with a giant bronze Buddha. Pair it with the morning hike."],
["ska","sokcho","culture","pm","Abai Village & hand-pulled ferry","아바이마을·갯배","Founded by refugees from North Korea. Cross the harbor on the tiny hand-pulled ferry."],
["skm","sokcho","food","eve","Sokcho Jungang Market","속초 관광수산시장","Sweet crispy dakgangjeong and squid sundae are the local favorites."],
["skb","sokcho","local","eve","Sokcho Beach & Sokcho Eye","속초해변·속초아이","A beachside Ferris wheel with sea views, lit up at night."],
["adh","andong","history","am","Hahoe Folk Village","하회마을","A UNESCO-listed clan village where families still live. Cross by boat to Buyongdae cliff for the view."],
["adb","andong","history","pm","Byeongsan Seowon","병산서원","A Confucian academy with a famous open pavilion facing the river and cliffs."],
["adm","andong","culture","pm","Hahoe Byeolsingut mask dance","하회별신굿탈놀이","Short traditional mask dance shows near the village on scheduled days. Check times first."],
["adj","andong","food","eve","Andong jjimdak alley","안동 찜닭골목","Braised chicken with glass noodles, invented in Andong's old market. One plate feeds two or three."],
["adw","andong","nature","eve","Woryeonggyo Bridge","월영교","Korea's longest wooden footbridge, lit up at night over the lake."],
["dgm","daegu","history","am","Modern history alleys & Gyesan Cathedral","근대골목·계산성당","A walking route through early-1900s houses, a cathedral and the 3.1 Movement stairs."],
["dgd","daegu","history","am","Donghwasa Temple","동화사","A large temple on Palgongsan mountain with a giant stone Buddha."],
["dgk","daegu","culture","pm","Kim Gwang-seok Road","김광석 다시그리기길","A mural alley dedicated to a beloved folk singer, with live music on weekends."],
["dgl","daegu","local","pm","Dongseong-ro","동성로","Daegu's main shopping and café district, busy with students."],
["dgs","daegu","food","eve","Seomun Night Market","서문시장 야시장","One of Korea's biggest night markets. Try kalguksu and grilled skewers."],
["dga","daegu","nature","eve","Apsan Observatory","앞산전망대","Ride the cable car up for a night view over the whole city."],
["ysh","yeosu","history","am","Hyangiram Hermitage","향일암","A cliffside hermitage facing the sea, famous for sunrise. Expect stairs."],
["yso","yeosu","nature","am","Odongdo Island","오동도","Walk the causeway to a small island of camellia trees and sea cliffs."],
["ysc","yeosu","nature","pm","Yeosu Maritime Cable Car","여수 해상케이블카","Crosses the harbor over the sea. Glass-floor cabins are available."],
["ysg","yeosu","food","pm","Ganjang gejang lunch","간장게장","Soy-marinated raw crab, a southern specialty. Rice in the shell is the best part."],
["ysn","yeosu","night","eve","Yeosu night sea & pocha street","여수 밤바다·낭만포차","Seaside tent bars along the harbor, made famous by the song Yeosu Night Sea."],
["tys","tongyeong","history","am","Sebyeonggwan Hall","세병관","A huge Joseon naval command hall linked to Admiral Yi Sun-sin."],
["tyd","tongyeong","culture","am","Dongpirang Mural Village","동피랑 벽화마을","A hillside village of murals overlooking the harbor."],
["tyc","tongyeong","nature","pm","Tongyeong Cable Car","통영 케이블카","Up Mireuksan for views over the islands of Hallyeosu Waterway."],
["tyl","tongyeong","local","pm","Skyline Luge Tongyeong","스카이라인 루지 통영","Downhill luge carts with sea views. Fun for all ages."],
["tym","tongyeong","food","eve","Jungang Market & chungmu gimbap","중앙시장·충무김밥","Try chungmu gimbap: plain rice rolls with spicy squid and radish on the side."],
// Sports. An 8th field lists the months the place is in season; outside them the planner skips it.
["kbo","seoul","sports","eve","KBO baseball at Jamsil Stadium","잠실야구장","Home of the Doosan Bears and LG Twins. Sit in the cheering zone, learn the player songs and bring fried chicken.",[3,4,5,6,7,8,9,10]],
["gcd","seoul","sports","eve","Kiwoom Heroes at Gocheok Sky Dome","고척스카이돔","Korea's only domed ballpark, so games go ahead even when it rains.",[3,4,5,6,7,8,9,10]],
["fcs","seoul","sports","eve","FC Seoul at Seoul World Cup Stadium","서울월드컵경기장","K League football in the 2002 World Cup stadium. Tickets are cheap and usually available on match day.",[3,4,5,6,7,8,9,10,11]],
["vbl","seoul","sports","eve","V-League volleyball at Jangchung Arena","장충체육관","Pro volleyball with loud, friendly crowds. The women's league is especially popular.",[10,11,12,1,2,3]],
["lck","seoul","sports","pm","LoL Park esports arena","롤파크","Watch live League of Legends (LCK) matches in Jongno. Tickets for T1 games sell out fast, so check the schedule early."],
["tkd","seoul","sports","am","Taekwondo experience class","태권도 체험","Beginner classes for visitors teach basic kicks and board-breaking in about an hour. Book a day ahead."],
["hrb","seoul","sports","pm","Han River cycling","한강 자전거","Rent a Seoul public bike (Ttareungyi) with the app and ride the flat riverside paths from Yeouido."],
["sjk","busan","sports","eve","Lotte Giants at Sajik Stadium","사직야구장","Busan has Korea's most passionate baseball fans. Join the songs in the cheering zone.",[3,4,5,6,7,8,9,10]],
["sjs","busan","sports","am","Surf lesson at Songjeong Beach","송정해수욕장 서핑","Busan's surf beach, with beginner lessons and board rental most of the year (wetsuits in the cold months)."],
["ssg","incheon","sports","eve","SSG Landers baseball, Incheon","인천SSG랜더스필드","A big, modern ballpark known for its food. An easy trip from Seoul or the airport.",[3,4,5,6,7,8,9,10]],
["ktw","suwon","sports","eve","KT Wiz baseball, Suwon","수원KT위즈파크","Home of the KT Wiz. The team app sells tickets in English and takes overseas cards.",[3,4,5,6,7,8,9,10]],
["dsl","daegu","sports","eve","Samsung Lions Park, Daegu","삼성라이온즈파크","A newer ballpark with grass and picnic seats and one of the loudest cheering sections.",[3,4,5,6,7,8,9,10]],
["gop","gangneung","sports","pm","Gangneung Olympic Park","강릉올림픽파크","Walk around the 2018 Winter Olympics ice venues and the Olympic museum."],
["ypg","gangneung","sports","am","Ski day at Yongpyong or Phoenix","용평·휘닉스 스키장","The 2018 Olympic ski resorts in Pyeongchang are about 40 minutes away. Rentals and English lessons are available.",[12,1,2,3]],
["yys","sokcho","sports","am","Surfing at Yangyang","양양 서핑","Korea's surf capital, about 40 minutes south of Sokcho. Beginner lessons run most of the year; autumn has the best waves."],
["gpw","gapyeong","sports","pm","Water sports on the Bukhan River","북한강 수상레저","Wakeboarding and banana boats, a classic summer weekend for Seoulites.",[6,7,8,9]],
["jhr","jeju","sports","pm","Horse riding on Jeju","제주 승마","Jeju has a long horse-breeding tradition; many ranches offer short beginner rides."],
["jol","jeju","sports","am","Jeju Olle Trail walk","제주올레길","Walk part of a coastal route. Route 7 near Seogwipo is a favorite."]
];
// Map coordinates [lat, lng, area]. area=1 means a representative point for a neighborhood or generic activity.
const GEO={gbg:[37.5796,126.9770],cdg:[37.5794,126.9910],bch:[37.5826,126.9830],jgs:[37.5740,126.9817],bhs:[37.6588,126.9779],
gjm:[37.5700,126.9996],mwm:[37.5560,126.9056],isd:[37.5741,126.9895],nmk:[37.5239,126.9803],lee:[37.5383,126.9990],hkr:[37.5689,126.9848],
kdc:[37.5563,126.9236,1],ksr:[37.5265,127.0430],hdb:[37.5547,126.9227],eul:[37.5663,126.9917],nst:[37.5512,126.9882],hrc:[37.5284,126.9330,1],
gje:[37.5702,127.0000],sgb:[37.5395,126.9900,1],kbo:[37.5122,127.0719],gcd:[37.4982,126.8671],fcs:[37.5683,126.8972],vbl:[37.5583,127.0070],
lck:[37.5704,126.9831],tkd:[37.5636,126.9834,1],hrb:[37.5284,126.9330,1],
gcv:[35.0975,129.0107],jgl:[35.0967,129.0306],hdy:[35.1883,129.2233],bbp:[35.1585,129.1703],jpc:[35.1555,129.0640],bms:[35.2837,129.0683],
gal:[35.1532,129.1187],bpk:[35.1018,129.0262],sjk:[35.1940,129.0615],sjs:[35.1786,129.1999],
sio:[33.4581,126.9426],hls:[33.3427,126.4951],hny:[33.5222,126.8601,1],wjr:[33.5565,126.7958],p43:[33.4495,126.6114],bpg:[33.5090,126.5277],
dmm:[33.5125,126.5279],jhr:[33.4300,126.6600,1],jol:[33.2398,126.5450],
bgs:[35.7900,129.3320],drw:[35.8383,129.2116],hrd:[35.8376,129.2089],dgw:[35.8346,129.2266],gcf:[35.8296,129.2152],
jhv:[35.8150,127.1530],gkj:[35.8155,127.1497],jbb:[35.8170,127.1480,1],nbm:[35.8135,127.1458],mkg:[35.7997,127.1290,1],
icp:[37.4740,126.6183],icc:[37.4757,126.6181],ics:[37.3925,126.6391],icw:[37.4755,126.5985],ssg:[37.4370,126.6933],
swh:[37.2871,127.0200],swp:[37.2820,127.0135],swl:[37.2830,127.0160],swg:[37.2730,127.0300,1],swn:[37.2876,127.0203],ktw:[37.2997,127.0097],
gpn:[37.7911,127.5255],gpr:[37.8136,127.6213],gpp:[37.7186,127.4967],gpg:[37.7433,127.3527],gpd:[37.8315,127.5105,1],gpw:[37.7362,127.4235,1],
gnc:[37.7907,128.9150],gnb:[37.8055,128.9087],gna:[37.7724,128.9476],gnh:[37.7795,128.8785],gnk:[37.8950,128.8293],gnm:[37.7545,128.8986],
gop:[37.7745,128.8972],ypg:[37.6447,128.6807],
skr:[38.1726,128.4893],sks:[38.1716,128.4876],ska:[38.2016,128.5913],skm:[38.2050,128.5900],skb:[38.1910,128.6015],yys:[37.9734,128.7593],
adh:[36.5394,128.5180],adb:[36.5390,128.5550],adm:[36.5410,128.5250,1],adj:[36.5651,128.7287],adw:[36.5761,128.7642],
dgm:[35.8693,128.5862],dgd:[35.9890,128.6970],dgk:[35.8603,128.6060],dgl:[35.8690,128.5960],dgs:[35.8687,128.5806],dga:[35.8291,128.5843],dsl:[35.8410,128.6812],
ysh:[34.5916,127.8047],yso:[34.7438,127.7660],ysc:[34.7350,127.7450],ysg:[34.7340,127.7360,1],ysn:[34.7395,127.7375],
tys:[34.8466,128.4247],tyd:[34.8443,128.4281],tyc:[34.8268,128.4223],tyl:[34.8273,128.4253],tym:[34.8435,128.4250]};
// Cities with a subway network; elsewhere taxis or a rental car are the practical way between stops.
const METRO=["seoul","busan","incheon","daegu","suwon"];
const byId=Object.fromEntries(P.map(p=>[p[0],p]));
const cityOf=id=>CITIES.find(x=>x[0]===id);
const GUIDES=window.SEOULMATE_GUIDES||{};
const $=id=>document.getElementById(id);
const qs=new URLSearchParams(location.search);
const qCity=(qs.get("city")||"").split(",").filter(c=>cityOf(c));
const qCat=(qs.get("cat")||"").split(",").filter(c=>CATS.some(x=>x[0]===c));
const state={cities:qCity.length?qCity:["seoul","busan"],cats:qCat.length?qCat:["food","kpop","history"],plan:[],picks:{}};

// Default dates: two weeks from today, five days long
const iso=d=>d.toISOString().slice(0,10);
const start=new Date();start.setDate(start.getDate()+14);
const qDays=Math.min(14,Math.max(1,parseInt(qs.get("days"),10)||5));
const end=new Date(start);end.setDate(end.getDate()+qDays-1);
$("arrive").value=iso(start);$("depart").value=iso(end);

function chips(el,list,sel,name){
  el.innerHTML=list.map(([id,en,ko])=>`<label class="chip"><input type="checkbox" id="${name}-${id}" value="${id}" ${sel.includes(id)?"checked":""}>${en}${ko?` <span class="ko">${ko}</span>`:""}</label>`).join("");
}
chips($("cityChips"),CITIES,state.cities,"city");
chips($("catChips"),CATS,state.cats,"cat");
$("cityChips").addEventListener("change",e=>{
  const v=e.target.value;
  state.cities=e.target.checked?[...state.cities,v]:state.cities.filter(c=>c!==v);
  hint();
});
$("catChips").addEventListener("change",()=>{state.cats=[...document.querySelectorAll("#catChips input:checked")].map(i=>i.value)});

function dayCount(){
  const a=new Date($("arrive").value+"T00:00"),d=new Date($("depart").value+"T00:00");
  const n=Math.round((d-a)/864e5)+1;return isNaN(n)?0:Math.max(0,Math.min(n,14));
}
function hint(){
  const n=dayCount();const order=state.cities.map(c=>cityOf(c)[1]).join(" → ");
  $("dayCount").textContent=n?`${n} day${n>1?"s":""}${order?" · "+order:""}${n===14?" (max 14)":""}`:"Pick a departure date after arrival";
}
$("arrive").addEventListener("change",hint);$("depart").addEventListener("change",hint);

function build(){
  const n=dayCount();const cities=state.cities.length?state.cities:["seoul"];
  const pace=+document.querySelector("input[name=pace]:checked").value;
  const used=new Set();state.plan=[];state.picks={};
  if(!n){render();return}
  const k=Math.min(cities.length,n);const base=Math.floor(n/k);let extra=n-base*k;
  const alloc=cities.slice(0,k).map(()=>base+(extra-->0?1:0));
  const score=p=>(state.cats.includes(p[2])?10:0)+(p[3]==="am"?0.1:0);
  let di=0;
  alloc.forEach((cnt,ci)=>{
    for(let i=0;i<cnt;i++){
      const city=cities[ci];
      const date=new Date($("arrive").value+"T00:00");date.setDate(date.getDate()+di);
      const move=(i===0&&ci>0)?{from:cities[ci-1],to:city}:null;
      const slots=SLOTS.slice(0,pace).map(([sid])=>{
        const ok=p=>p[1]===city&&!used.has(p[0])&&(!p[7]||p[7].includes(date.getMonth()+1));
        let c=P.filter(p=>ok(p)&&p[3]===sid).sort((a,b)=>score(b)-score(a)).slice(0,3);
        if(!c.length&&sid!=="late")c=P.filter(ok).sort((a,b)=>score(b)-score(a)).slice(0,2);
        c.forEach(p=>used.add(p[0]));
        return {sid,opts:c.map(p=>p[0])};
      });
      // Default picks: the best match first, then whichever option is closest to the previous stop.
      let prev=null;
      slots.forEach((s,si)=>{
        if(!s.opts.length)return;
        let pick=s.opts[0];
        if(prev&&GEO[prev]){
          const best=s.opts.filter(id=>GEO[id]&&state.cats.includes(byId[id][2]));
          const pool=best.length?best:s.opts.filter(id=>GEO[id]);
          if(pool.length)pick=pool.reduce((a,b)=>km(GEO[prev],GEO[a])<=km(GEO[prev],GEO[b])?a:b);
        }
        state.picks[di+"-"+si]=pick;prev=pick;
      });
      state.plan.push({city,date,move,slots});di++;
    }
  });
  render();
}

const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function render(){
  const n=state.plan.length;
  const names=[...new Set(state.plan.map(d=>d.city))].map(c=>cityOf(c)[1]);
  $("tripTitle").textContent=n?`${n} days in ${names.join(" & ")}`:"Add your dates to start";
  const fmt=d=>d.toLocaleDateString("en-US",{weekday:"short",month:"short",day:"numeric"});
  $("days").innerHTML=state.plan.map((d,di)=>{
    const c=cityOf(d.city);
    const mv=d.move?`<div class="move">Travel day: ${cityOf(d.move.from)[1]} → ${c[1]} · ${moveText(d.move.from,d.move.to)}</div>`:"";
    const g=(GUIDES[d.city]||[])[0];
    const guide=(g&&(di===0||state.plan[di-1].city!==d.city))?`<div class="move no-print">Read first: <a href="${esc(g.url)}">${esc(g.title)}</a></div>`:"";
    const slots=d.slots.map((s,si)=>{
      const meta=SLOTS.find(x=>x[0]===s.sid);
      const body=s.opts.length?`<div class="opts">${s.opts.map(id=>{
        const p=byId[id];const on=state.picks[di+"-"+si]===id;const cat=CATS.find(x=>x[0]===p[2])[1];
        const gq=encodeURIComponent(p[4]+" "+c[1]);const nq=encodeURIComponent(p[5]);
        return `<div class="opt" role="button" tabindex="0" aria-pressed="${on}" data-key="${di}-${si}" data-id="${id}">
          <div class="row"><span class="cat ${state.cats.includes(p[2])?"match":""}">${cat}</span>${on?'<span class="pick">Selected</span>':""}</div>
          <div class="name">${esc(p[4])}<small>${esc(p[5])}</small></div>
          <p class="tip">${esc(p[6])}</p>
          <div class="links no-print"><a href="https://www.google.com/maps/search/?api=1&query=${gq}" target="_blank" rel="noopener">Traveler reviews ↗</a><a href="https://map.naver.com/p/search/${nq}" target="_blank" rel="noopener">Naver Map ↗</a></div>
        </div>`}).join("")}</div>`:`<div class="free">Free time. Rest up or explore the neighborhood.</div>`;
      return `<div class="slot"><div class="slot-t">${meta[1]}<small>${meta[2]}</small></div>${body}</div>`;
    }).join("");
    return `<article class="pday"><div class="day-h"><h3>Day ${di+1}</h3><span class="date">${fmt(d.date)}</span><span class="cty">${c[1]} ${c[2]}</span></div>${mv}${guide}${slots}${routeBlock(d,di)}</article>`;
  }).join("");
  $("meter").textContent=`${Object.keys(state.picks).length} stops chosen · ${n} days`;
  $("pricePlan").innerHTML=`$${12+2*n}<small> one-time · ${n} days</small>`;
  $("priceConcierge").innerHTML=`$${39+6*n}<small> one-time · ${n} days</small>`;
  initMaps();
}

// ---- Route: the day's chosen stops in order, how to get between them, and a map
function stopsOf(di){
  return state.plan[di].slots.map((s,si)=>state.picks[di+"-"+si]).filter(id=>id&&GEO[id]).map(id=>({id,p:byId[id],g:GEO[id]}));
}
function km(a,b){
  const r=Math.PI/180,dl=(b[0]-a[0])*r,dn=(b[1]-a[1])*r;
  const h=Math.sin(dl/2)**2+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)**2;
  return 12742*Math.asin(Math.sqrt(h));
}
// Rough guidance from straight-line distance; the map links give real routes.
function legText(d,city){
  const fast=d>8;  // longer hops use expressways and express subway lines
  const walk=Math.max(1,Math.round(d*1.3/4.5*60)), taxi=Math.round(5+d*1.3/(fast?38:24)*60), transit=Math.round(12+d*1.3/(fast?32:22)*60);
  if(d<0.3)return ["walk","Right next door · a few minutes on foot"];
  if(d<=1.2)return ["walk",`Walk · about ${walk} min`];
  if(d<=3)return ["walk",`Walk about ${walk} min, or a short taxi ride (~${taxi} min)`];
  if(METRO.includes(city))return ["transit",`Subway or bus · about ${transit} min (taxi ~${taxi} min)`];
  return ["car",`Taxi or rental car · about ${taxi} min (local buses are infrequent)`];
}
function routeBlock(d,di){
  const st=stopsOf(di);
  if(!st.length)return "";
  const legs=st.slice(1).map((s,i)=>{
    const a=st[i],dist=km(a.g,s.g),[mode,txt]=legText(dist,d.city);
    const g=`https://www.google.com/maps/dir/?api=1&origin=${a.g[0]},${a.g[1]}&destination=${s.g[0]},${s.g[1]}&travelmode=${mode==="walk"?"walking":mode==="transit"?"transit":"driving"}`;
    const k=`https://map.kakao.com/link/to/${encodeURIComponent(s.p[5])},${s.g[0]},${s.g[1]}`;
    return `<li class="leg leg-${mode}"><span class="lg-n">${i+1} → ${i+2}</span><span class="lg-t"><b>${esc(a.p[4])} → ${esc(s.p[4])}</b>
      ${txt} · ${dist<1?Math.round(dist*1000)+" m":dist.toFixed(1)+" km"}</span>
      <span class="lg-a no-print"><a href="${g}" target="_blank" rel="noopener">Google Maps ↗</a><a href="${k}" target="_blank" rel="noopener">KakaoMap ↗</a></span></li>`}).join("");
  const order=st.map((s,i)=>`<li><span class="num">${i+1}</span>${esc(s.p[4])}${s.g[2]?' <span class="hint">(area)</span>':""}</li>`).join("");
  return `<div class="route">
    <div class="route-map no-print" id="map-${di}" role="img" aria-label="Map of Day ${di+1} route"></div>
    <div class="route-info"><span class="lbl">Day ${di+1} route</span><ol class="stops">${order}</ol>
      ${legs?`<ul class="legs">${legs}</ul><p class="hint">Times are rough estimates from distance. Tap a map link for live transit routes.</p>`:""}</div>
  </div>`;
}
let maps=[];
function initMaps(){
  maps.forEach(m=>m.remove());maps=[];
  if(!window.L)return;
  state.plan.forEach((d,di)=>{
    const el=$("map-"+di),st=stopsOf(di);if(!el||!st.length)return;
    const m=L.map(el,{scrollWheelZoom:false,attributionControl:true});
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(m);
    const pts=st.map(s=>[s.g[0],s.g[1]]);
    if(pts.length>1)L.polyline(pts,{color:getComputedStyle(document.documentElement).getPropertyValue("--accent").trim()||"#1F4E79",weight:3,dashArray:"6 6"}).addTo(m);
    st.forEach((s,i)=>L.marker(pts[i],{icon:L.divIcon({className:"pin-num"+(s.g[2]?" area":""),html:String(i+1),iconSize:[26,26]}),title:s.p[4]}).addTo(m).bindPopup(`<b>${esc(s.p[4])}</b><br>${esc(s.p[5])}`));
    pts.length>1?m.fitBounds(pts,{padding:[28,28],maxZoom:15}):m.setView(pts[0],14);
    maps.push(m);
  });
}
function choose(el){
  state.picks[el.dataset.key]=el.dataset.id;render();
  const again=$("days").querySelector(`.opt[data-key="${el.dataset.key}"][data-id="${el.dataset.id}"]`);again&&again.focus();
}
$("days").addEventListener("click",e=>{if(e.target.closest("a"))return;const b=e.target.closest(".opt");if(b)choose(b)});
$("days").addEventListener("keydown",e=>{const b=e.target.closest(".opt");if(b&&(e.key==="Enter"||e.key===" ")){e.preventDefault();choose(b)}});
$("tripForm").addEventListener("submit",e=>{e.preventDefault();build()});

function asText(){
  return state.plan.map((d,di)=>{
    const lines=d.slots.map((s,si)=>{const id=state.picks[di+"-"+si];const meta=SLOTS.find(x=>x[0]===s.sid);return `  ${meta[1]}: ${id?byId[id][4]+" ("+byId[id][5]+")":"Free time"}`});
    const st=stopsOf(di);
    const legs=st.slice(1).map((s,i)=>`  ${i+1}→${i+2}: ${legText(km(st[i].g,s.g),d.city)[1]}`);
    return `Day ${di+1} · ${d.date.toDateString()} · ${cityOf(d.city)[1]}\n${lines.join("\n")}${legs.length?"\n  Getting around:\n"+legs.join("\n"):""}`;
  }).join("\n\n");
}
$("copyPlan").addEventListener("click",()=>{
  const t=asText();
  navigator.clipboard.writeText(t).then(()=>{$("toast").textContent="Itinerary copied. Paste it into your notes or messages."},
    ()=>{$("toast").textContent="Copy didn't work in this browser. Use Print instead."});
});
$("printPlan").addEventListener("click",()=>window.print());

hint();build();
})();
