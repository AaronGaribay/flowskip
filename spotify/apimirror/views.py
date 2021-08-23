from collections import namedtuple
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.urls import resolve
from room.decorators import in_room_required, is_host_required
from room import serializers as room_serializers
from flowskip.auths import UserAuthentication
from flowskip.snippets import action_in_view_validation
from spotify import api as spotify_api
from spotify.decorators import is_authenticated_in_spotify_required
from spotify.snippets import spotify_action_handler
# Create your views here.
spotify_authenticated_valid_actions = dict()
spotify_authenticated_valid_actions['POST'] = (
    'playlist-create',
    'playlist-add-items',
    'playlist-upload-cover-image',
)

is_host_valid_actions = dict()
is_host_valid_actions['POST'] = (
    'next-track',
    'previous-track',
    'seek-track',
    'repeat',
    'volume',
    'shuffle',
    'add-to-queue'
)
is_host_valid_actions['PUT'] = (
    'start-playback',
    'pause-playback',
    'transfer-playback',
)

Action = namedtuple('Action', ['callable', 'success_code'])


class ApiMirrorAuthenticated(APIView):
    """
    This class is responsible for handling the requests to the
    apimirror"""

    authentication_classes = [UserAuthentication]

    @in_room_required
    @is_authenticated_in_spotify_required
    def post(self, request, format=None):
        response = {}
        room_serializers.CodeSerializer(data=request.data).is_valid(raise_exception=True)
        if not request.user.room.code == request.data['code']:
            raise exceptions.APIException(
                detail="code for this room has changed",
                code=status.HTTP_426_UPGRADE_REQUIRED
            )
        del(request.data['code'])
        action = action_in_view_validation(
            spotify_authenticated_valid_actions,
            resolve(request.path).url_name.lower(),
            request.method
        )
        sp_api_tunnel = spotify_api.api_manager(request.user.room.host.spotify_basic_data)
        actions_definitions = (
            Action(sp_api_tunnel.user_playlist_create, status.HTTP_201_CREATED),
            Action(sp_api_tunnel.playlist_add_items, status.HTTP_201_CREATED),
            Action(sp_api_tunnel.playlist_upload_cover_image, status.HTTP_202_ACCEPTED)
        )

        response, status_code = spotify_action_handler(
            actions_names=spotify_authenticated_valid_actions[request.method],
            actions_definitions=actions_definitions,
            action=action,
            body=request.data,
        )
        return Response(response, status=status_code)


class ApiMirrorIsHostRequired(APIView):
    """
    This class is responsible for handling the requests that only the host can
    send to the apimirror"""

    authentication_classes = [UserAuthentication]

    @in_room_required
    @is_host_required
    def post(self, request, format=None):
        response = {}
        room_serializers.CodeSerializer(data=request.data).is_valid(raise_exception=True)
        if not request.user.room.code == request.data['code']:
            raise exceptions.APIException(
                detail="code for this room has changed",
                code=status.HTTP_426_UPGRADE_REQUIRED
            )
        del(request.data['code'])
        action = action_in_view_validation(
            is_host_valid_actions,
            resolve(request.path).url_name.lower(),
            request.method
        )

        sp_api_tunnel = spotify_api.api_manager(request.user.room.host.spotify_basic_data)
        actions_definitions = (
            Action(sp_api_tunnel.next_track, status.HTTP_204_NO_CONTENT),
            Action(sp_api_tunnel.previous_track, status.HTTP_204_NO_CONTENT),
            Action(sp_api_tunnel.seek_track, status.HTTP_204_NO_CONTENT),
            Action(sp_api_tunnel.repeat, status.HTTP_204_NO_CONTENT),
            Action(sp_api_tunnel.volume, status.HTTP_204_NO_CONTENT),
            Action(sp_api_tunnel.shuffle, status.HTTP_204_NO_CONTENT),
            Action(sp_api_tunnel.add_to_queue, status.HTTP_204_NO_CONTENT),
        )

        response, status_code = spotify_action_handler(
            actions_names=is_host_valid_actions[request.method],
            actions_definitions=actions_definitions,
            action=action,
            body=request.data,
        )

        return Response(response, status=status_code)

    @in_room_required
    @is_host_required
    def put(self, request, format=None):
        response = {}
        room_serializers.CodeSerializer(data=request.data).is_valid(raise_exception=True)
        if not request.user.room.code == request.data['code']:
            raise exceptions.APIException(
                detail="code for this room has changed",
                code=status.HTTP_426_UPGRADE_REQUIRED
            )
        del(request.data['code'])
        action = action_in_view_validation(
            is_host_valid_actions,
            resolve(request.path).url_name.lower(),
            request.method
        )
        sp_api_tunnel = spotify_api.api_manager(request.user.room.host.spotify_basic_data)
        actions_definitions = (
            Action(sp_api_tunnel.start_playback, status.HTTP_204_NO_CONTENT),
            Action(sp_api_tunnel.pause_playback, status.HTTP_204_NO_CONTENT),
            Action(sp_api_tunnel.transfer_playback, status.HTTP_204_NO_CONTENT),
        )

        response, status_code = spotify_action_handler(
            actions_names=is_host_valid_actions[request.method],
            actions_definitions=actions_definitions,
            action=action,
            body=request.data,
        )

        return Response(response, status=status_code)
