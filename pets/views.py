from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from groups.models import Group
from traits.models import Trait
from pets.models import Pet
from .serializer import PetSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

class PetView(APIView, PageNumberPagination):
        def get(self, request: Request) -> Response:
            trait_param = request.query_params.get('trait')

            if trait_param:
                pets = Pet.objects.filter(traits__name=trait_param).all()
                result_page = self.paginate_queryset(pets, request)
                serializer = PetSerializer(result_page, many=True)
                return self.get_paginated_response(serializer.data)

            pets = Pet.objects.all()
            result_page = self.paginate_queryset(pets, request)
            serializer = PetSerializer(result_page, many=True)
            return self.get_paginated_response(serializer.data)
        
        def post(self, request: Request) -> Response:
            serializer = PetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            group_data = serializer.validated_data.pop('group')
            trait_list = serializer.validated_data.pop('traits')

            try:
                group = Group.objects.get(
                    scientific_name=group_data['scientific_name'])
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)

            pet = Pet.objects.create(**serializer.validated_data, group=group)
            print(pet)
            for trait_data in trait_list:
                try:

                    trait = Trait.objects.get(name__iexact=trait_data['name'])

                except Trait.DoesNotExist:
                    trait = Trait.objects.create(**trait_data)

                pet.traits.add(trait)

            serializer = PetSerializer(pet)

            return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
        def delete(self, request: Request, pet_id) -> Response:
            pet = get_object_or_404(Pet, id=pet_id)
            pet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        def get(self, request: Request, pet_id) -> Response:
            pet = get_object_or_404(Pet, id=pet_id)
            serializer = PetSerializer(pet)
            return Response(serializer.data, status.HTTP_200_OK)
        
        def patch(self, request: Request, pet_id) -> Response:
            pet = get_object_or_404(Pet, id=pet_id)
            serializer = PetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            traits_data = serializer.validated_data.pop("traits")
            group_data = serializer.validated_data.pop("group")
            dict_data = (serializer.validated_data)

            for key, value in dict_data.items():
                setattr(pet, key, value)

            if group_data:
                print(group_data)
                try:
                    group_obj = Group.objects.get(
                        scientific_name__iexact=group_data['scientific_name'])
                    pet.group = group_obj

                except Group.DoesNotExist:
                    group_obj = Group.objects.create(**group_data)
                    pet.group = group_obj

            if traits_data:
                pet.traits.clear()
                for trait_dict in traits_data:
                    trait_obj = Trait.objects.filter(
                        name__iexact=trait_dict["name"]
                    ).first()

                    if not trait_obj:
                        trait_obj = Trait.objects.create(**trait_dict)
                        pet.traits.add(trait_obj)

                    pet.traits.add(trait_obj)

            pet.save()
            print(pet)
            serializer = PetSerializer(pet)

            return Response(serializer.data, status.HTTP_200_OK)