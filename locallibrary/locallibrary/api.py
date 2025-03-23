from ninja import NinjaAPI, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from catalog.models import Author, Genre, Language

api = NinjaAPI()


class AuthorSchema(Schema):
    id: int = None
    first_name: str
    last_name: str
    date_of_birth: Optional[str] = None
    date_of_death: Optional[str] = None


class GenreSchema(Schema):
    id: int = None
    name: str


class LanguageSchema(Schema):
    id: int = None
    name: str


def serialize_language(language):
    return {
        "id": language.id,
        "name": language.name,
    }


def serialize_author(author):
    return {
        "id": author.id,
        "first_name": author.first_name,
        "last_name": author.last_name,
        "date_of_birth": author.date_of_birth.strftime("%Y-%m-%d") if author.date_of_birth else None,
        "date_of_death": author.date_of_death.strftime("%Y-%m-%d") if author.date_of_death else None,
    }


def serialize_genre(genre):
    return {
        "id": genre.id,
        "name": genre.name,
    }


# Create Language
@api.post("/languages/", response=LanguageSchema)
def create_language(request, data: LanguageSchema):
    language = Language.objects.create(name=data.name)
    return serialize_language(language)


# Get all Languages
@api.get("/languages/", response=List[LanguageSchema])
def list_languages(request):
    languages = Language.objects.all()
    return [serialize_language(language) for language in languages]


# Get a single Language
@api.get("/languages/{language_id}/", response=LanguageSchema)
def get_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    return serialize_language(language)


# Update a Language
@api.put("/languages/{language_id}/", response=LanguageSchema)
def update_language(request, language_id: int, data: LanguageSchema):
    language = get_object_or_404(Language, id=language_id)
    language.name = data.name
    language.save()
    return serialize_language(language)


# Delete a Language
@api.delete("/languages/{language_id}/")
def delete_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    language.delete()
    return {"success": True}


# GENRE
@api.post("/genres/", response=GenreSchema)
def create_genre(request, data: GenreSchema):
    genre = Genre.objects.create(name=data.name)
    return serialize_genre(genre)


@api.get("/genres/", response=List[GenreSchema])
def list_genres(request):
    genres = Genre.objects.all()
    return [serialize_genre(genre) for genre in genres]


@api.get("/genres/{genre_id}/", response=GenreSchema)
def get_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    return serialize_genre(genre)


@api.put("/genres/{genre_id}/", response=GenreSchema)
def update_genre(request, genre_id: int, data: GenreSchema):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.name = data.name
    genre.save()
    return serialize_genre(genre)


@api.delete("/genres/{genre_id}/")
def delete_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    return {"success": True}


# Author
@api.post("/authors/", response=AuthorSchema)
def create_author(request, data: AuthorSchema):
    author = Author.objects.create(
        first_name=data.first_name,
        last_name=data.last_name,
        date_of_birth=data.date_of_birth,
        date_of_death=data.date_of_death,
    )
    return serialize_author(author)


@api.get("/authors/", response=List[AuthorSchema])
def list_authors(request):
    authors = Author.objects.all()
    return [serialize_author(author) for author in authors]


@api.get("/authors/{author_id}/", response=AuthorSchema)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return serialize_author(author)


@api.put("/authors/{author_id}/", response=AuthorSchema)
def update_author(request, author_id: int, data: AuthorSchema):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in data.dict().items():
        if value is not None:
            setattr(author, attr, value)
    author.save()
    return serialize_author(author)


@api.delete("/authors/{author_id}/")
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"success": True}
