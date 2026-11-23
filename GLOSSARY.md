# Glosario

Términos fijos de la traducción. La guía de estilo está en [STYLE.md](STYLE.md).

## Reglas

- **G-1** No hay traducción oficial al español de la serie. La referencia es el glosario de Shadow Tower PS1 (`shadow-tower-esp`): si el concepto es el mismo en los dos juegos, se usa el mismo término. Se toma solo el término; el registro es siempre el de esta traducción. [DECISIONS 2026-11-20]
- **G-2** Lo propio de este juego se decide aquí. Hasta que esté decidido, el término va a [PENDING.md](PENDING.md) con una propuesta. [IVA]
- **G-3** Un término de esta tabla se usa igual en todo el juego. `loc.py check` avisa cuando el original lo tiene y la traducción no (`glosario`). [Encargo §6]

## Cómo se arma

1. El terminólogo revisa los candidatos (los de la fuente oficial, si hay, y los términos de sistema del juego) y propone las filas: *oficial* si es el mismo término, o *por decidir* si significa otra cosa en este juego.
2. Las filas *oficial* entran a la tabla. Las *por decidir* van a [PENDING.md](PENDING.md) para que las decida el usuario.

## Términos

Por sección. *Shadow Tower PS1* (G-1) o *decidido* por el usuario (G-2), con fecha. La primera columna es el original japonés; `loc.py` lee toda tabla cuya cabecera empiece por `| Original |`.

Lo que lleva un paréntesis en «Original» no lo controla `loc.py check` (ese texto no aparece en el juego): son kanji sueltos que también forman otras palabras, y el control daría falsas alarmas.

### Sistema y menú (Shadow Tower PS1)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| HP | PV | Shadow Tower PS1 | Puntos de vida. También dentro de efectos y del menú (HP回復, HP・MP回復, HPが足りません). |
| MP | PM | Shadow Tower PS1 | Puntos de magia. |
| クーン | cunes | Shadow Tower PS1 | Moneda del juego (ST1: CUNES). En singular, «cune». |
| アイテム | objeto | Shadow Tower PS1 | ST1: ITEM. Menú y tienda (アイテムを使用します, ショートカットアイテム). |
| ITEM | OBJETO | Shadow Tower PS1 | Ranura del menú de equipo (`sys/menu#0090`), en inglés en el original. |
| RING | ANILLO | Shadow Tower PS1 | Ranura del menú de equipo (`sys/menu#0086`). |
| BRACELET | BRAZALETE | Shadow Tower PS1 | Ranura del menú de equipo (`sys/menu#0087`). |
| AMULET | AMULETO | Shadow Tower PS1 | Ranura del menú de equipo (`sys/menu#0088`). |
| 装備 | equipo | Shadow Tower PS1 | ST1: EQUIPMENT, NO EQUIP. También 装備品. |
| 購入 | comprar | Shadow Tower PS1 | ST1: BUY. Tienda (購入します, 購入数). |
| 修理 | reparar | Shadow Tower PS1 | ST1: REPAIR. Tienda (アイテム修理). |
| メモリーカード | memory card | Shadow Tower PS1 | Accesorio de la consola: queda en inglés. «メモリーカード(PS2)» → «memory card (PS2)». |
| データ | datos | Shadow Tower PS1 | ST1: LOAD DATA → CARGAR DATOS, SAVE → GUARDAR DATOS. |
| セーブ | guardar | Shadow Tower PS1 | ST1: SAVE → GUARDAR DATOS. セーブデータ → datos guardados. |
| ロード (datos) | cargar | Shadow Tower PS1 | ST1: LOAD DATA → CARGAR DATOS. Entre paréntesis porque ロード también está en el nombre グローリーロード. |
| クリーチャー | criatura | Shadow Tower PS1 | ST1: creature = criatura. |

### Estados, elementos y daño (Shadow Tower PS1)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| 毒 (estado y elemento) | veneno | Shadow Tower PS1 | ST1: POISON. Envenenar, venenoso. 毒 también forma 解毒酒 y 毒虫. |
| 麻痺 | parálisis | Shadow Tower PS1 | Estado. ST1: PARALYZE. |
| 呪い | maldición | Shadow Tower PS1 | Estado. ST1: CURSE, CURSED. 呪われた → maldito. |
| 封印 | sellar | Shadow Tower PS1 | Estado que impide usar magia. ST1: SEAL (SEALS MAGIC → SELLA LA MAGIA). Sello, sellado. |
| 暗闇 | ceguera | Shadow Tower PS1 | Estado que ciega. ST1: DARK (estado) → CEGUERA. Como elemento, 闇 → oscuridad. |
| 重化 | lento | Shadow Tower PS1 | Estado que vuelve pesado y lento («歩みを重くする»). ST1: SLOW (HEAVY en FDAT.T). Lentitud. |
| 炎 (elemento) | fuego | Shadow Tower PS1 | ST1: FIRE. En la prosa también «llamas». |
| 凍 (elemento) | hielo | Shadow Tower PS1 | ST1: COLD (también FREEZE, FROST, ICE). |
| 氷 | hielo | Shadow Tower PS1 | ST1: ICE. 氷の矢 → flechas de hielo; 氷塊 → bloque de hielo. |
| 酸 | ácido | Shadow Tower PS1 | Elemento. ST1: ACID. |
| 闇 (elemento) | oscuridad | Shadow Tower PS1 | ST1: DARK (elemento) → OSCURIDAD. Como estado, 暗闇 → ceguera. |
| クリティカル | crítico | Shadow Tower PS1 | Efecto especial del equipo. ST1: CRITICAL. |
| 斬撃 | corte | Shadow Tower PS1 | Tipo de daño. ST1: SLASH. Cortar. |
| 打撃 | golpe | Shadow Tower PS1 | Tipo de daño. ST1: SMASH. Golpear. |
| 刺突 | estocada | Shadow Tower PS1 | Tipo de daño. ST1: PIERCE. 刺突剣 tiene fila aparte. |
| 魔法 | magia | Shadow Tower PS1 | ST1: MAGIC (ATAQUE MÁGICO, DEFENSA MÁGICA). Mágico. |
| 魔法防御 | defensa mágica | Shadow Tower PS1 | ST1: MAGIC DEFENSE. |
| 物理防御 | defensa física | Shadow Tower PS1 | ST1: WEAPON DEFENSE → DEFENSA FÍSICA. |
| 防御力 | defensa | Shadow Tower PS1 | ST1: DEFENSE. |
| 重量 | peso | Shadow Tower PS1 | ST1: WEIGHT. 重量軽減 → reduce el peso. |
| 耐久 | durabilidad | Shadow Tower PS1 | Del equipo. ST1: DURA → DUR (forma larga). También 耐久値, 耐久力 y 耐久性. |
| HP吸収 | absorción de PV | Shadow Tower PS1 | Efecto: quita PV al enemigo. ST1: HP DRAIN. |
| MP吸収 | absorción de PM | Shadow Tower PS1 | Efecto: quita PM al enemigo. ST1: MP DRAIN. |
| HP回復 | recuperación de PV | Shadow Tower PS1 | Efecto del equipo. ST1: HP RECOVERY. El grado va detrás (・弱/中/強). Si la forma entera no entra en la caja, «Recup. de PV» (T-3); el chequeo avisa igual [DECISIONS 2026-11-23]. |
| MP回復 | recuperación de PM | Shadow Tower PS1 | Efecto del equipo. ST1: MP RECOVERY. Si no entra en la caja, «Recup. de PM» (T-3) [DECISIONS 2026-11-23]. |
| HP・MP回復 | recuperación de PV y PM | decidido 2026-11-23 | Compuesto: una sola «recuperación». Si no entra, «Recup. de PV/PM» (T-3). |
| HP・MP吸収 | absorción de PV y PM | decidido 2026-11-23 | Compuesto: una sola «absorción». |
| バランス | equilibrio | Shadow Tower PS1 | ST1: BALANCE. En las descripciones: «バランスよく整えられた» → bien equilibrado. |

### Equipo: familias (Shadow Tower PS1)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| 片手 | de una mano | Shadow Tower PS1 | ST1: ONE-HANDED. 片手剣 → espada de una mano. |
| 両手 | de dos manos | Shadow Tower PS1 | ST1: TWO-HANDED. 両手剣, 両手用, 両手持ち. |
| ソード | espada | Shadow Tower PS1 | ST1: SWORD (LONG SWORD → ESPADA LARGA). Familia: ローソード, ハイソード, ウォーソード… |
| ローソード | Espada menor | decidido 2026-11-23 | Grado de la familia; su par es ハイソード → «Espada mayor» (y sus variantes). |
| ハイソード | Espada mayor | decidido 2026-11-23 | Ver ローソード. |
| 輝石 | gema luminosa | decidido 2026-11-23 | `sys/objetos#0746` a `#0751`. |
| 数珠 | cuentas de oración | decidido 2026-11-23 | |
| (朱) | bermellón | decidido 2026-11-23 | Kanji suelto, con paréntesis: sin control. |
| 具足 | grebas | decidido 2026-11-23 | |
| 長剣 | espada larga | Shadow Tower PS1 | ST1: LONG SWORD. 片手長剣 → espada larga de una mano. |
| 大剣 | mandoble | Shadow Tower PS1 | ST1: GREAT SWORD. |
| 幅広剣 | espada ancha | Shadow Tower PS1 | ST1: BROAD SWORD. |
| 刺突剣 | estoque | Shadow Tower PS1 | ST1: RAPIER. Espada para estocadas (エペ, スピットソード). |
| メイス | maza | Shadow Tower PS1 | ST1: MACE. |
| アックス | hacha | Shadow Tower PS1 | ST1: AXE. |
| 斧 | hacha | Shadow Tower PS1 | ST1: AXE. 斧頭 → cabeza del hacha. |
| 戦斧 | hacha de guerra | Shadow Tower PS1 | ST1: BATTLE AXE. |
| バトルアックス | hacha de guerra | Shadow Tower PS1 | ST1: BATTLE AXE. |
| ボウ | arco | Shadow Tower PS1 | ST1: BOW. Familia: ウッドボウ, カーテシーボウ, カタパルトボウ. |
| 弓 | arco | Shadow Tower PS1 | ST1: BOW. 魔弓 → arco mágico. |
| クロスボウ | ballesta | Shadow Tower PS1 | ST1: BOW GUN → BALLESTA. |
| ボウガン | ballesta | Shadow Tower PS1 | ST1: BOW GUN. |
| ヘルム | yelmo | Shadow Tower PS1 | ST1: HELM. Familia: ラウンドヘルム, バレルヘルム, クロスヘルム. |
| 兜 | yelmo | Shadow Tower PS1 | ST1: HELM. También en 鉄威星兜 y 銀威星兜. |
| 冠 | corona | Shadow Tower PS1 | ST1: CROWN. 宝冠 → corona enjoyada. |
| アーマー | armadura | Shadow Tower PS1 | ST1: ARMOR (LEATHER ARMOR → ARMADURA DE CUERO). |
| 鎧 | armadura | Shadow Tower PS1 | ST1: ARMOR. |
| メイル | cota | Shadow Tower PS1 | ST1: MAIL (SCALE MAIL → COTA DE ESCAMAS). ベルトメイル, ウォーメイル. |
| グローブ | guante | Shadow Tower PS1 | ST1: GLOVE. |
| ブーツ | botas | Shadow Tower PS1 | ST1: BOOTS, en plural. |
| すねあて | grebas | Shadow Tower PS1 | ST1: LEG GUARD → GREBAS, en plural. |
| ブレスレット | brazalete | Shadow Tower PS1 | ST1: BRACELET. 三連ブレスレット → brazalete triple. |
| 腕輪 | brazalete | Shadow Tower PS1 | ST1: BRACELET. |
| リング | anillo | Shadow Tower PS1 | ST1: RING. ネチェルリング, アースリング, ゲイザーリング. |
| 指輪 | anillo | Shadow Tower PS1 | ST1: RING. |
| アミュレット | amuleto | Shadow Tower PS1 | ST1: AMULET. |
| ドクロ | calavera | Shadow Tower PS1 | ST1: SKULL (ACID SKULL → CALAVERA ÁCIDA). `loc.py check` da un falso positivo en `sys/objetos#0754/nombre` y `#0755` (ヴォイドクロウ, «Garra del vacío»): queda como está. |

### Lugares (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| 域 (cabeza de nombre de lugar) | zona | decidido 2026-11-20 | Cabezas de los nombres de lugar. 域, 層 y 界 siguen a ST1 (AREA → ZONA, LAYER → ESTRATO, WORLD → MUNDO; las descripciones de los 界 los llaman 世界), pero no se puede confirmar que sean las mismas palabras japonesas de ST1. 陣 (formación, campo cercado) no tiene par en ST1: «recinto»; alternativa «dominio» (ST1 DOMAIN). En la tabla irían con paréntesis, sin control: 界 también forma 世界 y 異界, y 層 forma 上層. |
| 層 (cabeza de nombre de lugar) | estrato | decidido 2026-11-20 | Cabezas de los nombres de lugar. 域, 層 y 界 siguen a ST1 (AREA → ZONA, LAYER → ESTRATO, WORLD → MUNDO; las descripciones de los 界 los llaman 世界), pero no se puede confirmar que sean las mismas palabras japonesas de ST1. 陣 (formación, campo cercado) no tiene par en ST1: «recinto»; alternativa «dominio» (ST1 DOMAIN). En la tabla irían con paréntesis, sin control: 界 también forma 世界 y 異界, y 層 forma 上層. |
| 界 (cabeza de nombre de lugar) | mundo | decidido 2026-11-20 | Cabezas de los nombres de lugar. 域, 層 y 界 siguen a ST1 (AREA → ZONA, LAYER → ESTRATO, WORLD → MUNDO; las descripciones de los 界 los llaman 世界), pero no se puede confirmar que sean las mismas palabras japonesas de ST1. 陣 (formación, campo cercado) no tiene par en ST1: «recinto»; alternativa «dominio» (ST1 DOMAIN). En la tabla irían con paréntesis, sin control: 界 también forma 世界 y 異界, y 層 forma 上層. |
| 陣 (cabeza de nombre de lugar) | recinto | decidido 2026-11-20 | Cabezas de los nombres de lugar. 域, 層 y 界 siguen a ST1 (AREA → ZONA, LAYER → ESTRATO, WORLD → MUNDO; las descripciones de los 界 los llaman 世界), pero no se puede confirmar que sean las mismas palabras japonesas de ST1. 陣 (formación, campo cercado) no tiene par en ST1: «recinto»; alternativa «dominio» (ST1 DOMAIN). En la tabla irían con paréntesis, sin control: 界 también forma 世界 y 異界, y 層 forma 上層. |
| 底森の祠 | Santuario Subterráneo | decidido 2026-11-20 | 底森 es el bosque del fondo, que según la descripción se extiende bajo unas ruinas; 祠 → santuario. Ancho 196. La forma completa, «Santuario del Bosque Hondo», mide 255 y no entra. |
| 静澄の岸 | Orilla Serena | decidido 2026-11-20 | 静澄 = quieto y límpido. Ancho 124. |
| 蒼光の域 | Zona de la Luz Azul | decidido 2026-11-20 | Ancho 195. |
| 浮座の層 | Estrato Flotante | decidido 2026-11-20 | 浮座 es la plataforma flotante del centro de la torre (entrada 浮座, abajo). El inglés fan («Bridge Area») sale de la descripción, no del nombre. Ancho 145; «Estrato de la Plataforma Flotante» mide 312. |
| 奇虫の域 | Zona de los Insectos | decidido 2026-11-20 | Forma corta: con 奇 («Zona de los Insectos Raros») mide 282. Ancho 196. |
| 白亜の域 | Zona del Muro Blanco | decidido 2026-11-20 | 白亜 = blanco de cal; la descripción habla de un castillo blanco. Ancho 210. |
| 烈毒の域 | Zona del Veneno Letal | decidido 2026-11-20 | 烈 = violento, feroz; «letal» es además el afijo LETHAL de ST1. Ancho 215 (justo). «Zona del Veneno Feroz» mide 219. |
| 木賊の界 | Mundo de los Equisetos | decidido 2026-11-20 | 木賊 (tokusa) es la planta equiseto o cola de caballo; el inglés fan, «Scouring Rush», es su nombre en inglés. «Mundo de la Cola de Caballo» mide 291. Ancho 214. |
| 落滝の界 | Mundo de la Cascada | decidido 2026-11-20 | Ancho 215 (justo); alternativa «Mundo de Cascadas» (197). |
| 断崖の界 | Mundo del Acantilado | decidido 2026-11-20 | Ancho 211. |
| 赤砂の塔 | Torre de Arena Roja | decidido 2026-11-20 | Ancho 196. Los mapas hablan también de «赤い砂の地» (tierra de arena roja). |
| 濃霧の陣 | Recinto de la Niebla | decidido 2026-11-20 | 濃霧 = niebla densa; «Recinto de Niebla Densa» mide 236. Ancho 196. |
| 幻影の陣 | Recinto de Ilusiones | decidido 2026-11-20 | ILLUSION → ILUSIÓN en ST1. Ancho 182. |
| 移床の陣 | Recinto del Piso Móvil | decidido 2026-11-20 | 移床 = suelo que se mueve. Ancho 206; «Recinto del Suelo Móvil» mide 220. |
| 煌珠の層 | Estrato de la Gema | decidido 2026-11-20 | 煌珠 = gema deslumbrante; «Estrato de la Gema Brillante» mide 267. Se evita «orbe» para no confundirlo con la criatura オーブ. Ancho 183. |
| 浮座 | plataforma flotante | decidido 2026-11-20 | 浮座 aparece en el lugar 浮座の層 y en las llaves que la suben y bajan («浮座の昇降を司る»); 昇降の珀鍵 → Llave del elevador de ámbar (los nombres completos pasan de 215: forma corta en el lote). |
| 昇降 | elevador | decidido 2026-11-20 | 浮座 aparece en el lugar 浮座の層 y en las llaves que la suben y bajan («浮座の昇降を司る»); 昇降の珀鍵 → Llave del elevador de ámbar (los nombres completos pasan de 215: forma corta en el lote). |
| 奇虫 | insecto raro | decidido 2026-11-20 | Pieza de 奇虫牙, 奇虫角, 奇虫眼 (Colmillo, Antena y Ojo de insecto raro) y del lugar 奇虫の域. |
| 塔 | torre | decidido 2026-11-20 | La torre donde pasa el juego (14 textos: lugares, criaturas y mapas). Con minúscula a media frase (E-59). |

### Criaturas (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| ガレ | Gare | decidido 2026-11-20 | Prefijo de 10 criaturas, casi todas «de cuerpo robusto» (頑強な身体). Se aparta del inglés fan («Grey»): ガレ se lee «gare»; gris sería グレイ. También dentro de ウィガレ → «Wigare» y ミガレ → «Migare». |
| パラ | Para | decidido 2026-11-20 | Prefijo de 4 criaturas (y de パラフェルム). Se aparta del inglés fan («Bara»): パ es «pa». `loc.py check` da un falso positivo en `sys/objetos#0989/nombre` y `#0990` (パラッシュ, «Pallasch»): queda como está. |
| クィドル | Quiddle | decidido 2026-11-20 | Forma del inglés fan, fiel a «kuidoru» [DECISIONS 2026-11-20]. |
| クィドリィ | Quiddly | decidido 2026-11-20 | Forma del inglés fan, fiel a «kuidoru» [DECISIONS 2026-11-20]. |
| ガープ | Galp | decidido 2026-11-20 | Inglés fan, salvo los prefijos ガレ y パラ. |
| ガーピス | Galpis | decidido 2026-11-20 | Inglés fan, salvo los prefijos ガレ y パラ. |
| クィドル・ガープ | Quiddle Galp | decidido 2026-11-20 | Inglés fan, salvo los prefijos ガレ y パラ. |
| ガレ・ガープ | Gare Galp | decidido 2026-11-20 | Inglés fan, salvo los prefijos ガレ y パラ. |
| パラ・ガープ | Para Galp | decidido 2026-11-20 | Inglés fan, salvo los prefijos ガレ y パラ. |
| ロフ | Rof | decidido 2026-11-20 | Inglés fan. |
| ロフィス | Rofis | decidido 2026-11-20 | Inglés fan. |
| ラルド | Raldo | decidido 2026-11-20 | Inglés fan, salvo ガレ y パラ. El más ancho, «Quiddly Raldo», mide 136. |
| ラルディス | Raldis | decidido 2026-11-20 | Inglés fan, salvo ガレ y パラ. El más ancho, «Quiddly Raldo», mide 136. |
| ミラ・ラルド | Mira Raldo | decidido 2026-11-20 | Inglés fan, salvo ガレ y パラ. El más ancho, «Quiddly Raldo», mide 136. |
| ガレ・ラルド | Gare Raldo | decidido 2026-11-20 | Inglés fan, salvo ガレ y パラ. El más ancho, «Quiddly Raldo», mide 136. |
| ウィ・ラルド | Wi Raldo | decidido 2026-11-20 | Inglés fan, salvo ガレ y パラ. El más ancho, «Quiddly Raldo», mide 136. |
| ウィガレ・ラルド | Wigare Raldo | decidido 2026-11-20 | Inglés fan, salvo ガレ y パラ. El más ancho, «Quiddly Raldo», mide 136. |
| クィドリィ・ラルド | Quiddly Raldo | decidido 2026-11-20 | Inglés fan, salvo ガレ y パラ. El más ancho, «Quiddly Raldo», mide 136. |
| パラ・ラルド | Para Raldo | decidido 2026-11-20 | Inglés fan, salvo ガレ y パラ. El más ancho, «Quiddly Raldo», mide 136. |
| ヴァーム | Vam | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ヴァーミス | Vamis | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| クィドル・ヴァーム | Quiddle Vam | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ドマ・ヴァーム | Doma Vam | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ガレ・ヴァーム | Gare Vam | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ネガ・モルドーリィ | Nega Mordory | decidido 2026-11-20 | Inglés fan, salvo los prefijos; además, el fan escribe «Grey Mordory» para ガレ・モルドール, que es Mordor. |
| ネガ・モルドール | Nega Mordor | decidido 2026-11-20 | Inglés fan, salvo los prefijos; además, el fan escribe «Grey Mordory» para ガレ・モルドール, que es Mordor. |
| ミラ・モルドーリィ | Mira Mordory | decidido 2026-11-20 | Inglés fan, salvo los prefijos; además, el fan escribe «Grey Mordory» para ガレ・モルドール, que es Mordor. |
| ガレ・モルドール | Gare Mordor | decidido 2026-11-20 | Inglés fan, salvo los prefijos; además, el fan escribe «Grey Mordory» para ガレ・モルドール, que es Mordor. |
| クィドル・モルドール | Quiddle Mordor | decidido 2026-11-20 | Inglés fan, salvo los prefijos; además, el fan escribe «Grey Mordory» para ガレ・モルドール, que es Mordor. |
| パラ・モルドール | Para Mordor | decidido 2026-11-20 | Inglés fan, salvo los prefijos; además, el fan escribe «Grey Mordory» para ガレ・モルドール, que es Mordor. |
| マンダス | Mandas | decidido 2026-11-20 | Inglés fan, salvo los prefijos. |
| ガレ・マンダス | Gare Mandas | decidido 2026-11-20 | Inglés fan, salvo los prefijos. |
| クィドル・マンダス | Quiddle Mandas | decidido 2026-11-20 | Inglés fan, salvo los prefijos. |
| パラ・マンダス | Para Mandas | decidido 2026-11-20 | Inglés fan, salvo los prefijos. |
| ソルガンド | Sorgand | decidido 2026-11-20 | Inglés fan, salvo los prefijos. |
| パラフェルム | Paraferm | decidido 2026-11-20 | Se aparta del inglés fan («Balaferma»): パ es «pa» y la ム final queda como en Vam y Grundam. «Quiddle Paraferm» mide 163. |
| ガレ・パラフェルム | Gare Paraferm | decidido 2026-11-20 | Se aparta del inglés fan («Balaferma»): パ es «pa» y la ム final queda como en Vam y Grundam. «Quiddle Paraferm» mide 163. |
| クィドル・パラフェルム | Quiddle Paraferm | decidido 2026-11-20 | Se aparta del inglés fan («Balaferma»): パ es «pa» y la ム final queda como en Vam y Grundam. «Quiddle Paraferm» mide 163. |
| ビラッシュ | Birash | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ビラッシス | Birassis | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ガレ・ビラッシュ | Gare Birash | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ア・グルンダム | A Grundam | decidido 2026-11-20 | Inglés fan, salvo ミガレ («Mi Grey» en el fan). |
| ア・グルンダミス | A Grundamis | decidido 2026-11-20 | Inglés fan, salvo ミガレ («Mi Grey» en el fan). |
| ア・グルンダミィ | A Grundami | decidido 2026-11-20 | Inglés fan, salvo ミガレ («Mi Grey» en el fan). |
| ミ・グルンダム | Mi Grundam | decidido 2026-11-20 | Inglés fan, salvo ミガレ («Mi Grey» en el fan). |
| ミ・グルンダミス | Mi Grundamis | decidido 2026-11-20 | Inglés fan, salvo ミガレ («Mi Grey» en el fan). |
| ミガレ・グルンダム | Migare Grundam | decidido 2026-11-20 | Inglés fan, salvo ミガレ («Mi Grey» en el fan). |
| バルーヴァ | Baluva | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| バルーヴィ | Baluvi | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| バルーヴィス | Baluvis | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ガレ・バルーヴァ | Gare Baluva | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| クィドル・バルーヴァ | Quiddle Baluva | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ファルト | Falto | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ファルティス | Faltis | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ガレ・ファルト | Gare Falto | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| ネガ・ファルト | Nega Falto | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| クィドル・ファルト | Quiddle Falto | decidido 2026-11-20 | Inglés fan, salvo ガレ. |
| デル・ガルディア | Del Gardia | decidido 2026-11-20 | Se aparta del inglés fan («Guardia»): ガルディア se lee «garudia» [DECISIONS 2026-11-20]. |
| ソル・ガルディア | Sol Gardia | decidido 2026-11-20 | Se aparta del inglés fan («Guardia»): ガルディア se lee «garudia» [DECISIONS 2026-11-20]. |
| ギル・ガルディア | Gil Gardia | decidido 2026-11-20 | Se aparta del inglés fan («Guardia»): ガルディア se lee «garudia» [DECISIONS 2026-11-20]. |
| ノル・ガルディア | Nor Gardia | decidido 2026-11-20 | Se aparta del inglés fan («Guardia»): ガルディア se lee «garudia» [DECISIONS 2026-11-20]. |
| ガレ・ガルディア | Gare Gardia | decidido 2026-11-20 | Se aparta del inglés fan («Guardia»): ガルディア se lee «garudia» [DECISIONS 2026-11-20]. |
| ナダ・ガルディア | Nada Gardia | decidido 2026-11-20 | Se aparta del inglés fan («Guardia»): ガルディア se lee «garudia» [DECISIONS 2026-11-20]. |
| ペスティス | Pestis | decidido 2026-11-20 | Inglés fan. |
| ミラ・ペスティス | Mira Pestis | decidido 2026-11-20 | Inglés fan. |
| ネメシス | Némesis | decidido 2026-11-20 | ネメシス es una palabra real: va con la ortografía española. El fan escribe «Nega Guardia» para ネガ・ネメシス (error). El más ancho mide 171. |
| ネガ・ネメシス | Nega Némesis | decidido 2026-11-20 | ネメシス es una palabra real: va con la ortografía española. El fan escribe «Nega Guardia» para ネガ・ネメシス (error). El más ancho mide 171. |
| グ・ネガ・ネメシス | Gu Nega Némesis | decidido 2026-11-20 | ネメシス es una palabra real: va con la ortografía española. El fan escribe «Nega Guardia» para ネガ・ネメシス (error). El más ancho mide 171. |
| ル・ネガ・ネメシス | Ru Nega Némesis | decidido 2026-11-20 | ネメシス es una palabra real: va con la ortografía española. El fan escribe «Nega Guardia» para ネガ・ネメシス (error). El más ancho mide 171. |
| オーブ | Orbe | decidido 2026-11-20 | Palabra real (orb): se traduce. Ancho 42. |
| ルルフォン | Rurufon | decidido 2026-11-20 | Inglés fan. También es nombre de personaje (`mapa/2288#0001`); su descripción la presenta como mujer (`sys/criaturas#0119/desc`, para E-40). |
| ネガ・ルルフォン | Nega Rurufon | decidido 2026-11-20 | Inglés fan. También es nombre de personaje (`mapa/2288#0001`); su descripción la presenta como mujer (`sys/criaturas#0119/desc`, para E-40). |

### Términos de la historia (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| 槍 (la lanza de los mapas) | lanza | decidido 2026-11-20 | La lanza de la que hablan muchos textos de mapa (43 textos, también objetos). Con minúscula: el original no la trata como nombre propio. |
| 槍の王 | Rey de la Lanza | decidido 2026-11-20 | Título de un personaje del que hablan los mapas (3 textos); el fan, «Spear King». |
| 長 (los que mandan en cada mundo) | señor | decidido 2026-11-20 | Como LORD → SEÑOR en ST1. Con paréntesis en la tabla, sin control: 長 forma muchas palabras (長剣, 長い). |
| 支配者 | soberano | decidido 2026-11-20 | 支配者 sigue a ST1 (RULER → SOBERANO, que se mantenía distinto de LORD → SEÑOR); 高位支配者 aparece en 5 descripciones de criaturas. No se puede confirmar que sea el mismo concepto que en ST1. |
| 高位支配者 | soberano supremo | decidido 2026-11-20 | 支配者 sigue a ST1 (RULER → SOBERANO, que se mantenía distinto de LORD → SEÑOR); 高位支配者 aparece en 5 descripciones de criaturas. No se puede confirmar que sea el mismo concepto que en ST1. |
| 意志 | voluntad | decidido 2026-11-20 | Entidad que nombran algunos habitantes de la torre (mapas, la descripción de オーブ y la de 煌珠の層). 意志 de una persona («貴様の意志») es «voluntad» común, en minúscula. |
| 偉大なる意志 | Gran Voluntad | decidido 2026-11-20 | Entidad que nombran algunos habitantes de la torre (mapas, la descripción de オーブ y la de 煌珠の層). 意志 de una persona («貴様の意志») es «voluntad» común, en minúscula. |
| 意思 | voluntad | decidido 2026-11-23 | Lo que uno quiere; en minúscula, frente a 意志 → «Voluntad» con mayúscula cuando es la entidad (`mapa/2283#0001`). |
| (王, el de la lanza) | Rey | decidido 2026-11-23 | Con mayúscula siempre que nombra a ese rey («el Rey», «nuestro Rey»). 伝承の王 (`mapa/2272#0081`) es otro: «el rey de la leyenda». Con paréntesis, sin control. |
| 破壊者 | destructor | decidido 2026-11-23 | `mapa/2253#0101`. |
| 千尋 | hondura insondable | decidido 2026-11-23 | `mapa/2253#0030`. |
| 使い手 | portador | decidido 2026-11-23 | Quien empuña o lleva el objeto, en las descripciones («protege a su portador»). Como el glosario para los efectos sobre quien lo lleva. |
| ボス | jefe | decidido 2026-11-20 | Cómo llaman unas criaturas a quien las manda (8 textos, `mapa/2262` a `mapa/2265`). Con mayúscula si lo usan como nombre («Jefe... dijo...»). |
| 異形 | aberrante | decidido 2026-11-20 | Adjetivo; como sustantivo, «aberración». 14 textos: criaturas, objetos («異形の斧», «異形の鎧»), lugares y mapas. Alternativa «deforme». |
| シャドウタワー　アビス | Shadow Tower Abyss | decidido 2026-11-20 | Título del juego en los mensajes de la memory card (10 textos). Queda como en el logo. ST1 tradujo el lugar y el nombre de los datos guardados (TORRE DE LAS SOMBRAS); aquí es el título del producto entre comillas, no un lugar. |
| ソウルポット | Frasco de alma | decidido 2026-11-20 | ST1 tiene SOUL POD → FRASCO DE ALMA; aquí es «pot» (壷, vasija con un alma que mejora las capacidades). Si no es el mismo objeto de la serie, «Vasija de alma». |
| 霧のかけら | Fragmento de niebla | decidido 2026-11-20 | Objeto que se repite (4) y se nombra en su descripción («全てのかけら»). Ancho 190. |

### Magia y efectos del equipo (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| 霊 (clase de magia) | espíritu | decidido 2026-11-20 | Las tres clases de magia: 粒 rige fuego e hielo, 溶 veneno y ácido, 霊 luz y oscuridad (呪符 de `sys/objetos#0015` a `#0017`). Son los términos de ST1 (SPIRIT, PARTICLE, MELTING), que coinciden con el kanji, pero no se puede confirmar que sean las mismas categorías de ST1. El fan dice «Spirit / Element / Solvent». Con paréntesis en la tabla, sin control. |
| 粒 (clase de magia) | partícula | decidido 2026-11-20 | Las tres clases de magia: 粒 rige fuego e hielo, 溶 veneno y ácido, 霊 luz y oscuridad (呪符 de `sys/objetos#0015` a `#0017`). Son los términos de ST1 (SPIRIT, PARTICLE, MELTING), que coinciden con el kanji, pero no se puede confirmar que sean las mismas categorías de ST1. El fan dice «Spirit / Element / Solvent». Con paréntesis en la tabla, sin control. |
| 溶 (clase de magia) | disolución | decidido 2026-11-20 | Las tres clases de magia: 粒 rige fuego e hielo, 溶 veneno y ácido, 霊 luz y oscuridad (呪符 de `sys/objetos#0015` a `#0017`). Son los términos de ST1 (SPIRIT, PARTICLE, MELTING), que coinciden con el kanji, pero no se puede confirmar que sean las mismas categorías de ST1. El fan dice «Spirit / Element / Solvent». Con paréntesis en la tabla, sin control. |
| 光 (elemento) | luz | decidido 2026-11-20 | Pareja de 闇 (陰陽の呪符: «光・闇»). ST1 tenía HOLY → SAGRADO, que es otra palabra; aquí el japonés dice «luz». Sin control: 光 está en 蒼光, 光輪, 閃光. |
| 雷 | rayo | decidido 2026-11-20 | 7 textos («刀身に雷をまとった», «球状の雷», 冥雷). Alternativa «relámpago». |
| 魔力 | poder mágico | decidido 2026-11-20 | 90 textos («魔力を宿した»). Distinto de 魔法 → magia (fila de ST1). Alternativa: «magia» para los dos. Donde «poder mágico» no entra, «poder de partícula / disolución / espíritu» (`sys/objetos#0613`-`#0615`) y «Mineral mágico en bruto» (`#0036`); el chequeo avisa igual [DECISIONS 2026-11-23]. |
| 精神力 | fuerza mental | decidido 2026-11-20 | El fan usa «spirit» para 精神力, que chocaría con 霊 → espíritu; 体力 es lo que baja con HP減少 («体力を奪う»). «Vigor» coincide con el prefijo ヴィガー. |
| 精神 | mente | decidido 2026-11-20 | El fan usa «spirit» para 精神力, que chocaría con 霊 → espíritu; 体力 es lo que baja con HP減少 («体力を奪う»). «Vigor» coincide con el prefijo ヴィガー. |
| 体力 | vigor | decidido 2026-11-20 | El fan usa «spirit» para 精神力, que chocaría con 霊 → espíritu; 体力 es lo que baja con HP減少 («体力を奪う»). «Vigor» coincide con el prefijo ヴィガー. |
| 状態異常 | estado alterado | decidido 2026-11-20 | 21 textos (状態異常耐性, 状態異常無効; también 状態変化). ST1 solo tenía STATUS RECOVERY → CURA DE ESTADOS. |
| 特殊： | Especial: | decidido 2026-11-20 | Etiqueta de los efectos del equipo (224 textos). ST1 decía «DE PODER ESPECIAL» en la prosa. |
| 希少品 | Objeto raro | decidido 2026-11-20 | 123 descripciones, casi siempre en su propio renglón. El fan, «Rare». |
| 敵暗闇 | Ciega | decidido 2026-11-20 | Efectos sobre el enemigo (48 textos). Ojo: con las filas 暗闇 → ceguera y 重化 → lento, `loc.py check` avisará en «Ciega» y «Ralentiza»; si se quiere evitar, «Causa ceguera / Causa lentitud». |
| 敵封印 | Sella | decidido 2026-11-20 | Efectos sobre el enemigo (48 textos). Ojo: con las filas 暗闇 → ceguera y 重化 → lento, `loc.py check` avisará en «Ciega» y «Ralentiza»; si se quiere evitar, «Causa ceguera / Causa lentitud». |
| 敵毒化 | Envenena | decidido 2026-11-20 | Efectos sobre el enemigo (48 textos). Ojo: con las filas 暗闇 → ceguera y 重化 → lento, `loc.py check` avisará en «Ciega» y «Ralentiza»; si se quiere evitar, «Causa ceguera / Causa lentitud». |
| 敵重化 | Ralentiza | decidido 2026-11-20 | Efectos sobre el enemigo (48 textos). Ojo: con las filas 暗闇 → ceguera y 重化 → lento, `loc.py check` avisará en «Ciega» y «Ralentiza»; si se quiere evitar, «Causa ceguera / Causa lentitud». |
| 封印 (sobre quien lo lleva) | Sellado | decidido 2026-11-20 | Efectos negativos para el portador (17 textos). |
| 呪い (sobre quien lo lleva) | Maldición | decidido 2026-11-20 | Efectos negativos para el portador (17 textos). |
| 毒化 (sobre quien lo lleva) | Envenenado | decidido 2026-11-20 | Efectos negativos para el portador (17 textos). |
| 暗闇 (sobre quien lo lleva) | Ceguera | decidido 2026-11-20 | Efectos negativos para el portador (17 textos). |
| 〜耐性 | Resiste X | decidido 2026-11-20 | 魔法耐性 → «Resiste magia»; 物理耐性 → «Resiste daño físico»; 状態異常耐性 → «Resiste estados alterados»; 麻痺無効 → «Inmune a parálisis». 70 y 44 textos. |
| 〜無効 | Inmune a X | decidido 2026-11-20 | 魔法耐性 → «Resiste magia»; 物理耐性 → «Resiste daño físico»; 状態異常耐性 → «Resiste estados alterados»; 麻痺無効 → «Inmune a parálisis». 70 y 44 textos. |
| ・弱 | baja | decidido 2026-11-20 | Grado de los efectos: HP回復・弱 → «Recuperación de PV baja». El fan, «Low / Mid / Fast». Concuerda con el efecto: «Recuperación de PV baja», pero «Consumo de PV bajo» [DECISIONS 2026-11-23]. |
| ・中 | media | decidido 2026-11-20 | Grado de los efectos: HP回復・弱 → «Recuperación de PV baja». El fan, «Low / Mid / Fast». Concuerda con el efecto: «Recuperación de PV media», pero «Consumo de PV medio» [DECISIONS 2026-11-23]. |
| ・強 | alta | decidido 2026-11-20 | Grado de los efectos: HP回復・弱 → «Recuperación de PV baja». El fan, «Low / Mid / Fast». `loc.py check` da un falso positivo en `mapa/2264#0130` («・・・強い», puntos suspensivos): esa línea queda como está. Concuerda con el efecto: «Recuperación de PV alta», pero «Consumo de PV alto» [DECISIONS 2026-11-23]. |
| HP減少 | Pérdida de PV | decidido 2026-11-20 | El equipo le quita PV o PM a quien lo lleva. El fan dice «Drain», que chocaría con 吸収 → absorción (ST1 DRAIN). |
| MP減少 | Pérdida de PM | decidido 2026-11-20 | El equipo le quita PV o PM a quien lo lleva. El fan dice «Drain», que chocaría con 吸収 → absorción (ST1 DRAIN). |
| HP消費 | Consumo de PV | decidido 2026-11-20 | El equipo le quita PV o PM a quien lo lleva. El fan dice «Drain», que chocaría con 吸収 → absorción (ST1 DRAIN). |
| MP消費 | Consumo de PM | decidido 2026-11-20 | El equipo le quita PV o PM a quien lo lleva. El fan dice «Drain», que chocaría con 吸収 → absorción (ST1 DRAIN). |
| 重量軽減 | Reduce el peso | decidido 2026-11-20 | Efecto (8 textos); 重量 → peso es fila de ST1. |
| 破砕 | aplastar | decidido 2026-11-20 | 破砕力 → fuerza para aplastar. Va con el prefijo ブレイク, cuyas armas lo describen; distinto de 打撃 → golpe. 10 textos. |
| 装弾数 | Capacidad | decidido 2026-11-20 | «装弾数7発» → «Capacidad: 7 disparos» (singular con 1: «Capacidad: 1 disparo»). «Disparos» sirve también para el Panzerfaust y el lanzagranadas [DECISIONS 2026-11-23]. 29 textos. |

### Equipo: familias sin equivalente en ST1 (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| 小剣 | espada corta | decidido 2026-11-20 | Como SHORT SWORD de ST1; si se lee como el arma histórica «small sword», «espadín». Distinto de 短剣. |
| ダガー | daga | decidido 2026-11-20 | 11 textos. |
| 短剣 | daga | decidido 2026-11-20 | 11 textos. |
| 湾曲刀 | espada curva | decidido 2026-11-20 | 11 textos (ファルクス, カットラス, サーベル). |
| カットラス | alfanje | decidido 2026-11-20 | El ejemplo de DECISIONS 2026-11-20. |
| セイバー | sable | decidido 2026-11-20 | セイバー, パイレーツセイバー, コーカサスサーベル. |
| サーベル | sable | decidido 2026-11-20 | セイバー, パイレーツセイバー, コーカサスサーベル. |
| 棍棒 | garrote | decidido 2026-11-20 | 12 descripciones (también de las メイス, que son «maza»). |
| ハンマー | martillo | decidido 2026-11-20 | ウォーハンマー, ハードハンマー. |
| 戦槌 | martillo de guerra | decidido 2026-11-20 | ウォーハンマー, ハードハンマー. |
| 手斧 | hacha de mano | decidido 2026-11-20 | 10 textos. |
| ハルベルト | alabarda | decidido 2026-11-20 |  |
| 斧槍 | alabarda | decidido 2026-11-20 |  |
| ヘルメット | casco | decidido 2026-11-20 | Los cascos modernos (フリッツヘルメット); los de fantasía son yelmos. |
| コロネット | diadema | decidido 2026-11-20 | Coronet; 冠 (corona) es fila de ST1. |
| 手甲 | guantelete | decidido 2026-11-20 | Como GAUNTLET → GUANTELETE y ARM GUARD → BRAZAL de ST1; en japonés son dos piezas distintas (13 y 16 textos). |
| 篭手 | brazal | decidido 2026-11-20 | Como GAUNTLET → GUANTELETE y ARM GUARD → BRAZAL de ST1; en japonés son dos piezas distintas (13 y 16 textos). |
| ハンド | guanteletes | decidido 2026-11-20 | メタルハンド se describe como 手甲, y スチールアーム como 篭手: así queda igual que en las descripciones. El fan, «Hands / Arms / Wrist Guard». |
| アーム | brazales | decidido 2026-11-20 | メタルハンド se describe como 手甲, y スチールアーム como 篭手: así queda igual que en las descripciones. El fan, «Hands / Arms / Wrist Guard». アームプロテクター → «Protector de brazo» (`sys/objetos#0344`), y レッグプロテクター → «Protector de pierna» (`#0443`); el chequeo avisa igual [DECISIONS 2026-11-23]. |
| リストガード | muñequeras | decidido 2026-11-20 | メタルハンド se describe como 手甲, y スチールアーム como 篭手: así queda igual que en las descripciones. El fan, «Hands / Arms / Wrist Guard». |
| シンガーダー | grebas | decidido 2026-11-20 | Su descripción dice すねあて, que es «grebas» (fila de ST1). |
| タリスマン | talismán | decidido 2026-11-20 | Las タリスマン se describen como お守り; 護符 es el resto de lo que va en la ranura de amuleto. |
| お守り | talismán | decidido 2026-11-20 | Las タリスマン se describen como お守り; 護符 es el resto de lo que va en la ranura de amuleto. |
| 護符 | amuleto | decidido 2026-11-20 | Las タリスマン se describen como お守り; 護符 es el resto de lo que va en la ranura de amuleto. |
| バングル | pulsera | decidido 2026-11-20 | Accesorios (セヴァバングル, スペルループ, スタブバンド, レリクスネイル). |
| ループ | aro | decidido 2026-11-20 | Accesorios (セヴァバングル, スペルループ, スタブバンド, レリクスネイル). |
| バンド | banda | decidido 2026-11-20 | Accesorios (セヴァバングル, スペルループ, スタブバンド, レリクスネイル). |
| レリクス | reliquia | decidido 2026-11-20 | Accesorios (セヴァバングル, スペルループ, スタブバンド, レリクスネイル). |
| ジャケット | chaqueta | decidido 2026-11-20 |  |
| プロテクター | protector | decidido 2026-11-20 |  |
| ゴーグル | lentes protectores | decidido 2026-11-20 | «Gafas» se evita (E-12). |
| スニーカー | tenis | decidido 2026-11-20 | La forma más extendida en América [DECISIONS 2026-11-20]. «Tenis de lona» mide 126. |
| 魔石 | gema mágica | decidido 2026-11-20 | 29 y 26 textos. 秘石 y 輝石 (4 y 6) quedan para el lote. |
| 宝石 | gema | decidido 2026-11-20 | 29 y 26 textos. 秘石 y 輝石 (4 y 6) quedan para el lote. |
| メタル | de metal | decidido 2026-11-20 | Piezas de nombre. ハイド (hide) → «de cuero» como LEATHER en ST1; キルト como QUILTED → ACOLCHADA; ウォー como BATTLE → DE GUERRA. |
| スチール | de acero | decidido 2026-11-20 | Piezas de nombre. ハイド (hide) → «de cuero» como LEATHER en ST1; キルト como QUILTED → ACOLCHADA; ウォー como BATTLE → DE GUERRA. |
| ハイド | de cuero | decidido 2026-11-20 | Piezas de nombre. ハイド (hide) → «de cuero» como LEATHER en ST1; キルト como QUILTED → ACOLCHADA; ウォー como BATTLE → DE GUERRA. |
| キルト | acolchado | decidido 2026-11-20 | Piezas de nombre. ハイド (hide) → «de cuero» como LEATHER en ST1; キルト como QUILTED → ACOLCHADA; ウォー como BATTLE → DE GUERRA. |
| ウォー | de guerra | decidido 2026-11-20 | Piezas de nombre. ハイド (hide) → «de cuero» como LEATHER en ST1; キルト como QUILTED → ACOLCHADA; ウォー como BATTLE → DE GUERRA. |

### Equipo: prefijos que modifican (decidido)

Van detrás del sustantivo y concuerdan con él, como los afijos de ST1. Muchos nombres armados pasan de 215 (por ejemplo, «Armadura reforzada gélida», 256): la forma corta se decide en el lote.

| Original | Español | Fuente | Nota |
|---|---|---|---|
| スタンド | firme | decidido 2026-11-20 | Stand (resistir). 15 objetos; en los brazaletes mejora la defensa mágica. |
| イクオル | ecuánime | decidido 2026-11-20 | Equal. 6 objetos. Alternativa «igualado». |
| アラート | alerta | decidido 2026-11-20 | Alert. 9 objetos. «Vigilante» es más largo (los anillos ya pasan de 215 con él). |
| ワイズ | sabio | decidido 2026-11-20 | Wise. 8 objetos. |
| ロバスト | robusto | decidido 2026-11-20 | Robust. 11 objetos. |
| ソリッド | sólido | decidido 2026-11-20 | Solid. 14 objetos. |
| ラピッド | rápido | decidido 2026-11-20 | Rapid. 10 objetos («veloz» ya es SWIFT en ST1). |
| ヴィガー | de vigor | decidido 2026-11-20 | Vigor. 8 objetos; suben el 体力 (vigor) o la defensa física. |
| フィール | sensible | decidido 2026-11-20 | Se aparta del inglés fan («Fear»): フィール es «feel» (fear sería フィア). 12 objetos que suben la fuerza mental o la magia (フィールドジャケット es otra palabra: field). Alternativa «perceptivo». `loc.py check` da un falso positivo en `sys/objetos#0260/nombre` (フィールドジャケット, «Chaqueta de campaña»): queda como está. |
| アリア | aria | decidido 2026-11-20 | Aria (pieza musical), sin traducción más clara; invariable, en aposición («Botas de acero aria»). 3 objetos. Alternativa «melodioso». |
| セヴァー | tajante | decidido 2026-11-20 | Sever. 9 armas que destacan en el corte, y セヴァバングル (sin ー). Invariable. |
| セヴァ | tajante | decidido 2026-11-20 | Sever. 9 armas que destacan en el corte, y セヴァバングル (sin ー). Invariable. |
| ブレイク | aplastante | decidido 2026-11-20 | Break. 8 objetos que destacan en 破砕. Como CRUSHING → aplastante en ST1. Invariable. |
| スタブ | punzante | decidido 2026-11-20 | Stab. スタブバルキーソード (estocada); en スタブバンド (sube los PV) el fan lee «Stub», pero el japonés es el mismo. Invariable. |
| ハード | reforzado | decidido 2026-11-20 | Hard. ハードアーマー, ハードハンマー. Como HARDEN → reforzado en ST1; «armadura dura» suena mal. |
| インファイト | de combate cercano | decidido 2026-11-20 | Infighting. インファイトソード, インファイトメイス. |

### Equipo: sufijos de elemento (decidido)

Concuerdan con el objeto. El afijo de ST1 con el mismo elemento (coherencia de la serie) [DECISIONS 2026-11-20].

| Original | Español | Fuente | Nota |
|---|---|---|---|
| ブレイズ | ígneo | decidido 2026-11-20 | Blaze; fuego (炎). Como FIERY → ígneo en ST1. Literal: «llameante». 11 objetos. |
| フロスト | gélido | decidido 2026-11-20 | Frost; hielo (凍). Coincide con FROSTY → gélido de ST1 y con lo literal. 10 objetos. |
| ヴェノム | venenoso | decidido 2026-11-20 | Venom; veneno (毒). 9 objetos. |
| リキッド | cáustico | decidido 2026-11-20 | Liquid; ácido (酸). Como CAUSTIC → cáustico en ST1. Literal: «líquido», que en español no dice ácido. 8 objetos. |
| グリター | radiante | decidido 2026-11-20 | Glitter; luz (光). Como SHINING → radiante en ST1. Literal: «resplandeciente». 7 objetos. |
| シェイド | oscuro | decidido 2026-11-20 | Shade; oscuridad (闇). Como DARK (afijo) → oscuro en ST1. Literal: «sombrío». 6 objetos. |

### Anillos de magia y nombres que quedan (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| ルビーウイング | Ala de rubí | decidido 2026-11-20 | Seis familias de anillos con 4 o 5 variantes cada una. イル es «ill» (el fan dice «Set Sapphire»); «glass» va como «vidrio» (E-12, «cristal» se evita). |
| イルサファイア | Zafiro funesto | decidido 2026-11-20 | Seis familias de anillos con 4 o 5 variantes cada una. イル es «ill» (el fan dice «Set Sapphire»); «glass» va como «vidrio» (E-12, «cristal» se evita). |
| トパーズグラス | Vidrio de topacio | decidido 2026-11-20 | Seis familias de anillos con 4 o 5 variantes cada una. イル es «ill» (el fan dice «Set Sapphire»); «glass» va como «vidrio» (E-12, «cristal» se evita). |
| サッドジェイド | Jade triste | decidido 2026-11-20 | Seis familias de anillos con 4 o 5 variantes cada una. イル es «ill» (el fan dice «Set Sapphire»); «glass» va como «vidrio» (E-12, «cristal» se evita). |
| アメジストアイ | Ojo de amatista | decidido 2026-11-20 | Seis familias de anillos con 4 o 5 variantes cada una. イル es «ill» (el fan dice «Set Sapphire»); «glass» va como «vidrio» (E-12, «cristal» se evita). |
| ロストアンバー | Ámbar perdido | decidido 2026-11-20 | Seis familias de anillos con 4 o 5 variantes cada una. イル es «ill» (el fan dice «Set Sapphire»); «glass» va como «vidrio» (E-12, «cristal» se evita). |
| ロリカ・ハマタ | Lorica hamata | decidido 2026-11-20 | Nombres históricos o míticos que quedan [DECISIONS 2026-11-20]: lorica hamata es el ejemplo de la decisión; «jacerina» es la forma española de jazerant (cota de origen árabe); «udyat», la española del ojo udjat; gandharva queda igual. |
| ジャザラント | Jacerina | decidido 2026-11-20 | Nombres históricos o míticos que quedan [DECISIONS 2026-11-20]: lorica hamata es el ejemplo de la decisión; «jacerina» es la forma española de jazerant (cota de origen árabe); «udyat», la española del ojo udjat; gandharva queda igual. |
| ウジャト | Udyat | decidido 2026-11-20 | Nombres históricos o míticos que quedan [DECISIONS 2026-11-20]: lorica hamata es el ejemplo de la decisión; «jacerina» es la forma española de jazerant (cota de origen árabe); «udyat», la española del ojo udjat; gandharva queda igual. |
| ガンダルヴァ | Gandharva | decidido 2026-11-20 | Nombres históricos o míticos que quedan [DECISIONS 2026-11-20]: lorica hamata es el ejemplo de la decisión; «jacerina» es la forma española de jazerant (cota de origen árabe); «udyat», la española del ojo udjat; gandharva queda igual. |

### Armas de fuego (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| ガバメントＭ1911 | Government M1911 | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| M3スーパー90 | M3 Super 90 | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| SSG69 | SSG69 | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| デリンジャー | Derringer | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| 南部十四年式 | Nambu Tipo 14 | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| スーパーブラックホーク | Super Blackhawk | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| S&W No.2 | S&W No.2 | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| イングラムM11 | Ingram M11 | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| RPK | RPK | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| AR-15 | AR-15 | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| M14 | M14 | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| パンツァーファウスト | Panzerfaust | decidido 2026-11-20 | Modelos reales: quedan [DECISIONS 2026-11-20]. Se repiten en las municiones. |
| フリントロック銃 | pistola de chispa | decidido 2026-11-20 | No son modelos: se traducen. «Munición de Government M1911» mide 299: forma corta en el lote. |
| グレネードランチャー | lanzagranadas | decidido 2026-11-20 | No son modelos: se traducen. «Munición de Government M1911» mide 299: forma corta en el lote. |
| 〜の弾 | munición X | decidido 2026-11-23 | Sin «de» delante del modelo: «Munición M1911», «Munición Nambu Tipo 14». Lo que no es modelo lleva «de»: «Munición de granadas», «Munición de lanzagranadas», «Munición de pistola de chispa» [DECISIONS 2026-11-23]. |
| マガジン | cargador | decidido 2026-11-20 | Neutro (E-10): «subfusil» es de España. |
| サブマシンガン | subametralladora | decidido 2026-11-20 | Neutro (E-10): «subfusil» es de España. |
| アサルトライフル | fusil de asalto | decidido 2026-11-20 | Neutro (E-10): «subfusil» es de España. |

### Menú (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| データブック | Libro de datos | decidido 2026-11-20 | Reúne mapa, criaturas y equipo, así que no es el BESTIARIO de ST1. |
| WEAPON | ARMA | decidido 2026-11-20 | Ranuras del equipo (máximo 125). R y L → DER. e IZQ. como en ST1. «ACCESO RÁPIDO» mide 177 y no entra; «ATAJO», 73. Las ayudas de arriba van igual: 頭部, 胴体, 腕部, 脚部 → cabeza, cuerpo, brazos, piernas; ショートカット → atajo. |
| WEAPON R | ARMA DER. | decidido 2026-11-20 | Ranuras del equipo (máximo 125). R y L → DER. e IZQ. como en ST1. «ACCESO RÁPIDO» mide 177 y no entra; «ATAJO», 73. Las ayudas de arriba van igual: 頭部, 胴体, 腕部, 脚部 → cabeza, cuerpo, brazos, piernas; ショートカット → atajo. |
| WEAPON L | ARMA IZQ. | decidido 2026-11-20 | Ranuras del equipo (máximo 125). R y L → DER. e IZQ. como en ST1. «ACCESO RÁPIDO» mide 177 y no entra; «ATAJO», 73. Las ayudas de arriba van igual: 頭部, 胴体, 腕部, 脚部 → cabeza, cuerpo, brazos, piernas; ショートカット → atajo. |
| HEAD | CABEZA | decidido 2026-11-20 | Ranuras del equipo (máximo 125). R y L → DER. e IZQ. como en ST1. «ACCESO RÁPIDO» mide 177 y no entra; «ATAJO», 73. Las ayudas de arriba van igual: 頭部, 胴体, 腕部, 脚部 → cabeza, cuerpo, brazos, piernas; ショートカット → atajo. |
| BODY | CUERPO | decidido 2026-11-20 | Ranuras del equipo (máximo 125). R y L → DER. e IZQ. como en ST1. «ACCESO RÁPIDO» mide 177 y no entra; «ATAJO», 73. Las ayudas de arriba van igual: 頭部, 胴体, 腕部, 脚部 → cabeza, cuerpo, brazos, piernas; ショートカット → atajo. |
| ARMS | BRAZOS | decidido 2026-11-20 | Ranuras del equipo (máximo 125). R y L → DER. e IZQ. como en ST1. «ACCESO RÁPIDO» mide 177 y no entra; «ATAJO», 73. Las ayudas de arriba van igual: 頭部, 胴体, 腕部, 脚部 → cabeza, cuerpo, brazos, piernas; ショートカット → atajo. |
| LEGS | PIERNAS | decidido 2026-11-20 | Ranuras del equipo (máximo 125). R y L → DER. e IZQ. como en ST1. «ACCESO RÁPIDO» mide 177 y no entra; «ATAJO», 73. Las ayudas de arriba van igual: 頭部, 胴体, 腕部, 脚部 → cabeza, cuerpo, brazos, piernas; ショートカット → atajo. |
| SHORT CUT | ATAJO | decidido 2026-11-20 | Ranuras del equipo (máximo 125). R y L → DER. e IZQ. como en ST1. «ACCESO RÁPIDO» mide 177 y no entra; «ATAJO», 73. Las ayudas de arriba van igual: 頭部, 胴体, 腕部, 脚部 → cabeza, cuerpo, brazos, piernas; ショートカット → atajo. |
| OK | OK | decidido 2026-11-20 | Líneas de botones (máximo 680); la más larga mide 533. |
| QUIT | SALIR | decidido 2026-11-20 | Líneas de botones (máximo 680); la más larga mide 533. |
| CHANGE | CAMBIAR | decidido 2026-11-20 | Líneas de botones (máximo 680); la más larga mide 533. |
| GUIDE | GUÍA | decidido 2026-11-20 | Líneas de botones (máximo 680); la más larga mide 533. |
| DATA | DATOS | decidido 2026-11-20 | Líneas de botones (máximo 680); la más larga mide 533. |
| GAME START | EMPEZAR | decidido 2026-11-20 | Líneas de botones (máximo 680); la más larga mide 533. |
| GAME OVER | FIN DE LA PARTIDA | decidido 2026-11-20 | En inglés en el original. ST1 decía CARGAR DATOS para la memory card; aquí es cargar una partida. |
| RETURN TO TITLE | VOLVER AL TÍTULO | decidido 2026-11-20 | En inglés en el original. ST1 decía CARGAR DATOS para la memory card; aquí es cargar una partida. |
| LOAD GAME | CARGAR PARTIDA | decidido 2026-11-20 | En inglés en el original. ST1 decía CARGAR DATOS para la memory card; aquí es cargar una partida. |
| CANCEL | CANCELAR | decidido 2026-11-20 | En inglés en el original. ST1 decía CARGAR DATOS para la memory card; aquí es cargar una partida. |
| RETRY | REINTENTAR | decidido 2026-11-20 | En inglés en el original. ST1 decía CARGAR DATOS para la memory card; aquí es cargar una partida. |
| タイトル | pantalla de título | decidido 2026-11-20 |  |
| 売却 | vender | decidido 2026-11-20 | Tienda. «Guardar» se evita para 預ける: es セーブ. |
| 預ける | depositar | decidido 2026-11-20 | Tienda. «Guardar» se evita para 預ける: es セーブ. |
| 引き出す | retirar | decidido 2026-11-20 | Tienda. «Guardar» se evita para 預ける: es セーブ. |
| 在庫数 | En venta | decidido 2026-11-20 | Contadores de la tienda. |
| 購入数 | Comprar | decidido 2026-11-20 | Contadores de la tienda. |
| 所有数 | Tienes | decidido 2026-11-20 | Contadores de la tienda. |
| 引出数 | Retirar | decidido 2026-11-20 | Contadores de la tienda. |
| 預け数 | Depositar | decidido 2026-11-20 | Contadores de la tienda. |
| 消費HP | Consumo de PV | decidido 2026-11-23 | Lo que se paga con PV en la tienda; como MP USED → COSTO DE PM de ST1. Unificado con HP消費 [DECISIONS 2026-11-23]. |
| メモリーカードスロット | ranura para memory card | decidido 2026-11-20 | 9 textos. |
| フォーマット | formatear | decidido 2026-11-20 |  |
| ファイル | archivo | decidido 2026-11-20 | Ranuras de la memory card. ST1 llamaba NUEVO ARCHIVO a la ranura vacía; alternativa para 未使用. |
| 破損ファイル | archivo dañado | decidido 2026-11-20 | Ranuras de la memory card. ST1 llamaba NUEVO ARCHIVO a la ranura vacía; alternativa para 未使用. |
| 未使用 | sin usar | decidido 2026-11-20 | Ranuras de la memory card. ST1 llamaba NUEVO ARCHIVO a la ranura vacía; alternativa para 未使用. |
| クリアデータ | datos de partida completada | decidido 2026-11-20 | Lo que se guarda al terminar el juego. |

### Hablantes de los mapas (decidido)

| Original | Español | Fuente | Nota |
|---|---|---|---|
| 我が主 | mi amo | decidido 2026-11-20 | Lo dice el siervo (`characters/siervo-del-rey.md`). No «mi señor»: «señor» es 長. |
| 主 (amo de los seres creados) | amo | decidido 2026-11-20 | `mapa/2280`. Sin control: 主 forma otras palabras. |
| 神様 | Dios | decidido 2026-11-20 | Como nombre, con mayúscula y sin artículo (voz quebrada). |
| 神 (fuera de 神様) | dios | decidido 2026-11-20 | En minúscula. Sin control: 神 está en 精神. |
