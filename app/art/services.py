import openpyxl
from django.http import HttpResponse

from .models import Art, Artist


def export_arts_backup():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Arts"

    ws.append([
        "ID", "Artist", "Categories", "Tags",
        "Artist Order", "Category Order", "Display Order",
        "Name", "Persian Name", "Title", "Slug", "Description", "Blog",
        "Image", "Voice", "Second Voice",
        "Width", "Height", "Released Year",
        "Created At", "Updated At",
    ])

    arts = Art.objects.select_related("artist").prefetch_related("category", "tags")

    for art in arts:
        category_names = ", ".join(c.name for c in art.category.all())
        tag_names = ", ".join(f"{t.type}:{t.name}" for t in art.tags.all())

        ws.append([
            art.id, art.artist.name, category_names, tag_names,
            art.artist_order, art.category_order, art.display_order,
            art.name, art.persian_name, art.title, art.slug, art.description, art.blog,
            art.image.url if art.image else "",
            art.voice.url if art.voice else "",
            art.second_voice.url if art.second_voice else "",
            art.width, art.height, art.released_year,
            art.created_at.strftime("%Y-%m-%d %H:%M"),
            art.updated_at.strftime("%Y-%m-%d %H:%M"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="arts_backup.xlsx"'
    response.status_code = 200
    wb.save(response)
    return response


def export_artists_backup():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Artists"

    ws.append([
        "ID", "Name", "Persian Name", "Order",
        "Banner1", "Banner2", "Head1", "Head2",
        "Title", "Slug", "Description", "Blog",
        "Image", "Banner Image", "Arts",
        "Created At", "Updated At",
    ])

    artists = Artist.objects.prefetch_related("arts")

    for artist in artists:
        art_names = ", ".join(a.name for a in artist.arts.all())

        ws.append([
            artist.id, artist.name, artist.persian_name, artist.order,
            artist.banner1, artist.banner2, artist.head1, artist.head2,
            artist.title, artist.slug, artist.description, artist.blog,
            artist.image.url if artist.image else "",
            artist.banner_image.url if artist.banner_image else "",
            art_names,
            artist.created_at.strftime("%Y-%m-%d %H:%M"),
            artist.updated_at.strftime("%Y-%m-%d %H:%M"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="artists_backup.xlsx"'
    response.status_code = 200
    wb.save(response)
    return response