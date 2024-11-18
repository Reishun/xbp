import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import requests

def get_historical_date():
    # 今日から10年前の日付を取得
    ten_years_ago = datetime.now() - timedelta(days=365*10)
    return ten_years_ago.strftime('%Y-%m-%d')

def get_historical_event():
    # NewsAPIを使用して10年前のニュースを取得
    api_key = "9b45ee79d1994d968c817617e9869bc2" 
    date = get_historical_date()
    url = f"https://newsapi.org/v2/everything?q=history&from={date}&to={date}&sortBy=popularity&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        # ニュースがある場合、最初の記事を出す
        if data["articles"]:
            article = data["articles"][0]
            title = article["title"]
            description = article["description"] or "No description available."
            url = article["url"]
            return f"Title: {title}\nDescription: {description}\nURL: {url}"
        else:
            return "No news found for this date."
    except Exception as e:
        return f"Error fetching news: {e}"

def send_email(event):
    # メール情報を設定
    sender_email = "r202402050fm@jindai.jp"
    receiver_email = "r202402050fm@jindai.jp"
    password = "----------"
    
    # メールの内容を作成
    subject = f"10年前の今日: {get_historical_date()}"
    body = f"こんにちは！\n\n10年前の今日({get_historical_date()})に起こった出来事:\n\n{event}"
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        
        with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
            server.starttls()  # 暗号化
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("メール送信完了!")
    except Exception as e:
        print(f"メール送信に失敗しました: {e}")

if __name__ == "__main__":
    event = get_historical_event()  # ニュース取得
    send_email(event)
