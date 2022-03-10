from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from django.views.decorators.http import require_http_methods
from App.models import Post
import requests

# Jednoduchá forma cache -> zoznam príspevkov v tvare 'id prispevku' : 'prispevok v json formate'
cache = {}


def validUserId(userId):
    response = requests.get("https://jsonplaceholder.typicode.com/users/{}".format(userId))
    return True if response else False


def addValid(body):
    requiredFields = ["id", "userId", "title", "body"]
    for parameter in requiredFields:
        if (parameter not in body):
            return False
    return True


def validTypes(body):
    if (type(body["id"]) is not int or type(body["userId"]) is not int):
        return False
    else:
        return True


# Povoli iba get,put, delete pre api so zadanym id
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def apiHandler(request, id):
    if (request.method == "PUT"):
        return editPost(request, id)

    elif (request.method == "DELETE"):
        return deletePost(request, id)

    else:
        return showPost(request, id)


@csrf_exempt
@require_http_methods(["POST"])
def addPost(request):
    body = json.loads(request.body)
    # Kontrola počtu vstupných údajov -> všetky údaje sú potrebné
    if (not addValid(body)):
        return HttpResponse("Nezadali ste všetky potrebné údaje!", status=400)

    # Kontrola typu vstupných údajov -> overujem iba int
    if (not validTypes(body)):
        return HttpResponse("Nevhodný typ vstupných údajov!", status=400)

    # Kontrola správneho user id (1-10) pomocou externej API
    if (not validUserId(body["userId"])):
        return HttpResponse("Nespravne user Id !", status=400)

    if (Post.objects.filter(id=body["id"])):
        return HttpResponse("Post so zadaným Id už existuje!", status=400)

    # Ak je príspevok v poriadku, vytvorím ho a uložím do databázy (lokálne)
    Post.objects.create(id=body["id"], userId=body["userId"], title=body["title"], body=body["body"])
    #Odstránim príspevok s daným id z cache (ak sa v cache nachádza)
    try:
        del cache[body["id"]]
    except:
        pass

    return HttpResponse("Príspevok bol pridaný. Id príspevku : " + str(body["id"]), status=201)


# Zobrazí príspevok podľa id
def showPost(request, id):
    # Ak sa príspevok s daným ID nachádza v cache, použijem ho, ak nie hľadám v databáze
    if (id in cache.keys()):
        return HttpResponse(cache[id], status=200, content_type="application/json")
    if (Post.objects.filter(id=id).exists()):
        post = Post.objects.filter(id=id).values()
        return HttpResponse(json.dumps(list(post)[0],indent=2),status=200,content_type="application/json");
    else:
        # Ak sa nenašiel príspevok s daným id ani v cache ani v databáze tak prehľadávam externú API.
        response = requests.get("https://jsonplaceholder.typicode.com/posts/{}".format(id))
        # V prípade, že sa podarilo nájsť prípsevok s daným id na externej API, tak vložím príspevok do cache a zobrazím ho používateľovi
        if (response):
            response = response.json()
            #Upravim response => aby mali prispevky rovnaky tvar
            post = {
                    "id": response["id"],
                    "userId": response["userId"],
                    "title": response["title"],
                    "body": response["body"]
                    }
            post = json.dumps(post, indent=2)
            cache[id] = post
            return HttpResponse(post, status=200, content_type="application/json")
        else:
            return HttpResponse("Príspevok so zadaným id neexistuje.", status=404)


# Ak post s daným id existuje tak ho odstránim
def deletePost(request, id):
    if (Post.objects.filter(id=id).values()):
        Post.objects.get(id=id).delete()
        try:
            del cache[id]
        except:
            pass
        return HttpResponse("Príspevok bol odstránený", status=200)
    else:
        return HttpResponse("Príspevok so zadaným id neexistuje.", status=404)


# Úprava príspevku -> vo formáte JSON v tele požiadavky PUT sa nachádzajú title a body parametre
def editPost(request, id):
    # Načítam obsah tela požiadavky a zistím,či post so zadaným id vôbec existuje (v cache alebo v db)
    body = json.loads(request.body)
    post = Post.objects.filter(id=id).values()

    # Ak post existuje upravím ho v db a následne aj prepíšem cache
    if (post):
        try:
            post.update(title=body["title"])
        except:
            pass
        try:
            post.update(body=body["body"])
        except:
            pass
        return HttpResponse("Udaje boli zmenene!", status=200)
    else:
        return HttpResponse("Príspevok so zadaným id neexistuje.!", status=404)
