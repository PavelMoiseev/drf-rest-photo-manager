from rest_framework import serializers
from .models import Images, People


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = (
            'name',
        )


class ImageUploadSerializer(serializers.ModelSerializer):
    people = PeopleSerializer()

    class Meta:
        model = Images
        fields = (
            'image',
            'date',
            'geolocation',
            'description',
            'people',
        )

    def create(self, validated_data):
        people_in_photo = validated_data.pop('people')
        people_obj_dict = {}
        image = Images.objects.create(**validated_data)
        image.people = {'name': people_in_photo['name']}
        image.save()
        if people_in_photo['name']:
            for name in people_in_photo['name'].replace(' ', '').split(','):
                people_obj_dict['name'] = name
                People.objects.create(image=image, **people_obj_dict)
        return image

    def update(self, instance, validated_data):
        people_in_photo = validated_data.pop('people')
        instance.image = validated_data.get('image', instance.image)
        instance.people = {'name': people_in_photo['name']}
        instance.date = validated_data.get('date', instance.date)
        instance.geolocation = validated_data.get('geolocation', instance.geolocation)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        people_obj_dict = {}
        People.objects.filter(image=instance.pk).delete()
        if people_in_photo['name']:
            for name in people_in_photo['name'].replace(' ', '').split(','):
                people_obj_dict['name'] = name
                People.objects.create(image=instance, **people_obj_dict)
        return instance


class DisplayImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Images
        fields = (
            'id',
            'image',
            'geolocation',
            'description',
        )

    def get_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)


class SelectImageSerializer(serializers.ModelSerializer):
    people_in_photo = PeopleSerializer(many=True)

    class Meta:
        model = Images
        fields = (
            'id',
            'image',
            'date',
            'geolocation',
            'description',
            'people_in_photo',
        )