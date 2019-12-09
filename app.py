from flask import Flask, render_template,request,redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "Çok gizli bir key"
#Veri Tabanı Bağlantısı
client = MongoClient("mongodb+srv://egitim:egitim48@cluster0-zazdg.mongodb.net/test?retryWrites=true&w=majority")
# tododb: Veri tabanı todos : koleksiyon
db = client.tododb.todos
#artık db ile veri tabanında herşeyi yapabilir

@app.route('/')
def index():
    #Veri tabanından kayıtları çek, bir listeye al
    yapilacaklar =[]
    for yap in db.find():
        yapilacaklar.append({"_id":str(yap.get("_id")),
        "isim":yap.get("isim"),
        "durum":yap.get("durum")})
        
    #index.html'e bu listeyi gönder
    return render_template('index.html',yapilacaklar=yapilacaklar)
@app.route('/guncelle/<id>')
def guncelle(id):
   #Gelen id değeri ile kaydı bulalım
   yap=db.find_one({'_id':ObjectId(id)})
   #Durum değeri True ise false, False ise True yap
   durum= not yap.get('durum')
   #Kaydı güncelle
   db.find_one_and_update({'_id':ObjectId(id)},{'$set':{'durum':durum}})
   return  redirect('/')
@app.route('/sil/<id>')
def sil(id):
   #Gelen id değeri ile kaydı bulalım
   db.find_one_and_delete({'_id':ObjectId(id)})
   return  redirect('/')
@app.route('/ekle',methods=['POST'])
def ekle():
    isim = request.form.get('isim')
    db.insert_one({'isim':isim,'durum':'False'})
    return redirect('/')
#Hatalı URL veya Olmayan URL
@app.errorhandler(404)
def hatali_url():
    return redirect('/')
def kimiz():
   return render_template('kimiz.html')
@app.route('/user/<isim>')
def user(isim):
    #ismi sayfaya gönder
   return render_template('user.html',isim=isim)
if __name__ == '__main__':
  app.run(debug=True)
 