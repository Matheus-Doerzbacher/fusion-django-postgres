import uuid
from django.db import models
from stdimage.models import StdImageField


def get_file_path(_instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return filename


class Base(models.Model):
    criado = models.DateField("Criação", auto_now_add=True)
    modificado = models.DateField("Modificação", auto_now=True)
    ativo = models.BooleanField("Ativo?", default=True)

    class Meta:
        abstract = True


# CLASS SERVICO
class Servico(Base):
    ICONE_CHOICE = (
        ("lni-cog", "Engrenagem"),
        ("lni-stats-up", "Gráfico"),
        ("lni-users", "Usuários"),
        ("lni-layers", "Design"),
        ("lni-mobile", "Mobile"),
        ("lni-rocket", "Fogete"),
    )
    servico = models.CharField("Serviço", max_length=100)
    descricao = models.TextField("Descrição", max_length=200)
    icone = models.CharField("Icone", max_length=12, choices=ICONE_CHOICE)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.servico


# CLASS CARGO
class Cargo(Base):
    cargo = models.CharField("Cargo", max_length=100)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.cargo


# CLASS FUNCIONARIO
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image_extension(value):
    valid_extensions = ["jpg", "jpeg", "png"]
    extension = value.name.split(".")[-1]
    print(extension)
    if extension.lower() not in valid_extensions:
        raise ValidationError(
            _(
                "Formato de arquivo inválido. Somente arquivos JPG, JPEG e PNG são permitidos."
            )
        )


class Funcionario(Base):
    nome = models.CharField("Nome", max_length=100)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name="Cargo")
    bio = models.CharField("Bio", max_length=200)
    imagem = StdImageField(
        "Imagem",
        upload_to=get_file_path,
        variations={"thumb": {"width": 480, "height": 480, "crop": True}},
        validators=[validate_image_extension],
    )
    facebook = models.CharField("Facebook", max_length=100, default="#")
    x = models.CharField("X", max_length=100, default="#")
    instagram = models.CharField("Instagram", max_length=100, default="#")

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.nome


# CLASS Feature
class Feature(Base):
    ICONE_CHOICE = (
        ("lni-cog", "Engrenagem"),
        ("lni-laptop-phone", "Laptop"),
        ("lni-rocket", "Fogete"),
    )

    feature = models.CharField("Recurso", max_length=100)
    icone = models.CharField("Icone", max_length=16, choices=ICONE_CHOICE)
    descricao = models.TextField("Descrição", max_length=200)

    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"

    def __str__(self):
        return self.feature
