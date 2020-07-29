import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

db = {}
app = Flask("DayEleven")


@app.route("/")
def home():

  return render_template("home.html")


@app.route("/read")
def read():
  check = []
  post_list = []
  for subreddit in subreddits:
    sub = request.args.get(subreddit)
    if sub:
      print(f"{subreddit} is on")
      url = f"https://reddit.com/r/{subreddit}/top/?t=month"
      result = requests.get(url, headers=headers)
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"}).find_all("div", {"class": "_1oQyIsiPHYt6nx7VOmd1sz"})
      for result in results:
        post_list.append(post_info(result, subreddit))
      check.append(subreddit)
      post_list.sort(key= lambda element: element[1], reverse=True)
    else:
      print(f"{subreddit} is None")
  print(check)
  return render_template("read.html", 
  check = check, 
  post_list = post_list
  )


def post_info(result, subreddit):
  vote = ""
  title = ""
  if result:
    vote = result.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).text
    vote = vote.replace("k", "00")
    vote = vote.replace(".", "")
    if vote == "•":
      vote = 0
    elif type(vote) != int:
      vote = int(vote)
    title = result.find("h3").text
  return (
    title,
    vote,
    subreddit
  )
app.run(host="0.0.0.0")