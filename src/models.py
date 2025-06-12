# Importa la extensión de SQLAlchemy para integrarse con Flask
from flask_sqlalchemy import SQLAlchemy

# Importa tipos de datos necesarios desde SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey

# Importa el nuevo sistema de mapeo tipado (recomendado en SQLAlchemy 2.0)
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Crea una instancia de SQLAlchemy para usarla en toda la app
db = SQLAlchemy()


class User(db.Model):  # Define una tabla llamada "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    # Clave primaria única (autoincremental por defecto)

    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    # Columna de email, debe ser única y no puede estasr|

    password: Mapped[str] = mapped_column(nullable=False)
    # Columna de contraseña (no se cifra aquí), es obligatoria

    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    # Indica si el usuario está activo, es un valor booleano obligatorio

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="user")
    # Relación uno-a-muchos: un usuario puede tener muchos favoritos

    def serialize(self):
        # Convierte el objeto a un diccionario para respuestas JSON
        return {
            "id": self.id,
            "email": self.email
            # No se incluye la contraseña por seguridad
        }


class People(db.Model):  # Define una tabla llamada "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    # Clave primaria para la tabla de personas

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Nombre del personaje, obligatorio

    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    # Color de cabello del personaje, opcional

    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    # Color de ojos del personaje, opcional

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="people")
    # Relación inversa: una persona puede estar en varios favoritos

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }


class Planet(db.Model):  # Define una tabla llamada "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    # Clave primaria para la tabla de planetas

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Nombre del planeta, obligatorio

    climate: Mapped[str] = mapped_column(String(50), nullable=True)
    # Clima, opcional

    terrain: Mapped[str] = mapped_column(String(50), nullable=True)
    # Terreno, opcional

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="planet")
    # Relación inversa: un planeta puede estar en varios favoritos

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.hair_color,
            "terrain": self.eye_color
        }


class Favorite(db.Model):  # Define una tabla llamada "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    # Clave primaria del favorito

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    # Llave foránea que apunta al usuario que hizo el favorito

    people_id: Mapped[int] = mapped_column(
        ForeignKey('people.id'), nullable=True)
    # Llave foránea opcional hacia una persona favorita

    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planet.id'), nullable=True)
    # Llave foránea opcional hacia un planeta favorito

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    # Relación directa con el modelo User (para acceder a sus datos)

    people: Mapped["People"] = relationship(
        "People", back_populates="favorites")
    # Relación directa con el modelo People

    planet: Mapped["Planet"] = relationship(
        "Planet", back_populates="favorites")
    # Relación directa con el modelo Planet

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people": self.people.serialize() if self.people else None,
            # Si hay persona favorita, la serializa; si no, pone None

            "planet": self.planet.serialize() if self.planet else None
            # Si hay planeta favorito, lo serializa; si no, pone None
        }
