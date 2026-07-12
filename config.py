"""
 鐢垫姣忔棩鏂伴椈鎺ㄩ€?- 閰嶇疆鏂囦欢

 浣跨敤鏂规硶锛? 1. 灏嗘鏂囦欢澶嶅埗涓?config.py锛堝鏋滃凡缁忔槸 config.py 鍒欑洿鎺ョ紪杈戯級
 2. 濉啓涓嬫柟鐨?QQ 閭閰嶇疆
 3. GitHub Actions 涓€氳繃 Repository Secrets 娉ㄥ叆浠ヤ笅鍙橀噺锛?    - QQ_EMAIL: 浣犵殑 QQ 閭鍦板潃
    - QQ_EMAIL_AUTH_CODE: QQ 閭鎺堟潈鐮侊紙闈炵櫥褰曞瘑鐮侊級
    - NEWS_RECEIVER: 鎺ユ敹鏂伴椈鐨勯偖绠卞湴鍧€锛堝彲濉悓涓€涓級

 鑾峰彇 QQ 閭鎺堟潈鐮佺殑姝ラ锛? 1. 鐧诲綍 mail.qq.com 鈫?璁剧疆 鈫?璐︽埛
 2. 鎵惧埌 "POP3/SMTP鏈嶅姟" 鈫?寮€鍚? 3. 鎸夌収鎸囧紩鍙戦€佺煭淇¤幏鍙栨巿鏉冪爜锛?6浣嶅瓧姣嶏級
 """

 import os


 # ============================================================
 # 閭閰嶇疆锛堥€氳繃鐜鍙橀噺璇诲彇锛孏itHub Secrets 娉ㄥ叆锛? # ============================================================
 QQ_EMAIL = os.environ.get("QQ_EMAIL", "noah30@qq.com")
 QQ_EMAIL_AUTH_CODE = os.environ.get("QQ_EMAIL_AUTH_CODE", "")
 NEWS_RECEIVER = os.environ.get("NEWS_RECEIVER", QQ_EMAIL)

 SMTP_SERVER = "smtp.qq.com"
 SMTP_PORT = 465  # SSL


 # ============================================================
 # 鏂伴椈婧愰厤缃? # ============================================================

 # ---- 鑻辨枃婧?(50%) ----
 ELEVATOR_WORLD_RSS = [
     "https://www.elevatorworld.com/feed/",
     "https://www.elevatorworld.com/rss/",
     "https://www.elevatorworld.com/rss2/",
 ]
 ELEVATOR_WORLD_NEWS_URL = "https://www.elevatorworld.com/category/news/"
 ELEVATOR_WORLD_INDUSTRY_URL = "https://www.elevatorworld.com/category/industry-news/"

 # 鍏朵粬鑻辨枃鐢垫琛屼笟婧? OTHER_ENGLISH_RSS = [
     # 鍙墿灞曪細娣诲姞鍏朵粬鑻辨枃鐢垫琛屼笟 RSS
 ]

 # ---- 涓枃婧?(50%) ----
 BAIDU_NEWS_KEYWORDS = [
     "鐢垫",
     "鐢垫琛屼笟",
     "鐢垫鎷涙爣",
     "鐢垫鍑哄彛",
     "鐢垫澶栬锤",
     "elevator",
 ]

 # 鐢垫鍏徃鏂伴椈椤甸潰
 ELEVATOR_COMPANY_NEWS = [
     # 杩欎簺缃戠珯缁撴瀯涓嶅悓锛岄渶瑕佸垎鍒€傞厤鐖櫕
     # 鍚庣画鐗堟湰鍙互閫愪釜娣诲姞
 ]

 # 鎷涙爣淇℃伅
 BIDDING_URLS = [
     # 涓浗閲囨嫑缃?/ 鎷涙爣缃戠瓑
 ]


 # ============================================================
 # 鎺ㄩ€侀厤缃? # ============================================================
 MAX_ARTICLES_ENGLISH = 6   # 姣忔鎺ㄩ€佹渶澶氳嫳鏂囨潯鏁? MAX_ARTICLES_CHINESE = 6   # 姣忔鎺ㄩ€佹渶澶氫腑鏂囨潯鏁? NEWS_LANGUAGE_MIX = 0.5    # 涓嫳鏂囨瘮渚?50/50
