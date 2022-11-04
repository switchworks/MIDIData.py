# fixTPQ.py

## required
* [Python 3.x](https://www.python.org/downloads/windows/)
* [MIDIData.dll](https://openmidiproject.osdn.jp/MIDIDataLibrary.html)
* [MIDIData.py](https://github.com/switchworks/MIDIData.py)


ログ系midなどの「解像度がズレていて小節線と合わない」midを修正します。  
具体的には以下の処理を行います。  
・ノートとノートの距離の総洗い出し  
・最頻出及び全要素を表示  
・(上記を目視して手動で)新しいTPQの入力  
・TPQ(Ticks Per Quarter Note)の書き換え  
・新しいTPQに合わせたテンポイベントの修正  
・おまけとして「最初に現れるノートのtick数の表示」及び「曲全体の前詰め」も可能

「大きすぎる値は無視」「綺麗そうな公約数を見つける」というコツを掴めば  
綺麗なmidを得られるかもしれません。  
一応fixTPQ.batも置いておきますのでこちらにmidをD&Dすれば自分でコマンドライン叩かなくても使えるかも。

![fixTPQ](https://github.com/switchworks/MIDIData.py/blob/main/fixTPQ/fixTPQ.png?raw=true)

このサンプル画像の場合は64で適切でした。(32/128等でも大きな支障は無いでしょう)
