from rest_framework.generics import GenericAPIView, ListAPIView
from .models import Images
from rest_framework import status
from .serializers import ImageUploadSerializer, DisplayImagesSerializer, SelectImageSerializer
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ApiOverview(GenericAPIView):
    def get(self, arg):
        api_urls = {
            "Display and upload images (with the ability to filter by date and geolocation)": "display-and-upload/?geolocation=&date=",
            "Select and delete image": "select-and-delete/<str:pk>",
            "Update image and metadata/": "update-image/<str:pk>",
            "Basic registration": "registr/",
            "Basic authentication": "auth/",
            "Get authorization token": "auth/token/login/",
            "Admin-panel": "admin/",
            "info": "Log in to make any changes.",
        }
        return Response(api_urls)
          

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class MainImages(GenericAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request):
        images = Images.objects.all()
        geolocation = self.request.query_params.get('geolocation')
        date = self.request.query_params.get('date')
        if date is not None:
            images = images.filter(date=date)
        if geolocation is not None:
            images = images.filter(geolocation=geolocation)
        serializer = DisplayImagesSerializer(images, context={"request": request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "image": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SelectImage(GenericAPIView):
    queryset = Images.objects.all()
    serializer_class = SelectImageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        image = Images.objects.get(id=pk)
        if image is None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = SelectImageSerializer(image, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, pk):
        image = Images.objects.get(id=pk)
        if image == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateImage(GenericAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response({f"Введите новые данные для объекта с id={pk} в фото менеджере"})

    def put(self, request, pk):
        image = Images.objects.get(id=pk)
        if image == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = ImageUploadSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "note": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
