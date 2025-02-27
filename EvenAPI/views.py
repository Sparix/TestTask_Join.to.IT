from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse


from EvenAPI.models import Event, JoinEvent
from EvenAPI.permissions import IsOrganizerOrReadOnly
from EvenAPI.serializers import EventSerializer, JoinEventSerializer, EventDetailSerializer, JoinEventCreateSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("organizer")
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "event_join":
            return JoinEventSerializer

        if self.action == "retrieve":
            return EventDetailSerializer

        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        search = self.request.query_params.get("search", None)
        location = self.request.query_params.get("location", None)
        date = self.request.query_params.get("date", None)

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if location:
            queryset = queryset.filter(location__icontains=location)
        if date:
            queryset = queryset.filter(date__date=date)

        return queryset


    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user:
            return Response(
                {"detail": "You do not have permission to edit this event."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user:
            return Response(
                {"detail": "You do not have permission to delete this event."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def event_join(self, request, pk=None):
        event = self.get_queryset().get(pk=pk)
        data = {"user": request.user.id, "event": event.id}

        serializer = JoinEventCreateSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"detail": "Successfully joined the event."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def event_leave(self, request, pk=None):
        event = self.get_queryset().get(pk=pk)
        join_event = JoinEvent.objects.filter(user=request.user, event=event).first()

        if join_event:
            join_event.delete()
            return Response({"detail": "Successfully left the event."}, status=status.HTTP_200_OK)

        return Response({"detail": "You are not joined to this event."}, status=status.HTTP_400_BAD_REQUEST)