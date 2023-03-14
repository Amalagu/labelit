from rest_framework.serializers import ModelSerializer
from .models import  UserProfile, LabelProject, SampleImage

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields ='__all__'

class SampleImageSerializer(ModelSerializer):
    class Meta:
        model = SampleImage
        fields = '__all__'

class LabelProjectSerializer(ModelSerializer):
    manager = UserProfileSerializer()
    #annotators = UserProfileSerializer(many = True)
    class Meta:
        model = LabelProject
        fields = '__all__'

class AnotatorSerializer(ModelSerializer):
    class Meta:
        read_only = True

