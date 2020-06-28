from flask import Flask, jsonify, request
import pymongo

app = Flask(__name__)

@app.route('/')
def index():
   st = 'exchanges'
   st = st.replace('"', '')
   st = st.replace("'", '"')
   return st

@app.route('/exchanges')
def getExchanges():
  data = []
  for exchange in db["exchanges"].find({}, {'_id': False}):
      data.append(str(exchange))
  st = str(data)
  st = st.replace('"','')
  st = st.replace("'",'"')
  return st

@app.route('/<exchange>')
def getExchange(exchange):
  st = str(["ticker", "tradingpairs", "history", "orderbooks"])
  st = st.replace('"', '')
  st = st.replace("'", '"')
  return st

@app.route('/<exchange>/ticker')
def getExchangeTicker(exchange):
   data = []
   for ticker in db[exchange + "_ticker"].find({}, {'_id': False}):
       data.append(str(ticker))
   st = str(data)
   st = st.replace('"', '')
   st = st.replace("'", '"')
   return st


@app.route('/<exchange>/tradingpairs')
def getExchangeTradingPairs(exchange):
   data = []
   for ticker in db[exchange + "_tradingpairs"].find({}, {'_id': False}):
       data.append(str(ticker))
   st = str(data)
   st = st.replace('"', '')
   st = st.replace("'", '"')
   return st

@app.route('/<exchange>/orderbooks')
def getExchangeOrderbooks(exchange):
   data = []
   for ticker in db[exchange + "_orderbooks"].find({}, {'_id': False}):
       data.append(str(ticker))
   st = str(data)
   st = st.replace('"', '')
   st = st.replace("'", '"')
   return st



@app.route('/<exchange>/history')
def getExchangeHistory(exchange):
   base = request.args.get('base')
   quote = request.args.get('quote')
   if base is None or quote is None:
       return jsonify({'error': "you have to assign fitting base and quote parameters"})
   data = []
   for stuff in db[exchange + "_history_1d"].find({"baseTradingSymbol": base, "quoteTradingSymbol": quote},{'_id': False}):
       data.append(str(stuff))
   st = str(data)
   st = st.replace('"', '')
   st = st.replace("'", '"')
   return st

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["crypto"]
    app.run(host='0.0.0.0', port=443, ssl_context=('fullchain.pem','privkey.pem'))
