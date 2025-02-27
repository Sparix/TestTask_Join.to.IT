from rest_framework import serializers

from EvenAPI.models import Event, JoinEvent
from userAuth.models import User


class UserView(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff")


class EventSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
    )
    organizer = UserView(many=False, read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "date",
            "location",
            "organizer",
            "count_place",
            "description"
        )


class EventDetailSerializer(EventSerializer):
    connected_users = serializers.SerializerMethodField()

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ("connected_users",)

    @staticmethod
    def get_connected_users(obj):
        users = [join.user for join in JoinEvent.objects.filter(event=obj).select_related("user")]
        return UserView(users, many=True).data


class JoinEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(many=False, read_only=True)
    user = UserView(many=False, read_only=True)
    registered_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
    )

    class Meta:
        model = JoinEvent
        fields = ("id", "user", "event", "registered_at")


class JoinEventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinEvent
        fields = ("id", "user", "event",)

    def validate(self, data):
        user = data["user"]
        event = data["event"]

        if user == event.organizer:
            raise serializers.ValidationError("You are the organizer, you already have a place!")

        if JoinEvent.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("You have already joined this event!")

        joined_count = JoinEvent.objects.filter(event=event).count()
        if joined_count >= event.count_place:
            raise serializers.ValidationError("All seats are already taken!")

        return data
