Viel kostenlose Software konzentiert sich auf DJ-Licht und eignet sich kaum für Theater. Andere, wie MagicQ sind eigentlich gut, aber auf dem PC schlecht zu nutzen. GrandMA on PC ist super, aber kostet mindestens 1000€, um DMX heraus zu bekommen. Vielleicht bekommen wir ja was besseres hin.
An der Schule brauchen wir Steuerung für Theater/Musical/Oper, aber auch für Partys und Feste. Das eher im kleineren Rahmen bis rund 200 DMX Kanäle.

Die UI im Browser, Verarbeitung auf einem HTTP basierten Server. Dann kann man später zum Beispiel Smartphone Apps über WLAN einbinden oder Sachen übers Internet fernsteuern. Man kann aber auch einfach lokal hosten.
Gerade das mit dem Smartphone ist interessant, z. B. für virtuelle Encoder Wheels.
In Sachen UI plädiere ich für einen Mix aus Kommandozeile und GUI, ähnlich wie bei einer GrandMA. Eine spezielle, einfache Skriptsprache, die man sehr schnell auf einer Laptop-Tastatur tippen kann, bietet die Möglichkeit, live einzugreifen oder einfache Makros zu schreiben, die man später auf Tastendruck abrufen kann. Die GUI hilft den Überblick zu bewahren, Fader anzuzeigen oder schnell auf vorprogrammierte Funktionen zuzugreifen. Man kann entweder die Kommandozeile mit beiden Händern auf der Tastatur verwenden, oder die Maus mit einer Hand an der Tasatur für schnelle Befehle. Falls man was spezielleres braucht, kann man über einen Skripteditor oder die Kommandozeile direkt auf die zugrundeliegende serverseitige Library, z. B. in Python implementiert, zugreifen. Damit hat man dann die komplette Palette an Datentypen, conditionals und loops der zugrunde liegenden Sprache zur Verfügung.

# Ein "Mental Model"
Neben der Domain Specific Language (DSL) habe ich mir vor allem Gedanken über das Model des Lichtpultes gemacht. Wie programmiert man komplexes Licht ohne dabei verrückt zu werden? Wie interagiere ich mit der Konsole? Welche Vorstellung in meinen Kopf brauche ich, damit ich die Konsole verstehe?
Die klassische Möglichkeit, wie z. B. bei GrandMA oder anderen Tracking-Konsolen, ist so: Alle Änderungen an der aktuellen Szene werden im Programmer gespeichert. Drückt man "Store", werden diese spezifischen Einstellungen irgendwo hin gespeichert. Ruft man sie später wieder auf, werden nur die Dinge, die im Programmer waren, wieder aufgerufen. Die Pulte bieten meist große Anzahlen von Playbacks, sodass man durch Überlagern mehrerer Cues verschiedenste Szenen erstellen kann. Problem: Möchte man etwas bearbeiten, muss man erst herausfinden, aus welcher Cue die Eigenschaft, die man bearbeiten will, kommt. Dann muss man diese Cue editieren (also in den Programmer laden) und anschließend wieder abspeichern.
Was mich auch stört: Man weiß meist nicht, warum eine Lampe jetzt gerade an ist. Durch die hohe Anzahl Playbacks und Cues verliert man gerne den Überblick.
Ich habe mir deswegen, vor dem Hintergrund der lezten Opernaufführung, etwas Neues überlegt:
 * Es gibt eine einzige Cue-Liste.
 * Jede Cue repräsentiert den kompletten Output der Konsole (eine ganze "Szene").
 * Jede Änderung an der aktuellen Szene wird automatisch in der aktuellen Cue gespeichert.
 * Wenn ein Licht an ist, dann nur, weil es in der aktuellen Cue an ist. Mag ich es nicht, mache ich es aus und bin fertig.
 * Cues oder Teile von Cues können schnell über Editierfunktionen in neue Cues kopiert werden.
 * Jeder Kopiervorgang erstellt einen Bucket. Buckets speichern Werte von ausgewählten Kanälen. Sollte man den Teil, den man schon einmal kopiert hat, noch einmal brauchen, klickt man den Bucket an und hat die Einstellung noch einmal.
 * Erstellt man aus einer Cue heraus einen Bucket oder fügt ihn in eine Cue ein, ist dieser Bucket zu den entsprechenen Kanälen in den Cues "soft-linked".
 * Ein Soft-Link bietet die Möglichkeit, schnell Änderungen in einer Cue durchzuführen und diese Änderungen auf den Bucket zu übertragen. Von dort aus kann der neue Inhalt schnell auf alle oder einen gefilterten Teil der soft-gelinkten Cues verteilt werden. Diese Prozesse nenne ich Propagation.
 * Das Bucket-System ersetzt das übliche Preset-System (selective presets bei GrandMA). Im Gegensatz zu Presets muss ich aber nicht vorher wissen, was ich später noch einmal brauche, sondern kopiere mir einfach aus anderen Cues, was ich brauche und erhalte automatisch Buckets.
 * Hard-Links sind wie Soft-Links, aber synchronisieren sich automatisch. Ist ein Kanalwert in zwei Cues hart gelinkt und man ändert ihn in einer Cue, wird er auch in der anderen geändert. Das kann ein Ersatz für Tracking sein.
 * Auch Hard-Links haben einen Bucket, der mit anderen Cues per Soft-Link verbunden sein kann. Damit kann eine Änderung, die per Hard-Link gemacht wird, direkt vom Bucket an soft-gelinkte Cues weiter gereicht werden.
 * Kanalwerte können standardmäßig in jeder Cue gelinkt werden (Ausnahmen möglich). Das ersetzt Independents.
 * Möchte man Änderungen in mehreren Cues auf einmal durchführen, können neben der aktuellen Cue noch andere Cues markiert werden. Änderungen in der aktuellen Cue werden auch auf die anderen markierten Cues angewandt.
 * Cue Selection Groups bieten schnellen Zugriff auf häufig ausgewählte Cues für Multi-Cue Editing.
 * Eine Main Cue List Playback Sektion bietet Kontrolle über Fades. Fadezeiten für jede Cue sollte man auch einstellen können.
 * Einzel-Werte, die auf verschiedene Fixtures angewandt werden können, sollen in Variablen abgespeichert werden können (z. B. 42 % Dimmer, 255/128/0 RGB-Farbe, ...). Das entspricht universal/global presets bei GrandMA.
 * Selection Groups erlauben die schnelle Auswahl von oft ausgewählten Fixture Gruppen.
 * Eine Fixture Library abstrahiert die Kanalstruktur der einzelnen Scheinwerfer. Statt RGB+Dimmer kann man Farben dann z. B. auch in HSL mischen.
 * Effekte bieten bewegte Zustände im Licht. Aber nicht alles lässt sich mit Effekten gut machen. Irgendwie müsste man auch Chaser integrieren. Vielleicht Sub-Cue Listen? Konsolenweites Tap to Sync muss auch gehen.

Ich glaube, dass man im Theater so sehr gut arbeiten könnte. Die einzelne Cue-Liste mit Editier-Funktionen ist übersichtlich und Änderungen sind schnell gemacht und müssen nicht umständlich abgespeichert werden. Inwiefern es auch für Feste und "Live-Einstellen" (Busking) der Lichtshow passt, weiß ich nicht so genau. Vielleicht kann man sich einfach live seine Looks aus Buckets zusammendrücken? Effekte könnten für Bewegung in den Szenen sorgen. Inwiefern das funktioniert, müsst ihr mir sagen.
Es gibt in meinem Konzept auch noch ein paar logische Probleme, z. B. bin ich mir noch nicht ganz sicher, wie sich Buckets verhalten sollen, die wieder auf Buckets verweisen. Oder was passiert, wenn ich schnell nacheinander verschiedene Buckets in meiner Cue ausprobiere (z. B. verschiedene Farben)? Habe ich dann einfach viele Soft-Links zu Buckets in meiner Cue? Was ist, wenn ich die gar nicht will?
spezielle Skriptsprache

# Kommandozeile
Zu der "Kommandozeilensprache" habe ich mir auch ein bisschen Gedanken gemacht. Mein erster, unvollständiger Vorschlag:
In Anlehnung an GrandMA kann man Fixtures über Nummern auswählen:
<code>1\<ENTER\></code>

Bereiche von Fixtures:

<code>1 thru 5\<ENTER\></code> oder in kurzer Form <code>1t5\<ENTER\></code>

<code>10t\<ENTER\></code> wählt alle Fixtures nach dem zehnten aus. <code>t\<ENTER\></code> oder <code>tt</code> wählt alle Fixtures aus. Die Idee hinter <code>tt</code> ist, dass viele Buchstaben doppelt angetippt werden können, um eine Funktion auszulösen, ohne dass man danach Enter zu drücken braucht. Das beschleunigt die Eingabe und ist bekannt von GrandMA.

Möchte man zum Beispiel Fixtures 2 bis 4 voll anmachen:

<code>2t4 at 100\<ENTER\></code> oder <code>2t4a100\<ENTER\></code> oder aber <code>2t4aa</code>

Möchte ich sie ausmachen, kann ich eingeben:

<code>2t4..</code> oder <code>2 thru 4 at 0\<ENTER\></code>

Die aktuelle Selektion bleibt natürlich auch über die Zeilen hinweg erhalten:

1t3<ENTER>

aa (1 bis 3 an)

.. (1 bis 3 aus)

Die aktuelle Cue kann man einfach in eine neue Cue (direkt dahinter) hineinkopieren, indem man tippt:

new<ENTER> oder nn

Möchte man nicht die aktuelle Cue kopieren, sondern unter der aktuellen Cue eine neue Cue basierend auf Cue 1 anlegen, tippt man:

new cue 1<ENTER> oder n q1<ENTER> oder n1qq

Wie ihr seht, muss man zwischen Zahlen und Buchstaben kein Leerzeichen setzen. Das ist nur zwischen mehreren Buchstaben nötig. Damit braucht man weniger Zeit zum Tippen, weil die hat man beim Programmieren von Licht immer zu wenig. Auch Groß-/Kleinschreibung soll völlig egal sein, damit man sich damit nicht herumschlagen muss.
