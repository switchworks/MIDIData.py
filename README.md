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
```
このクラスは内部でpMIDIData/pMIDITrack/pMIDIEvent等の変数でポインタを格納している為、  
(あまりメリットはありませんが)前述の関数とも相互に利用が可能です。
```python
from MIDIData import *
i = MIDIData.loadFromSMF('./hoge.mid')
MIDIData_GetTitle(i.pMIDIData)
```
また一部メソッドはプロパティとしても利用可能です。
```python
from MIDIData import *
i = MIDIData.loadFromSMF('./hoge.mid')
i.title = 'hello MIDIData'
```
現在利用可能なプロパティは以下になります。
| Property					| Read	| Write	|
|:--------------------------|:-----:|:-----:|
| MIDIData.title			| O		| O     |
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
