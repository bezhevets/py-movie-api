from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from cinema.models import Movie
from cinema.serializers import MovieSerializers


# Create your views here.
@api_view(["GET", "POST"])
def movie_list(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSerializers(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = MovieSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET", "PUT", "DELETE"])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = MovieSerializers(movie)

        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    elif request.method == "PUT":
        serializer = MovieSerializers(movie, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
