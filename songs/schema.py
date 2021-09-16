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

class SwapSongs(graphene.Mutation):
    class Arguments:
        # new_pos = graphene.Int(required=True)
        id1 = graphene.ID()
        id2 = graphene.ID() 
    
    song1 = graphene.Field(SongType)
    song2 = graphene.Field(SongType)

    @classmethod
    def mutate(cls, root, info, id1, id2):
        song1 = Song.objects.get(pk=id1)
        song2 = Song.objects.get(pk=id2)
        temp = song1.queue_position
        song1.queue_position = song2.queue_position
        song2.queue_position = temp 
        song1.save()
        song2.save() 
        return SwapSongs(song1=song1,song2=song2)

class DeleteSong(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    song = graphene.Field(SongType)

    @classmethod
    def mutate(cls, root, info, id):
        song = Song.objects.get(pk=id)
        song.delete()
        return cls(ok=True)


class Mutation(graphene.ObjectType):
    create_song = CreateSong.Field()
    swap_songs = SwapSongs.Field()
    delete_song = DeleteSong.Field()
 
schema = graphene.Schema(query=Query, mutation=Mutation)
