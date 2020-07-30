from django.urls import reverse, resolve


def test_book_detail_url():
    path = reverse("book-detail", kwargs={"pk": 2})
    assert resolve(path).view_name == "book-detail"

