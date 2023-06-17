from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

# model serializers
class ReviewSerializer(serializers.ModelSerializer):

    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):

    # reviews = ReviewSerializer(many=True, read_only=True)
    
    platform = serializers.CharField(source='platform.name')  # getting platform name by accessing name from the StreamPlatformPlatform model using the foreign key name

    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    
    # the name watchlist is the same as what was given to the related_name in the watchlist model
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'


    # StringRelatedField
    # this will just get the field stated in the __str__() function stated in the models.py file for this serializer
    # watchlist = serializers.StringRelatedField(many=True)

    # PrimaryKeyRelatedField
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # HyperlinkedRelatedField
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')


 

































# from rest_framework import serializers
# from watchlist_app.models import Movie

# # model serializers
# class MovieSerializer(serializers.ModelSerializer):
#     # creating a field without specifying it in the models.py file
#     len_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Movie
#         fields = '__all__'

        # fields = ['id', 'name', 'description']
        # excludes = ['active']

    # # custom method
    # def get_len_name(self, object):
    #     length = len(object.name)
    #     return length

    # # if you need tp have validations
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError('Name and Description cannot be the same')
    #     else:
    #         return data

    # # field level validation
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError('Name is too short!')
    #     else:
    #         return value


# normal serializers
# # validators
# def name_length(value):
#      if len(value) < 2:
#         raise serializers.ValidationError('Name is too short!')
#      else:
#         return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])  # using validators
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     # instance carries the old values and validated_data carries the new values
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)

#         instance.save()
#         return instance

#     # object level validation
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Name and Description cannot be the same')
#         else:
#             return data

#     # field level validation
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError('Name is too short!')
#     #     else:
#     #         return value