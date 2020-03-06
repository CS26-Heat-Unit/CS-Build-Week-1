from django.http import JsonResponse
from django.http import HttpResponse
from adventure.models import Player, Room


def getRooms(request):
    room_dict = {}

    for room in Room.objects.all():
        room_dict[room.id] = {
            "title": room.title,
            "description": room.description,
            "n_to": room.n_to,
            "s_to": room.s_to,
            "e_to": room.e_to,
            "w_to": room.w_to
        }

    return JsonResponse(room_dict)


def getPlayers(request):
    player_dict = {}

    for player in Player.objects.all():
        player_dict[player.id] = {
            "currentRoom": player.currentRoom,
            "uuid": player.uuid,
            "user_id": player.user_id
        }

    return JsonResponse(player_dict)
