# -*- coding: utf-8 -*-
import sys
import os
from ctypes import *
from struct import *

if not os.path.isfile('./MIDIData.dll'):
	sys.exit(1)
try:
    MIDIDataDLL = windll.LoadLibrary('./MIDIData.dll')
except OSError as e:
    print(f"Error loading library: {e}")
    sys.exit(1)

MIDIDATA_FORMAT0 = 0x00 # フォーマット0
MIDIDATA_FORMAT1 = 0x01 # フォーマット1
MIDIDATA_FORMAT2 = 0x02 # フォーマット2

MIDIEVENT_SEQUENCENUMBER = 0x00 # シーケンスナンバー(2バイト)
MIDIEVENT_TEXTEVENT = 0x01 # テキスト(可変長文字列)
MIDIEVENT_COPYRIGHTNOTICE = 0x02 # 著作権(可変長文字列)
MIDIEVENT_TRACKNAME = 0x03 # トラック名・シーケンサ名(可変長文字列)
MIDIEVENT_INSTRUMENTNAME = 0x04 # インストゥルメント(可変長文字列)
MIDIEVENT_LYRIC = 0x05 # 歌詞(可変長文字列)
MIDIEVENT_MARKER = 0x06 # マーカー(可変長文字列)
MIDIEVENT_CUEPOINT = 0x07 # キューポイント(可変長文字列)
MIDIEVENT_PROGRAMNAME = 0x08 # プログラム名(可変長文字列)
MIDIEVENT_DEVICENAME = 0x09 # デバイス名(可変長文字列)
MIDIEVENT_CHANNELPREFIX = 0x20 # チャンネルプレフィックス(1バイト)
MIDIEVENT_PORTPREFIX = 0x21 # ポートプレフィックス(1バイト)
MIDIEVENT_ENDOFTRACK = 0x2F # エンドオブトラック(0バイト)
MIDIEVENT_TEMPO = 0x51 # テンポ(3バイト)
MIDIEVENT_SMPTEOFFSET = 0x54 # SMPTEオフセット(5バイト)
MIDIEVENT_TIMESIGNATURE = 0x58 # 拍子記号(4バイト)
MIDIEVENT_KEYSIGNATURE = 0x59 # 調性記号(2バイト)
MIDIEVENT_SEQUENCERSPECIFIC = 0x7F # シーケンサー独自のイベント(可変長バイナリ)
MIDIEVENT_NOTEOFF = 0x80 # ノートオフ(3バイト)
MIDIEVENT_NOTEON = 0x90 # ノートオン(3バイト)
MIDIEVENT_KEYAFTERTOUCH = 0xA0 # キーアフター(3バイト)
MIDIEVENT_CONTROLCHANGE = 0xB0 # コントローラー(3バイト)
MIDIEVENT_PROGRAMCHANGE = 0xC0 # プログラムチェンジ(2バイト)
MIDIEVENT_CHANNELAFTERTOUCH = 0xD0 # チャンネルアフター(2バイト)
MIDIEVENT_PITCHBEND = 0xE0 # ピッチベンド(3バイト)
MIDIEVENT_SYSEXSTART = 0xF0 # システムエクスクルーシヴ(可変長バイナリ)
MIDIEVENT_SYSEXCONTINUE = 0xF7 # システムエクスクルーシヴの続き(可変長バイナリ)

MIDIEVENT_NOTEONNOTEOFF = 0x180 # ノート(0x9n+0x8n)
MIDIEVENT_NOTEONNOTEON0 = 0x190 # ノート(0x9n+0x9n(vel==0))
MIDIEVENT_PATCHCHANGE = 0x1C0 # パッチチェンジ(CC#32+CC#0+プログラムチェンジ)
MIDIEVENT_RPNCHANGE = 0x1A0 # RPNチェンジ(CC#101+CC#100+CC#6)
MIDIEVENT_NRPNCHANGE = 0x1B0 # NRPNチェンジ(CC#99+CC#98+CC#6)


#　MIDIDataクラス関数
# MIDIデータの指定トラックの直前にトラックを挿入
MIDIData_InsertTrackBefore = MIDIDataDLL.MIDIData_InsertTrackBefore
MIDIData_InsertTrackBefore.restype = c_bool
MIDIData_InsertTrackBefore.argtypes = (c_void_p,c_void_p,c_void_p,)
# MIDIデータの指定トラックの直後にトラックを挿入
MIDIData_InsertTrackAfter = MIDIDataDLL.MIDIData_InsertTrackAfter
MIDIData_InsertTrackAfter.restype = c_bool
MIDIData_InsertTrackAfter.argtypes = (c_void_p,c_void_p,c_void_p,)
# MIDIデータにトラックを追加(トラックは予め生成しておく)
MIDIData_AddTrack = MIDIDataDLL.MIDIData_AddTrack
MIDIData_AddTrack.restype = c_uint
MIDIData_AddTrack.argtypes = (c_void_p,c_void_p,)
# MIDIデータからトラックを除去(トラック自体及びトラック内のイベントは削除しない)
MIDIData_RemoveTrack = MIDIDataDLL.MIDIData_RemoveTrack
MIDIData_RemoveTrack.restype = c_bool
MIDIData_RemoveTrack.argtypes = (c_void_p,c_void_p,)
# MIDIデータの削除(含まれるトラック及びイベントもすべて削除)
MIDIData_Delete = MIDIDataDLL.MIDIData_Delete
MIDIData_Delete.restype = None
MIDIData_Delete.argtypes = (c_void_p,)
# MIDIデータを生成し、MIDIデータへのポインタを返す(失敗時NULL)
MIDIData_Create = MIDIDataDLL.MIDIData_Create
MIDIData_Create.restype = c_void_p
MIDIData_Create.argtypes = (c_uint,c_uint,c_uint,c_uint,)
# MIDIデータのフォーマット0/1/2を取得
MIDIData_GetFormat = MIDIDataDLL.MIDIData_GetFormat
MIDIData_GetFormat.restype = c_uint
MIDIData_GetFormat.argtypes = (c_void_p,)
# MIDIデータのフォーマット0/1/2を設定(変更時コンバート機能を含む)
MIDIData_SetFormat = MIDIDataDLL.MIDIData_SetFormat
MIDIData_SetFormat.restype = c_bool
MIDIData_SetFormat.argtypes = (c_void_p,c_uint,)
# MIDIデータのタイムベース取得
MIDIData_GetTimeBase = MIDIDataDLL.MIDIData_GetTimeBase
MIDIData_GetTimeBase.restype = c_uint
MIDIData_GetTimeBase.argtypes = (c_void_p,)
# MIDIデータのタイムベースのタイムモード取得
MIDIData_GetTimeMode = MIDIDataDLL.MIDIData_GetTimeMode
MIDIData_GetTimeMode.restype = c_uint
MIDIData_GetTimeMode.argtypes = (c_void_p,)
# MIDIデータのタイムベースのレゾリューション取得
MIDIData_GetTimeResolution = MIDIDataDLL.MIDIData_GetTimeResolution
MIDIData_GetTimeResolution.restype = c_uint
MIDIData_GetTimeResolution.argtypes = (c_void_p,)
# MIDIデータのタイムベース設定
MIDIData_SetTimeBase = MIDIDataDLL.MIDIData_SetTimeBase
MIDIData_SetTimeBase.restype = c_bool
MIDIData_SetTimeBase.argtypes = (c_void_p,c_uint,c_uint,)
# MIDIデータのトラック数取得
MIDIData_GetNumTrack = MIDIDataDLL.MIDIData_GetNumTrack
MIDIData_GetNumTrack.restype = c_uint
MIDIData_GetNumTrack.argtypes = (c_void_p,)
# トラック数をカウントし、各トラックのインデックスと総トラック数を更新し、トラック数を返す。
MIDIData_CountTrack = MIDIDataDLL.MIDIData_CountTrack
MIDIData_CountTrack.restype = c_uint
MIDIData_CountTrack.argtypes = (c_void_p,)
# XFであるとき、XFのヴァージョンを取得(XFでなければ0)
MIDIData_GetXFVersion = MIDIDataDLL.MIDIData_GetXFVersion
MIDIData_GetXFVersion.restype = c_uint
MIDIData_GetXFVersion.argtypes = (c_void_p,)
# MIDIデータの最初のトラックへのポインタを取得(なければNULL)
MIDIData_GetFirstTrack = MIDIDataDLL.MIDIData_GetFirstTrack
MIDIData_GetFirstTrack.restype = c_void_p
MIDIData_GetFirstTrack.argtypes = (c_void_p,)
# MIDIデータの最後のトラックへのポインタを取得(なければNULL)
MIDIData_GetLastTrack = MIDIDataDLL.MIDIData_GetLastTrack
MIDIData_GetLastTrack.restype = c_void_p
MIDIData_GetLastTrack.argtypes = (c_void_p,)
# 指定インデックスのMIDIトラックへのポインタを取得する(なければNULL)
MIDIData_GetTrack = MIDIDataDLL.MIDIData_GetTrack
MIDIData_GetTrack.restype = c_void_p
MIDIData_GetTrack.argtypes = (c_void_p,c_uint,)
# MIDIデータの開始時刻[Tick]を取得
MIDIData_GetBeginTime = MIDIDataDLL.MIDIData_GetBeginTime
MIDIData_GetBeginTime.restype = c_uint
MIDIData_GetBeginTime.argtypes = (c_void_p,)
# MIDIデータの終了時刻[Tick]を取得
MIDIData_GetEndTime = MIDIDataDLL.MIDIData_GetEndTime
MIDIData_GetEndTime.restype = c_uint
MIDIData_GetEndTime.argtypes = (c_void_p,)
# MIDIデータのタイトルを簡易取得
MIDIData_GetTitle = MIDIDataDLL.MIDIData_GetTitleW
MIDIData_GetTitle.restype = c_wchar_p
MIDIData_GetTitle.argtypes = (c_void_p,c_wchar_p,c_void_p,)
# MIDIデータのタイトルを簡易設定
MIDIData_SetTitle = MIDIDataDLL.MIDIData_SetTitleW
MIDIData_SetTitle.restype = c_bool
MIDIData_SetTitle.argtypes = (c_void_p,c_wchar_p,)
# MIDIデータのサブタイトルを簡易取得
MIDIData_GetSubTitle = MIDIDataDLL.MIDIData_GetSubTitleW
MIDIData_GetSubTitle.restype = c_wchar_p
MIDIData_GetSubTitle.argtypes = (c_void_p,c_wchar_p,c_void_p,)
# MIDIデータのサブタイトルを簡易設定
MIDIData_SetSubTitle = MIDIDataDLL.MIDIData_SetSubTitleW
MIDIData_SetSubTitle.restype = c_void_p
MIDIData_SetSubTitle.argtypes = (c_void_p,c_wchar_p,)
# MIDIデータの著作権を簡易取得
MIDIData_GetCopyright = MIDIDataDLL.MIDIData_GetCopyrightW
MIDIData_GetCopyright.restype = c_wchar_p
MIDIData_GetCopyright.argtypes = (c_void_p,c_wchar_p,c_void_p,)
# MIDIデータの著作権を簡易設定
MIDIData_SetCopyright = MIDIDataDLL.MIDIData_SetCopyrightW
MIDIData_SetCopyright.restype = c_void_p
MIDIData_SetCopyright.argtypes = (c_void_p,c_wchar_p,)
# MIDIデータのコメントを簡易取得
MIDIData_GetComment = MIDIDataDLL.MIDIData_GetCommentW
MIDIData_GetComment.restype = c_wchar_p
MIDIData_GetComment.argtypes = (c_void_p,c_wchar_p,c_void_p,)
# MIDIデータのコメントを簡易設定
MIDIData_SetComment = MIDIDataDLL.MIDIData_SetCommentW
MIDIData_SetComment.restype = c_void_p
MIDIData_SetComment.argtypes = (c_void_p,c_wchar_p,)
# タイムコードをミリ秒に変換(フォーマット0/1の場合のみ)
MIDIData_TimeToMillisec = MIDIDataDLL.MIDIData_TimeToMillisec
MIDIData_TimeToMillisec.restype = c_uint
MIDIData_TimeToMillisec.argtypes = (c_void_p,c_uint,)
# ミリ秒をタイムコードに変換(フォーマット0/1の場合のみ)
MIDIData_MillisecToTime = MIDIDataDLL.MIDIData_MillisecToTime
MIDIData_MillisecToTime.restype = c_uint
MIDIData_MillisecToTime.argtypes = (c_void_p,c_uint,)
# タイムコードを小節：拍：ティックに分解(最初のトラック内の拍子記号から計算)
MIDIData_BreakTime = MIDIDataDLL.MIDIData_BreakTime
MIDIData_BreakTime.restype = c_void_p
MIDIData_BreakTime.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,c_void_p,)
# タイムコードを小節：拍：ティックに分解(最初のトラック内の拍子記号を基に計算)
MIDIData_BreakTimeEx = MIDIDataDLL.MIDIData_BreakTimeEx
MIDIData_BreakTimeEx.restype = c_void_p
MIDIData_BreakTimeEx.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,)
# 小節：拍：ティックからタイムコードを生成(最初のトラック内の拍子記号から計算)
MIDIData_MakeTime = MIDIDataDLL.MIDIData_MakeTime
MIDIData_MakeTime.restype = c_void_p
MIDIData_MakeTime.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_void_p,)
# 小節：拍：ティックからタイムコードを生成(最初のトラック内の拍子記号を基に計算)
MIDIData_MakeTimeEx = MIDIDataDLL.MIDIData_MakeTimeEx
MIDIData_MakeTimeEx.restype = c_void_p
MIDIData_MakeTimeEx.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,)
# 指定位置におけるテンポを取得
MIDIData_FindTempo = MIDIDataDLL.MIDIData_FindTempo
MIDIData_FindTempo.restype = c_void_p
MIDIData_FindTempo.argtypes = (c_void_p,c_uint,c_void_p,)
# 指定位置における拍子記号を取得
MIDIData_FindTimeSignature = MIDIDataDLL.MIDIData_FindTimeSignature
MIDIData_FindTimeSignature.restype = c_void_p
MIDIData_FindTimeSignature.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,c_void_p,c_void_p,)
# 指定位置における調性記号を取得
MIDIData_FindKeySignature = MIDIDataDLL.MIDIData_FindKeySignature
MIDIData_FindKeySignature.restype = c_void_p
MIDIData_FindKeySignature.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,)
# MIDIDataをスタンダードMIDIファイル(SMF)から読み込み、*/
# 新しいMIDIデータへのポインタを返す(失敗時NULL)
MIDIData_LoadFromSMF = MIDIDataDLL.MIDIData_LoadFromSMFW
MIDIData_LoadFromSMF.restype = c_void_p
MIDIData_LoadFromSMF.argtypes = (c_wchar_p,)
# MIDIデータをスタンダードMIDIファイル(SMF)として保存
MIDIData_SaveAsSMF = MIDIDataDLL.MIDIData_SaveAsSMFW
MIDIData_SaveAsSMF.restype = c_bool
MIDIData_SaveAsSMF.argtypes = (c_void_p,c_wchar_p,)
# MIDIDataをテキストファイルから読み込み、
# 新しいMIDIデータへのポインタを返す(失敗時NULL)
MIDIData_LoadFromText = MIDIDataDLL.MIDIData_LoadFromTextW
MIDIData_LoadFromText.restype = c_void_p
MIDIData_LoadFromText.argtypes = (c_wchar_p,)
# MIDIDataをテキストファイルとして保存
MIDIData_SaveAsText = MIDIDataDLL.MIDIData_SaveAsTextW
MIDIData_SaveAsText.restype = c_bool
MIDIData_SaveAsText.argtypes = (c_void_p,c_wchar_p,)
# MIDIDataをバイナリファイルから読み込み、*/
# 新しいMIDIデータへのポインタを返す(失敗時NULL)
MIDIData_LoadFromBinary = MIDIDataDLL.MIDIData_LoadFromBinaryW
MIDIData_LoadFromBinary.restype = c_void_p
MIDIData_LoadFromBinary.argtypes = (c_wchar_p,)
# MIDIDataをバイナリファイルに保存
MIDIData_SaveAsBinary = MIDIDataDLL.MIDIData_SaveAsBinaryW
MIDIData_SaveAsBinary.restype = c_bool
MIDIData_SaveAsBinary.argtypes = (c_void_p,c_wchar_p,)
# MIDIDataをCherrryファイル(*.chy)から読み込み、
# 新しいMIDIデータへのポインタを返す(失敗時NULL)
MIDIData_LoadFromCherry = MIDIDataDLL.MIDIData_LoadFromCherryW
MIDIData_LoadFromCherry.restype = c_void_p
MIDIData_LoadFromCherry.argtypes = (c_wchar_p,)
# MIDIデータをCherryファイル(*.chy)に保存
MIDIData_SaveAsCherry = MIDIDataDLL.MIDIData_SaveAsCherryW
MIDIData_SaveAsCherry.restype = c_bool
MIDIData_SaveAsCherry.argtypes = (c_void_p,c_wchar_p,)
# MIDIデータをMIDICSVファイル(*.csv)から読み込み
# 新しいMIDIデータへのポインタを返す(失敗時NULL)
MIDIData_LoadFromMIDICSV = MIDIDataDLL.MIDIData_LoadFromMIDICSVW
MIDIData_LoadFromMIDICSV.restype = c_void_p
MIDIData_LoadFromMIDICSV.argtypes = (c_wchar_p,)
# MIDIデータをMIDICSVファイル(*.csv)として保存
MIDIData_SaveAsMIDICSV = MIDIDataDLL.MIDIData_SaveAsMIDICSVW
MIDIData_SaveAsMIDICSV.restype = c_bool
MIDIData_SaveAsMIDICSV.argtypes = (c_void_p,c_wchar_p,)
# MIDIデータを旧Cakewalkシーケンスファイル(*.wrk)から読み込み
# 新しいMIDIデータへのポインタを返す(失敗時NULL)
MIDIData_LoadFromWRK = MIDIDataDLL.MIDIData_LoadFromWRKW
MIDIData_LoadFromWRK.restype = c_void_p
MIDIData_LoadFromWRK.argtypes = (c_wchar_p,)
# MIDIデータをマビノギMMLファイル(*.mml)から読み込み
# 新しいMIDIデータへのポインタを返す(失敗時NULL)
MIDIData_LoadFromMabiMML = MIDIDataDLL.MIDIData_LoadFromMabiMMLW
MIDIData_LoadFromMabiMML.restype = c_void_p
MIDIData_LoadFromMabiMML.argtypes = (c_wchar_p,)

#　MIDITrackクラス関数
# トラック内のイベントの総数を取得
MIDITrack_GetNumEvent = MIDIDataDLL.MIDITrack_GetNumEvent
MIDITrack_GetNumEvent.restype = c_void_p
MIDITrack_GetNumEvent.argtypes = (c_void_p,)
# トラックの最初のイベントへのポインタを取得(なければNULL)
MIDITrack_GetFirstEvent = MIDIDataDLL.MIDITrack_GetFirstEvent
MIDITrack_GetFirstEvent.restype = c_void_p
MIDITrack_GetFirstEvent.argtypes = (c_void_p,)
# トラックの最後のイベントへのポインタを取得(なければNULL)
MIDITrack_GetLastEvent = MIDIDataDLL.MIDITrack_GetLastEvent
MIDITrack_GetLastEvent.restype = c_void_p
MIDITrack_GetLastEvent.argtypes = (c_void_p,)
# トラック内の指定種類の最初のイベント取得(なければNULL)
MIDITrack_GetFirstKindEvent = MIDIDataDLL.MIDITrack_GetFirstKindEvent
MIDITrack_GetFirstKindEvent.restype = c_void_p
MIDITrack_GetFirstKindEvent.argtypes = (c_void_p,c_uint,)
# トラック内の指定種類の最後のイベント取得(なければNULL)
MIDITrack_GetLastKindEvent = MIDIDataDLL.MIDITrack_GetLastKindEvent
MIDITrack_GetLastKindEvent.restype = c_void_p
MIDITrack_GetLastKindEvent.argtypes = (c_void_p,c_uint,)
# 次のMIDIトラックへのポインタ取得(なければNULL)(20080715追加)
MIDITrack_GetNextTrack = MIDIDataDLL.MIDITrack_GetNextTrack
MIDITrack_GetNextTrack.restype = c_void_p
MIDITrack_GetNextTrack.argtypes = (c_void_p,)
# 前のMIDIトラックへのポインタ取得(なければNULL)(20080715追加)
MIDITrack_GetPrevTrack = MIDIDataDLL.MIDITrack_GetPrevTrack
MIDITrack_GetPrevTrack.restype = c_void_p
MIDITrack_GetPrevTrack.argtypes = (c_void_p,)
# トラックの親MIDIデータへのポインタを取得(なければNULL)
MIDITrack_GetParent = MIDIDataDLL.MIDITrack_GetParent
MIDITrack_GetParent.restype = c_void_p
MIDITrack_GetParent.argtypes = (c_void_p,)
# トラック内のイベント数をカウントし、各イベントのインデックスと総イベント数を更新し、イベント数を返す。
MIDITrack_CountEvent = MIDIDataDLL.MIDITrack_CountEvent
MIDITrack_CountEvent.restype = c_uint
MIDITrack_CountEvent.argtypes = (c_void_p,)
# トラックの開始時刻(最初のイベントの時刻)[Tick]を取得(20081101追加)
MIDITrack_GetBeginTime = MIDIDataDLL.MIDITrack_GetBeginTime
MIDITrack_GetBeginTime.restype = c_uint
MIDITrack_GetBeginTime.argtypes = (c_void_p,)
# トラックの終了時刻(最後のイベントの時刻)[Tick]を取得(20081101追加)
MIDITrack_GetEndTime = MIDIDataDLL.MIDITrack_GetEndTime
MIDITrack_GetEndTime.restype = c_uint
MIDITrack_GetEndTime.argtypes = (c_void_p,)
# トラックの名前を簡易に取得
MIDITrack_GetName = MIDIDataDLL.MIDITrack_GetNameW
MIDITrack_GetName.restype = c_wchar_p
MIDITrack_GetName.argtypes = (c_void_p,c_wchar_p,c_void_p,)
# 入力取得(0=OFF, 1=On)
MIDITrack_GetInputOn = MIDIDataDLL.MIDITrack_GetInputOn
MIDITrack_GetInputOn.restype = c_bool
MIDITrack_GetInputOn.argtypes = (c_void_p,)
# 入力ポート取得(-1=n/a, 0～15=ポート番号)
MIDITrack_GetInputPort = MIDIDataDLL.MIDITrack_GetInputPort
MIDITrack_GetInputPort.restype = c_uint
MIDITrack_GetInputPort.argtypes = (c_void_p,)
# 入力チャンネル取得(-1=n/a, 0～15=チャンネル番号)
MIDITrack_GetInputChannel = MIDIDataDLL.MIDITrack_GetInputChannel
MIDITrack_GetInputChannel.restype = c_uint
MIDITrack_GetInputChannel.argtypes = (c_void_p,)
# 出力取得(0=OFF, 1=On)
MIDITrack_GetOutputOn = MIDIDataDLL.MIDITrack_GetOutputOn
MIDITrack_GetOutputOn.restype = c_bool
MIDITrack_GetOutputOn.argtypes = (c_void_p,)
# 出力ポート(-1=n/a, 0～15=ポート番号)
MIDITrack_GetOutputPort = MIDIDataDLL.MIDITrack_GetOutputPort
MIDITrack_GetOutputPort.restype = c_uint
MIDITrack_GetOutputPort.argtypes = (c_void_p,)
# 出力チャンネル(-1=n/a, 0～15=チャンネル番号)
MIDITrack_GetOutputChannel = MIDIDataDLL.MIDITrack_GetOutputChannel
MIDITrack_GetOutputChannel.restype = c_uint
MIDITrack_GetOutputChannel.argtypes = (c_void_p,)
# タイム+取得
MIDITrack_GetTimePlus = MIDIDataDLL.MIDITrack_GetTimePlus
MIDITrack_GetTimePlus.restype = c_uint
MIDITrack_GetTimePlus.argtypes = (c_void_p,)
# キー+取得
MIDITrack_GetKeyPlus = MIDIDataDLL.MIDITrack_GetKeyPlus
MIDITrack_GetKeyPlus.restype = c_uint
MIDITrack_GetKeyPlus.argtypes = (c_void_p,)
# ベロシティ+取得
MIDITrack_GetVelocityPlus = MIDIDataDLL.MIDITrack_GetVelocityPlus
MIDITrack_GetVelocityPlus.restype = c_uint
MIDITrack_GetVelocityPlus.argtypes = (c_void_p,)
# 表示モード取得(0=通常、1=ドラム)
MIDITrack_GetViewMode = MIDIDataDLL.MIDITrack_GetViewMode
MIDITrack_GetViewMode.restype = c_bool
MIDITrack_GetViewMode.argtypes = (c_void_p,)
# 前景色取得
MIDITrack_GetForeColor = MIDIDataDLL.MIDITrack_GetForeColor
MIDITrack_GetForeColor.restype = c_uint
MIDITrack_GetForeColor.argtypes = (c_void_p,)
# 背景色取得
MIDITrack_GetBackColor = MIDIDataDLL.MIDITrack_GetBackColor
MIDITrack_GetBackColor.restype = c_uint
MIDITrack_GetBackColor.argtypes = (c_void_p,)
# トラックの名前を簡易に設定
MIDITrack_SetName = MIDIDataDLL.MIDITrack_SetNameW
MIDITrack_SetName.restype = c_void_p
MIDITrack_SetName.argtypes = (c_void_p,c_wchar_p,)
# 入力設定(0=OFF, 1=On)
MIDITrack_SetInputOn = MIDIDataDLL.MIDITrack_SetInputOn
MIDITrack_SetInputOn.restype = c_bool
MIDITrack_SetInputOn.argtypes = (c_void_p,c_bool,)
# 入力ポート設定(-1=n/a, 0～15=ポート番号)
MIDITrack_SetInputPort = MIDIDataDLL.MIDITrack_SetInputPort
MIDITrack_SetInputPort.restype = c_bool
MIDITrack_SetInputPort.argtypes = (c_void_p,c_uint,)
# 入力チャンネル設定(-1=n/a, 0～15=チャンネル番号)
MIDITrack_SetInputChannel = MIDIDataDLL.MIDITrack_SetInputChannel
MIDITrack_SetInputChannel.restype = c_bool
MIDITrack_SetInputChannel.argtypes = (c_void_p,c_uint,)
# 出力設定(0=OFF, 1=On)
MIDITrack_SetOutputOn = MIDIDataDLL.MIDITrack_SetOutputOn
MIDITrack_SetOutputOn.restype = c_bool
MIDITrack_SetOutputOn.argtypes = (c_void_p,c_bool,)
# 出力ポート(-1=n/a, 0～15=ポート番号)
MIDITrack_SetOutputPort = MIDIDataDLL.MIDITrack_SetOutputPort
MIDITrack_SetOutputPort.restype = c_bool
MIDITrack_SetOutputPort.argtypes = (c_void_p,c_uint,)
# 出力チャンネル(-1=n/a, 0～15=チャンネル番号)
MIDITrack_SetOutputChannel = MIDIDataDLL.MIDITrack_SetOutputChannel
MIDITrack_SetOutputChannel.restype = c_bool
MIDITrack_SetOutputChannel.argtypes = (c_void_p,c_uint,)
# タイム+設定
MIDITrack_SetTimePlus = MIDIDataDLL.MIDITrack_SetTimePlus
MIDITrack_SetTimePlus.restype = c_bool
MIDITrack_SetTimePlus.argtypes = (c_void_p,c_uint,)
# キー+設定
MIDITrack_SetKeyPlus = MIDIDataDLL.MIDITrack_SetKeyPlus
MIDITrack_SetKeyPlus.restype = c_bool
MIDITrack_SetKeyPlus.argtypes = (c_void_p,c_uint,)
# ベロシティ+設定
MIDITrack_SetVelocityPlus = MIDIDataDLL.MIDITrack_SetVelocityPlus
MIDITrack_SetVelocityPlus.restype = c_bool
MIDITrack_SetVelocityPlus.argtypes = (c_void_p,c_uint,)
# 表示モード設定(0=通常、1=ドラム)
MIDITrack_SetViewMode = MIDIDataDLL.MIDITrack_SetViewMode
MIDITrack_SetViewMode.restype = c_bool
MIDITrack_SetViewMode.argtypes = (c_void_p,c_bool,)
# 前景色設定
MIDITrack_SetForeColor = MIDIDataDLL.MIDITrack_SetForeColor
MIDITrack_SetForeColor.restype = c_bool
MIDITrack_SetForeColor.argtypes = (c_void_p,c_uint,)
# 背景色設定
MIDITrack_SetBackColor = MIDIDataDLL.MIDITrack_SetBackColor
MIDITrack_SetBackColor.restype = c_bool
MIDITrack_SetBackColor.argtypes = (c_void_p,c_uint,)
# XFであるとき、XFのヴァージョンを取得(XFでなければ0)
MIDITrack_GetXFVersion = MIDIDataDLL.MIDITrack_GetXFVersion
MIDITrack_GetXFVersion.restype = c_uint
MIDITrack_GetXFVersion.argtypes = (c_void_p,)
# トラックの削除(含まれるイベントオブジェクトも削除されます)
MIDITrack_Delete = MIDIDataDLL.MIDITrack_Delete
MIDITrack_Delete.restype = None
MIDITrack_Delete.argtypes = (c_void_p,)
# トラックを生成し、トラックへのポインタを返す(失敗時NULL)
MIDITrack_Create = MIDIDataDLL.MIDITrack_Create
MIDITrack_Create.restype = c_void_p
MIDITrack_Create.argtypes = ()
# MIDIトラックのクローンを生成
MIDITrack_CreateClone = MIDIDataDLL.MIDITrack_CreateClone
MIDITrack_CreateClone.restype = c_void_p
MIDITrack_CreateClone.argtypes = (c_void_p,)
# トラックにイベントを挿入(イベントはあらかじめ生成しておく)
#MIDITrack_InsertSingleEventAfter = MIDIDataDLL.MIDITrack_InsertSingleEventAfter
#MIDITrack_InsertSingleEventAfter.restype = c_void_p
#MIDITrack_InsertSingleEventAfter.argtypes = (c_void_p,)
# トラックにイベントを挿入(イベントはあらかじめ生成しておく)
#MIDITrack_InsertSingleEventBefore = MIDIDataDLL.MIDITrack_InsertSingleEventBefore
#MIDITrack_InsertSingleEventBefore.restype = c_void_p
#MIDITrack_InsertSingleEventBefore.argtypes = (c_void_p,)
# トラックにイベントを挿入(イベントはあらかじめ生成しておく)
MIDITrack_InsertEventAfter = MIDIDataDLL.MIDITrack_InsertEventAfter
MIDITrack_InsertEventAfter.restype = c_uint
MIDITrack_InsertEventAfter.argtypes = (c_void_p,c_void_p,c_void_p,)
# トラックにイベントを挿入(イベントはあらかじめ生成しておく)
MIDITrack_InsertEventBefore = MIDIDataDLL.MIDITrack_InsertEventBefore
MIDITrack_InsertEventBefore.restype = c_uint
MIDITrack_InsertEventBefore.argtypes = (c_void_p,c_void_p,c_void_p,)
# トラックにイベントを挿入(イベントはあらかじめ生成しておく)
MIDITrack_InsertEvent = MIDIDataDLL.MIDITrack_InsertEvent
MIDITrack_InsertEvent.restype = c_uint
MIDITrack_InsertEvent.argtypes = (c_void_p,c_void_p,)
# トラックにシーケンス番号イベントを生成して挿入
MIDITrack_InsertSequenceNumber = MIDIDataDLL.MIDITrack_InsertSequenceNumber
MIDITrack_InsertSequenceNumber.restype = c_bool
MIDITrack_InsertSequenceNumber.argtypes = (c_void_p,c_uint,c_uint,)
# トラックにテキストベースのイベントを生成して挿入
#MIDITrack_InsertTextBasedEvent = MIDIDataDLL.MIDITrack_InsertTextBasedEventW
#MIDITrack_InsertTextBasedEvent.restype = c_void_p
#MIDITrack_InsertTextBasedEvent.argtypes = (c_void_p,)
# トラックにテキストベースのイベントを生成して挿入(文字コード指定あり)
#MIDITrack_InsertTextBasedEventEx = MIDIDataDLL.MIDITrack_InsertTextBasedEventExW
#MIDITrack_InsertTextBasedEventEx.restype = c_void_p
#MIDITrack_InsertTextBasedEventEx.argtypes = (c_void_p,)
# トラックにテキストイベントを生成して挿入
MIDITrack_InsertTextEvent = MIDIDataDLL.MIDITrack_InsertTextEventW
MIDITrack_InsertTextEvent.restype = c_bool
MIDITrack_InsertTextEvent.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックにテキストイベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertTextEventEx = MIDIDataDLL.MIDITrack_InsertTextEventExW
MIDITrack_InsertTextEventEx.restype = c_bool
MIDITrack_InsertTextEventEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックに著作権イベントを生成して挿入
MIDITrack_InsertCopyrightNotice = MIDIDataDLL.MIDITrack_InsertCopyrightNoticeW
MIDITrack_InsertCopyrightNotice.restype = c_bool
MIDITrack_InsertCopyrightNotice.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックに著作権イベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertCopyrightNoticeEx = MIDIDataDLL.MIDITrack_InsertCopyrightNoticeExW
MIDITrack_InsertCopyrightNoticeEx.restype = c_bool
MIDITrack_InsertCopyrightNoticeEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックにトラック名イベントを生成して挿入
MIDITrack_InsertTrackName = MIDIDataDLL.MIDITrack_InsertTrackNameW
MIDITrack_InsertTrackName.restype = c_bool
MIDITrack_InsertTrackName.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックにトラック名イベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertTrackNameEx = MIDIDataDLL.MIDITrack_InsertTrackNameExW
MIDITrack_InsertTrackNameEx.restype = c_bool
MIDITrack_InsertTrackNameEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックにインストゥルメント名イベントを生成して挿入
MIDITrack_InsertInstrumentName = MIDIDataDLL.MIDITrack_InsertInstrumentNameW
MIDITrack_InsertInstrumentName.restype = c_bool
MIDITrack_InsertInstrumentName.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックにインストゥルメント名イベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertInstrumentNameEx = MIDIDataDLL.MIDITrack_InsertInstrumentNameExW
MIDITrack_InsertInstrumentNameEx.restype = c_bool
MIDITrack_InsertInstrumentNameEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックに歌詞イベントを生成して挿入
MIDITrack_InsertLyric = MIDIDataDLL.MIDITrack_InsertLyricW
MIDITrack_InsertLyric.restype = c_bool
MIDITrack_InsertLyric.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックに歌詞イベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertLyricEx = MIDIDataDLL.MIDITrack_InsertLyricExW
MIDITrack_InsertLyricEx.restype = c_bool
MIDITrack_InsertLyricEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックにマーカーイベントを生成して挿入
MIDITrack_InsertMarker = MIDIDataDLL.MIDITrack_InsertMarkerW
MIDITrack_InsertMarker.restype = c_bool
MIDITrack_InsertMarker.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックにマーカーイベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertMarkerEx = MIDIDataDLL.MIDITrack_InsertMarkerExW
MIDITrack_InsertMarkerEx.restype = c_bool
MIDITrack_InsertMarkerEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックにキューポイントイベントを生成して挿入
MIDITrack_InsertCuePoint = MIDIDataDLL.MIDITrack_InsertCuePointW
MIDITrack_InsertCuePoint.restype = c_bool
MIDITrack_InsertCuePoint.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックにキューポイントイベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertCuePointEx = MIDIDataDLL.MIDITrack_InsertCuePointExW
MIDITrack_InsertCuePointEx.restype = c_bool
MIDITrack_InsertCuePointEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックにプログラム名イベントを生成して挿入
MIDITrack_InsertProgramName = MIDIDataDLL.MIDITrack_InsertProgramNameW
MIDITrack_InsertProgramName.restype = c_bool
MIDITrack_InsertProgramName.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックにプログラム名イベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertProgramNameEx = MIDIDataDLL.MIDITrack_InsertProgramNameExW
MIDITrack_InsertProgramNameEx.restype = c_bool
MIDITrack_InsertProgramNameEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックにデバイス名イベントを生成して挿入
MIDITrack_InsertDeviceName = MIDIDataDLL.MIDITrack_InsertDeviceNameW
MIDITrack_InsertDeviceName.restype = c_bool
MIDITrack_InsertDeviceName.argtypes = (c_void_p,c_uint,c_wchar_p,)
# トラックにデバイス名イベントを生成して挿入(文字コード指定あり)
MIDITrack_InsertDeviceNameEx = MIDIDataDLL.MIDITrack_InsertDeviceNameExW
MIDITrack_InsertDeviceNameEx.restype = c_bool
MIDITrack_InsertDeviceNameEx.argtypes = (c_void_p,c_uint,c_uint,c_wchar_p,)
# トラックにチャンネルプレフィックスイベントを生成して挿入
MIDITrack_InsertChannelPrefix = MIDIDataDLL.MIDITrack_InsertChannelPrefix
MIDITrack_InsertChannelPrefix.restype = c_bool
MIDITrack_InsertChannelPrefix.argtypes = (c_void_p,c_uint,c_uint,)
# トラックにポートプレフィックスイベントを生成して挿入
MIDITrack_InsertPortPrefix = MIDIDataDLL.MIDITrack_InsertPortPrefix
MIDITrack_InsertPortPrefix.restype = c_bool
MIDITrack_InsertPortPrefix.argtypes = (c_void_p,c_uint,c_uint,)
# トラックにエンドオブトラックイベントを生成して挿入
MIDITrack_InsertEndofTrack = MIDIDataDLL.MIDITrack_InsertEndofTrack
MIDITrack_InsertEndofTrack.restype = c_bool
MIDITrack_InsertEndofTrack.argtypes = (c_void_p,c_uint,)
# トラックにテンポイベントを生成して挿入
MIDITrack_InsertTempo = MIDIDataDLL.MIDITrack_InsertTempo
MIDITrack_InsertTempo.restype = c_bool
MIDITrack_InsertTempo.argtypes = (c_void_p,c_uint,c_uint,)
# トラックにSMPTEオフセットイベントを生成して挿入
MIDITrack_InsertSMPTEOffset = MIDIDataDLL.MIDITrack_InsertSMPTEOffset
MIDITrack_InsertSMPTEOffset.restype = c_bool
MIDITrack_InsertSMPTEOffset.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,)
# トラックに拍子記号イベントを生成して挿入
MIDITrack_InsertTimeSignature = MIDIDataDLL.MIDITrack_InsertTimeSignature
MIDITrack_InsertTimeSignature.restype = c_bool
MIDITrack_InsertTimeSignature.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,c_uint,)
# トラックに調性記号イベントを生成して挿入
MIDITrack_InsertKeySignature = MIDIDataDLL.MIDITrack_InsertKeySignature
MIDITrack_InsertKeySignature.restype = c_bool
MIDITrack_InsertKeySignature.argtypes = (c_void_p,c_uint,c_uint,c_uint,)
# トラックにシーケンサー独自のイベントを生成して挿入
MIDITrack_InsertSequencerSpecific = MIDIDataDLL.MIDITrack_InsertSequencerSpecific
MIDITrack_InsertSequencerSpecific.restype = c_bool
MIDITrack_InsertSequencerSpecific.argtypes = (c_void_p,c_uint,c_wchar_p,c_uint,)
# トラックにノートオフイベントを生成して挿入
MIDITrack_InsertNoteOff = MIDIDataDLL.MIDITrack_InsertNoteOff
MIDITrack_InsertNoteOff.restype = c_bool
MIDITrack_InsertNoteOff.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,)
# トラックにノートオンイベントを生成して挿入
MIDITrack_InsertNoteOn = MIDIDataDLL.MIDITrack_InsertNoteOn
MIDITrack_InsertNoteOn.restype = c_bool
MIDITrack_InsertNoteOn.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,)
# トラックにノートイベントを生成して挿入
MIDITrack_InsertNote = MIDIDataDLL.MIDITrack_InsertNote
MIDITrack_InsertNote.restype = c_uint
MIDITrack_InsertNote.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,c_uint,)
# トラックにキーアフタータッチイベントを生成して挿入
MIDITrack_InsertKeyAftertouch = MIDIDataDLL.MIDITrack_InsertKeyAftertouch
MIDITrack_InsertKeyAftertouch.restype = c_bool
MIDITrack_InsertKeyAftertouch.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,)
# トラックにコントロールチェンジイベントを生成して挿入
MIDITrack_InsertControlChange = MIDIDataDLL.MIDITrack_InsertControlChange
MIDITrack_InsertControlChange.restype = c_bool
MIDITrack_InsertControlChange.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,)
# トラックにRPNチェンジイベントを生成して挿入
#MIDITrack_InsertRPNChange = MIDIDataDLL.MIDITrack_InsertRPNChange
#MIDITrack_InsertRPNChange.restype = c_void_p
#MIDITrack_InsertRPNChange.argtypes = (c_void_p,)
# トラックにNRPNチェンジイベントを生成して挿入
#MIDITrack_InsertNRPNChange = MIDIDataDLL.MIDITrack_InsertNRPNChange
#MIDITrack_InsertNRPNChange.restype = c_void_p
#MIDITrack_InsertNRPNChange.argtypes = (c_void_p,)
# トラックにプログラムチェンジイベントを生成して挿入
MIDITrack_InsertProgramChange = MIDIDataDLL.MIDITrack_InsertProgramChange
MIDITrack_InsertProgramChange.restype = c_bool
MIDITrack_InsertProgramChange.argtypes = (c_void_p,c_uint,c_uint,c_uint,)
# トラックにパッチチェンジイベントを生成して挿入
#MIDITrack_InsertPatchChange = MIDIDataDLL.MIDITrack_InsertPatchChange
#MIDITrack_InsertPatchChange.restype = c_void_p
#MIDITrack_InsertPatchChange.argtypes = (c_void_p,)
# トラックにチャンネルアフターイベントを生成して挿入
MIDITrack_InsertChannelAftertouch = MIDIDataDLL.MIDITrack_InsertChannelAftertouch
MIDITrack_InsertChannelAftertouch.restype = c_bool
MIDITrack_InsertChannelAftertouch.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,)
# トラックにピッチベンドイベントを生成して挿入
MIDITrack_InsertPitchBend = MIDIDataDLL.MIDITrack_InsertPitchBend
MIDITrack_InsertPitchBend.restype = c_bool
MIDITrack_InsertPitchBend.argtypes = (c_void_p,c_uint,c_uint,c_uint,)
# トラックにシステムエクスクルーシヴイベントを生成して挿入
MIDITrack_InsertSysExEvent = MIDIDataDLL.MIDITrack_InsertSysExEvent
MIDITrack_InsertSysExEvent.restype = c_bool
MIDITrack_InsertSysExEvent.argtypes = (c_void_p,c_uint,c_wchar_p,c_uint,)
# トラックからイベントを1つ取り除く(イベントオブジェクトは削除しません)
MIDITrack_RemoveSingleEvent = MIDIDataDLL.MIDITrack_RemoveSingleEvent
MIDITrack_RemoveSingleEvent.restype = c_bool
MIDITrack_RemoveSingleEvent.argtypes = (c_void_p,c_void_p,)
# トラックからイベントを取り除く(イベントオブジェクトは削除しません)
MIDITrack_RemoveEvent = MIDIDataDLL.MIDITrack_RemoveEvent
MIDITrack_RemoveEvent.restype = c_uint
MIDITrack_RemoveEvent.argtypes = (c_void_p,c_void_p,)
# MIDIトラックが浮遊トラックであるかどうかを調べる
MIDITrack_IsFloating = MIDIDataDLL.MIDITrack_IsFloating
MIDITrack_IsFloating.restype = c_bool
MIDITrack_IsFloating.argtypes = (c_void_p,)
# MIDIトラックがセットアップトラックとして正しいことを確認する
MIDITrack_CheckSetupTrack = MIDIDataDLL.MIDITrack_CheckSetupTrack
MIDITrack_CheckSetupTrack.restype = c_bool
MIDITrack_CheckSetupTrack.argtypes = (c_void_p,)
# MIDIトラックがノンセットアップトラックとして正しいことを確認する
MIDITrack_CheckNonSetupTrack = MIDIDataDLL.MIDITrack_CheckNonSetupTrack
MIDITrack_CheckNonSetupTrack.restype = c_bool
MIDITrack_CheckNonSetupTrack.argtypes = (c_void_p,)
# タイムコードをミリ秒時刻に変換(指定トラック内のテンポイベントを基に計算)
MIDITrack_TimeToMillisec = MIDIDataDLL.MIDITrack_TimeToMillisec
MIDITrack_TimeToMillisec.restype = c_uint
MIDITrack_TimeToMillisec.argtypes = (c_void_p,c_uint,)
# ミリ秒時刻をタイムコードに変換(指定トラック内のテンポイベントを基に計算)
MIDITrack_MillisecToTime = MIDIDataDLL.MIDITrack_MillisecToTime
MIDITrack_MillisecToTime.restype = c_uint
MIDITrack_MillisecToTime.argtypes = (c_void_p,c_uint,)
# タイムコードを小節：拍：ティックに分解(指定トラック内の拍子記号を基に計算)
MIDITrack_BreakTimeEx = MIDIDataDLL.MIDITrack_BreakTimeEx
MIDITrack_BreakTimeEx.restype = c_uint
MIDITrack_BreakTimeEx.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,)
# タイムコードを小節：拍：ティックに分解(指定トラック内の拍子記号を基に計算)
MIDITrack_BreakTime = MIDIDataDLL.MIDITrack_BreakTime
MIDITrack_BreakTime.restype = c_uint
MIDITrack_BreakTime.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,c_void_p,)
# 小節：拍：ティックからタイムコードを生成(指定トラック内の拍子記号を基に計算)
MIDITrack_MakeTimeEx = MIDIDataDLL.MIDITrack_MakeTimeEx
MIDITrack_MakeTimeEx.restype = c_uint
MIDITrack_MakeTimeEx.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,)
# 小節：拍：ティックからタイムコードを生成(指定トラック内の拍子記号を基に計算)
MIDITrack_MakeTime = MIDIDataDLL.MIDITrack_MakeTime
MIDITrack_MakeTime.restype = c_uint
MIDITrack_MakeTime.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,c_void_p,c_void_p,)
# 指定位置におけるテンポを取得
MIDITrack_FindTempo = MIDIDataDLL.MIDITrack_FindTempo
MIDITrack_FindTempo.restype = c_uint
MIDITrack_FindTempo.argtypes = (c_void_p,c_uint,c_void_p,)
# 指定位置における拍子記号を取得
MIDITrack_FindTimeSignature = MIDIDataDLL.MIDITrack_FindTimeSignature
MIDITrack_FindTimeSignature.restype = c_uint
MIDITrack_FindTimeSignature.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,c_void_p,c_void_p,)
# 指定位置における調性記号を取得
MIDITrack_FindKeySignature = MIDIDataDLL.MIDITrack_FindKeySignature
MIDITrack_FindKeySignature.restype = c_uint
MIDITrack_FindKeySignature.argtypes = (c_void_p,c_uint,c_void_p,c_void_p,)

#　MIDIEventクラス関数
# 結合イベントの最初のイベントを返す。 */
# 結合イベントでない場合、pEvent自身を返す。*/
MIDIEvent_GetFirstCombinedEvent = MIDIDataDLL.MIDIEvent_GetFirstCombinedEvent
MIDIEvent_GetFirstCombinedEvent.restype = c_void_p
MIDIEvent_GetFirstCombinedEvent.argtypes = (c_void_p,)
# 結合イベントの最後のイベントを返す。 */
# 結合イベントでない場合、pEvent自身を返す。*/
MIDIEvent_GetLastCombinedEvent = MIDIDataDLL.MIDIEvent_GetLastCombinedEvent
MIDIEvent_GetLastCombinedEvent.restype = c_void_p
MIDIEvent_GetLastCombinedEvent.argtypes = (c_void_p,)
# 単体イベントを結合する */
MIDIEvent_Combine = MIDIDataDLL.MIDIEvent_Combine
MIDIEvent_Combine.restype = c_uint
MIDIEvent_Combine.argtypes = (c_void_p,)
# 結合イベントを切り離す */
MIDIEvent_Chop = MIDIDataDLL.MIDIEvent_Chop
MIDIEvent_Chop.restype = c_void_p
MIDIEvent_Chop.argtypes = (c_void_p,)
# MIDIイベントの削除(結合している場合でも単一のMIDIイベントを削除) */
MIDIEvent_DeleteSingle = MIDIDataDLL.MIDIEvent_DeleteSingle
MIDIEvent_DeleteSingle.restype = c_void_p
MIDIEvent_DeleteSingle.argtypes = (c_void_p,)
# MIDIイベントの削除(結合している場合、結合しているMIDIイベントも削除) */
MIDIEvent_Delete = MIDIDataDLL.MIDIEvent_Delete
MIDIEvent_Delete.restype = c_uint
MIDIEvent_Delete.argtypes = (c_void_p,)
# MIDIイベント(任意)を生成し、MIDIイベントへのポインタを返す(失敗時NULL、以下同様) */
#MIDIEvent_Create = MIDIDataDLL.MIDIEvent_Create
#MIDIEvent_Create.restype = c_void_p
#MIDIEvent_Create.argtypes = (c_void_p,)
# 指定イベントと同じMIDIイベントを生成し、MIDIイベントへのポインタを返す(失敗時NULL、以下同様) */
MIDIEvent_CreateClone = MIDIDataDLL.MIDIEvent_CreateClone
MIDIEvent_CreateClone.restype = c_void_p
MIDIEvent_CreateClone.argtypes = (c_void_p,)
# シーケンス番号イベントの生成 */
MIDIEvent_CreateSequenceNumber = MIDIDataDLL.MIDIEvent_CreateSequenceNumber
MIDIEvent_CreateSequenceNumber.restype = c_void_p
MIDIEvent_CreateSequenceNumber.argtypes = (c_uint,c_uint,)
# テキストベースのイベントの生成 */
MIDIEvent_CreateTextBasedEvent = MIDIDataDLL.MIDIEvent_CreateTextBasedEventW
MIDIEvent_CreateTextBasedEvent.restype = c_void_p
MIDIEvent_CreateTextBasedEvent.argtypes = (c_uint,c_uint,c_wchar_p,)
# テキストベースのイベントの生成(文字コード指定あり) */
MIDIEvent_CreateTextBasedEventEx = MIDIDataDLL.MIDIEvent_CreateTextBasedEventExW
MIDIEvent_CreateTextBasedEventEx.restype = c_void_p
MIDIEvent_CreateTextBasedEventEx.argtypes = (c_uint,c_uint,c_uint,c_wchar_p,)
# テキストイベントの生成 */
MIDIEvent_CreateTextEvent = MIDIDataDLL.MIDIEvent_CreateTextEventW
MIDIEvent_CreateTextEvent.restype = c_void_p
MIDIEvent_CreateTextEvent.argtypes = (c_uint,c_wchar_p,)
# テキストイベントの生成(文字コード指定あり) */
MIDIEvent_CreateTextEventEx = MIDIDataDLL.MIDIEvent_CreateTextEventExW
MIDIEvent_CreateTextEventEx.restype = c_void_p
MIDIEvent_CreateTextEventEx.argtypes = (c_uint,c_uint,c_wchar_p,)
# 著作権イベントの生成 */
MIDIEvent_CreateCopyrightNotice = MIDIDataDLL.MIDIEvent_CreateCopyrightNoticeW
MIDIEvent_CreateCopyrightNotice.restype = c_void_p
MIDIEvent_CreateCopyrightNotice.argtypes = (c_uint,c_wchar_p,)
# 著作権イベントの生成(文字コード指定あり) */
MIDIEvent_CreateCopyrightNoticeEx = MIDIDataDLL.MIDIEvent_CreateCopyrightNoticeExW
MIDIEvent_CreateCopyrightNoticeEx.restype = c_void_p
MIDIEvent_CreateCopyrightNoticeEx.argtypes = (c_uint,c_void_p,c_wchar_p,)
# トラック名イベントの生成 */
MIDIEvent_CreateTrackName = MIDIDataDLL.MIDIEvent_CreateTrackNameW
MIDIEvent_CreateTrackName.restype = c_void_p
MIDIEvent_CreateTrackName.argtypes = (c_uint,c_wchar_p,)
# トラック名イベントの生成(文字コード指定あり) */
MIDIEvent_CreateTrackNameEx = MIDIDataDLL.MIDIEvent_CreateTrackNameExW
MIDIEvent_CreateTrackNameEx.restype = c_void_p
MIDIEvent_CreateTrackNameEx.argtypes = (c_uint,c_uint,c_wchar_p,)
# インストゥルメント名イベントの生成 */
MIDIEvent_CreateInstrumentName = MIDIDataDLL.MIDIEvent_CreateInstrumentNameW
MIDIEvent_CreateInstrumentName.restype = c_void_p
MIDIEvent_CreateInstrumentName.argtypes = (c_uint,c_wchar_p,)
# インストゥルメント名イベントの生成(文字コード指定あり) */
MIDIEvent_CreateInstrumentNameEx = MIDIDataDLL.MIDIEvent_CreateInstrumentNameExW
MIDIEvent_CreateInstrumentNameEx.restype = c_void_p
MIDIEvent_CreateInstrumentNameEx.argtypes = (c_uint,c_uint,c_wchar_p,)
# 歌詞イベントの生成 */
MIDIEvent_CreateLyric = MIDIDataDLL.MIDIEvent_CreateLyricW
MIDIEvent_CreateLyric.restype = c_void_p
MIDIEvent_CreateLyric.argtypes = (c_uint,c_wchar_p,)
# 歌詞イベントの生成(文字コード指定あり) */
MIDIEvent_CreateLyricEx = MIDIDataDLL.MIDIEvent_CreateLyricExW
MIDIEvent_CreateLyricEx.restype = c_void_p
MIDIEvent_CreateLyricEx.argtypes = (c_uint,c_void_p,c_wchar_p,)
# マーカーイベントの生成 */
MIDIEvent_CreateMarker = MIDIDataDLL.MIDIEvent_CreateMarkerW
MIDIEvent_CreateMarker.restype = c_void_p
MIDIEvent_CreateMarker.argtypes = (c_uint,c_wchar_p,)
# マーカーイベントの生成(文字コード指定あり) */
MIDIEvent_CreateMarkerEx = MIDIDataDLL.MIDIEvent_CreateMarkerExW
MIDIEvent_CreateMarkerEx.restype = c_void_p
MIDIEvent_CreateMarkerEx.argtypes = (c_uint,c_uint,c_wchar_p,)
# キューポイントイベントの生成 */
MIDIEvent_CreateCuePoint = MIDIDataDLL.MIDIEvent_CreateCuePointW
MIDIEvent_CreateCuePoint.restype = c_void_p
MIDIEvent_CreateCuePoint.argtypes = (c_uint,c_wchar_p,)
# キューポイントイベントの生成(文字コード指定あり) */
#MIDIEvent_CreateCuePointEx = MIDIDataDLL.MIDIEvent_CreateCuePointExW
#MIDIEvent_CreateCuePointEx.restype = c_void_p
#MIDIEvent_CreateCuePointEx.argtypes = (c_void_p,c_void_p,c_wchar_p,)
# プログラム名イベントの生成 */
MIDIEvent_CreateProgramName = MIDIDataDLL.MIDIEvent_CreateProgramNameW
MIDIEvent_CreateProgramName.restype = c_void_p
MIDIEvent_CreateProgramName.argtypes = (c_uint,c_wchar_p,)
# プログラム名イベントの生成(文字コード指定あり) */
MIDIEvent_CreateProgramNameEx = MIDIDataDLL.MIDIEvent_CreateProgramNameExW
MIDIEvent_CreateProgramNameEx.restype = c_void_p
MIDIEvent_CreateProgramNameEx.argtypes = (c_uint,c_uint,c_wchar_p,)
# デバイス名イベント生成 */
MIDIEvent_CreateDeviceName = MIDIDataDLL.MIDIEvent_CreateDeviceNameW
MIDIEvent_CreateDeviceName.restype = c_void_p
MIDIEvent_CreateDeviceName.argtypes = (c_uint,c_wchar_p,)
# デバイス名イベント生成(文字コード指定あり) */
MIDIEvent_CreateDeviceNameEx = MIDIDataDLL.MIDIEvent_CreateDeviceNameExW
MIDIEvent_CreateDeviceNameEx.restype = c_void_p
MIDIEvent_CreateDeviceNameEx.argtypes = (c_uint,c_uint,c_wchar_p,)
# チャンネルプレフィックスイベントの生成 */
MIDIEvent_CreateChannelPrefix = MIDIDataDLL.MIDIEvent_CreateChannelPrefix
MIDIEvent_CreateChannelPrefix.restype = c_void_p
MIDIEvent_CreateChannelPrefix.argtypes = (c_uint,c_void_p,)
# ポートプレフィックスイベントの生成 */
MIDIEvent_CreatePortPrefix = MIDIDataDLL.MIDIEvent_CreatePortPrefix
MIDIEvent_CreatePortPrefix.restype = c_void_p
MIDIEvent_CreatePortPrefix.argtypes = (c_uint,c_void_p,)
# エンドオブトラックイベントの生成 */
MIDIEvent_CreateEndofTrack = MIDIDataDLL.MIDIEvent_CreateEndofTrack
MIDIEvent_CreateEndofTrack.restype = c_void_p
MIDIEvent_CreateEndofTrack.argtypes = (c_uint,)
# テンポイベントの生成 */
MIDIEvent_CreateTempo = MIDIDataDLL.MIDIEvent_CreateTempo
MIDIEvent_CreateTempo.restype = c_void_p
MIDIEvent_CreateTempo.argtypes = (c_uint,c_uint,)
# SMPTEオフセットイベントの生成 */
MIDIEvent_CreateSMPTEOffset = MIDIDataDLL.MIDIEvent_CreateSMPTEOffset
MIDIEvent_CreateSMPTEOffset.restype = c_void_p
MIDIEvent_CreateSMPTEOffset.argtypes = (c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,)
# 拍子記号イベントの生成 */
MIDIEvent_CreateTimeSignature = MIDIDataDLL.MIDIEvent_CreateTimeSignature
MIDIEvent_CreateTimeSignature.restype = c_void_p
MIDIEvent_CreateTimeSignature.argtypes = (c_uint,c_uint,c_uint,c_uint,c_uint,)
# 調性記号イベントの生成 */
MIDIEvent_CreateKeySignature = MIDIDataDLL.MIDIEvent_CreateKeySignature
MIDIEvent_CreateKeySignature.restype = c_void_p
MIDIEvent_CreateKeySignature.argtypes = (c_uint,c_uint,c_uint,)
# シーケンサー独自のイベントの生成 */
#MIDIEvent_CreateSequencerSpecific = MIDIDataDLL.MIDIEvent_CreateSequencerSpecific
#MIDIEvent_CreateSequencerSpecific.restype = c_void_p
#MIDIEvent_CreateSequencerSpecific.argtypes = (c_void_p,)
# ノートオフイベントの生成 */
MIDIEvent_CreateNoteOff = MIDIDataDLL.MIDIEvent_CreateNoteOff
MIDIEvent_CreateNoteOff.restype = c_void_p
MIDIEvent_CreateNoteOff.argtypes = (c_uint,c_uint,c_uint,c_uint,)
# ノートオンイベントの生成 */
MIDIEvent_CreateNoteOn = MIDIDataDLL.MIDIEvent_CreateNoteOn
MIDIEvent_CreateNoteOn.restype = c_void_p
MIDIEvent_CreateNoteOn.argtypes = (c_uint,c_uint,c_uint,c_uint,)
# ノートイベントの生成(MIDIEvent_CreateNoteOnNoteOn0と同じ) */
# (ノートオン・ノートオン(0x9n(vel==0))の2イベントを生成し、*/
# ノートオンイベントへのポインタを返す。) */
MIDIEvent_CreateNote = MIDIDataDLL.MIDIEvent_CreateNote
MIDIEvent_CreateNote.restype = c_void_p
MIDIEvent_CreateNote.argtypes = (c_uint,c_uint,c_uint,c_uint,c_uint,)
# ノートイベントの生成(0x8n離鍵型) */
# (ノートオン(0x9n)・ノートオフ(0x8n)の2イベントを生成し、*/
# NoteOnへのポインタを返す) */
MIDIEvent_CreateNoteOnNoteOff = MIDIDataDLL.MIDIEvent_CreateNoteOnNoteOff
MIDIEvent_CreateNoteOnNoteOff.restype = c_void_p
MIDIEvent_CreateNoteOnNoteOff.argtypes = (c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,)
# ノートイベントの生成(0x9n離鍵型) */
# (ノートオン(0x9n)・ノートオン(0x9n(vel==0))の2イベントを生成し、*/
# NoteOnへのポインタを返す) */
MIDIEvent_CreateNoteOnNoteOn0 = MIDIDataDLL.MIDIEvent_CreateNoteOnNoteOn0
MIDIEvent_CreateNoteOnNoteOn0.restype = c_void_p
MIDIEvent_CreateNoteOnNoteOn0.argtypes = (c_uint,c_uint,c_uint,c_uint,c_uint,)
# キーアフタータッチイベントの生成 */
MIDIEvent_CreateKeyAftertouch = MIDIDataDLL.MIDIEvent_CreateKeyAftertouch
MIDIEvent_CreateKeyAftertouch.restype = c_void_p
MIDIEvent_CreateKeyAftertouch.argtypes = (c_uint,c_uint,c_uint,c_uint,)
# コントローラーイベントの生成 */
MIDIEvent_CreateControlChange = MIDIDataDLL.MIDIEvent_CreateControlChange
MIDIEvent_CreateControlChange.restype = c_void_p
MIDIEvent_CreateControlChange.argtypes = (c_uint,c_uint,c_uint,c_uint,)
# RPNイベントの生成 */
# (CC#101+CC#100+CC#6の3イベントを生成し、CC#101へのポインタを返す) */
MIDIEvent_CreateRPNChange = MIDIDataDLL.MIDIEvent_CreateRPNChange
MIDIEvent_CreateRPNChange.restype = c_void_p
MIDIEvent_CreateRPNChange.argtypes = (c_uint,c_uint,c_uint,c_uint,c_uint,)
# NRPNイベントの生成 */
# (CC#99+CC#98+CC#6の3イベントを生成し、CC#99へのポインタを返す) */
MIDIEvent_CreateNRPNChange = MIDIDataDLL.MIDIEvent_CreateNRPNChange
MIDIEvent_CreateNRPNChange.restype = c_void_p
MIDIEvent_CreateNRPNChange.argtypes = (c_uint,c_uint,c_uint,c_uint,c_uint,)
# プログラムチェンジイベントの生成 */
MIDIEvent_CreateProgramChange = MIDIDataDLL.MIDIEvent_CreateProgramChange
MIDIEvent_CreateProgramChange.restype = c_void_p
MIDIEvent_CreateProgramChange.argtypes = (c_uint,c_uint,c_uint,)
# バンク・パッチイベントの生成 */
# (CC#0+CC#32+PCの3イベントを生成し、CC#0へのポインタを返す) */
MIDIEvent_CreatePatchChange = MIDIDataDLL.MIDIEvent_CreatePatchChange
MIDIEvent_CreatePatchChange.restype = c_void_p
MIDIEvent_CreatePatchChange.argtypes = (c_uint,c_uint,c_uint,c_uint,c_uint,)
# チャンネルアフタータッチイベントの生成 */
MIDIEvent_CreateChannelAftertouch = MIDIDataDLL.MIDIEvent_CreateChannelAftertouch
MIDIEvent_CreateChannelAftertouch.restype = c_void_p
MIDIEvent_CreateChannelAftertouch.argtypes = (c_uint,c_uint,c_uint,)
# ピッチベンドイベントの生成 */
MIDIEvent_CreatePitchBend = MIDIDataDLL.MIDIEvent_CreatePitchBend
MIDIEvent_CreatePitchBend.restype = c_void_p
MIDIEvent_CreatePitchBend.argtypes = (c_uint,c_uint,c_uint,)
# システムエクスクルーシヴイベントの生成 */
#MIDIEvent_CreateSysExEvent = MIDIDataDLL.MIDIEvent_CreateSysExEvent
#MIDIEvent_CreateSysExEvent.restype = c_void_p
#MIDIEvent_CreateSysExEvent.argtypes = (c_void_p,)
# メタイベントであるかどうかを調べる */
MIDIEvent_IsMetaEvent = MIDIDataDLL.MIDIEvent_IsMetaEvent
MIDIEvent_IsMetaEvent.restype = c_bool
MIDIEvent_IsMetaEvent.argtypes = (c_void_p,)
# シーケンス番号であるかどうかを調べる */
MIDIEvent_IsSequenceNumber = MIDIDataDLL.MIDIEvent_IsSequenceNumber
MIDIEvent_IsSequenceNumber.restype = c_bool
MIDIEvent_IsSequenceNumber.argtypes = (c_void_p,)
# テキストイベントであるかどうかを調べる */
MIDIEvent_IsTextEvent = MIDIDataDLL.MIDIEvent_IsTextEvent
MIDIEvent_IsTextEvent.restype = c_bool
MIDIEvent_IsTextEvent.argtypes = (c_void_p,)
# 著作権イベントであるかどうかを調べる */
MIDIEvent_IsCopyrightNotice = MIDIDataDLL.MIDIEvent_IsCopyrightNotice
MIDIEvent_IsCopyrightNotice.restype = c_bool
MIDIEvent_IsCopyrightNotice.argtypes = (c_void_p,)
# トラック名イベントであるかどうかを調べる */
MIDIEvent_IsTrackName = MIDIDataDLL.MIDIEvent_IsTrackName
MIDIEvent_IsTrackName.restype = c_bool
MIDIEvent_IsTrackName.argtypes = (c_void_p,)
# インストゥルメント名イベントであるかどうかを調べる */
MIDIEvent_IsInstrumentName = MIDIDataDLL.MIDIEvent_IsInstrumentName
MIDIEvent_IsInstrumentName.restype = c_bool
MIDIEvent_IsInstrumentName.argtypes = (c_void_p,)
# 歌詞イベントであるかどうかを調べる */
MIDIEvent_IsLyric = MIDIDataDLL.MIDIEvent_IsLyric
MIDIEvent_IsLyric.restype = c_bool
MIDIEvent_IsLyric.argtypes = (c_void_p,)
# マーカーイベントであるかどうかを調べる */
MIDIEvent_IsMarker = MIDIDataDLL.MIDIEvent_IsMarker
MIDIEvent_IsMarker.restype = c_bool
MIDIEvent_IsMarker.argtypes = (c_void_p,)
# キューポイントイベントであるかどうかを調べる */
MIDIEvent_IsCuePoint = MIDIDataDLL.MIDIEvent_IsCuePoint
MIDIEvent_IsCuePoint.restype = c_bool
MIDIEvent_IsCuePoint.argtypes = (c_void_p,)
# プログラム名イベントであるかどうかを調べる */
MIDIEvent_IsProgramName = MIDIDataDLL.MIDIEvent_IsProgramName
MIDIEvent_IsProgramName.restype = c_bool
MIDIEvent_IsProgramName.argtypes = (c_void_p,)
# デバイス名イベントであるかどうかを調べる */
MIDIEvent_IsDeviceName = MIDIDataDLL.MIDIEvent_IsDeviceName
MIDIEvent_IsDeviceName.restype = c_bool
MIDIEvent_IsDeviceName.argtypes = (c_void_p,)
# チャンネルプレフィックスイベントであるかどうかを調べる */
MIDIEvent_IsChannelPrefix = MIDIDataDLL.MIDIEvent_IsChannelPrefix
MIDIEvent_IsChannelPrefix.restype = c_bool
MIDIEvent_IsChannelPrefix.argtypes = (c_void_p,)
# ポートプレフィックスイベントであるかどうかを調べる */
MIDIEvent_IsPortPrefix = MIDIDataDLL.MIDIEvent_IsPortPrefix
MIDIEvent_IsPortPrefix.restype = c_bool
MIDIEvent_IsPortPrefix.argtypes = (c_void_p,)
# エンドオブトラックイベントであるかどうかを調べる */
MIDIEvent_IsEndofTrack = MIDIDataDLL.MIDIEvent_IsEndofTrack
MIDIEvent_IsEndofTrack.restype = c_bool
MIDIEvent_IsEndofTrack.argtypes = (c_void_p,)
# テンポイベントであるかどうかを調べる */
MIDIEvent_IsTempo = MIDIDataDLL.MIDIEvent_IsTempo
MIDIEvent_IsTempo.restype = c_bool
MIDIEvent_IsTempo.argtypes = (c_void_p,)
# SMPTEオフセットイベントであるかどうかを調べる */
MIDIEvent_IsSMPTEOffset = MIDIDataDLL.MIDIEvent_IsSMPTEOffset
MIDIEvent_IsSMPTEOffset.restype = c_bool
MIDIEvent_IsSMPTEOffset.argtypes = (c_void_p,)
# 拍子記号イベントであるかどうかを調べる */
MIDIEvent_IsTimeSignature = MIDIDataDLL.MIDIEvent_IsTimeSignature
MIDIEvent_IsTimeSignature.restype = c_bool
MIDIEvent_IsTimeSignature.argtypes = (c_void_p,)
# 調性記号イベントであるかどうかを調べる */
MIDIEvent_IsKeySignature = MIDIDataDLL.MIDIEvent_IsKeySignature
MIDIEvent_IsKeySignature.restype = c_bool
MIDIEvent_IsKeySignature.argtypes = (c_void_p,)
# シーケンサ独自のイベントであるかどうかを調べる */
MIDIEvent_IsSequencerSpecific = MIDIDataDLL.MIDIEvent_IsSequencerSpecific
MIDIEvent_IsSequencerSpecific.restype = c_bool
MIDIEvent_IsSequencerSpecific.argtypes = (c_void_p,)
# MIDIイベントであるかどうかを調べる */
MIDIEvent_IsMIDIEvent = MIDIDataDLL.MIDIEvent_IsMIDIEvent
MIDIEvent_IsMIDIEvent.restype = c_bool
MIDIEvent_IsMIDIEvent.argtypes = (c_void_p,)
# ノートオンイベントであるかどうかを調べる */
# (ノートオンイベントでベロシティ0のものはノートオフイベントとみなす。以下同様) */
MIDIEvent_IsNoteOn = MIDIDataDLL.MIDIEvent_IsNoteOn
MIDIEvent_IsNoteOn.restype = c_bool
MIDIEvent_IsNoteOn.argtypes = (c_void_p,)
# ノートオフイベントであるかどうかを調べる */
MIDIEvent_IsNoteOff = MIDIDataDLL.MIDIEvent_IsNoteOff
MIDIEvent_IsNoteOff.restype = c_bool
MIDIEvent_IsNoteOff.argtypes = (c_void_p,)
# ノートイベントであるかどうかを調べる */
MIDIEvent_IsNote = MIDIDataDLL.MIDIEvent_IsNote
MIDIEvent_IsNote.restype = c_bool
MIDIEvent_IsNote.argtypes = (c_void_p,)
# NOTEONOTEOFFイベントであるかどうかを調べる */
# これはノートオン(0x9n)とノートオフ(0x8n)が結合イベントしたイベントでなければならない。 */
MIDIEvent_IsNoteOnNoteOff = MIDIDataDLL.MIDIEvent_IsNoteOnNoteOff
MIDIEvent_IsNoteOnNoteOff.restype = c_bool
MIDIEvent_IsNoteOnNoteOff.argtypes = (c_void_p,)
# NOTEONNOTEON0イベントであるかどうかを調べる */
# これはノートオン(0x9n)とノートオフ(0x9n,vel==0)が結合イベントしたイベントでなければならない。 */
MIDIEvent_IsNoteOnNoteOn0 = MIDIDataDLL.MIDIEvent_IsNoteOnNoteOn0
MIDIEvent_IsNoteOnNoteOn0.restype = c_bool
MIDIEvent_IsNoteOnNoteOn0.argtypes = (c_void_p,)
# キーアフタータッチイベントであるかどうかを調べる */
MIDIEvent_IsKeyAftertouch = MIDIDataDLL.MIDIEvent_IsKeyAftertouch
MIDIEvent_IsKeyAftertouch.restype = c_bool
MIDIEvent_IsKeyAftertouch.argtypes = (c_void_p,)
# コントロールチェンジイベントであるかどうかを調べる */
MIDIEvent_IsControlChange = MIDIDataDLL.MIDIEvent_IsControlChange
MIDIEvent_IsControlChange.restype = c_bool
MIDIEvent_IsControlChange.argtypes = (c_void_p,)
# RPNチェンジイベントであるかどうかを調べる */
MIDIEvent_IsRPNChange = MIDIDataDLL.MIDIEvent_IsRPNChange
MIDIEvent_IsRPNChange.restype = c_bool
MIDIEvent_IsRPNChange.argtypes = (c_void_p,)
# NRPNチェンジイベントであるかどうかを調べる */
MIDIEvent_IsNRPNChange = MIDIDataDLL.MIDIEvent_IsNRPNChange
MIDIEvent_IsNRPNChange.restype = c_bool
MIDIEvent_IsNRPNChange.argtypes = (c_void_p,)
# プログラムチェンジイベントであるかどうかを調べる */
MIDIEvent_IsProgramChange = MIDIDataDLL.MIDIEvent_IsProgramChange
MIDIEvent_IsProgramChange.restype = c_bool
MIDIEvent_IsProgramChange.argtypes = (c_void_p,)
# パッチチェンジイベントであるかどうかを調べる */
MIDIEvent_IsPatchChange = MIDIDataDLL.MIDIEvent_IsPatchChange
MIDIEvent_IsPatchChange.restype = c_bool
MIDIEvent_IsPatchChange.argtypes = (c_void_p,)
# チャンネルアフタータッチイベントであるかどうかを調べる */
MIDIEvent_IsChannelAftertouch = MIDIDataDLL.MIDIEvent_IsChannelAftertouch
MIDIEvent_IsChannelAftertouch.restype = c_bool
MIDIEvent_IsChannelAftertouch.argtypes = (c_void_p,)
# ピッチベンドイベントであるかどうかを調べる */
MIDIEvent_IsPitchBend = MIDIDataDLL.MIDIEvent_IsPitchBend
MIDIEvent_IsPitchBend.restype = c_bool
MIDIEvent_IsPitchBend.argtypes = (c_void_p,)
# システムエクスクルーシヴイベントであるかどうかを調べる */
MIDIEvent_IsSysExEvent = MIDIDataDLL.MIDIEvent_IsSysExEvent
MIDIEvent_IsSysExEvent.restype = c_bool
MIDIEvent_IsSysExEvent.argtypes = (c_void_p,)
# 浮遊イベントであるかどうか調べる */
MIDIEvent_IsFloating = MIDIDataDLL.MIDIEvent_IsFloating
MIDIEvent_IsFloating.restype = c_bool
MIDIEvent_IsFloating.argtypes = (c_void_p,)
# 結合イベントであるかどうか調べる */
MIDIEvent_IsCombined = MIDIDataDLL.MIDIEvent_IsCombined
MIDIEvent_IsCombined.restype = c_bool
MIDIEvent_IsCombined.argtypes = (c_void_p,)
# イベントの種類を取得 */
MIDIEvent_GetKind = MIDIDataDLL.MIDIEvent_GetKind
MIDIEvent_GetKind.restype = c_uint
MIDIEvent_GetKind.argtypes = (c_void_p,)
# イベントの種類を設定 */
#MIDIEvent_SetKind = MIDIDataDLL.MIDIEvent_SetKind
#MIDIEvent_SetKind.restype = c_void_p
#MIDIEvent_SetKind.argtypes = (c_void_p,)
# イベントの長さ取得 */
MIDIEvent_GetLen = MIDIDataDLL.MIDIEvent_GetLen
MIDIEvent_GetLen.restype = c_void_p
MIDIEvent_GetLen.argtypes = (c_void_p,)
# イベントのデータ部を取得 */
MIDIEvent_GetData = MIDIDataDLL.MIDIEvent_GetData
MIDIEvent_GetData.restype = c_uint
MIDIEvent_GetData.argtypes = (c_void_p,c_wchar_p,c_uint,)
# イベントのデータ部を設定(この関数は大変危険です。整合性のチェキはしません) */
#MIDIEvent_SetData = MIDIDataDLL.MIDIEvent_SetData
#MIDIEvent_SetData.restype = c_void_p
#MIDIEvent_SetData.argtypes = (c_void_p,)
# イベントの文字コードを取得(テキスト・著作権・トラック名・インストゥルメント名・ */
# 歌詞・マーカー・キューポイント・プログラム名・デバイス名のみ) */
#MIDIEvent_GetCharCode = MIDIDataDLL.MIDIEvent_GetCharCode
#MIDIEvent_GetCharCode.restype = c_void_p
#MIDIEvent_GetCharCode.argtypes = (c_void_p,)
# イベントの文字コードを設定(テキスト・著作権・トラック名・インストゥルメント名・ */
# 歌詞・マーカー・キューポイント・プログラム名・デバイス名のみ) */
#MIDIEvent_SetCharCode = MIDIDataDLL.MIDIEvent_SetCharCode
#MIDIEvent_SetCharCode.restype = c_void_p
#MIDIEvent_SetCharCode.argtypes = (c_void_p,)
# イベントのテキストを取得(テキスト・著作権・トラック名・インストゥルメント名・ */
# 歌詞・マーカー・キューポイント・プログラム名・デバイス名のみ) */
#MIDIEvent_GetText = MIDIDataDLL.MIDIEvent_GetTextW
#MIDIEvent_GetText.restype = c_void_p
#MIDIEvent_GetText.argtypes = (c_void_p,)
# イベントのテキストを設定(テキスト・著作権・トラック名・インストゥルメント名・ */
# 歌詞・マーカー・キューポイント・プログラム名・デバイス名のみ) */
#MIDIEvent_SetText = MIDIDataDLL.MIDIEvent_SetTextW
#MIDIEvent_SetText.restype = c_void_p
#MIDIEvent_SetText.argtypes = (c_void_p,)
# SMPTEオフセットの取得(SMPTEオフセットイベントのみ) */
#MIDIEvent_GetSMPTEOffset = MIDIDataDLL.MIDIEvent_GetSMPTEOffset
#MIDIEvent_GetSMPTEOffset.restype = c_void_p
#MIDIEvent_GetSMPTEOffset.argtypes = (c_void_p,)
# SMPTEオフセットの設定(SMPTEオフセットイベントのみ) */
#MIDIEvent_SetSMPTEOffset = MIDIDataDLL.MIDIEvent_SetSMPTEOffset
#MIDIEvent_SetSMPTEOffset.restype = c_void_p
#MIDIEvent_SetSMPTEOffset.argtypes = (c_void_p,)
# テンポ取得(テンポイベントのみ) */
MIDIEvent_GetTempo = MIDIDataDLL.MIDIEvent_GetTempo
MIDIEvent_GetTempo.restype = c_uint
MIDIEvent_GetTempo.argtypes = (c_void_p,)
# テンポ設定(テンポイベントのみ) */
MIDIEvent_SetTempo = MIDIDataDLL.MIDIEvent_SetTempo
MIDIEvent_SetTempo.restype = c_bool
MIDIEvent_SetTempo.argtypes = (c_void_p,c_uint,)
# 拍子記号取得(拍子記号イベントのみ) */
MIDIEvent_GetTimeSignature = MIDIDataDLL.MIDIEvent_GetTimeSignature
MIDIEvent_GetTimeSignature.restype = c_uint
MIDIEvent_GetTimeSignature.argtypes = (c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,)
# 拍子記号の設定(拍子記号イベントのみ) */
MIDIEvent_SetTimeSignature = MIDIDataDLL.MIDIEvent_SetTimeSignature
MIDIEvent_SetTimeSignature.restype = c_bool
MIDIEvent_SetTimeSignature.argtypes = (c_void_p,c_uint,c_uint,c_uint,c_uint,)
# 調性記号の取得(調性記号イベントのみ) */
MIDIEvent_GetKeySignature = MIDIDataDLL.MIDIEvent_GetKeySignature
MIDIEvent_GetKeySignature.restype = c_uint
MIDIEvent_GetKeySignature.argtypes = (c_void_p,c_void_p,c_void_p,)
# 調性記号の設定(調性記号イベントのみ) */
MIDIEvent_SetKeySignature = MIDIDataDLL.MIDIEvent_SetKeySignature
MIDIEvent_SetKeySignature.restype = c_bool
MIDIEvent_SetKeySignature.argtypes = (c_void_p,c_uint,c_uint,)
# イベントのメッセージ取得(MIDIチャンネルイベント及びシステムエクスクルーシヴのみ) */
#MIDIEvent_GetMIDIMessage = MIDIDataDLL.MIDIEvent_GetMIDIMessage
#MIDIEvent_GetMIDIMessage.restype = c_void_p
#MIDIEvent_GetMIDIMessage.argtypes = (c_void_p,)
# イベントのメッセージ設定(MIDIチャンネルイベント及びシステムエクスクルーシヴのみ) */
#MIDIEvent_SetMIDIMessage = MIDIDataDLL.MIDIEvent_SetMIDIMessage
#MIDIEvent_SetMIDIMessage.restype = c_void_p
#MIDIEvent_SetMIDIMessage.argtypes = (c_void_p,)
# イベントのチャンネル取得(MIDIチャンネルイベントのみ) */
MIDIEvent_GetChannel = MIDIDataDLL.MIDIEvent_GetChannel
MIDIEvent_GetChannel.restype = c_uint
MIDIEvent_GetChannel.argtypes = (c_void_p,)
# イベントのチャンネル設定(MIDIチャンネルイベントのみ) */
MIDIEvent_SetChannel = MIDIDataDLL.MIDIEvent_SetChannel
MIDIEvent_SetChannel.restype = c_bool
MIDIEvent_SetChannel.argtypes = (c_void_p,c_uint,)
# イベントの時刻取得 */
MIDIEvent_GetTime = MIDIDataDLL.MIDIEvent_GetTime
MIDIEvent_GetTime.restype = c_uint
MIDIEvent_GetTime.argtypes = (c_void_p,)
# イベントの時刻設定 */
#MIDIEvent_SetTimeSingle = MIDIDataDLL.MIDIEvent_SetTimeSingle
#MIDIEvent_SetTimeSingle.restype = c_void_p
#MIDIEvent_SetTimeSingle.argtypes = (c_void_p,)
# イベントの時刻設定 */
MIDIEvent_SetTime = MIDIDataDLL.MIDIEvent_SetTime
MIDIEvent_SetTime.restype = c_uint
MIDIEvent_SetTime.argtypes = (c_void_p,c_uint,)
# イベントのキー取得(ノートオフ・ノートオン・チャンネルアフターのみ) */
MIDIEvent_GetKey = MIDIDataDLL.MIDIEvent_GetKey
MIDIEvent_GetKey.restype = c_uint
MIDIEvent_GetKey.argtypes = (c_void_p,)
# イベントのキー設定(ノートオフ・ノートオン・チャンネルアフターのみ) */
MIDIEvent_SetKey = MIDIDataDLL.MIDIEvent_SetKey
MIDIEvent_SetKey.restype = c_uint
MIDIEvent_SetKey.argtypes = (c_void_p,c_uint,)
# イベントのベロシティ取得(ノートオフ・ノートオンのみ) */
MIDIEvent_GetVelocity = MIDIDataDLL.MIDIEvent_GetVelocity
MIDIEvent_GetVelocity.restype = c_uint
MIDIEvent_GetVelocity.argtypes = (c_void_p,)
# イベントのベロシティ設定(ノートオフ・ノートオンのみ) */
MIDIEvent_SetVelocity = MIDIDataDLL.MIDIEvent_SetVelocity
MIDIEvent_SetVelocity.restype = c_bool
MIDIEvent_SetVelocity.argtypes = (c_void_p,c_uint,)
# 結合イベントの音長さ取得(ノートのみ) */
MIDIEvent_GetDuration = MIDIDataDLL.MIDIEvent_GetDuration
MIDIEvent_GetDuration.restype = c_uint
MIDIEvent_GetDuration.argtypes = (c_void_p,)
# 結合イベントの音長さ設定(ノートのみ) */
MIDIEvent_SetDuration = MIDIDataDLL.MIDIEvent_SetDuration
MIDIEvent_SetDuration.restype = c_bool
MIDIEvent_SetDuration.argtypes = (c_void_p,c_uint,)
# 結合イベントのバンク取得(RPNチェンジ・NRPNチェンジ・パッチチェンジのみ) */
MIDIEvent_GetBank = MIDIDataDLL.MIDIEvent_GetBank
MIDIEvent_GetBank.restype = c_uint
MIDIEvent_GetBank.argtypes = (c_void_p,)
# 結合イベントのバンク上位(MSB)取得(RPNチェンジ・NRPNチェンジ・パッチチェンジのみ) */
MIDIEvent_GetBankMSB = MIDIDataDLL.MIDIEvent_GetBankMSB
MIDIEvent_GetBankMSB.restype = c_uint
MIDIEvent_GetBankMSB.argtypes = (c_void_p,)
# 結合イベントのバンク下位(LSB)取得(RPNチェンジ・NRPNチェンジ・パッチチェンジのみ) */
MIDIEvent_GetBankLSB = MIDIDataDLL.MIDIEvent_GetBankLSB
MIDIEvent_GetBankLSB.restype = c_uint
MIDIEvent_GetBankLSB.argtypes = (c_void_p,)
# 結合イベントのバンク設定(RPNチェンジ・NRPNチェンジ・パッチチェンジのみ) */
MIDIEvent_SetBank = MIDIDataDLL.MIDIEvent_SetBank
MIDIEvent_SetBank.restype = c_uint
MIDIEvent_SetBank.argtypes = (c_void_p,c_uint,)
# 結合イベントのバンク上位(MSB)設定(RPNチェンジ・NRPNチェンジ・パッチチェンジのみ) */
MIDIEvent_SetBankMSB = MIDIDataDLL.MIDIEvent_SetBankMSB
MIDIEvent_SetBankMSB.restype = c_bool
MIDIEvent_SetBankMSB.argtypes = (c_void_p,c_uint,)
# 結合イベントのバンク下位(LSB)設定(RPNチェンジ・NRPNチェンジ・パッチチェンジのみ) */
MIDIEvent_SetBankLSB = MIDIDataDLL.MIDIEvent_SetBankLSB
MIDIEvent_SetBankLSB.restype = c_bool
MIDIEvent_SetBankLSB.argtypes = (c_void_p,c_uint,)
# 結合イベントのプログラムナンバーを取得(パッチイベントのみ) */
MIDIEvent_GetPatchNum = MIDIDataDLL.MIDIEvent_GetPatchNum
MIDIEvent_GetPatchNum.restype = c_uint
MIDIEvent_GetPatchNum.argtypes = (c_void_p,)
# 結合イベントのプログラムナンバーを設定(パッチイベントのみ) */
MIDIEvent_SetPatchNum = MIDIDataDLL.MIDIEvent_SetPatchNum
MIDIEvent_SetPatchNum.restype = c_bool
MIDIEvent_SetPatchNum.argtypes = (c_void_p,c_uint,)
# 結合イベントのデータエントリーMSBを取得(RPNチェンジ・NPRNチェンジのみ) */
MIDIEvent_GetDataEntryMSB = MIDIDataDLL.MIDIEvent_GetDataEntryMSB
MIDIEvent_GetDataEntryMSB.restype = c_uint
MIDIEvent_GetDataEntryMSB.argtypes = (c_void_p,)
# 結合イベントのデータエントリーMSBを設定(RPNチェンジ・NPRNチェンジのみ) */
MIDIEvent_SetDataEntryMSB = MIDIDataDLL.MIDIEvent_SetDataEntryMSB
MIDIEvent_SetDataEntryMSB.restype = c_bool
MIDIEvent_SetDataEntryMSB.argtypes = (c_void_p,c_uint,)
# イベントの番号取得(コントロールチェンジ・プログラムチェンジのみ) */
MIDIEvent_GetNumber = MIDIDataDLL.MIDIEvent_GetNumber
MIDIEvent_GetNumber.restype = c_uint
MIDIEvent_GetNumber.argtypes = (c_void_p,)
# イベントの番号設定(コントロールチェンジ・プログラムチェンジのみ) */
MIDIEvent_SetNumber = MIDIDataDLL.MIDIEvent_SetNumber
MIDIEvent_SetNumber.restype = c_uint
MIDIEvent_SetNumber.argtypes = (c_void_p,c_uint,)
# イベントの値取得(キーアフター・コントローラー・チャンネルアフター・ピッチベンド) */
MIDIEvent_GetValue = MIDIDataDLL.MIDIEvent_GetValue
MIDIEvent_GetValue.restype = c_uint
MIDIEvent_GetValue.argtypes = (c_void_p,)
# イベントの値設定(キーアフター・コントローラー・チャンネルアフター・ピッチベンド) */
MIDIEvent_SetValue = MIDIDataDLL.MIDIEvent_SetValue
MIDIEvent_SetValue.restype = c_uint
MIDIEvent_SetValue.argtypes = (c_void_p,c_uint,)
# 次のイベントへのポインタを取得(なければNULL) */
MIDIEvent_GetNextEvent = MIDIDataDLL.MIDIEvent_GetNextEvent
MIDIEvent_GetNextEvent.restype = c_void_p
MIDIEvent_GetNextEvent.argtypes = (c_void_p,)
# 前のイベントへのポインタを取得(なければNULL) */
MIDIEvent_GetPrevEvent = MIDIDataDLL.MIDIEvent_GetPrevEvent
MIDIEvent_GetPrevEvent.restype = c_void_p
MIDIEvent_GetPrevEvent.argtypes = (c_void_p,)
# 次の同種のイベントへのポインタを取得(なければNULL) */
MIDIEvent_GetNextSameKindEvent = MIDIDataDLL.MIDIEvent_GetNextSameKindEvent
MIDIEvent_GetNextSameKindEvent.restype = c_void_p
MIDIEvent_GetNextSameKindEvent.argtypes = (c_void_p,)
# 前の同種のイベントへのポインタを取得(なければNULL) */
MIDIEvent_GetPrevSameKindEvent = MIDIDataDLL.MIDIEvent_GetPrevSameKindEvent
MIDIEvent_GetPrevSameKindEvent.restype = c_void_p
MIDIEvent_GetPrevSameKindEvent.argtypes = (c_void_p,)
# 親トラックへのポインタを取得(なければNULL) */
MIDIEvent_GetParent = MIDIDataDLL.MIDIEvent_GetParent
MIDIEvent_GetParent.restype = c_void_p
MIDIEvent_GetParent.argtypes = (c_void_p,)
# イベントの内容を文字列表現に変換 */
MIDIEvent_ToStringEx = MIDIDataDLL.MIDIEvent_ToStringExW
MIDIEvent_ToStringEx.restype = c_wchar_p
MIDIEvent_ToStringEx.argtypes = (c_void_p,c_wchar_p,c_void_p,c_uint,)
# イベンの内容トを文字列表現に変換 */
MIDIEvent_ToString = MIDIDataDLL.MIDIEvent_ToStringW
MIDIEvent_ToString.restype = c_wchar_p
MIDIEvent_ToString.argtypes = (c_void_p,c_wchar_p,c_void_p,)



class MIDIData():
	def __init__(self,pMIDIData):
		self.pMIDIData = pMIDIData
		self.instMIDITracks = []
		self.index = -1

	def __len__(self):
		return self.countTrack()

	def __del__(self):
		for instMIDITrack in self.instMIDITracks:
			del instMIDITrack
		MIDIData_Delete(self.pMIDIData)

	def __iter__(self):
		return self

	def __next__(self):
		if self.index == -1:
			pMIDITrack = self.getFirstTrack()
			self.index = pMIDITrack.pMIDITrack
			return pMIDITrack
		else:
			if self.index == self.getLastTrack().pMIDITrack :
				self.index = -1
				raise StopIteration()
			pMIDITrack = self.getMIDITrack(self.index)
			pMIDITrack = pMIDITrack.getNextTrack()
			self.index = pMIDITrack.pMIDITrack
			return pMIDITrack

	def __reversed__(self):
		pMIDITrack = self.getLastTrack()
		self.reversed = [pMIDITrack]
		while True:
			if pMIDITrack.pMIDITrack == self.getFirstTrack().pMIDITrack:
				break
			pMIDITrack = pMIDITrack.getPrevTrack()
			self.reversed = [pMIDITrack] + self.reversed
		return self.reversed

	def getMIDITrack(self,pMIDITrack):
		for instMIDITrack in self.instMIDITracks:
			if instMIDITrack.pMIDITrack == pMIDITrack:
				return instMIDITrack
		instMIDITrack = MIDIData.MIDITrack(pMIDITrack,self)
		self.instMIDITracks.append(instMIDITrack)
		return instMIDITrack


	def insertTrackBefore(self,pMIDITrack,pTarget):
		return MIDIData_InsertTrackBefore(self.pMIDIData,pMIDITrack.pMIDITrack,pTarget.pMIDITrack)

	def insertTrackAfter(self,pMIDITrack,pTarget):
		return MIDIData_InsertTrackAfter(self.pMIDIData,pMIDITrack.pMIDITrack,pTarget.pMIDITrack)

	def addTrack(self,pMIDITrack):
		return MIDIData_AddTrack(self.pMIDIData,pMIDITrack.pMIDITrack)

	def removeTrack(self,pMIDITrack):
		return MIDIData_RemoveTrack(self.pMIDIData,pMIDITrack.pMIDITrack)

	def delete(self):
		del self

	@classmethod
	def create(cls,lFormat,lNumTrack,lTimeMode,lTimeResolution):
		return cls(MIDIData_Create(lFormat,lNumTrack,lTimeMode,lTimeResolution))

	def getFormat(self):
		return MIDIData_GetFormat(self.pMIDIData)

	def setFormat(self,lFormat):
		return MIDIData_SetFormat(self.pMIDIData,lFormat)

	def getTimeBase(self):
		return MIDIData_GetTimeBase(self.pMIDIData)

	def getTimeMode(self):
		return MIDIData_GetTimeMode(self.pMIDIData)

	def getTimeResolution(self):
		return MIDIData_GetTimeResolution(self.pMIDIData)

	def setTimeBase(self,lTimeMode,lTimeResolution):
		return MIDIData_SetTimeBase(self.pMIDIData,lTimeMode,lTimeResolution)

	def getNumTrack(self):
		return MIDIData_GetNumTrack(self.pMIDIData)

	def countTrack(self):
		return MIDIData_CountTrack(self.pMIDIData)

	def getXFVersion(self):
		return MIDIData_GetXFVersion(self.pMIDIData)

	def getFirstTrack(self):
		return self.getMIDITrack(MIDIData_GetFirstTrack(self.pMIDIData))

	def getLastTrack(self):
		return self.getMIDITrack(MIDIData_GetLastTrack(self.pMIDIData))

	def getTrack(self,lTrackIndex):
		return self.getMIDITrack(MIDIData_GetTrack(self.pMIDIData,lTrackIndex))

	def getBeginTime(self):
		return MIDIData_GetBeginTime(self.pMIDIData)

	def getEndTime(self):
		return MIDIData_GetEndTime(self.pMIDIData)

	def getTitle(self):
		return MIDIData_GetTitle(self.pMIDIData,"",64)

	def setTitle(self,pszText):
		return MIDIData_SetTitle(self.pMIDIData,pszText)

	def getSubTitle(self):
		return MIDIData_GetSubTitle(self.pMIDIData)

	def setSubTitle(self,pszText):
		return MIDIData_SetSubTitle(self.pMIDIData,pszText)

	def getCopyright(self):
		return MIDIData_GetCopyright(self.pMIDIData)

	def setCopyright(self,pszText):
		return MIDIData_SetCopyright(self.pMIDIData,pszText)

	def getComment(self):
		return MIDIData_GetComment(self.pMIDIData)

	def setComment(self,pszText):
		return MIDIData_SetComment(self.pMIDIData,pszText)

	def timeToMillisec(self,lTime):
		return MIDIData_TimeToMillisec(self.pMIDIData,lTime)

	def millisecToTime(self,lMillisec):
		return MIDIData_MillisecToTime(self.pMIDIData,lMillisec)

	def breakTime(self,lTime,pMeasure,pBeat,pTick):
		return MIDIData_BreakTime(self.pMIDIData,lTime,pMeasure,pBeat,pTick)

	def breakTimeEx(self,lTime,pMeasure,pBeat,pTick,pnn,pdd,pcc,pbb):
		return MIDIData_BreakTimeEx(self.pMIDIData,lTime,pMeasure,pBeat,pTick,pnn,pdd,pcc,pbb)

	def makeTime(self,lMeasure,lBeat,lTick,pTime):
		return MIDIData_MakeTime(self.pMIDIData,lMeasure,lBeat,lTick,pTime)

	def makeTimeEx(self,lMeasure,lBeat,lTick,pTime,pnn,pdd,pcc,pbb):
		return MIDIData_MakeTimeEx(self.pMIDIData,lMeasure,lBeat,lTick,pTime,pnn,pdd,pcc,pbb)

	def findTempo(self,lTime,pTempo):
		return MIDIData_FindTempo(self.pMIDIData,lTime,pTempo)

	def findTimeSignature(self,lTime,pnn,pdd,pcc,pbb):
		return MIDIData_FindTimeSignature(self.pMIDIData,lTime,pnn,pdd,pcc,pbb)

	def findKeySignature(self,lTime,psf,pmi):
		return MIDIData_FindKeySignature(self.pMIDIData,lTime,psf,pmi)

	@classmethod
	def loadFromSMF(cls,fn):
		return cls(MIDIData_LoadFromSMF(fn))

	def saveAsSMF(self,fn):
		return MIDIData_SaveAsSMF(self.pMIDIData,fn)

	@classmethod
	def loadFromText(cls,fn):
		return cls(MIDIData_LoadFromText(fn))

	def saveAsText(self,fn):
		return MIDIData_SaveAsText(self.pMIDIData,fn)

	@classmethod
	def loadFromBinary(cls,fn):
		return cls(MIDIData_LoadFromBinary(fn))

	def saveAsBinary(self,fn):
		return MIDIData_SaveAsBinary(self.pMIDIData,fn)

	@classmethod
	def loadFromCherry(cls,fn):
		return cls(MIDIData_LoadFromCherry(fn))

	def saveAsCherry(self,fn):
		return MIDIData_SaveAsCherry(self.pMIDIData,fn)

	@classmethod
	def loadFromMIDICSV(cls,fn):
		return cls(MIDIData_LoadFromMIDICSV(fn))

	def saveAsMIDICSV(self,fn):
		return MIDIData_SaveAsMIDICSV(self.pMIDIData,fn)

	@classmethod
	def loadFromWRK(cls,fn):
		return cls(MIDIData_LoadFromWRK(fn))

	def loadFromMabiMML(cls,fn):
		return cls(MIDIData_LoadFromMabiMML(fn))

	@property
	def title(self):
		return self.getTitle()

	@title.setter
	def title(self,pszText):
		return self.setTitle(pszText)

	@property
	def format(self):
		return self.getFormat()
	
	@format.setter
	def format(self,lFormat):
		return self.setFormat(lFormat)

	@property
	def timeBase(self):
		return self.getTimeBase()

	@timeBase.setter
	def timeBase(self,lTimeMode,lTimeResolution):
		return self.setTimeBase(lTimeMode,lTimeResolution)

	@property
	def timeMode(self):
		return self.getTimeMode()
	
	@property
	def timeResolution(self):
		return self.getTimeResolution()

	@property
	def numTrack(self):
		return self.getNumTrack()

	@property
	def beginTime(self):
		return self.getBeginTime()
	
	@property
	def endTime(self):
		return self.getEndTime()

	@property
	def subtitle(self):
		return self.getSubTitle()

	@subtitle.setter
	def subtitle(self,pszText):
		return self.setSubTitle(pszText)

	@property
	def copyright(self):
		return self.getCopyright()

	@copyright.setter
	def copyright(self,pszText):
		return self.setCopyright(pszText)

	@property
	def comment(self):
		return self.getComment()

	@comment.setter
	def comment(self,pszText):
		return self.setComment(pszText)


	class MIDITrack():
		def __init__(self,pMIDITrack,parent):
			self.parent = parent
			self.pMIDITrack = pMIDITrack
			self.instMIDIEvents = []
			self.index = -1

		def __len__(self):
			return self.countEvent()

		def __del__(self):
			for instMIDIEvent in self.instMIDIEvents:
				del instMIDIEvent
			self.parent.instMIDITracks.remove(self)

		def __iter__(self):
			return self

		def __next__(self):
			if self.index == -1:
				pMIDIEvent = self.getFirstEvent()
				self.index = pMIDIEvent.pMIDIEvent
				return pMIDIEvent
			else:
				if self.index == self.getLastEvent().pMIDIEvent:
					self.index = -1
					raise StopIteration()
				pMIDIEvent = self.getMIDIEvent(self.index)
				pMIDIEvent = pMIDIEvent.getNextEvent()
				self.index = pMIDIEvent.pMIDIEvent
				return pMIDIEvent

		def __reversed__(self):
			pMIDIEvent = self.getLastEvent()
			self.reversed = [pMIDIEvent]
			while True:
				if pMIDIEvent.pMIDIEvent == self.getFirstEvent().pMIDIEvent:
					break
				pMIDIEvent = pMIDIEvent.getPrevEvent()
				self.reversed = [pMIDIEvent] + self.reversed
			return self.reversed

		def getMIDIEvent(self,pMIDIEvent):
			for instMIDIEvent in self.instMIDIEvents:
				if instMIDIEvent.pMIDIEvent == pMIDIEvent:
					return instMIDIEvent
			instMIDIEvent = MIDIData.MIDITrack.MIDIEvent(pMIDIEvent,self)
			self.instMIDIEvents.append(instMIDIEvent)
			return instMIDIEvent

		def getNumEvent(self):
			return MIDITrack_GetNumEvent(self.pMIDITrack)

		def getFirstEvent(self):
			return self.getMIDIEvent(MIDITrack_GetFirstEvent(self.pMIDITrack))

		def getLastEvent(self):
			return self.getMIDIEvent(MIDITrack_GetLastEvent(self.pMIDITrack))

		def getFirstKindEvent(self,lKind):
			return self.getMIDIEvent(MIDITrack_GetFirstKindEvent(self.pMIDITrack,lKind))

		def getLastKindEvent(self,lKind):
			return self.getMIDIEvent(MIDITrack_GetLastKindEvent(self.pMIDITrack,lKind))

		def getNextTrack(self):
			return self.parent.getMIDITrack(MIDITrack_GetNextTrack(self.pMIDITrack))

		def getPrevTrack(self):
			return self.parent.getMIDITrack(MIDITrack_GetPrevTrack(self.pMIDITrack))

		def getParent(self):
			return self.parent

		def countEvent(self):
			return MIDITrack_CountEvent(self.pMIDITrack)

		def getBeginTime(self):
			return MIDITrack_GetBeginTime(self.pMIDITrack)

		def getEndTime(self):
			return MIDITrack_GetEndTime(self.pMIDITrack)

		def getName(self):
			return MIDITrack_GetName(self.pMIDITrack,"",64)

		def getInputOn(self):
			return MIDITrack_GetInputOn(self.pMIDITrack)

		def getInputPort(self):
			return MIDITrack_GetInputPort(self.pMIDITrack)

		def getInputChannel(self):
			return MIDITrack_GetInputChannel(self.pMIDITrack)

		def getOutputOn(self):
			return MIDITrack_GetOutputOn(self.pMIDITrack)

		def getOutputPort(self):
			return MIDITrack_GetOutputPort(self.pMIDITrack)

		def getOutputChannel(self):
			return MIDITrack_GetOutputChannel(self.pMIDITrack)

		def getTimePlus(self):
			return MIDITrack_GetTimePlus(self.pMIDITrack)

		def getKeyPlus(self):
			return MIDITrack_GetKeyPlus(self.pMIDITrack)

		def getVelocityPlus(self):
			return MIDITrack_GetVelocityPlus(self.pMIDITrack)

		def getViewMode(self):
			return MIDITrack_GetViewMode(self.pMIDITrack)

		def getForeColor(self):
			return MIDITrack_GetForeColor(self.pMIDITrack)

		def getBackColor(self):
			return MIDITrack_GetBackColor(self.pMIDITrack)

		def setName(self,pszText):
			return MIDITrack_SetName(self.pMIDITrack,pszText)

		def setInputOn(self,lInputOn):
			return MIDITrack_SetInputOn(self.pMIDITrack,lInputOn)
		
		def setInputPort(self,lInputPort):
			return MIDITrack_SetInputPort(self.pMIDITrack,lInputPort)

		def setInputChannel(self,lInputChannel):
			return MIDITrack_SetInputChannel(self.pMIDITrack,lInputChannel)

		def setOutputOn(self,lOutputOn):
			return MIDITrack_SetOutputOn(self.pMIDITrack,lOutputOn)

		def setOutputPort(self,lOutputPort):
			return MIDITrack_SetOutputPort(self.pMIDITrack,lOutputPort)

		def setOutputChannel(self,lOutputChannel):
			return MIDITrack_SetOutputChannel(self.pMIDITrack,lOutputChannel)

		def setTimePlus(self,lTimePlus):
			return MIDITrack_SetTimePlus(self.pMIDITrack,lTimePlus)

		def setKeyPlus(self,lKeyPlus):
			return MIDITrack_SetKeyPlus(self.pMIDITrack,lKeyPlus)

		def setVelocityPlus(self,lVelocityPlus):
			return MIDITrack_SetVelocityPlus(self.pMIDITrack,lVelocityPlus)

		def setViewMode(self,lViewMode):
			return MIDITrack_SetViewMode(self.pMIDITrack,lViewMode)

		def setForeColor(self,lForeColor):
			return MIDITrack_SetForeColor(self.pMIDITrack,lForeColor)

		def setBackColor(self,lBackColor):
			return MIDITrack_SetBackColor(self.pMIDITrack,lBackColor)

		def getXFVersion(self):
			return MIDITrack_GetXFVersion(self.pMIDITrack)

		def delete(self):
			MIDITrack_Delete(self.pMIDITrack)
			del self

		def create(self):
			return self.parent.getMIDITrack(MIDITrack_Create())

		def createClone(self,pMIDITrack):
			return self.parent.getMIDITrack(MIDITrack_CreateClone(pMIDITrack.pMIDITrack))

	#	def insertSingleEventAfter(self):
	#	def insertSingleEventBefore(self):

		def insertEventAfter(self,pMIDIEvent,pTarget):
			return MIDITrack_InsertEventAfter(self.pMIDITrack,pMIDIEvent.pMIDIEvent,pTarget.pMIDIEvent)

		def insertEventBefore(self,pMIDIEvent,pTarget):
			return MIDITrack_InsertEventBefore(self.pMIDITrack,pMIDIEvent.pMIDIEvent,pTarget.pMIDIEvent)

		def insertEvent(self,pMIDIEvent):
			return MIDITrack_InsertEvent(self.pMIDITrack,pMIDIEvent.pMIDIEvent)

		def insertSequenceNumber(self,lTime,lNum):
			return MIDITrack_InsertSequenceNumber(self.pMIDITrack,lTime,lNum)

	#	def insertTextBasedEvent(self):
	#	def insertTextBasedEventEx(self):

		def insertTextEvent(self,lTime,pszText):
			return MIDITrack_InsertTextEvent(self.pMIDITrack,lTime,pszText)

		def insertTextEventEx(self,lTime,lCharCode,pszText):
			return MIDITrack_InsertTextEventEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertCopyrightNotice(self,lTime,pszText):
			return MIDITrack_InsertCopyrightNotice(self.pMIDITrack,lTime,pszText)

		def insertCopyrightNoticeEx(self,lTime,lCharCode,pszText):
			return MIDITrack_InsertCopyrightNoticeEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertTrackName(self,lTime,pszText):
			return MIDITrack_InsertTrackName(self.pMIDITrack,lTime,pszText)

		def insertTrackNameEx(self,lTime,lCharCode,pszText):
			return MIDITrack_InsertTrackNameEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertInstrumentName(self,lTime,pszText):
			return MIDITrack_InsertInstrumentName(self.pMIDITrack,lTime,pszText)

		def insertInstrumentNameEx(self):
			return MIDITrack_InsertInstrumentNameEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertLyric(self,lTime,pszText):
			return MIDITrack_InsertLyric(self.pMIDITrack,lTime,pszText)

		def insertLyricEx(self,lTime,lCharCode,pszText):
			return MIDITrack_InsertLyricEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertMarker(self,lTime,pszText):
			return MIDITrack_InsertMarker(self.pMIDITrack,lTime,pszText)

		def insertMarkerEx(self,lTime,lCharCode,pszText):
			return MIDITrack_InsertMarkerEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertCuePoint(self,lTime,pszText):
			return MIDITrack_InsertCuePoint(self.pMIDITrack,lTime,pszText)

		def insertCuePointEx(self,lTime,lCharCode,pszText):
			return MIDITrack_InsertCuePointEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertProgramName(self,lTime,pszText):
			return MIDITrack_InsertProgramName(self.pMIDITrack,lTime,pszText)

		def insertProgramNameEx(self,lTime,lCharCode,pszText):
			return MIDITrack_InsertProgramNameEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertDeviceName(self,lTime,pszText):
			return MIDITrack_InsertDeviceName(self.pMIDITrack,lTime,pszText)

		def insertDeviceNameEx(self,lTime,lCharCode,pszText):
			return MIDITrack_InsertDeviceNameEx(self.pMIDITrack,lTime,lCharCode,pszText)

		def insertChannelPrefix(self,lTime,lNum):
			return MIDITrack_InsertChannelPrefix(self.pMIDITrack,lTime,lNum)

		def insertPortPrefix(self,lTime,lNum):
			return MIDITrack_InsertPortPrefix(self.pMIDITrack,lTime,lNum)

		def insertEndofTrack(self,lTime):
			return MIDITrack_InsertEndofTrack(self.pMIDITrack,lTime)

		def insertTempo(self,lTime,lTempo):
			return MIDITrack_InsertTempo(self.pMIDITrack,lTime,lTempo)

		def insertSMPTEOffset(self,lTime,lMode,lHour,lMin,lSec,lFrame,lSubFrame):
			return MIDITrack_InsertSMPTEOffset(self.pMIDITrack,lTime,lMode,lHour,lMin,lSec,lFrame,lSubFrame)

		def insertTimeSignature(self,lTime,lnn,ldd,lcc,lbb):
			return MIDITrack_InsertTimeSignature(self.pMIDITrack,lTime,lnn,ldd,lcc,lbb)

		def insertKeySignature(self,lTime,lsf,lmi):
			return MIDITrack_InsertKeySignature(self.pMIDITrack,lTime,lsf,lmi)

		def insertSequencerSpecific(self,lTime,pBuf,lLen):
			return MIDITrack_InsertSequencerSpecific(self.pMIDITrack,lTime,pBuf,lLen)

		def insertNoteOff(self,lTime,lCh,lKey,lVel):
			return MIDITrack_InsertNoteOff(self.pMIDITrack,lTime,lCh,lKey,lVel)

		def insertNoteOn(self,lTime,lCh,lKey,lVel):
			return MIDITrack_InsertNoteOn(self.pMIDITrack,lTime,lCh,lKey,lVel)

		def insertNote(self,lTime,lCh,lKey,lVel,lDur):
			return MIDITrack_InsertNote(self.pMIDITrack,lTime,lCh,lKey,lVel,lDur)

		def insertKeyAftertouch(self,lTime,lCh,lKey,lVel):
			return MIDITrack_InsertKeyAftertouch(self.pMIDITrack,lTime,lCh,lKey,lVel)

		def insertControlChange(self,lTime,lCh,lNum,lVal):
			return MIDITrack_InsertControlChange(self.pMIDITrack,lTime,lCh,lNum,lVal)

	#	def insertRPNChange(self):
	#	def insertNRPNChange(self):

		def insertProgramChange(self,lTime,lCh,lNum):
			return MIDITrack_InsertProgramChange(self.pMIDITrack,lTime,lCh,lNum)

	#	def insertPatchChange(self):

		def insertChannelAftertouch(self,lTime,lCh,lVal):
			return MIDITrack_InsertChannelAftertouch(self.pMIDITrack,lTime,lCh,lVal)

		def insertPitchBend(self,lTime,lCh,lVal):
			return MIDITrack_InsertPitchBend(self.pMIDITrack,lTime,lCh,lVal)

		def insertSysExEvent(self,lTime,pBuf,lLen):
			return MIDITrack_InsertSysExEvent(self.pMIDITrack,lTime,pBuf,lLen)

		def removeSingleEvent(self,pMIDIEvent):
			return MIDITrack_RemoveSingleEvent(self.pMIDITrack,pMIDIEvent.pMIDIEvent)

		def removeEvent(self,pMIDIEvent):
			return MIDITrack_RemoveEvent(self.pMIDITrack,pMIDIEvent.pMIDIEvent)

		def isFloating(self):
			return MIDITrack_IsFloating(self.pMIDITrack)

		def checkSetupTrack(self):
			return MIDITrack_CheckSetupTrack(self.pMIDITrack)

		def checkNonSetupTrack(self):
			return MIDITrack_CheckNonSetupTrack(self.pMIDITrack)

		def timeToMillisec(self,lTime):
			return MIDITrack_TimeToMillisec(self.pMIDITrack,lTime)

		def millisecToTime(self,lMillisec):
			return MIDITrack_MillisecToTime(self.pMIDITrack,lMillisec)

		def breakTimeEx(self,lTime,pMeasure,pBeat,pTick,pnn,pdd,pcc,pbb):
			return MIDITrack_BreakTimeEx(self.pMIDITrack,lTime,pMeasure,pBeat,pTick,pnn,pdd,pcc,pbb)

		def breakTime(self,lTime,pMeasure,pBeat,pTick):
			return MIDITrack_BreakTime(self.pMIDITrack,lTime,pMeasure,pBeat,pTick)

		def makeTimeEx(self,lTime,pMeasure,pBeat,pTick,pnn,pdd,pcc,pbb):
			return MIDITrack_MakeTimeEx(self.pMIDITrack,lTime,pMeasure,pBeat,pTick,pnn,pdd,pcc,pbb)

		def makeTime(self,lTime,pMeasure,pBeat,pTick):
			return MIDITrack_MakeTime(self.pMIDITrack,lTime,pMeasure,pBeat,pTick)

		def findTempo(self,lTime,pTempo):
			return MIDITrack_FindTempo(self.pMIDITrack,lTime,pTempo)

		def findTimeSignature(self,lTime,pnn,pdd,pcc,pbb):
			return MIDITrack_FindTimeSignature(self.pMIDITrack,lTime,pnn,pdd,pcc,pbb)

		def findKeySignature(self,lTime,psf,pmi):
			return MIDITrack_FindKeySignature(self.pMIDITrack,lTime,psf,pmi)

		@property
		def numEvent(self):
			return self.getNumEvent()

		@property
		def beginTime(self):
			return self.getBeginTime()

		@property
		def endTime(self):
			return self.getEndTime()

		@property
		def name(self):
			return self.getName()
		
		@name.setter
		def name(self,pszText):
			return self.setName(pszText)

		@property
		def inputOn(self):
			return self.getInputOn()
		
		@inputOn.setter
		def inputOn(self,lInputOn):
			return self.setInputOn(lInputOn)

		@property
		def inputPort(self):
			return self.getInputPort()
		
		@inputPort.setter
		def inputPort(self,lInputPort):
			return self.setInputPort(lInputPort)

		@property
		def inputChannel(self):
			return self.getInputChannel()
		
		@inputChannel.setter
		def inputChannel(self,lInputChannel):
			return self.setInputChannel(lInputChannel)
		
		@property
		def outputOn(self):
			return self.getOutputOn()
		
		@outputOn.setter
		def outputOn(self,lOutputOn):
			return self.setOutputOn(lOutputOn)

		@property
		def outputPort(self):
			return self.getOutputPort()

		@outputPort.setter
		def outputPort(self,lOutputPort):
			return self.setOutputPort(lOutputPort)

		@property
		def outputChannel(self):
			return self.getOutputChannel()
		
		@outputChannel.setter
		def outputChannel(self,lOutputChannel):
			return self.setOutputChannel(lOutputChannel)

		@property
		def viewMode(self):
			return self.getViewMode()
		
		@viewMode.setter
		def viewMode(self,lViewMode):
			return self.setViewMode(lViewMode)

		@property
		def foreColor(self):
			return self.getForeColor()
		
		@foreColor.setter
		def coreFolor(self,lForeColor):
			return self.setForeColor(lForeColor)

		@property
		def backColor(self):
			return self.getBackColor()
		
		@backColor.setter
		def backColor(self,lBackColor):
			return self.setBackColor(lBackColor)


		class MIDIEvent():
			def __init__(self,pMIDIEvent,parent):
				self.parent = parent
				self.pMIDIEvent = pMIDIEvent
				self.index = -1

			def __del__(self):
				self.parent.instMIDIEvents.remove(self)

			def getFirstCombinedEvent(self):
				return self.parent.getMIDIEvent(MIDIEvent_GetFirstCombinedEvent(self.pMIDIEvent))

			def getLastCombinedEvent(self):
				return self.parent.getMIDIEvent(MIDIEvent_GetLastCombinedEvent(self.pMIDIEvent))

			def combine(self):
				return MIDIEvent_Combine(self.pMIDIEvent)

			def chop(self):
				return MIDIEvent_Chop(self.pMIDIEvent)

			def deleteSingle(self):
				if self.isCombined():
					self.chop()
				del self

			def delete(self):
				MIDIEvent_Delete(self.pMIDIEvent)
				del self

		#	def create(self):

			def createClone(self):
				return self.parent.getMIDIEvent(MIDIEvent_CreateClone(self.pMIDIEvent))

			def createSequenceNumber(self,lTime,lNum):
				return self.parent.getMIDIEvent(MIDIEvent_CreateSequenceNumber(lTime,lNum))

			def createTextBasedEvent(self,lTime,lKind,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateTextBasedEvent(lTime,lKind,pszText))

			def createTextBasedEventEx(self,lTime,lKind,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateTextBasedEventEx(lTime,lKind,lCharCode,pszText))

			def createTextEvent(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateTextEvent(lTime,pszText))

			def createTextEventEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateTextEventEx(lTime,lCharCode,pszText))

			def createCopyrightNotice(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateCopyrightNotice(lTime,pszText))

			def createCopyrightNoticeEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateCopyrightNoticeEx(lTime,lCharCode,pszText))

			def createTrackName(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateTrackName(lTime,pszText))

			def createTrackNameEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateTrackNameEx(lTime,lCharCode,pszText))

			def createInstrumentName(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateInstrumentName(lTime,pszText))

			def createInstrumentNameEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateInstrumentNameEx(lTime,lCharCode,pszText))

			def createLyric(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateLyric(lTime,pszText))

			def createLyricEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateLyricEx(lTime,lCharCode,pszText))

			def createMarker(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateMarker(lTime,pszText))

			def createMarkerEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateMarkerEx(lTime,lCharCode,pszText))

			def createCuePoint(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateCuePoint(lTime,pszText))

			def createCuePointEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateCuePointEx(lTime,lCharCode,pszText))

			def createProgramName(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateProgramName(lTime,pszText))

			def createProgramNameEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateProgramNameEx(lTime,lCharCode,pszText))

			def createDeviceName(self,lTime,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateDeviceName(lTime,pszText))

			def createDeviceNameEx(self,lTime,lCharCode,pszText):
				return self.parent.getMIDIEvent(MIDIEvent_CreateDeviceNameEx(lTime,lCharCode,pszText))

			def createChannelPrefix(self,lTime,lCh):
				return self.parent.getMIDIEvent(MIDIEvent_CreateChannelPrefix(lTime,lCh))

			def createPortPrefix(self,lTime,lNum):
				return self.parent.getMIDIEvent(MIDIEvent_CreatePortPrefix(lTime,lNum))

			def createEndofTrack(self,lTime):
				return self.parent.getMIDIEvent(MIDIEvent_CreateEndofTrack(lTime))

			def createTempo(self,lTime,lTempo):
				return self.parent.getMIDIEvent(MIDIEvent_CreateTempo(lTime,lTempo))

			def createSMPTEOffset(self,lTime,lMode,lHour,lMin,lSec,lFrame,lSubFrame):
				return self.parent.getMIDIEvent(MIDIEvent_CreateSMPTEOffset(lTime,lMode,lHour,lMin,lSec,lFrame,lSubFrame))

			def createTimeSignature(self,lTime,lnn,ldd,lcc,lbb):
				return self.parent.getMIDIEvent(MIDIEvent_CreateTimeSignature(lTime,lnn,ldd,lcc,lbb))

			def createKeySignature(self,lTime,lsf,lmi):
				return self.parent.getMIDIEvent(MIDIEvent_CreateKeySignature(lTime,lsf,lmi))

		#	def createSequencerSpecific(self):

			def createNoteOff(self,lTime,lCh,lKey,lVel):
				return self.parent.getMIDIEvent(MIDIEvent_CreateNoteOff(lTime,lCh,lKey,lVel))

			def createNoteOn(self,lTime,lCh,lKey,lVel):
				return self.parent.getMIDIEvent(MIDIEvent_CreateNoteOn(lTime,lCh,lKey,lVel))

			def createNote(self,lTime,lCh,lKey,lVel,lDur):
				return self.parent.getMIDIEvent(MIDIEvent_CreateNote(lTime,lCh,lKey,lVel,lDur))

			def createNoteOnNoteOff(self,lTime,lCh,lKey,lVel1,lVel2,lDur):
				return self.parent.getMIDIEvent(MIDIEvent_CreateNoteOnNoteOff(lTime,lCh,lKey,lVel1,lVel2,lDur))

			def createNoteOnNoteOn0(self,lTime,lCh,lKey,lVel,lDur):
				return self.parent.getMIDIEvent(MIDIEvent_CreateNoteOnNoteOn0(lTime,lCh,lKey,lVel,lDur))

			def createKeyAftertouch(self,lTime,lCh,lKey,lVal):
				return self.parent.getMIDIEvent(MIDIEvent_CreateKeyAftertouch(lTime,lCh,lKey,lVal))

			def createControlChange(self,lTime,lCh,lNum,lVal):
				return self.parent.getMIDIEvent(MIDIEvent_CreateControlChange(lTime,lCh,lNum,lVal))

			def createRPNChange(self,lTime,lCh,lCC101,lCC100,lVal):
				return self.parent.getMIDIEvent(MIDIEvent_CreateRPNChange(lTime,lCh,lCC101,lCC100,lVal))

			def createNRPNChange(self,lTime,lCh,lCC99,lCC98,lVal):
				return self.parent.getMIDIEvent(MIDIEvent_CreateNRPNChange(lTime,lCh,lCC99,lCC98,lVal))

			def createProgramChange(self,lTime,lCh,lNum):
				return self.parent.getMIDIEvent(MIDIEvent_CreateProgramChange(lTime,lCh,lNum))

			def createPatchChange(self,lTime,lCh,lCC0,lCC32,lNum):
				return self.parent.getMIDIEvent(MIDIEvent_CreatePatchChange(lTime,lCh,lCC0,lCC32,lNum))

			def createChannelAftertouch(self,lTime,lCh,lVal):
				return self.parent.getMIDIEvent(MIDIEvent_CreateChannelAftertouch(lTime,lCh,lVal))

			def createPitchBend(self,lTime,lCh,lVal):
				return self.parent.getMIDIEvent(MIDIEvent_CreatePitchBend(lTime,lCh,lVal))

		#	def createSysExEvent(self):

			@property
			def isMetaEvent(self):
				return MIDIEvent_IsMetaEvent(self.pMIDIEvent)

			@property
			def isSequenceNumber(self):
				return MIDIEvent_IsSequenceNumber(self.pMIDIEvent)

			@property
			def isTextEvent(self):
				return MIDIEvent_IsTextEvent(self.pMIDIEvent)

			@property
			def isCopyrightNotice(self):
				return MIDIEvent_IsCopyrightNotice(self.pMIDIEvent)

			@property
			def isTrackName(self):
				return MIDIEvent_IsTrackName(self.pMIDIEvent)

			@property
			def isInstrumentName(self):
				return MIDIEvent_IsInstrumentName(self.pMIDIEvent)

			@property
			def isLyric(self):
				return MIDIEvent_IsLyric(self.pMIDIEvent)

			@property
			def isMarker(self):
				return MIDIEvent_IsMarker(self.pMIDIEvent)

			@property
			def isCuePoint(self):
				return MIDIEvent_IsCuePoint(self.pMIDIEvent)

			@property
			def isProgramName(self):
				return MIDIEvent_IsProgramName(self.pMIDIEvent)

			@property
			def isDeviceName(self):
				return MIDIEvent_IsDeviceName(self.pMIDIEvent)

			@property
			def isChannelPrefix(self):
				return MIDIEvent_IsChannelPrefix(self.pMIDIEvent)

			@property
			def isPortPrefix(self):
				return MIDIEvent_IsPortPrefix(self.pMIDIEvent)

			@property
			def isEndofTrack(self):
				return MIDIEvent_IsEndofTrack(self.pMIDIEvent)

			@property
			def isTempo(self):
				return MIDIEvent_IsTempo(self.pMIDIEvent)

			@property
			def isSMPTEOffset(self):
				return MIDIEvent_IsSMPTEOffset(self.pMIDIEvent)

			@property
			def isTimeSignature(self):
				return MIDIEvent_IsTimeSignature(self.pMIDIEvent)

			@property
			def isKeySignature(self):
				return MIDIEvent_IsKeySignature(self.pMIDIEvent)

			@property
			def isSequencerSpecific(self):
				return MIDIEvent_IsSequencerSpecific(self.pMIDIEvent)

			@property
			def isMIDIEvent(self):
				return MIDIEvent_IsMIDIEvent(self.pMIDIEvent)

			@property
			def isNoteOn(self):
				return MIDIEvent_IsNoteOn(self.pMIDIEvent)

			@property
			def isNoteOff(self):
				return MIDIEvent_IsNoteOff(self.pMIDIEvent)

			@property
			def isNote(self):
				return MIDIEvent_IsNote(self.pMIDIEvent)

			@property
			def isNoteOnNoteOff(self):
				return MIDIEvent_IsNoteOnNoteOff(self.pMIDIEvent)

			@property
			def isNoteOnNoteOn0(self):
				return MIDIEvent_IsNoteOnNoteOn0(self.pMIDIEvent)

			@property
			def isKeyAftertouch(self):
				return MIDIEvent_IsKeyAftertouch(self.pMIDIEvent)

			@property
			def isControlChange(self):
				return MIDIEvent_IsControlChange(self.pMIDIEvent)

			@property
			def isRPNChange(self):
				return MIDIEvent_IsRPNChange(self.pMIDIEvent)

			@property
			def isNRPNChange(self):
				return MIDIEvent_IsNRPNChange(self.pMIDIEvent)

			@property
			def isProgramChange(self):
				return MIDIEvent_IsProgramChange(self.pMIDIEvent)

			@property
			def isPatchChange(self):
				return MIDIEvent_IsPatchChange(self.pMIDIEvent)

			@property
			def isChannelAftertouch(self):
				return MIDIEvent_IsChannelAftertouch(self.pMIDIEvent)

			@property
			def isPitchBend(self):
				return MIDIEvent_IsPitchBend(self.pMIDIEvent)

			@property
			def isSysExEvent(self):
				return MIDIEvent_IsSysExEvent(self.pMIDIEvent)

			@property
			def isFloating(self):
				return MIDIEvent_IsFloating(self.pMIDIEvent)

			@property
			def isCombined(self):
				return MIDIEvent_IsCombined(self.pMIDIEvent)

			def getKind(self):
				return MIDIEvent_GetKind(self.pMIDIEvent)

		#	def setKind(self):

			def getLen(self):
				return MIDIEvent_GetLen(self.pMIDIEvent)

			def getData(self):
				return MIDIEvent_GetData(self.pMIDIEvent,"",64)

		#	def setData(self):
		#	def getCharCode(self):
		#	def setCharCode(self):
		#	def getText(self):
		#	def setText(self):
		#	def getSMPTEOffset(self):
		#	def setSMPTEOffset(self):

			def getTempo(self):
				return MIDIEvent_GetTempo(self.pMIDIEvent)

			def setTempo(self,lTempo):
				return MIDIEvent_SetTempo(self.pMIDIEvent,lTempo)

			def getTimeSignature(self,pnn,pdd,pcc,pbb):
				return MIDIEvent_GetTimeSignature(self.pMIDIEvent,pnn,pdd,pcc,pbb)

			def setTimeSignature(self,pnn,pdd,pcc,pbb):
				return MIDIEvent_SetTimeSignature(self.pMIDIEvent,pnn,pdd,pcc,pbb)

			def getKeySignature(self,psf,pmi):
				return MIDIEvent_GetKeySignature(self.pMIDIEvent,psf,pmi)

			def setKeySignature(self,psf,pmi):
				return MIDIEvent_SetKeySignature(self.pMIDIEvent,psf,pmi)

		#	def getMIDIMessage(self):
		#	def setMIDIMessage(self):

			def getChannel(self):
				return MIDIEvent_GetChannel(self.pMIDIEvent)

			def setChannel(self,lChannel):
				return MIDIEvent_SetChannel(self.pMIDIEvent,lChannel)

			def getTime(self):
				return MIDIEvent_GetTime(self.pMIDIEvent)

		#	def setTimeSingle(self):

			def setTime(self,lTime):
				return MIDIEvent_SetTime(self.pMIDIEvent,lTime)

			def getKey(self):
				return MIDIEvent_GetKey(self.pMIDIEvent)

			def setKey(self,lKey):
				return MIDIEvent_SetKey(self.pMIDIEvent,lKey)

			def getVelocity(self):
				return MIDIEvent_GetVelocity(self.pMIDIEvent)

			def setVelocity(self,lVelocity):
				return MIDIEvent_SetVelocity(self.pMIDIEvent,lVelocity)

			def getDuration(self):
				return MIDIEvent_GetDuration(self.pMIDIEvent)

			def setDuration(self,lDuration):
				return MIDIEvent_SetDuration(self.pMIDIEvent,lDuration)

			def getBank(self):
				return MIDIEvent_GetBank(self.pMIDIEvent)

			def getBankMSB(self):
				return MIDIEvent_GetBankMSB(self.pMIDIEvent)

			def getBankLSB(self):
				return MIDIEvent_GetBankLSB(self.pMIDIEvent)

			def setBank(self,lBank):
				return MIDIEvent_SetBank(self.pMIDIEvent,lBank)

			def setBankMSB(self,lBankMSB):
				return MIDIEvent_SetBankMSB(self.pMIDIEvent,lBankMSB)

			def setBankLSB(self,lBankLSB):
				return MIDIEvent_SetBankLSB(self.pMIDIEvent,lBankLSB)

			def getPatchNum(self):
				return MIDIEvent_GetPatchNum(self.pMIDIEvent)

			def setPatchNum(self,lNum):
				return MIDIEvent_SetPatchNum(self.pMIDIEvent,lNum)

			def getDataEntryMSB(self):
				return MIDIEvent_GetDataEntryMSB(self.pMIDIEvent)
			
			def setDataEntryMSB(self,lDataEntryMSB):
				return MIDIEvent_SetDataEntryMSB(self.pMIDIEvent,lDataEntryMSB)

			def getNumber(self):
				return MIDIEvent_GetNumber(self.pMIDIEvent)

			def setNumber(self,lNumber):
				return MIDIEvent_SetNumber(self.pMIDIEvent,lNumber)

			def getValue(self):
				return MIDIEvent_GetValue(self.pMIDIEvent)

			def setValue(self,lValue):
				return MIDIEvent_SetValue(self.pMIDIEvent,lValue)

			def getNextEvent(self):
				return self.parent.getMIDIEvent(MIDIEvent_GetNextEvent(self.pMIDIEvent))

			def getPrevEvent(self):
				return self.parent.getMIDIEvent(MIDIEvent_GetPrevEvent(self.pMIDIEvent))

			def getNextSameKindEvent(self):
				return self.parent.getMIDIEvent(MIDIEvent_GetNextSameKindEvent(self.pMIDIEvent))

			def getPrevSameKindEvent(self):
				return self.parent.getMIDIEvent(MIDIEvent_GetPrevSameKindEvent(self.pMIDIEvent))

			def getParent(self):
				return self.parent

			def toStringEx(self,lFlags):
				return MIDIEvent_ToStringEx(self.pMIDIEvent,"",64,lFlags)
				
			def toString(self):
				return MIDIEvent_ToString(self.pMIDIEvent,"",64)

			@property
			def kind(self):
				return self.getKind()

			@property
			def len(self):
				return self.getLen()

			@property
			def tempo(self):
				return self.getTempo()
			
			@tempo.setter
			def tempo(self,lTempo):
				return self.setTempo(lTempo)
			
			@property
			def channel(self):
				return self.getChannel()
			
			@channel.setter
			def channel(self,lChannel):
				return self.setChannel(lChannel)
			
			@property
			def time(self):
				return self.getTime()
			
			@time.setter
			def time(self,lTime):
				return self.setTime(lTime)
			
			@property
			def key(self):
				return self.getKey()
			
			@key.setter
			def key(self,lKey):
				return self.setKey(lKey)
			
			@property
			def velocity(self):
				return self.getVelocity()
			
			@velocity.setter
			def velocity(self,lVelocity):
				return self.setVelocity(lVelocity)
			
			@property
			def duration(self):
				return self.getDuration()
			
			@duration.setter
			def duration(self,lDuration):
				return self.setDuration(lDuration)
			
			@property
			def bank(self):
				return self.getBank()
			
			@bank.setter
			def bank(self,lBank):
				return self.setBank(lBank)
			
			@property
			def bankMSB(self):
				return self.getBankMSB()
			
			@bankMSB.setter
			def bankMSB(self,lBankMSB):
				return self.setBankMSB(lBankMSB)
			
			@property
			def bankLSB(self):
				return self.getBankLSB()
			
			@bankLSB.setter
			def bankLSB(self,lBankLSB):
				return self.setBankLSB(lBankLSB)
			
			@property
			def patchNum(self):
				return self.getPatchNum()
			
			@patchNum.setter
			def patchNum(self,lNum):
				return self.setPatchNum(lNum)
			
			@property
			def dataEntryMSB(self):
				return self.getDataEntryMSB()
			
			@dataEntryMSB.setter
			def dataEntryMSB(self,lDataEntryMSB):
				return self.setDataEntryMSB(lDataEntryMSB)
			
			@property
			def number(self):
				return self.getNumber()
			
			@number.setter
			def number(self,lNumber):
				return self.setNumber(lNumber)
			
			@property
			def value(self):
				return self.getValue()
			
			@value.setter
			def value(self,lValue):
				return self.setValue(lValue)
