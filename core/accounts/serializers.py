from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "nome", "papel", "ativo", "criado_em", "atualizado_em"]
        read_only_fields = ["id", "criado_em", "atualizado_em"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "nome", "password", "papel", "ativo"]

    def create(self, validated_data):
        request = self.context.get("request")
        papel_req = validated_data.pop("papel", None)
        ativo = validated_data.pop("ativo", True)
        password = validated_data.pop("password", None)

        # se o request existir e o usuário for staff (admin), permite setar papel
        if request and getattr(request, "user", None) and request.user.is_staff and papel_req:
            papel = papel_req
        else:
            papel = "operador"

        user = User(**validated_data)
        user.papel = papel
        user.ativo = ativo
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

# customiza o payload do token para incluir info do usuário
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['papel'] = user.papel
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # adiciona dados do usuário na resposta
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'nome': self.user.nome,
            'papel': self.user.papel,
        }
        return data
