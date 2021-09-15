import graphene
from graphene_django import DjangoObjectType
from .models import Song

class SongType(DjangoObjectType):
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'queue_position')

class Query(graphene.ObjectType):
    songs = graphene.List(SongType)

    def resolve_songs(root, info, **kwargs):
        return Song.objects.all()

class SongInput(graphene.InputObjectType):
    title = graphene.String()
    artist = graphene.String()
    album = graphene.String()
    queue_position = graphene.Int()

class CreateSong(graphene.Mutation):
    class Arguments:
        input = SongInput(required=True)
    
    song = graphene.Field(SongType)

    @classmethod
    def mutate(cls, root, info, input):
        song = Song()
        song.title = input.title
        song.artist = input.title
        song.album = input.album
        song.queue_position = input.queue_position
        song.save()
        return CreateSong(song=song)

class UpdateSong(graphene.Mutation):
    class Arguments:
        new_pos = graphene.Int(required=True)
        id = graphene.ID()
    
    song = graphene.Field(SongType)

    @classmethod
    def mutate(cls, root, info, new_pos, id):
        song = Song.objects.get(pk=id)
        song.queue_position = new_pos
        song.save()
        return UpdateSong(song=song)

class Mutation(graphene.ObjectType):
    create_song = CreateSong.Field()
    update_song = UpdateSong.Field()
 
schema = graphene.Schema(query=Query, mutation=Mutation)
