# MIDIData.py
use [MIDIDataLibrary](https://openmidiproject.opal.ne.jp/MIDIDataLibrary.html) in Python3

※非推奨関数などは意図的にコメントアウトしています。  

MIDIDataライブラリのドキュメント通りに(ほぼ全ての)関数を利用可能です。
```python
from MIDIData import *
p = MIDIData_LoadFromSMF('./hoge.mid')
MIDIData_GetTitle(p)
```

# クラス
MIDIData/MIDITrack/MIDIEventクラスを利用出来ます。  
loadFrom系クラスメソッド等からインスタンスを作成出来ます。  
Pythonの命名規則に従いメソッドの1文字目は小文字に変更されています。  
また「自身のポインタを第一引数で渡す関数」に関しては第一引数を省略しています。
```python
from MIDIData import *
i = MIDIData.loadFromSMF('./hoge.mid')
i.getTitle()
i.getFirstTrack().getFirstEvent().getKind()
```
MIDIData/MIDITrackクラスはイテラブルな為、for文を利用出来ます。  
利用した全てのインスタンスが正しく破棄される為に、  
恐らくこのように利用するのが最も美しいと思います。
```python
try:
	i = MIDIData.loadFromSMF(filepath)
	for t in i: # 各トラックを取得
		for e in t: # 各イベントを取得
			# ここに色々処理を書く
finally:
	del i
```
これらのインスタンスは内部でpMIDIData/pMIDITrack/pMIDIEvent等の変数でポインタを格納している為、  
(あまりメリットはありませんが)前述の関数とも相互に利用が可能です。
```python
from MIDIData import *
i = MIDIData.loadFromSMF('./hoge.mid')
MIDIData_GetTitle(i.pMIDIData)
```
また一部メソッドはプロパティとしても利用可能です。  
※MIDIEventのIs系のようなbool値を返す物はプロパティに寄せました。
```python
from MIDIData import *
i = MIDIData.loadFromSMF('./hoge.mid')
i.title = 'hello MIDIData'
i.getFirstTrack().getFirstEvent().kind
```
現在利用可能なプロパティは以下になります。
| Property					| Read	| Write	|
|:--------------------------|:-----:|:-----:|
| MIDIData.title			| O		| O     |
| MIDIData.format			| O		| O     |
| MIDIData.timeBase			| O		| O     |
| MIDIData.timeMode			| O		| X     |
| MIDIData.timeResolution	| O		| X		|
| MIDIData.numTrack			| O		| X		|
| MIDIData.beginTime		| O		| X		|
| MIDIData.endTime			| O		| X		|
| MIDIData.subTitle			| O		| O		|
| MIDIData.copyright		| O		| O		|
| MIDIData.comment			| O		| O		|
| MIDITrack.numEvent		| O		| X		|
| MIDITrack.beginTime		| O		| X		|
| MIDITrack.endTime			| O		| X		|
| MIDITrack.name			| O		| O		|
| MIDITrack.inputOn			| O		| O		|
| MIDITrack.inputPort		| O		| O		|
| MIDITrack.inputChannel	| O		| O		|
| MIDITrack.outputOn		| O		| O		|
| MIDITrack.outputPort		| O		| O		|
| MIDITrack.outputChannel	| O		| O		|
| MIDITrack.viewMode		| O		| O		|
| MIDITrack.foreColor		| O		| O		|
| MIDITrack.backColor		| O		| O		|
| MIDIEvent.kind			| O		| X		|
| MIDIEvent.tempo			| O		| O		|
| MIDIEvent.channel			| O		| O		|
| MIDIEvent.time			| O		| O		|
| MIDIEvent.key				| O		| O		|
| MIDIEvent.velocity		| O		| O		|
| MIDIEvent.duration		| O		| O		|
| MIDIEvent.bank			| O		| O		|
| MIDIEvent.bankMSB			| O		| O		|
| MIDIEvent.bankLSB			| O		| O		|
| MIDIEvent.patchNum		| O		| O		|
| MIDIEvent.dataEntryMSB	| O		| O		|
| MIDIEvent.number			| O		| O		|
| MIDIEvent.value			| O		| O		|
| MIDIEvent.isMetaEvent			| O		| X		|
| MIDIEvent.isSequenceNumber			| O		| X		|
| MIDIEvent.isTextEvent			| O		| X		|
| MIDIEvent.isCopyrightNotice			| O		| X		|
| MIDIEvent.isTrackName			| O		| X		|
| MIDIEvent.isInstrumentName			| O		| X		|
| MIDIEvent.isLyric			| O		| X		|
| MIDIEvent.isMarker			| O		| X		|
| MIDIEvent.isCuePoint			| O		| X		|
| MIDIEvent.isProgramName			| O		| X		|
| MIDIEvent.isDeviceName			| O		| X		|
| MIDIEvent.isChannelPrefix			| O		| X		|
| MIDIEvent.isPortPrefix			| O		| X		|
| MIDIEvent.isEndofTrack			| O		| X		|
| MIDIEvent.isTempo			| O		| X		|
| MIDIEvent.isSMPTEOffset			| O		| X		|
| MIDIEvent.isTimeSignature			| O		| X		|
| MIDIEvent.isKeySignature			| O		| X		|
| MIDIEvent.isSequencerSpecific			| O		| X		|
| MIDIEvent.isMIDIEvent			| O		| X		|
| MIDIEvent.isNoteOn			| O		| X		|
| MIDIEvent.isNoteOff			| O		| X		|
| MIDIEvent.isNote			| O		| X		|
| MIDIEvent.isNoteOnNoteOff			| O		| X		|
| MIDIEvent.isNoteOnNoteOn0			| O		| X		|
| MIDIEvent.isKeyAftertouch			| O		| X		|
| MIDIEvent.isControlChange			| O		| X		|
| MIDIEvent.isRPNChange			| O		| X		|
| MIDIEvent.isNRPNChange			| O		| X		|
| MIDIEvent.isProgramChange			| O		| X		|
| MIDIEvent.isPatchChange			| O		| X		|
| MIDIEvent.isChannelAftertouch			| O		| X		|
| MIDIEvent.isPitchBend			| O		| X		|
| MIDIEvent.isSysExEvent			| O		| X		|
| MIDIEvent.isFloating			| O		| X		|
| MIDIEvent.isCombined			| O		| X		|
